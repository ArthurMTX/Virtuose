from django import forms
import re

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


class VMForm(forms.Form):
    ram = forms.IntegerField(label='RAM (en Go)', min_value=1, max_value=100, required=True,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cpu = forms.IntegerField(label='CPU', min_value=1, max_value=100, required=True,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    disk = forms.IntegerField(label='Taille du disque (en Go)', min_value=1, max_value=100, required=True,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    os = forms.ChoiceField(label='OS', choices=[('Windows', 'Windows'), ('Linux', 'Linux')], required=True,
                           widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Nom de la VM', max_length=100, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        ram = cleaned_data.get('ram')
        cpu = cleaned_data.get('cpu')
        disk = cleaned_data.get('disk')
        os = cleaned_data.get('os')
        name = cleaned_data.get('name')

        if name:
            print(name)
            if not re.match(r'^[\w]+$', name):
                self.add_error('name', 'Le nom doit être alphanumérique')
            if ' ' in name:
                self.add_error('name', 'Le nom ne doit pas contenir d\'espaces')

        if ram and cpu and disk and os and name:
            if os == 'Windows' and ram < 2:
                self.add_error('ram', 'Windows requiert au moins 2GB de RAM')
            if os == 'Linux' and ram < 1:
                self.add_error('ram', 'Linux requiert au moins 1GB de RAM')
            if disk < 10:
                self.add_error('disk', 'Le disque doit être au moins de 10GB')
        return cleaned_data
