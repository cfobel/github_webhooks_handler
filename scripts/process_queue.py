import sys
import os
from datetime import datetime
from pprint import pformat

import json
from path import path
site_root = path(__file__).parent.parent
sys.path.append(site_root)

from simple_mail import send_mail
from webhooks.models import WebHookRequest


if __name__ == '__main__':
    print datetime.now()
    for r in WebHookRequest.objects.filter(running=False, processed=False):
        r.process()
        try:
            request_data = json.loads(r.json_string)
        except:
            request_data = r.json_string
        description = '''\
{.added}:
{}'''.format(r, pformat(request_data))

        if r.error:
            message = '  [error] Encountered exception while processing: %s' % description
            send_mail(message[:message.find(':')], message, 'mailer@fobel.net',
                    ['christian@fobel.net', 'ryan.m.pattison@gmail.com'])
        elif r.processed and not r.error:
            message = '  [success] Successfully processed: %s' % description
