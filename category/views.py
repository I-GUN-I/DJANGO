from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from .models import Category
from .form import CategoryForm

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'category_list.html', {'categories': categories})

class AddCategoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/"
    permission_required = ["category.add_category"]
    def get(self, request):
        form = CategoryForm()
        return render(request, 'category_add.html', {'form': form})

    def post(self, request):
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')

class EditCategoryView(LoginRequiredMixin, View):
    login_url = "/auth/"
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        form = CategoryForm(instance=category)
        return render(request, 'category_edit.html', {'form': form, 'category': category})

    def post(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
        return render(request, 'category_edit.html', {'form': form, 'category': category})

class DeleteCategoryView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        return render(request, 'category_delete.html', {'category': category})
    
    def post(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
        return redirect('category-list')