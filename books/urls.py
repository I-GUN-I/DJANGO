from django.urls import path
from .views import BookListView, AddBookView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('add/', AddBookView.as_view(), name='book-add'),
]