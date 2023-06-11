import os
from django.http import HttpResponse
from django.conf import settings


def directory_index_view(request, path):
    directory = os.path.join(settings.STATIC_ROOT, path)
    if os.path.isdir(directory):
        files = os.listdir(directory)
        content = f"Directory Index for {path}\n\n"
        for file in files:
            content += f"{file}\n"
        return HttpResponse(content, content_type='text/plain')
    else:
        return HttpResponse("Not a directory", content_type='text/plain')
