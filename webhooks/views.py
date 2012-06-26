from django.http import HttpResponse


def process_webhook(request):
    # Once you have things working, you should probably add something
    # like the following two lines:
    #if request.method != 'POST':
        #return HttpResponse('Must use POST')
    
    print request.POST
    print request.GET
    return HttpResponse('Thanks :)\n')
