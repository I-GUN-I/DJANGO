from django.urls import path
from .views import CategoryListView, AddCategoryView, EditCategoryView, DeleteCategoryView, CategoryListAPI, CategoryDetailAPI

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('add/', AddCategoryView.as_view(), name='category-add'),
    path('edit/<int:category_id>/', EditCategoryView.as_view(), name='category-edit'),
    path('<int:category_id>/delete/', DeleteCategoryView.as_view(), name='category-delete'),
    path('api/', CategoryListAPI.as_view(), name='category-api-list'),
    path('api/<int:category_id>/', CategoryDetailAPI.as_view(), name='category-api-detail'),
]