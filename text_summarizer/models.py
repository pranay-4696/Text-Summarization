# from django.db import models

# class PDFModel(models.Model):
#     pdf = models.FileField(upload_to='pdfs/')  # PDF file field
#     audio = models.FileField(upload_to='audios/')  # Audio file field
#     date = models.DateTimeField(auto_now=True)
from django.db import models

class PDFModel(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='pdfs/')
    audio = models.CharField(max_length=255, default='', blank=True)
