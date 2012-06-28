from subprocess import Popen, PIPE, check_output

import json
from django.db import models
from . import app_settings


class WebHookRequest(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    running = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    json_string = models.TextField()

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
        call = '/usr/local/bin/fab %s -f %s -H %s ' % (key_text,
                app_settings.fab_script, app_settings.hosts)

        repo_name = app_settings.name_by_repository[repo]
        call += ' '.join(app_settings.commands[repo_name])

        print call
        print check_output('bash -c "%s" ' % call, shell=True)

    def parse_repo(self, json_string):
        payload = json.loads(json_string)

        repo = payload['repository']['url']

        if not repo in app_settings.valid_repos():
            print 'Unknown repo: ', repo
            return None
        print 'Found known repo: ', repo
        return repo

    def process(self):
        self.running = True
        self.save()
        repo = self.parse_repo(self.json_string)
        if repo:
            self.git_update(repo, key_file=getattr(app_settings, 'key_file',
                    None))
            self.error = False
        else:
            self.error = True
        self.processed = True
        self.running = False
        self.save()
