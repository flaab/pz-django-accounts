from django import forms
from django.utils.html import mark_safe

class PreviewImageWidget(forms.FileInput):
    """
    A bootstrap4-ready form widget that displays an ImageField with preview.
    """
    
    def __init__(self, attrs={}):
        super(PreviewImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer = None):
        output = []
        if value and hasattr(value, "url"):
            output.append('<figure class="figure"><img src="'+ value.url +'" style="height: 100px;" class="pl-1 pr-1 pt-1 pb-1 border" /></figure>')
        output.append(super(PreviewImageWidget, self).render(name, value, attrs, renderer = None ))
        return mark_safe(u''.join(output))