from django import forms

from .models import Image, Project, Tag, Category

from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.utils.safestring import mark_safe
# from bootstrap_datepicker.widgets import DatePicker
# class ClearableMultipleFileInput(ClearableFileInput):
#     template_name = 'create_project.html'  # Specify the template for rendering the widget

#     def value_from_datadict(self, data, files, name):
#         upload = super().value_from_datadict(data, files, name)
#         if self.is_required and not any(upload):  # Ensure at least one file is uploaded if the field is required
#             raise forms.ValidationError(self.error_messages['required'], code='required')
#         return upload

#     def format_value(self, value):
#         if isinstance(value, (list, tuple)):
#             return [super().format_value(v) for v in value]
#         return super().format_value(value)

#     def get_context(self, name, value, attrs):
#         context = super().get_context(name, value, attrs)
#         context['widget']['value'] = value
#         return context

#     def render(self, name, value, attrs=None, renderer=None):
#         if value is None:
#             value = []
#         final_attrs = self.build_attrs(self.attrs, attrs)
#         output = ['<ul>']
#         for i, file in enumerate(value):
#             output.append('<li><label{}>{}</label>{}</li>'.format(
#                 mark_safe(final_attrs['label_for']),
#                 mark_safe(file),
#                 CheckboxInput().render(name + '-clear', False, {'class': 'checkbox-clear'})
#             ))
#         output.append('</ul>')
#         return mark_safe('\n'.join(output))
    
class ProjectForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
    }))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={
        "class": "form-control",
    }))
    target = forms.DecimalField(widget=forms.TextInput(attrs={
        "class": "form-control",
    }))
    tags = forms.ModelChoiceField(queryset=Tag.objects.all(),widget=forms.Select(attrs={
        "class": "form-control",
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
    }))
    end = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control","type":"date"}
        
    ))
    class Meta:
        model = Project
        fields = [
            "name",
            "category",
            "target",
            "tags",
            "description",
            "end",
        ]

       
class ImageForm(forms.ModelForm):
    image = forms.FileField(widget = forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
    }), label = "Images")

    class Meta:
        model = Image
        fields = ("image",)

class DonationForm(forms.Form):
    donation = forms.DecimalField(max_digits=10, decimal_places=2)
    
  

class ReportForm(forms.Form):
    REASONS = (
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate content'),
        ('offensive', 'Offensive language'),
        ('other', 'Other'),
    )

    reason = forms.ChoiceField(choices=REASONS, widget=forms.RadioSelect)


  
