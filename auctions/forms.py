from .models import Listing
from django import forms
from django.forms import ModelForm

class ListingForm(ModelForm):
    
    class Meta:
        cat = [
                ("Co", "Computers"),
                ("PH", "Phones")
            ]
        
        model = Listing
        fields = ('product_name', 'product_description', 'product_image', 'is_active', 'initial_price', 'category')
        
        widgets = {
            'product_name': forms.TextInput(),
            'product_description': forms.Textarea(),
            'is_active': forms.CheckboxInput(),
            'initial_price': forms.NumberInput(attrs={'min': 1}),
            'category': forms.Select(attrs={'label': 'Choose category'}, choices=cat)
        }
