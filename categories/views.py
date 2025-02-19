from django.shortcuts import render,redirect
from .models import Category
from posts.models import Post

from . import forms

def add_catagory(request):
    if request.method == 'POST':
        catagory_form = forms.CategoryFrom(request.POST)
        if catagory_form.is_valid():
            catagory_form.save()
            return redirect('add_catagory')
    else:
        catagory_form = forms.CategoryFrom()
    return render(request, 'categories/add_categories.html', {'form' : catagory_form})


