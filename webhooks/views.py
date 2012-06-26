from django.http import HttpResponse
import json
import sys
import os


vpr_repo = 'https://github.com/gwg-placement-ga/vpr-v5-mod.git'
experiments_repo = 'https://github.com/gwg-placement-ga/pyvpr_experiments.git'
job_manager_repo = 'https://github.com/cfobel/job_manager.git'


def git_update(json_string):
	payload = json.loads(json_string)
	repo = payload['repository']['url']
	call = 'fab -f ~/git_update.py -H localhost,coalition@tobias.socs.uoguelph.ca,cfobel@kraken.sharcnet.ca '
	
	if repo == vpr_repo:
		call += 'pull_vpr build_vpr'
	elif repo == experiments_repo:
		call += 'pull_experiments'
	elif repo == job_manager_repo:
		call += 'pull_job_manager'
	else:
		print 'Unknown repo: ', repo
		return
	os.system(call)


def handle_post(request, verbose=False):
	if verbose:
		print 'request: ', request
	json_string = request.POST['payload']
	git_update(json_string)


def process_webhook(request):
    # Once you have things working, you should probably add something
    # like the following two lines:
    if request.method != 'POST':
        return HttpResponse('Must use POST')
    handle_post(request)
    return HttpResponse('Thanks :)\n')
