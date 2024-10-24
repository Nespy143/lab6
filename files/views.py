import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import UploadFileForm

API_URL = 'https://rnhva-178-207-11-125.a.free.pinggy.link/files'

def file_list(request):
    response = requests.get(API_URL)
    files = response.json()
    context = {'files': files}
    return render(request, 'files/file_list.html', context)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            files = {'file': file}
            response = requests.post(API_URL, files=files)
            if response.status_code == 200:
                return redirect('file_list')
            else:
                form.add_error(None, 'Ошибка загрузки файла')
    else:
        form = UploadFileForm()
    return render(request, 'files/upload_file.html', {'form': form})

def download_file(request, file_name):
    download_url = f'{API_URL}/{file_name}'
    response = requests.get(download_url, stream=True)
    response.headers['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return HttpResponse(response.content, content_type='application/octet-stream')