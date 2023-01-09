#!/usr/bin/env python
# coding: utf-8

# ---
# ---
# # Django Web software v0.3
# ---

# In[ ]:


# Importing Standard libraries
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Environment, PackageLoader, select_autoescape
from os.path import exists
import random
from faker import Faker
import os
from pathlib import Path
fake = Faker()


# In[ ]:


import argparse
parser = argparse.ArgumentParser(description='DjangoExcel script v0.3')
parser.add_argument("project_name", help="Prints the supplied argument.", default="mysite")
parser.add_argument("Home", help="Prints the supplied argument.", default="home")
parser.add_argument("App_1", help="Prints the supplied argument.", default="app1")
args = parser.parse_args()
print(args.project_name)


# ---
# ---
# # Special Functions
# ---
# ---
# 

# In[ ]:


# Importing Special libraries
from utils_functs.functions import subs_and_new_file, subs_and_same_file, insert_and_same_file
from utils_functs.functions import Create_Template, html_types
from utils_functs.functions import k_replace, models_types, write_models_to_forms
from utils_functs.functions import write_models_to_models
from utils_functs.functions import write_models_to_home_views
from utils_functs.functions import write_models_to_newApp_views
from utils_functs.functions import write_models_to_newApp_urls, migration_run
from utils_functs.functions import write_models_to_newApp_admin, project_run_2Apps, create_files_first
from utils_functs.functions import insert_by_line_and_same_file


# In[ ]:


# Name of the Django project and Apps (2 in this case)
DJANGO_PROJECT=args.project_name
MYAPP1=args.Home
MYAPP2=args.App_1
MYTEMPLATES=f"{DJANGO_PROJECT}/templates"
MYAPPS=[MYAPP1, MYAPP2]


# In[ ]:


# Creating everything! ...
project_run_2Apps(DJANGO_PROJECT, MYAPP1, MYAPP2)


# In[ ]:


# Copy static and templates directories
dir = f"{DJANGO_PROJECT}"
dir_t = f"{DJANGO_PROJECT}/templates"
# Creating projects and Apps.
if exists(dir) and not exists(dir_t):
    os.system(f'cp -r super_template_v1/static {dir}')
    os.system(f'cp -r super_template_v1/templates {dir}')
    print('Template copied.')
else:
    print('The project already exist! (or not created yet...)')


# In[ ]:


# Adding Apps to "INSTALLED_APPS = []"
myf = f'{DJANGO_PROJECT}/{DJANGO_PROJECT}/settings.py'
str1='\'django.contrib.staticfiles\','
str2=f'    \'{MYAPP1}.apps.{MYAPP1.capitalize()}Config\','
str3=f'    \'{MYAPP2}.apps.{MYAPP2.capitalize()}Config\','
# To run separate scripts.py
str_ext=f'    \'django_extensions\','

Final_Content=open(myf, 'r').read()
if str2 not in Final_Content and str3 not in Final_Content:
    
    str4=f'\'DIRS\': [],'
    str5=f'''        \'DIRS\': [Path(BASE_DIR, \'templates\'),
                Path(BASE_DIR, \'{MYAPP1}/templates\'),
                Path(BASE_DIR, \'{MYAPP2}/templates\'),],'''
    #--
    str6='STATIC_URL = \'/static/\''
    str7=f"""STATICFILES_DIRS = [
        Path(BASE_DIR, \'static\'),
    ]"""

    insert_and_same_file(myf, str1, str2)
    insert_and_same_file(myf, str2, str3)
    insert_and_same_file(myf, str6, str7)
    #
    insert_and_same_file(myf, str4, str5)
    subs_and_same_file(myf, str4, ' ',0)
    # Extension last:
    insert_and_same_file(myf, str1, str_ext)
else:
    print('Everything is done in (INSTALLED_APPS)! --')


# In[ ]:


# Adding two views, in the two Apps directories...
route_urls=["index", "form1"]

views_string="""
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


    

"""

views_string_index=f"""def index(request):
    context = {{\'segment\': \'index\'}}

    html_template = loader.get_template(f'{MYAPP1}/{route_urls[0]}.html')
    return HttpResponse(html_template.render(context, request))
    

"""

def views_apps(app:str, page:str, views_string:str, views_string_index:str)->str:
    if page=='index':
        views_string=views_string+views_string_index
    return f"""
{views_string}
"""

file="views.py"

# Home is in route_urls[0], additional apps run below.
for i,j in zip(MYAPPS, route_urls):
    dir=f"{DJANGO_PROJECT}/{i}/"
    string=f"{views_apps(i, j, views_string, views_string_index)}"
    create_files_first(string, dir, file)
#--------------------------------------------------------------------------------


# In[ ]:


# The < routes and urls > in the two directories.
def urls_apps(app:str, route:str, defs:str, where_url:str)->str:
    return f"""from django.urls import path, include
from . import views

# Register the app.
app_name = \'{app}\'
urlpatterns = [
    path(\'{where_url}\', views.{defs}, name=\'{route}\'),
]
"""

file="urls.py"
route_urls=["index", "form1"]
defs_urls=["index", "my_form1"]
where_urls=["", "form1"]

# Runing for home and APPs, customized urls.
for i,j,k,l in zip(MYAPPS, route_urls, defs_urls, where_urls):
    dir=f"{DJANGO_PROJECT}/{i}/"
    string=f"{urls_apps(i, j, k, l)}"
    create_files_first(string, dir, file)


# In[ ]:


# After that, edit {DJANGO_PROJECT}/urls.py accordingly:
myf = f'{DJANGO_PROJECT}/{DJANGO_PROJECT}/urls.py'
str2=f'    path("{MYAPP1}/", include("{MYAPP1}.urls")),'
str3=f'    path("{MYAPP2}/", include("{MYAPP2}.urls")),'

Final_Content = open(myf, 'r').read()
if str2 not in Final_Content and str3 not in Final_Content:
    str0='from django.urls import path'
    str01='from django.urls import include'
    str1='path(\'admin/\', admin.site.urls),'
    str21=f'    path(\'{where_urls[0]}\', include("{MYAPP1}.urls")),'
    str31=f'    path(\'{where_urls[1]}\', include("{MYAPP2}.urls")),'

    insert_and_same_file(myf, str0, str01)
    #
    insert_and_same_file(myf, str1, str2)
    insert_and_same_file(myf, str2, str21)
    #
    insert_and_same_file(myf, str1, str3)
    insert_and_same_file(myf, str3, str31)
else:
    print(f'Everything is done in ({DJANGO_PROJECT}/urls.py)! --')


# In[ ]:


# And the < pages HTML > in the two Apps directories
def home_pages(app:str, file:str):
  w_dir = Path('super_template_v1', f'{file}.html')
#------------------------------------------------------
  index_lines = w_dir.read_text()
  return f"""
  {index_lines}
"""
files_html=["index", "cv-form1"]

for i,j in zip(MYAPPS, files_html):
    dir=f"{DJANGO_PROJECT}/{i}/templates/{i}/"
    string=f"{home_pages(i, j)}"
    create_files_first(string, dir, j+'.html')


# In[ ]:


# Adding two < forms.py > in the two Apps directories...
def forms_apps(app:str):
    return f"""
from django import forms

"""
file="forms.py"

for i in MYAPPS:
    dir=f"{DJANGO_PROJECT}/{i}/"
    string=f"{forms_apps(i)}"
    create_files_first(string, dir, file)


# In[ ]:


# Adding < views.py > in the main directory ...
def views_main()->str:
    return views_string
file="views.py"

for i in [DJANGO_PROJECT]:
    dir=f"{DJANGO_PROJECT}/{i}/"
    string=f"{views_main()}"
    create_files_first(string, dir, file)


# In[ ]:


# Adding two < admin.py > in the two Apps directories...
def admin_apps(app:str)->str:
    return f"""
from django.contrib import admin

# Register your models here.



"""
file="admin.py"

for i in MYAPPS:
    dir=f"{DJANGO_PROJECT}/{i}/"
    string=f"{admin_apps(i)}"
    create_files_first(string, dir, file)


# ---
# ---
# # Index Pages
# ---

# In[ ]:


# To have a count of the Forms and Models.
All_the_Forms=[]
All_the_Models=[]


# In[ ]:


#-
home1=f"{DJANGO_PROJECT}/{MYAPP1}/templates/{MYAPP1}/"
home2=f"{DJANGO_PROJECT}/{MYAPP2}/templates/{MYAPP2}/"

#
Arr_dir_Work=[home1, home2]

# Taking all the names of the directory
myFilesT = []
myFilesF = []
# iterate through all file
kk=0
for m in Arr_dir_Work:
    for file in os.listdir(m):
        # Check whether file is in text format or not
        if file.endswith(".html"):
            kk+=1
            myFilesF.append(m+file)
            myFilesT.append({kk:file.replace('.html','')})

myFilesF


# In[ ]:


# Search of words for simple substitution process!
Arr_namesL=[('My title1', 'no','no'),
            ('My title2', 'no','no'),
            
           ]

# Recommendation how to name variables
for k,i in enumerate(Arr_namesL):
    print(k, k_replace(i[0], 'no') if i[1]=='no'
                  else 'schar'+k_replace(i[0], 'no'))


# In[ ]:


# Para correr scripts tienes que instalar django_extension
#!pip install django-extensions
# Y tienes que adherirlo a INSTALLED_APPS en settings.py
# add this:
#    'django_extensions',
# Finalmente corres el script:
# python manage.py runscript Add_siniestros_v1


# In[ ]:


# All the variables here.
My_title1 = 'My Beautiful Excel App'
My_title2 = 'My title2.5'


# In[ ]:


##-----
Var_index_Arr1_L = [k_replace(i[0], 'no') if i[1]=='no'
                    else 'schar'+k_replace(i[0], 'no')
                    for i in Arr_namesL]
#--
# From global!! ---
Var_index_Arr2_L = [globals()[i] for i in Var_index_Arr1_L]
##--
nav1_Var_L = [{s1: s2}
        for  s1, s2 in zip(Var_index_Arr1_L, Var_index_Arr2_L)]

# Here in Index: simple substitution --
for k,i in enumerate(Arr_namesL):
    ## Para reusar --
    print(k_replace(i[0]))
    for m in myFilesF:
        f1=f"{m}"
        #print(f1)
        subs_and_new_file(f1, f1, i[0], nav1_Var_L[k][k_replace(i[0], lowering='no')
                   if i[1]=='no' else 'schar'+k_replace(i[0], 'no')])
#############################################
#############################################


# ---
# ---
# # Your Excel App/computations here:

# In[ ]:


import pandas as pd
dir1 = './'
df = pd.read_excel(dir1+'Excel_Sheet_v1.xlsx', \
                   skiprows=1, usecols="A:C")
#---
df.dropna(inplace=True)
#print the column names
print(df.columns)
#-----------------------------------
#get the values for a given column
values = df[df.columns].values


# In[ ]:


print(df)


# ---
# ---
# # Navigation Bar:
# ---

# In[ ]:


#
page1="base"
home1=f"{DJANGO_PROJECT}/templates"
myFiles=[f'{home1}/{page1}.html']

Arr_names_side=[('Insurance Company', 'no','no'), #
                ('myapp2', 'no','no'),
                ('myapp1', 'no','no'),
                ('My Profile', 'no', 'no'),
                ('Link1:index', 'no','no'),
                ('Link2:index', 'no','no'),
           ]

# Recommendation how to name variables:
for k,i in enumerate(Arr_names_side):
    print(k, k_replace(i[0], 'no') if i[1]=='no'
                  else 'schar'+k_replace(i[0], 'no'))


# In[ ]:


# All the variables here.
Insurance_Company = "CRM App"
myapp2 = f"{MYAPP2}"
myapp1 = f"{MYAPP1}"
My_Profile = 'My Account'
# 
Link1_index = f'{MYAPP1}:{route_urls[0]}'
Link2_index = f'{MYAPP2}:{route_urls[1]}'


# In[ ]:


# --------------- Smart Array ------------------------------------------
Var_index_Arr1_side = [k_replace(i[0], 'no') if i[1]=='no'
                    else 'schar'+k_replace(i[0], 'no')
                    for i in Arr_names_side]
Var_index_Arr2_side = [globals()[i] for i in Var_index_Arr1_side]
##--
nav1_Var_side = [{s1: s2}
        for  s1, s2 in zip(Var_index_Arr1_side, Var_index_Arr2_side)]

## -----
# Here in Index, simple substitution --
for k,i in enumerate(Arr_names_side):
    ## Para reusar --
    print(i[0].replace(' ', '_') )
    for m in myFiles:
        f1=f"{m}"
        print(f1)
        subs_and_new_file(f1, f1, i[0], nav1_Var_side[k][k_replace(i[0], lowering='no')
                   if i[1]=='no' else 'schar'+k_replace(i[0], 'no')])
#############################################
#############################################


# ---
# ---
# # The Apps

# ---
# ---
# ### Some synthetic data

# In[ ]:


# ----------------------------------------------------------
# Models and Forms: 14 fields
# ----------------------------------------------------------
# ----------------------------------------------------------
labels=["Name", "Last Name", "Work place",
        "email",
        "Address1 (street)",
        "Address2 (#apt.)",
        "City", "State", "Zipcode",
        "Premium Plan", "Standard plan", "Plan care++",
        "Medical Risk", "Medical Conditions",
        ]


# In[ ]:


values1=[fake.name().split(' ')[0],
         fake.name().split(' ')[1],
         fake.company(), fake.email(),
         fake.address(), fake.address(), fake.city(),
         fake.state(), int(fake.zipcode()),
         fake.text(), fake.text(), fake.text(),
         fake.text(), fake.text(),
         ]

types = html_types(values1)
# Los nombres de la variables sacados de los Labels, con substitución:
# ----------------------------------------------------------------------
names = [k_replace(k) for k in labels]
ids=["id_"+ i for i in names]
fors=ids
maxlengths=["200" for _ in names]
places = ["mt-3 mt-sm-0" if (i % 2) == 0 else "" for i in range(len(names))]
# 6 = 2cols; 4 = 3cols |
cols_places = ["4" if k<=9 else "6" for k,_ in enumerate(names)]
# ----------------------------------------------------------
# ----------------------------------------------------------


# In[ ]:


##-- [:4]
ini=0
fin=4
nav1_For1 = [{'values1': s1, 'types':s2, 'names':s3,
            'ids':s4, 'fors':s5, 'labels': s6, 'maxlengths': s7,
            'places': s8, 'cols': s9}
            for  s1, s2, s3, s4, s5, s6, s7, s8, s9 in \
              zip(values1[ini:fin], types[ini:fin], names[ini:fin], ids[ini:fin],
                  fors[ini:fin], labels[ini:fin],
                  maxlengths[ini:fin], places[ini:fin], cols_places[ini:fin])]
nav1_For1


# In[ ]:


##--
ini=4
fin=9
nav1_For2 = [{'values1': s1, 'types':s2, 'names':s3,
            'ids':s4, 'fors':s5, 'labels': s6, 'maxlengths': s7,
            'places': s8, 'cols': s9}
            for  s1, s2, s3, s4, s5, s6, s7, s8, s9 in \
              zip(values1[ini:fin], types[ini:fin], names[ini:fin], ids[ini:fin],
                  fors[ini:fin], labels[ini:fin],
                  maxlengths[ini:fin], places[ini:fin], cols_places[ini:fin])]
#
##-- 3rd windows! -----------------------------------------------
ini=9
fin=12
nav1_For3 = [{'values1': s1, 'types':s2, 'names':s3,
            'ids':s4, 'fors':s5, 'labels': s6, 'maxlengths': s7,
            'places': s8, 'cols': s9}
            for  s1, s2, s3, s4, s5, s6, s7, s8, s9 in \
              zip(values1[ini:fin], types[ini:fin], names[ini:fin], ids[ini:fin],
                  fors[ini:fin], labels[ini:fin],
                  maxlengths[ini:fin], places[ini:fin], cols_places[ini:fin])]
#
##-- 4th windows! ------------------------------------------------
ini=12
fin=15
nav1_For4 = [{'values1': s1, 'types':s2, 'names':s3,
            'ids':s4, 'fors':s5, 'labels': s6, 'maxlengths': s7,
            'places': s8, 'cols': s9}
            for  s1, s2, s3, s4, s5, s6, s7, s8, s9 in \
              zip(values1[ini:fin], types[ini:fin], names[ini:fin], ids[ini:fin],
                  fors[ini:fin], labels[ini:fin],
                  maxlengths[ini:fin], places[ini:fin], cols_places[ini:fin])]


# In[ ]:


## It is important to run above |
## -----------------------------------------
newApp=f'{DJANGO_PROJECT}/{MYAPP2}'

# Nuevas formas y models --------
name_model = 'MyModel'
name_form = name_model+'Form'
# -------------------------------
number_Form = 1         # Has to change from model to model
name_context = 'app1'   # Has to change from model to model

# Write models into the form. ------------------------------
write_models_to_forms(newApp, name_form, name_model, names,
                      labels, All_the_Forms, All_the_Models)
# ----------------------------------------------------------
# For models.py
typesModels = models_types(types, values1)
# Write models into the models.py ------------------------------
write_models_to_models(newApp, name_form, name_model, names, typesModels)
# --------------------------------------------------------------


# ---
# ---
# # Substitution in 4 places:
# ---

# In[ ]:


All_the_Forms, All_the_Models, newApp, os.getcwd()


# In[ ]:


## Run in sequence:
# 4 Cells! ---
# 1)
dir_where = f'{DJANGO_PROJECT}/{DJANGO_PROJECT}'
write_models_to_home_views(dir_where, f'{MYAPP2}', name_form, 
                           name_model, name_context)
# 2)
write_models_to_newApp_views(newApp, name_form, name_model,
                                 name_context, number_Form,
                                 names, simulation=False,
                                 messages_All=True)
# 3)
write_models_to_newApp_urls(newApp, number_Form)
# 4)
write_models_to_newApp_admin(newApp, name_model)


# In[ ]:


# Finally migrate!-
migration_run(DJANGO_PROJECT, MYAPP2)


# In[ ]:


# General Django check
# Go to the terminal for optimal results.
os.chdir(f'{DJANGO_PROJECT}')
os.system('python manage.py check')
os.chdir(f'../')
print(os.getcwd())


# In[ ]:


# Go to the terminal for optimal results.
os.chdir(f'{DJANGO_PROJECT}')
# Create standard superuser.
os.system('echo \"from django.contrib.auth import get_user_model; User = get_user_model(); \
User.objects.create_superuser(\'admin\', \'admin@myproject.com\', \'test123\')\" | python manage.py shell')

os.chdir(f'../')
print(os.getcwd())


# ---
# ---
# # New Models and Forms:
# ## MyMessages
# ---

# In[ ]:


All_the_Models, All_the_Forms


# In[ ]:


# ----------------------------------------------------------
# ---- Everything depends on Labels.
labels = ["Imagen", "TypeofMessage", "FromName", "Howlong"]
values1 = [f"team-{random.randint(1,5)}.jpg",
           random.choices(['New Message!','New Call'])[0],
           fake.name().split(' ')[0], 10]

types = html_types(values1)
names = [k_replace(k) for k in labels]
# exercise taking for below:
names_MyMessages = names
ids = ["id_" + i for i in names]
# ----------------------------------------------------------
fors = ids
maxlengths = ["200" for _ in names]
places = ["mt-3 mt-sm-0" if (i % 2) == 0 else "" for i in range(len(names))]
# 6 = 2cols; 4 = 3cols |
cols_places = ["4" if k <= 9 else "6" for k, _ in enumerate(names)]
# ----------------------------------------------------------


# In[ ]:


## It is important to run above |
## -----------------------------------------
newApp=f'{DJANGO_PROJECT}/{MYAPP2}'

# New forms and models --------
name_model = 'MyMessages'
name_form = name_model+'Form'
# -------------------------------
number_Form = 2         # Has to change from model to model
name_context = 'Noti'   # Has to change from model to model

# Write models into the form. ------------------------------
write_models_to_forms(newApp, name_form, name_model, names,
                      labels, All_the_Forms, All_the_Models)
# ----------------------------------------------------------
# Para models.py
typesModels = models_types(types, values1)
# Write models into the models.py ------------------------------
write_models_to_models(newApp, name_form, name_model, names, typesModels)
# --------------------------------------------------------------


# In[ ]:


##
# 4 Cells! ---
# 1)
dir_where = f'{DJANGO_PROJECT}/{DJANGO_PROJECT}'
write_models_to_home_views(dir_where, f'{MYAPP2}', name_form, 
                           name_model, name_context)
# 2)
write_models_to_newApp_views(newApp, name_form, name_model,
                                 name_context, number_Form,
                                 names, simulation=True,
                                 messages_All=False)
# 3)
write_models_to_newApp_urls(newApp, number_Form)
# 4)
write_models_to_newApp_admin(newApp, name_model)


# In[ ]:


# If new models added has to run this --
migration_run(DJANGO_PROJECT, MYAPP2)


# In[ ]:


# General Django check
# Launching the site
# using of GET
# Go to the terminal for optimal results.
os.chdir(f'{DJANGO_PROJECT}')
os.system('http --follow --timeout 6 :8000/app1/form1')
os.chdir(f'../')
print(os.getcwd())


# In[ ]:




