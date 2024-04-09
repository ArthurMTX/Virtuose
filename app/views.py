from django.http import HttpResponse
from django.shortcuts import render
from .vm_form import VMForm
from uuid import uuid4
import yaml


def index(request):
    if request.method == "POST":
        form = VMForm(request.POST)
        if form.is_valid():
            vm_data = form.cleaned_data
            vm_name = vm_data['name']
            uuid = str(uuid4())

            yaml_data = {
                'name': vm_name,
                'uuid': uuid,
                'system': vm_data
            }

            try:
                yaml_str = yaml.safe_dump(yaml_data, allow_unicode=True, default_flow_style=False, sort_keys=False)
                with open(f'tmp./{vm_name}_{uuid}.yaml', 'w') as f:
                    f.write(yaml_str)

                return HttpResponse("YAML créé avec succès.")
            except Exception as e:
                return HttpResponse(f"Erreur lors de la création du fichier YAML : {e}")
        else:
            return render(request, 'app/vm_form.html', {'form': form})
    else:
        form = VMForm()
        return render(request, 'app/vm_form.html', {'form': form})
