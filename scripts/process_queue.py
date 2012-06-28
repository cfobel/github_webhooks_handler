import sys
import os
from datetime import datetime

from path import path
site_root = path(__file__).parent.parent
sys.path.append(site_root)

from webhooks.models import WebHookRequest


if __name__ == '__main__':
    print datetime.now()
    for r in WebHookRequest.objects.filter(running=False, processed=False):
        r.process()
