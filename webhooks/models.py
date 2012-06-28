from subprocess import Popen, PIPE, check_output

import json
from django.db import models


class WebHookRequest(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    running = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    json_string = models.TextField()

    vpr_repo = 'https://github.com/gwg-placement-ga/vpr-v5-mod'
    experiments_repo = 'https://github.com/gwg-placement-ga/pyvpr_experiments'
    job_manager_repo = 'https://github.com/cfobel/job_manager'
    valid_repos = [vpr_repo, experiments_repo, job_manager_repo]

    def __repr__(self):
        return 'WebHookRequest(added=%s, processed=%s, error=%s, '\
                'json_string=%s)' % (self.added, self.processed, self.error,
                        self.json_string)

    def __str__(self):
        return repr(self)

    def git_update(self, repo, key_file=None):
        if key_file:
            key_text = '-i %s' % key_file
        else:
            key_text = ''
        fab_script = '/home/coalition/git_update.py' 
        hosts = 'coalition@tobias.socs.uoguelph.ca,cfobel@kraken.sharcnet.ca'
        call = '/usr/local/bin/fab %s -f %s -H %s ' % (key_text, fab_script, hosts)

        if repo == self.vpr_repo:
            call += 'pull_vpr build_vpr'
        elif repo == self.experiments_repo:
            call += 'pull_experiments'
        elif repo == self.job_manager_repo:
            call += 'pull_job_manager'
        print call
        print check_output('bash -c "%s" ' % call, shell=True)

    def parse_repo(self, json_string):
        payload = json.loads(json_string)

        repo = payload['repository']['url']

        if repo not in self.valid_repos:
            print 'Unknown repo: ', repo
            return None
        print 'Found known repo: ', repo
        return repo

    def process(self):
        self.running = True
        self.save()
        repo = self.parse_repo(self.json_string)
        if repo:
            self.git_update(repo, key_file='/home/coalition/.ssh/id_rsa')
            self.error = False
        else:
            self.error = True
        self.processed = True
        self.running = False
        self.save()
