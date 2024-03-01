from django import forms
from .models import PDFModel

class pdfForm(forms.ModelForm):
    class Meta:
        model = PDFModel
        fields = ['pdf', 'audio']  # Add 'audio' field for the audio file input
