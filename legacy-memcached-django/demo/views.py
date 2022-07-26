import time

from django.http import JsonResponse
from django.utils import timezone


# See urls.py where this view is mapped to 2 paths, one of which is cached.
def slow(request):
    time.sleep(1)
    data = {'now': str(timezone.now())}

    return JsonResponse(data)
