from django import forms
from .services import get_templates
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
    TEMPLATE_CHOICES = get_templates()

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
    template = forms.ChoiceField(
        label=context_processors.CREATE_VM_TEMPLATE_LABEL,
        choices=TEMPLATE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(
        label=context_processors.CREATE_VM_NAME_LABEL,
        min_length=5,
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super(VMForm, self).__init__(*args, **kwargs)
        self.fields['template'].choices = get_templates()

    """
    Vérification des données du formulaire de création de VM
    """
    def clean(self):
        cleaned_data = super().clean()
        ram = int(cleaned_data.get('ram'))
        cpu = int(cleaned_data.get('cpu'))
        template = cleaned_data.get('template')
        name = cleaned_data.get('name').strip()

        fields = {
            'ram': {'value': ram, 'choices': self.RAM_CHOICES, 'error': context_processors.CREATE_VM_ERROR_RAM_GENERIC},
            'cpu': {'value': cpu, 'choices': self.CPU_CHOICES, 'error': context_processors.CREATE_VM_ERROR_CPU_GENERIC},
            'template': {'value': template, 'choices': self.TEMPLATE_CHOICES, 'error': context_processors.CREATE_VM_ERROR_TEMPLATE_GENERIC},
        }

        # Pour chaque champ, vérifie si la valeur est dans les choix possibles
        for field, data in fields.items():
            # Si le champ est 'template', vérifie si la valeur est dans les choix possibles
            if field == 'template':
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

        # Vérifie si les champs 'ram', 'cpu', 'template' et 'name' sont renseignés
        if ram and cpu and template and name:
            return cleaned_data