from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Book
from .form import BookForm

class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'book_list.html', {'books': books})

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