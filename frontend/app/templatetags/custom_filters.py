from django import template

register = template.Library()


@register.filter
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.filter(name='add_class_if_disabled')
def add_class_if_disabled(field, form_disabled):
    if form_disabled:
        return field.as_widget(attrs={"disabled": "disabled"})
    return field