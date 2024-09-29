from django.urls import path
from .views import CategoryListView, AddCategoryView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('add/', AddCategoryView.as_view(), name='category-add'),
]