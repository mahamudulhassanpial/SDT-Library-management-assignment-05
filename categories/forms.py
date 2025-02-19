from django import forms
from .models import Category

class CategoryFrom(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        # fields = ['name', 'bio']
        # exclude = ['bio']