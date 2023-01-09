from datetime import datetime
#
from os.path import exists
import os

####################################################################
## %%
# Substitute and create a new file (v0.1) --
def subs_and_new_file(f1:str, f1b:str, str1:str, str2:str)->None:
    ################# modificando *.html ##########################
    file1 = f1
    file1b = f1b
    ## -- Leo el archivo --
    file3dM = open(file1, "r")
    lines3dM  = file3dM.readlines()
    file3dM.close()
    ## -------------------------------------------------------------
    lines3dM_New=[]
    for k,line in enumerate(lines3dM):
        if str1 in line:
            print(f'Found this word in line: {k}', line)
            # -- Hacer un poquito mas grande las letras --
            if '<p' or '<span' in line:
                print(f'Changing size of the string in HTML: {k}', line)
                line = line.replace('<p', '<h5')
                line = line.replace('</p', '</h5')
                line = line.replace('<span', '<h5')
                line = line.replace('</span', '</h5')
        # --
        line = line.replace(str1, str2)
        lines3dM_New.append(line)
    file3dM = open(file1b, "w")
    file3dM.writelines(lines3dM_New)
    file3dM.close()
## ------------------------------------------


####################################################################
## %%
## -- Substitute and keep the same file (v0.1) ---------------
def subs_and_same_file(file2w:str, charwF:str, charw:str, ldown:int)->None:
    print(f'{file2w}')
    if charw==' ':
        msg1='Found and erased! ...'
    else:
        msg1='Found and added the line! ...'

    with open(file2w, 'r') as fh: #
        lines = fh.readlines()
        for i, line in enumerate(lines):
            if line.startswith(charwF) or line.strip()==charwF.strip():
                print(msg1)
                lines[i+ldown]=charw+'\n'

    with open(file2w, 'w') as fh:
        for line in lines:
            fh.write(line)
## ------------------------------------------


####################################################################
## %%
def shift(key, l, array):
    return array[:key+1] + [l] + array[key+1:]
## ------------------------------------------


####################################################################
## %%
# Insert and keep the file (v0.1) --
def insert_and_same_file(file2w:str, charwF:str, charw:str)->None:
    print(f'{file2w}')
    if charw==' ':
        msg1='Found and erase! ...'
    else:
        msg1='Found and add the line! ...'

    with open(file2w, 'r') as fh: #
        lines = fh.readlines()
        for i, line in enumerate(lines):
            if line.startswith(charwF) or line.strip()==charwF.strip():
                print(msg1)
                lines=shift(i, charw+'\n' ,lines)

    with open(file2w, 'w') as fh:
        for line in lines:
            fh.write(line)
## ------------------------------------------


####################################################################
## %%
# Insert by line and keep the file (v0.1) --
def insert_by_line_and_same_file(file2w:str, charwL:int, charw:str)->None:
    print(f'{file2w}')
    if charw==' ':
        msg1='Found and erase! ...'
    else:
        msg1='Found and add the line! ...'

    with open(file2w, 'r') as fh: #
        lines = fh.readlines()
        for i, line in enumerate(lines):
            if i==charwL:
                print(msg1)
                lines=shift(i, charw+'\n' ,lines)

    with open(file2w, 'w') as fh:
        for line in lines:
            fh.write(line)
## ------------------------------------------


################# modificando Index.html ###########################
def Create_Template(page1:str, home1:str, str1:str,
                    schar='no', mycp='no')->None:
    page1 = page1
    file1 = f"{home1}/{page1}_Jinja2.html"
    file1b = f'{home1}/{page1}.html'

    # Hagamos un template 1ro!
    if not exists(file1):
        if mycp=='yes':
            #---
            print(file1b)
            os.system(f'cp {file1b} {file1}')
    # Subtitucion! --
    str2 = str1.replace(' ','_')
    str2 = str2.replace('__','_')
    str2 = str2.replace('-','_')
    if schar=='no':
        str2 = str2.replace(str2,
                '{% for var1 in nav1_Var %} {{ var1.'+str2+' }} {% endfor %}')
    if schar=='yes':
        list_schar=['%','$','@','^',';','/', ',']
        for j in list_schar:
            str2=str2.replace(j,'')
        str2 = str2.replace(str2,
                '{% for var1 in nav1_Var %} {{ var1.schar'+str2+' }} {% endfor %}')
    ## Para reusar --
    subs_and_new_file(file1, file1, str1, str2)
    print(f'File created: {file1} and the new word {str2}')
## ------------------------------------------


####################################################################
## %%
# Function to declare types of classes in HTML (v0.1) --
def html_types(value_arr: list)->list:
    types=[]
    for i in value_arr:
        if isinstance(i, str) and '@' not in i:
            types.append('text')
        if isinstance(i, str) and '@' in i:
            types.append('email')
        if isinstance(i, float) or isinstance(i, int):
            types.append('number')
        if isinstance(i, datetime):
            types.append('date')
    return types
## ------------------------------------------


####################################################################
## %%
# Function to replace variables (v0.1) --
def k_replace(k_var:str, lowering='yes')->str:
    # If you add a symbol here, you have to add '' in symbols_to()
    symbols_from = [' ', '__', '(', ')', '.', '++', ',', '#', '%',':',
                    'á', 'é', 'í', 'ó', 'ú',
                    'Á', 'É', 'Í', 'Ó', 'Ú']
    symbols_to = ['_', '_', '', '', '', '', '', '', '','_',
                  'a', 'e', 'i', 'o', 'u',
                  'A', 'E', 'I', 'O', 'U']
    if lowering=='yes':
        k_var = k_var.lower()
    else:
        k_var = k_var
    for i,j in zip(symbols_from, symbols_to):
        #
        k_var=k_var.replace(i, j)
    return k_var
## ------------------------------------------


####################################################################
## %%
# Function to declare variables in Django (v0.1) --
def models_types(types: list, values: list)->list:
    typesModels = []
    for k, i in enumerate(types):
        if i == 'text':
            typesModels.append("models.CharField(max_length=200)")
        elif 'mail'.casefold() in i.casefold():
            typesModels.append("models.EmailField()")
        elif i == 'number' and not str(values[k]).isdecimal():
            typesModels.append("models.FloatField()")
        elif i == 'number' and str(values[k]).isdecimal():
            typesModels.append("models.IntegerField()")
        elif i == 'date':
            typesModels.append("models.DateField()")
    ## -----------------------------------------

    return typesModels
## ------------------------------------------


# Write Models to Forms --
def write_models_to_forms(newApp: str,
                          name_form:str, name_model:str, names:list,
                          labels:list,
                          All_the_Forms:list, All_the_Models:list)->None:
# --------------------------------------------------------------------------------
# ----------------------------------------- FORMAS -------------------------------
# --------------------------------------------------------------------------------
    # Archivo a Modificar.
    myf2 = f'{newApp}/forms.py'
    # Storage of the forms and models ----
    if name_form not in All_the_Forms:
        All_the_Forms.append(name_form)
    if name_model not in All_the_Models:
        All_the_Models.append(name_model)

    add_view1 = f"""
# -----------------------------------------------------------
# -- Model for [{name_model}]
from .models import {name_model}
# End Form model import [{name_model}] ----------------------
"""

    add_view2 = f"""
# -----------------------------------------------------------
class {name_form}(forms.ModelForm):
  class Meta:
    model = {name_model}
# End Form Class [{name_model}] -----------------------------
"""

    # -- Despues de estas lineas ! -------------------------------------------
    lineString1='from django import forms'
    lineString2=add_view1.split('\n')[-2]
    lineString3=add_view2.split('\n')[-2]
    # ------------------------------------------------------------
    #
    # Para forms.py
    nav1_Form = {s3: s6+":"
                 for s3, s6 in \
                 zip(names, labels)}

    myForm = f"""
    fields = {names}
    labels = {nav1_Form}
             """
    #------------------------------------------------------
    # Append to the file ----------------------------------

    Final_Content=open(myf2, 'r').read()
    if name_form not in Final_Content and name_model not in Final_Content:
        if exists(myf2):
            print('[1] Adding Class! --')
            subs_and_new_file(myf2, myf2, lineString1, lineString1 + '\n' + add_view1)
            print('[2] Adding Class! --')
            subs_and_new_file(myf2, myf2, lineString2, lineString2 + '\n' + add_view2)
            print('[3] Adding Class! --')
            subs_and_new_file(myf2, myf2, lineString3, lineString3 + '\n' + myForm)
    else:
        print('Everything is done in (FORMS)! --')
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


## Write Models to Models
def write_models_to_models(newApp:str,
                           name_form:str, name_model:str, names: list,
                           typesModels: list)->None:
# --------------------------------------------------------------------------------
## ----------------------------------------- MODELO ------------------------------
    myf2 = f'{newApp}/models.py'

    add_view1 = f"""
# -----------------------------------------------------------
class {name_model}(models.Model):
# End model import [{name_model}] ---------------------------
"""

    myModel = f"""
    {' '.join(x + ' = ' + y + ';' for x, y in zip(names, typesModels))}

    def __str__(self):
        return self.{names[0]}
         """

    lineString1='# Create your models here.'
    lineString2=add_view1.split('\n')[-2]

    #------------------------------------------------------
    # Append to the file ----------------------------------
    Final_Content=open(myf2, 'r').read()
    if name_form not in Final_Content and name_model not in Final_Content:
        if exists(myf2):
            print('[1] Adding Class! --')
            subs_and_new_file(myf2, myf2, lineString1, lineString1 + '\n' + add_view1)
            print('[2] Adding Class! --')
            subs_and_new_file(myf2, myf2, lineString2, lineString2 + '\n' + myModel)
    else:
        print('Everything is done in (MODELS)! --')


# --------------------------------
# Re-arrange apps/home/views.py
# --------------------------------
def write_models_to_home_views(dir_where:str, newApp:str, name_form:str, 
                               name_model:str, name_context:str)->None:
    myf2 = f'{dir_where}/views.py'

    add_view1 = f"""
# -----------------------------------------------------------
# -- Model para los {name_model}
from {newApp}.models import {name_model}
# -----------------------------------------------------------
    """

    add_view2 = f"""
        # Separado -- Agarro de la base de datos. -------------------
        context['mgs_{name_context.lower()}'] = {name_model}.objects.all()
        # -----------------------------------------------------------
    """

    lineString1='from django.urls import reverse'
    lineString2='context[\'active_menu\'] = active_menu'
    #------------------------------------------------------
    # Append to the file ----------------------------------
    Final_Content=open(myf2, 'r').read()
    if name_form not in Final_Content and name_model not in Final_Content:
        if exists(myf2):
            print('[1] Adding Class! --')
            subs_and_same_file(myf2, lineString1, add_view1, 1)
            print('[2] Adding Class! --')
            subs_and_same_file(myf2, lineString2, add_view2, 1)
    else:
        print(f'Everything is done in ({newApp}/VIEWS)! --')


# ----
def write_models_to_newApp_views(newApp:str, name_form:str, name_model:str,
                                 name_context:str,
                                 number_Form:int, names:list,
                                 simulation=False, messages_All=False)->None:

    # ------------------------------------------------------
    # ------------------------------------------------------
    # Now in views.py ---
    myf2 = f'{newApp}/views.py'

    simString1 = f"""
  # -- Generate Synthetic data for the messages
  p = {name_model}(
  {names[0]}=str(random.randint(1, 5)),
  {names[1]}=random.choices(['New Message',
                                'New Call', 
                                'Payment did OK!'])[0],
  {names[2]}=fake.name().split(' ')[0],
  {names[3]}=str(random.randint(1, 20))
  )
  # Salvo el modelo.
  p.save()"""



    messages_All_string1=f"""
  mgs_Gmessages = MyMessages.objects.all()"""

    messages_All_string2=f"""
  'mgs_Gmessages': mgs_Gmessages"""



    add_view1 = f"""
# -----------------------------------------------------------
# -- Model para los mensajes
# -- De navegacion
from .models import {name_model}
from .forms import {name_form}
# -----------------------------------------------------------
    """

    add_view2 = f"""
#--------- ----------------------- ----------------
#--------- ----------------------- ----------------
#--------- ----------------------- ----------------
# Para los [{name_model}]! --

def my_form{number_Form}(request):"""
    # -- Si quieres datos simulados ------
    if simulation:
        add_view2 = add_view2+simString1
    # ------------------------------------
    add_view2 = add_view2 + f"""
  # Separado --
  mgs_noti = {name_model}.objects.all()"""
      # -- Si quieres datos simulados ------
    if messages_All:
        add_view2 = add_view2+messages_All_string1
    # ------------------------------------
    add_view2 = add_view2 + f"""
#-----------------------------------------
  if request.method == "POST":
    form = {name_form}(request.POST)
    if form.is_valid():
      form.save()
  else:
      form = {name_form}()

  context= {{
        \'form\': form,
        \'mgs_noti\': mgs_noti,"""
    # -- Si quieres datos simulados ------
    if messages_All:
        add_view2 = add_view2+messages_All_string2
    # ------------------------------------
    add_view2 = add_view2 + f"""
        }}

  return render(request, f'{newApp.split('/')[1]}/cv-form{number_Form}.html', context)

#--------- ----------------------- ----------------
# Fin para los {name_model}! --
#--------- ----------------------- ----------------
    """

    add_view3 = f"""
        # [{name_model}] ---------------------------------------
        notis = {name_model}.objects.all()
        context['nav_{name_context}_db'] = notis
        #------------------------------------------------------
    """

    lineString1 = 'from django.urls import reverse'
    ## ----
    lineString2 = '# Create your views here.'
    lineString3 = 'context[\'active_menu\'] = active_menu'
    # ------------------------------------------------------
    # Insert to the file -----------------------------------
    Final_Content = open(myf2, 'r').read()
    if name_form not in Final_Content and name_model not in Final_Content:
        if exists(myf2):
            print('[1] Adding Class! --')
            subs_and_same_file(myf2, lineString1, add_view1, 2)
            print('[2] Adding Class! --')
            subs_and_same_file(myf2, lineString2, add_view2, 2)
            print('[3] Adding Class! --')
            subs_and_same_file(myf2, lineString3, add_view3, 2)
    elif messages_All==False and name_form not in Final_Content:
        if exists(myf2):
            print('[1] Adding Class! --')
            subs_and_same_file(myf2, lineString1, add_view1, 2)
            print('[2] Adding Class! --')
            subs_and_same_file(myf2, lineString2, add_view2, 2)
            print('[3] Adding Class! --')
            subs_and_same_file(myf2, lineString3, add_view3, 2)
    else:
        print(f'Everything is done in ({newApp}/VIEWS)! --')


# The URLs ----
def write_models_to_newApp_urls(newApp:str, number_Form:int)->None:
    # ------------------------------------------------------
    # ------------------------------------------------------
    # Ahora en Asegurados ---
    myf2 = f'{newApp}/urls.py'

    add_view1 = f"""
    path(r'form{number_Form}', views.my_form{number_Form}, name='form{number_Form}'),
    """

    ## Ultima linea del anterior url
    lineString1 = 'urlpatterns = ['
    # ------------------------------------------------------
    # Append to the file ----------------------------------
    # ------------------------------------------------------
    Final_Content = open(myf2, 'r').read()
    if f'views.my_form{number_Form}' not in Final_Content:
        if exists(myf2):
            print('[1] Adding Class! --')
            insert_and_same_file(myf2, lineString1, add_view1)
    else:
        print(f'Everything is done in ({newApp}/URLS)! --')

# ---- And register in Admin ------------------------------------------------------
def write_models_to_newApp_admin(newApp:str, name_model:str)->None:
    ## ------------------------------- Agregar Models a las formas ----------------
    myf2 = f'{newApp}/admin.py'

    add_view1 = f"""
# -----------------------------------------------------------
# -----------------------------------------------------------
# -- Model para los mensajes
from .models import {name_model}
# Fin admin [{name_model}] ----------------------------------
    """

    add_view2 = f"""
# -----------------------------------------------------------
# Separado -- Agarro de la base de datos. -------------------
admin.site.register({name_model})
# -----------------------------------------------------------
    """

    lineString1 = '# Register your models here.'
    lineString2 = add_view1.split('\n')[-2]

    # ------------------------------------------------------
    # Append to the file ----------------------------------
    Final_Content = open(myf2, 'r').read()
    if f'{name_model}' not in Final_Content:
        if exists(myf2):
            print('[1] Adding Class! --')
            subs_and_same_file(myf2, lineString1, add_view1, 1)
            print('[2] Adding Class! --')
            subs_and_same_file(myf2, lineString2, add_view2, 1)
    else:
        print(f'Everything is done in ({newApp}/ADMIN)! --')


# --- Runing linux commands
def migration_run(project:str, myapp:str)->None:
    # Removing stage:
    os.chdir(f'{project}')
    os.system(f'rm -rf {myapp}/migrations')
    os.system(f'rm -rf {myapp}/__pycache__')
    #os.system(f'cp -f db.sqlite3_ORIG db.sqlite3')
    # Second stage:
    os.system(f'python manage.py makemigrations')
    os.system(f'python manage.py migrate')
    os.system(f'python manage.py migrate --run-syncdb')
    # Optional.
    os.system(f'python manage.py makemigrations {myapp}')
    os.system(f'python manage.py sqlmigrate {myapp} 0001')
    os.chdir('../')
    print(os.getcwd())


# --- Runing linux commands
def project_run_2Apps(project:str, app1:str, app2:str)->None:
    # Creating projects and Apps.
    if not exists(f'{project}'):
        os.system(f'django-admin startproject {project}')
        os.chdir(f'{project}')
        os.system(f'django-admin startapp {app1}')
        os.system(f'django-admin startapp {app2}')
        os.system(f'python manage.py migrate')
        os.system(f'mkdir -pv {app1}/templates/{app1}/')
        os.system(f'mkdir -pv {app2}/templates/{app2}/')
        os.chdir(f'../')
        print(os.getcwd())
    else:
        print('The project already exist!')


# Create files first time
def create_files_first(string:str, dir:str, file:str)->None:
    print(f'{dir}{file}')
    file_new = open(f'{dir}{file}', "w")
    file_new.writelines(string)
    file_new.close()