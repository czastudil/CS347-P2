from django.conf import settings

def roles_processor(request):
    roles = []
    if hasattr(request, 'user'):
        if hasattr(request.user, 'student'):
            roles.append('student')
        if hasattr(request.user, 'ta'):
            roles.append('ta')
        if hasattr(request.user, 'professor'):
            roles.append('professor')
    return {'roles': roles}

def debug(context):
    return {'debug': settings.DEBUG}
