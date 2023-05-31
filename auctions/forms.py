from .models import Listing
from django import forms
from django.forms import ModelForm

class ListingForm(ModelForm):
    
    class Meta:
        model = Listing
        fields = ('product_name', 'product_description', 'product_image', 'is_active', 'price_bid', 'product_category')
        
        widgets = {
            'product_name': forms.TextInput(),
            'product_description': forms.Textarea(),
            'product_image': forms.TextInput(),
            'is_active': forms.CheckboxInput(),
            'price_bid': forms.NumberInput(attrs={'min': 1}),
        }
