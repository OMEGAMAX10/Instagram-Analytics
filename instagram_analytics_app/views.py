import os
import datetime
import zipfile
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.core.files.storage import default_storage
from django.contrib import messages

from instagram_analytics_app.forms import UploadZipForm


class InstagramAnalyticsIndexView(FormView):
    template_name = 'index.html'
    form_class = UploadZipForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        file = form.cleaned_data['fileToUpload']
        if zipfile.is_zipfile(file) is False:
            messages.error(self.request, 'Please upload a valid zip file!')
            return super().form_invalid(form)
        datetime_upload = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        folder_name = os.path.join('data', datetime_upload)
        file_path = os.path.join(folder_name, file.name)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(folder_name)
        os.remove(file_path)
        messages.success(self.request, f'Data archive {file.name} uploaded successfully at {datetime.datetime.now().strftime("%H:%M:%S, %d.%m.%Y")}.')
        return super().form_valid(form)
