from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):

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
