from django.urls import path
from .views import CategoryListView, AddCategoryView, EditCategoryView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('add/', AddCategoryView.as_view(), name='category-add'),
    path('edit/<int:pk>/', EditCategoryView.as_view(), name='category-edit'),
]