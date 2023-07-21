from django.shortcuts import render
from django.template import RequestContext


# page not found
def handler404(request, exception):
    response = render(request, 'templates/404.html', {})
    response.status_code = 404
    return response


# error view
def handler500(request, *args, **argv):
    response = render(request, 'templates/500.html', {})
    response.status_code = 500
    return response


# permission denied
def handler403(request, exception):
    response = render(request, 'templates/403.html', {})
    response.status_code = 403
    return response


# bad request view
def handler400(request, exception):
    response = render(request, 'templates/400.html', {})
    response.status_code = 400
    return response
