from django.http import HttpResponse
from django.shortcuts import render
from .vm_form import VMForm, get_form_fields_info
from uuid import uuid4
import xml.etree.ElementTree as ET
from xml.dom import minidom


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

            root = ET.Element("VM")
            ET.SubElement(root, "name").text = vm_name
            ET.SubElement(root, "uuid").text = uuid

            system = ET.SubElement(root, "system")
            for key, value in vm_data.items():
                if key != 'name':
                    ET.SubElement(system, key).text = str(value)

            try:
                xml_str = ET.tostring(root, encoding='unicode')
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
