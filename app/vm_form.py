from django import forms
from . import context_processors
import re

"""
Récupère les informations des champs du formulaire de création de VM
"""


def get_form_fields_info():
    form = VMForm()
    fields_info = []
    for field_name, field in form.fields.items():
        field_info = {
            'label': field.label,
            'name': field_name,
            'type': field.__class__.__name__,
            'attributes': {}
        }
        if hasattr(field, 'min_value'):
            field_info['attributes']['min'] = field.min_value
        if hasattr(field, 'max_value'):
            field_info['attributes']['max'] = field.max_value
        if hasattr(field, 'choices'):
            field_info['attributes']['choices'] = field.choices
        if hasattr(field, 'max_length'):
            field_info['attributes']['max_length'] = field.max_length

        fields_info.append(field_info)
    return fields_info


"""
Création dynamique du formulaire de création de VM
"""


class VMForm(forms.Form):
    RAM_CHOICES = [
        ('4', context_processors.CREATE_VM_RAM_LABEL_4GB),
        ('8', context_processors.CREATE_VM_RAM_LABEL_8GB),
        ('16', context_processors.CREATE_VM_RAM_LABEL_16GB),
        ('32', context_processors.CREATE_VM_RAM_LABEL_32GB),
    ]
    CPU_CHOICES = [
        ('1', context_processors.CREATE_VM_CPU_LABEL_1),
        ('2', context_processors.CREATE_VM_CPU_LABEL_2),
        ('4', context_processors.CREATE_VM_CPU_LABEL_4),
        ('8', context_processors.CREATE_VM_CPU_LABEL_8),
    ]
    DISK_CHOICES = [
        ('10', context_processors.CREATE_VM_DISK_LABEL_10GB),
        ('20', context_processors.CREATE_VM_DISK_LABEL_20GB),
        ('50', context_processors.CREATE_VM_DISK_LABEL_50GB),
        ('100', context_processors.CREATE_VM_DISK_LABEL_100GB),
        ('250', context_processors.CREATE_VM_DISK_LABEL_250GB),
        ('500', context_processors.CREATE_VM_DISK_LABEL_500GB),
    ]
    OS_CHOICES = [
        ('Windows', context_processors.CREATE_VM_OS_LABEL_WINDOWS),
        ('Linux', context_processors.CREATE_VM_OS_LABEL_LINUX),
    ]

    ram = forms.ChoiceField(
        label=context_processors.CREATE_VM_RAM_LABEL,
        choices=RAM_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))
    cpu = forms.ChoiceField(
        label=context_processors.CREATE_VM_CPU_LABEL,
        choices=CPU_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))
    disk = forms.ChoiceField(
        label=context_processors.CREATE_VM_DISK_LABEL,
        choices=DISK_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))
    os = forms.ChoiceField(
        label=context_processors.CREATE_VM_OS_LABEL,
        choices=OS_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(
        label=context_processors.CREATE_VM_NAME_LABEL,
        min_length=5,
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    """
    Vérification des données du formulaire de création de VM
    """
    def clean(self):
        cleaned_data = super().clean()
        ram = int(cleaned_data.get('ram'))
        cpu = int(cleaned_data.get('cpu'))
        disk = int(cleaned_data.get('disk'))
        os = cleaned_data.get('os')
        name = cleaned_data.get('name').strip()

        fields = {
            'ram': {'value': ram, 'choices': self.RAM_CHOICES, 'error': context_processors.CREATE_VM_ERROR_RAM_GENERIC},
            'cpu': {'value': cpu, 'choices': self.CPU_CHOICES, 'error': context_processors.CREATE_VM_ERROR_CPU_GENERIC},
            'disk': {'value': disk, 'choices': self.DISK_CHOICES, 'error': context_processors.CREATE_VM_ERROR_DISK_GENERIC},
            'os': {'value': os, 'choices': self.OS_CHOICES, 'error': context_processors.CREATE_VM_ERROR_OS_GENERIC},
        }

        # Pour chaque champ, vérifie si la valeur est dans les choix possibles
        for field, data in fields.items():
            # Si le champ est 'os', vérifie si la valeur est dans les choix possibles
            if field == 'os':
                if data['value'] not in [choice[0] for choice in data['choices']]:
                    self.add_error(field, data['error'])
            # Si le champ est 'ram', 'cpu' ou 'disk', vérifie si la valeur est un entier ET si la valeur est dans les choix possibles
            else:
                if data['value'] not in [int(choice[0]) for choice in data['choices'] if choice[0].isdigit()]:
                    self.add_error(field, data['error'])

        # Vérifie si le champ 'name' est alphanumérique et ne contient pas d'espace
        if name:
            if not re.match(r'^[\w]+$', name):
                self.add_error('name', context_processors.CREATE_VM_ERROR_NAME_NOT_ALPHANUMERIC)
            if ' ' in name:
                self.add_error('name', context_processors.CREATE_VM_ERROR_NAME_SPACE)

        # Vérifie si les champs 'ram', 'cpu', 'disk', 'os' et 'name' sont renseignés
        if ram and cpu and disk and os and name:
            # Vérifie si la RAM est suffisante pour l'OS (Windows: 2GB, Linux: 1GB)
            os_ram_requirements = {'Windows': 2, 'Linux': 1}

            if ram < os_ram_requirements.get(os, 0):
                self.add_error('ram',
                               context_processors.CREATE_VM_ERROR_WINDOWS_RAM if os == 'Windows' else context_processors.CREATE_VM_ERROR_LINUX_RAM)

            # Vérifie si le disque est suffisant
            if disk < 10:
                self.add_error('disk', context_processors.CREATE_VM_ERROR_DISK)

        return cleaned_data
