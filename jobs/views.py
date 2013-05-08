from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render, get_object_or_404, render_to_response, redirect

from profiles.models import Profile

from jobs.models import Job, JobParameter
from jobs.forms import CreateJobForm

from twilio.rest import TwilioRestClient

def index(request):
    latest_jobs_list = Job.objects.order_by('-created_at')[:5]
    return render_to_response('jobs/index.html', {'latest_jobs_list': latest_jobs_list}, context_instance=RequestContext(request))

def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render_to_response('jobs/detail.html', {'job': job}, context_instance=RequestContext(request))

from datetime import datetime
def projects(request):
	interests = Profile.objects.get(user_id=request.user.id).interests
	# fetch intern jobs
	intern_params = {}
	intern_jobs = Job.objects.filter(intern_project=True)
	for intern_job in intern_jobs:
		params = JobParameter.objects.filter(container_id=intern_job.id)
		for param in params:
			intern_params[param.name] = param.value
	# fetch extern jobs
	extern_params = {}
	extern_jobs = Job.objects.filter(intern_project=False)
	for extern_job in extern_jobs:
		params = JobParameter.objects.filter(container_id=extern_job.id)
		for param in params:
			extern_params[param.name] = param.value

	project_types = { 'embedded': ["arduino", "microcontroller", "ARM"],
					  'web': ["rails", "django", "web", "jquery", "html5"],
					  'mobile': ["iphone", "android", "nokia"],
					  'business': ["SAP", "enterprise", "business"] }

	begin = "Your assignment will be to build a %s application"
	requirements = "You have to use %s"
	deadline = "You should submit the task until %d of %s" \
		% (datetime.today().day+4, datetime.today().strftime('%B'))
	
	project_type = "your own choice "
	for key, value in project_types.items():
		for word in value:
			if word in interests:
				project_type = key
				break

	if request.method == 'POST':
		# twilio account
		account = "AC6fa8bf2b3c6bc38a55435561712d2bfd"
		token = "0d909e6f6f3b0c4d28076e245cb557ae"
		client = TwilioRestClient(account, token)

		# default sms number
		number = "+49017685645785"
		message = "Project submitted by: "+request.user.username
		message = client.sms.messages.create(to=number, from_="+15745842963", body=message)

	text = ""
	for key, value in intern_params.items():
		text += value + " "
	intern_projects = [begin % project_type, requirements % text, deadline]

	text = ""
	for key, value in extern_params.items():
		text += value + " "
	extern_projects = [begin % project_type, requirements % text, deadline]

	return render(request, 'jobs/projects.html', 
		{'extern_projects': extern_projects, 'intern_projects': intern_projects, 'int': interests})

def create(request, create_form=CreateJobForm,
           template_name='jobs/create_form.html', success_url=None,
           extra_context=None):
	
	#profile = Profile.objects.get(user_id=request.user.id)
	#if profile and not(profile.if_employer):
	#	return render_to_response('jobs/index.html', {'form': form}, context_instance=RequestContext(request))

	form = create_form()

	if request.method == 'POST':
		form = create_form(request.POST, request.FILES)

		if form.is_valid():
			job = Job()
			job.user = request.user
			job.name = form.cleaned_data['name']
			job.location = form.cleaned_data['location']
			job.intern_project = form.cleaned_data['intern_project']
			job.save()

			# split by new line
			names_values = form.cleaned_data['names_values'].split('\n')
			# go trough all names and values
			for name_value in names_values:
				# skip extra spaces and split by first colon
				result = ' '.join(name_value.split()).split(":", 1)
				# when name and value
				if len(result) == 2:
					parameter = JobParameter()
					parameter.name = result[0].strip()
					parameter.value = result[1].strip()
					parameter.container = job
					parameter.save()

			return redirect('/jobs')
	return render_to_response('jobs/create_form.html', {'form': form}, context_instance=RequestContext(request))