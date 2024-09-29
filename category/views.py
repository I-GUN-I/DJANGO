from django.shortcuts import render, redirect
from django.views import View
from .models import Category
from .form import AddCategoryForm

class CategoryListView(View):
    def get(self, request):
        context = Category.objects.prefetch_related('book_set').all()
        return render(request, 'category_list.html', {'context': context})

class AddCategoryView(View):
    def get(self, request):
        form = AddCategoryForm()
        return render(request, 'category_add.html', {'form': form})

    def post(self, request):
        form = AddCategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
        return render(request, 'category_add.html', {'form': form})
