from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Book
from .form import BookForm

class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('title')
        return render(request, 'book_list.html', {'books': books})

class BookDetailView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        return render(request, 'book_view.html', {'book': book})

class AddBookView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'book_add.html', {'form': form})

    def post(self, request):
        form = BookForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-list')
        return render(request, 'book_add.html', {'form': form})

class EditBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        form = BookForm(instance=book)
        return render(request, 'book_edit.html', {'form': form, 'book': book})

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        form = BookForm(data=request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-list')
        return render(request, 'book_edit.html', {'form': form, 'book': book})

class DeleteBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        return render(request, 'book_delete.html', {'book': book})

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return redirect('book-list')
