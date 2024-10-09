from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from .models import Category
from .form import CategoryForm
from .serializers import CategorySerializer, CategoryPostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly 
from .permissions import CategoryPermission, CategoryDetailPermission

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
        return render(request, 'category_add.html', {'form': form})

class EditCategoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/"
    permission_required = ["category.change_category"]

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

class DeleteCategoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/"
    permission_required = ["category.delete_category"]

    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        return render(request, 'category_delete.html', {'category': category})
    
    def post(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
        return redirect('category-list')

### API ###
class CategoryListAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, CategoryPermission]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(instance=categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoryPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPI(APIView):
    permission_classes = [IsAuthenticated, CategoryDetailPermission]
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        self.check_object_permissions(request, category)
        serializer = CategorySerializer(instance=category)
        return Response(serializer.data)

    def put(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        self.check_object_permissions(request, category)
        serializer = CategoryPostSerializer(data=request.data, instance=category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        self.check_object_permissions(request, category)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)