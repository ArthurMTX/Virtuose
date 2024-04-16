from django.http import HttpResponse
from .vm_form import VMForm, get_form_fields_info
from .register_form import CustomUserCreationForm
from uuid import uuid4
from xml.etree import ElementTree
from xml.dom import minidom
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def index(request):
    return render(request, 'app/index.html')


def vm_form(request):
    if request.method == "POST":
        print('POST submitted')
        form = VMForm(request.POST)
        if form.is_valid():
            vm_data = form.cleaned_data
            vm_name = vm_data['name']
            uuid = str(uuid4())

            root = ElementTree.Element("VM")
            ElementTree.SubElement(root, "name").text = vm_name
            ElementTree.SubElement(root, "uuid").text = uuid

            system = ElementTree.SubElement(root, "system")
            for key, value in vm_data.items():
                if key != 'name':
                    ElementTree.SubElement(system, key).text = str(value)

            try:
                xml_str = ElementTree.tostring(root, encoding='unicode')
                xml_pretty = minidom.parseString(xml_str).toprettyxml(indent="    ")

                with open(f'tmp./{vm_name}_{uuid}.xml', 'w') as f:
                    f.write(xml_pretty)

                return HttpResponse("Fichier XML créé avec succès.")
            except Exception as e:
                print(e)
                return HttpResponse(f"Erreur lors de la création du fichier YAML : {e}")
        else:
            fields_info = get_form_fields_info()
            errors = form.errors
            return render(request, 'app/vm_form.html', {'fields_info': fields_info, 'errors': errors, 'form': form})
    else:
        form = VMForm()
        fields_info = get_form_fields_info()
        return render(request, 'app/vm_form.html', {'fields_info': fields_info, 'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password.')
        except user_model.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
