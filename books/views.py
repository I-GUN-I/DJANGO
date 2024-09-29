from django.shortcuts import render
from django.views import View
from .models import Book

class BookListView(View):
    def get(self, request):
        context = Book.objects.all()
        return render(request, 'book_list.html', {'context': context})
