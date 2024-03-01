import fitz  # PyMuPDF
# from .models import PDFModel
import speech_recognition as sr
from os import path
from .forms import pdfForm
from django.shortcuts import render, redirect
from django.contrib import messages
import re
import time
from .Summarizer import summarizer, url_summarizer
from .models import PDFModel

def replace_stop_words(input_string):
    # Replace " stop " with ". "
    result_string = input_string.replace("stop", ".")
    
    return result_string


def pdf_text(pdf):
    pdf_path = f'./static/images/{pdf}'
    pdf_document = fitz.open(pdf_path)
    
    x = len(pdf_document)
    page = pdf_document.load_page(x - 1)  # Load the last page
    
    text = page.get_text()
    pdf_document.close()

    return text

def index(request):
    context = {'flag': False, 'url_error': False, 'summarize_div': True, 'pdfForm': pdfForm}

    if request.method == 'POST':

        if 'pdf' in request.FILES:
            pdf = request.FILES['pdf']
            PDFModel.objects.create(pdf=pdf)
            pdf = PDFModel.objects.latest('date')
            pdfText = pdf_text(f'{pdf.pdf}')

            if request.POST.get('num_lines'):
                num_lines = request.POST['num_lines']
            else:
                num_lines = 5

            start = time.time()
            summary = summarizer(pdfText, int(num_lines))
            end = time.time()

            context['time_taken'] = round(end - start, 2)
            context['flag'] = True
            context['content'] = pdfText
            context['summary'] = summary
            context['summarize_div'] = False

            return render(request, 'text_summarizer/index.html', context)
        elif 'audio' in request.FILES:
            wav = request.FILES['audio']
            AUDIO_FILE = wav
            r = sr.Recognizer()
            with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)  # read the entire audio file
            num_lines = 5
            try:
                s=(r.recognize_sphinx(audio))
                start = time.time()
                s=replace_stop_words(s)
                summary = summarizer(s, int(num_lines))
                end = time.time()
                context['time_taken'] = round(end - start, 2)
                context['flag'] = True
                context['content'] = s
                context['summary'] = summary
                context['summarize_div'] = False
                return render(request, 'text_summarizer/index.html', context)
            except sr.UnknownValueError:
                print("could not understand audio")
            except sr.RequestError as e:
                print("error; {0}".format(e))
        else:
            if len(request.POST['textarea']) > 0 and len(request.POST['url_link']) > 0:
                messages.error(request, "Enter either URL or Text, not Both.")
                return redirect('index')

            if len(request.POST['textarea']) > 0:
                if request.POST.get('num_lines'):
                    num_lines = request.POST['num_lines']
                else:
                    num_lines = 5
                content = request.POST['textarea']
                start = time.time()
                summary = summarizer(content, int(num_lines))
                end = time.time()
                context['time_taken'] = round(end - start, 2)
                context['flag'] = True
                context['content'] = content
                context['summary'] = summary
                context['summarize_div'] = False
                return render(request, 'text_summarizer/index.html', context)

            elif len(request.POST['url_link']) > 0:
                if re.search(
                    r"(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?",
                    request.POST['url_link'],
                ) is None:
                    context['url_error'] = True
                    return render(request, 'text_summarizer/index.html', context)
                else:
                    if request.POST.get('num_lines'):
                        num_lines = request.POST['num_lines']
                    else:
                        num_lines = 5
                    try:
                        start = time.time()
                        content, summary = url_summarizer(request.POST['url_link'], int(num_lines))
                        end = time.time()
                        context['time_taken'] = round(end - start, 2)
                        context['flag'] = True
                        context['content'] = content
                        context['summary'] = summary
                        context['summarize_div'] = False
                        return render(request, 'text_summarizer/index.html', context)
                    except:
                        messages.error(request, "Entered URL doesn't contain any data.")
                        return redirect('index')
            else:
                messages.error(request, "Enter URL or Text to summarize the content.")
                return redirect('index')
    return render(request, 'text_summarizer/index.html', context)