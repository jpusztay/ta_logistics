from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader

from ta_logistics_application.forms import ResumeForm

def index(request):
    template = loader.get_template('ta_logistics_application/index.html')
    return HttpResponse(template.render())

def submit(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            template = loader.get_template('ta_logistics_application/submission_received.html')
            return HttpResponse(template.render())
    else:
        form = ResumeForm()
    return render(request, 'ta_logistics_application/application.html', {'form': form})
