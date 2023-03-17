from django import forms
class UploadValidateFile(forms.Form):
    validate_file = forms.FileField()