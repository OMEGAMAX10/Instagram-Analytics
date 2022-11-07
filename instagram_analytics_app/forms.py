from django import forms


class UploadZipForm(forms.Form):
    fileToUpload = forms.FileField()
