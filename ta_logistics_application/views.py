from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader

from .forms import ResumeForm

def index(request):
    template = loader.get_template('ta_logistics_application/index.html')
    return HttpResponse(template.render())

def submit(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponse('Your resume has been uploaded successfully.')
    else:
        form = ResumeForm()
    return render(request, 'ta_logistics_application/submit.html', {'form': form})
