from django.shortcuts import render

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse



import random
from faker import Faker
fake = Faker()



# Create your views here.


#--------- Agregar a las apps para authentication ----------------

def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
