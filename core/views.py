from django.shortcuts import render
from django.views.generic import TemplateView
from posts.models import Post
from categories.models import Category
# Create your views here.

# class HomeView(TemplateView):
#     template_name = 'index.html'

def home(request, category_slug = None):
    data = Post.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        data = Post.objects.filter(category = category)
    categories = Category.objects.all()
    return render(request, 'index.html', {'data' : data, 'category' : categories})

