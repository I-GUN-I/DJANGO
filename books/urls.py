from django.urls import path
from .views import BookListView, BookDetailView, AddBookView, EditBookView, DeleteBookView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('add/', AddBookView.as_view(), name='book-add'),
    path('view/<int:book_id>/', BookDetailView.as_view(), name='book-view'),
    path('edit/<int:book_id>/', EditBookView.as_view(), name='book-edit'),
    path('<int:book_id>/delete/', DeleteBookView.as_view(), name='book-delete'),
]
