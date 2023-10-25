from django import forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        prohibited_words = [
            'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
        ]

        for word in prohibited_words:
            if word in name.lower() or word in description.lower():
                raise forms.ValidationError(f'Название или описание содержат запрещенное слово: {word}')

        return cleaned_data

class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'
