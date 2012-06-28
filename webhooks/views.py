from subprocess import Popen, PIPE

from django.http import HttpResponse

from models import WebHookRequest


def process_webhook(request):
    # Once you have things working, you should probably add something
    # like the following two lines:
    if request.method != 'POST':
        return HttpResponse('Must use POST')
    json_string = request.POST['payload']
    web_hook_request = WebHookRequest.objects.create(
            json_string=json_string)
    return HttpResponse('Got request\n%s\n' % web_hook_request)
