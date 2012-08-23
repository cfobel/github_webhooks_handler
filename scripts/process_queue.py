import sys
import os
from datetime import datetime

from path import path
site_root = path(__file__).parent.parent
sys.path.append(site_root)

from simple_mail import send_mail
from webhooks.models import WebHookRequest


if __name__ == '__main__':
    print datetime.now()
    for r in WebHookRequest.objects.filter(running=False, processed=False):
        r.process()
        if r.error:
            message = '  [error] Encountered exception while processing: %s' % r
            send_mail(message[:message.find(':')], message, 'mailer@fobel.net',
                    ['christian@fobel.net', 'ryan.m.pattison@gmail.com'])
        elif r.processed and not r.error:
            message = '  [success] Successfully processed: %s' % r
