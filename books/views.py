from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from .models import Book
from .form import BookForm
from .serializers import BookSerializer, BookPostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly 
from .permissions import BookPermission

class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('title')
        return render(request, 'book_list.html', {'books': books})

class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/"
    permission_required = 'books.view_book'
    
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        return render(request, 'book_detail.html', {'book': book})

class AddBookView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/"
    permission_required = 'books.add_book'

    def get(self, request):
        form = BookForm()
        return render(request, 'book_add.html', {'form': form})

    def post(self, request):
        form = BookForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-list')
        return render(request, 'book_add.html', {'form': form})

class EditBookView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/"
    permission_required = 'books.change_book'

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

class DeleteBookView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/"
    permission_required = 'books.delete_book'

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        return render(request, 'book_delete.html', {'book': book})

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return redirect('book-list')

### API ###
class BookListAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, BookPermission]
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(instance=books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailAPI(APIView):
    permission_classes = [IsAuthenticated, BookPermission]
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        self.check_object_permissions(request, book)
        serializer = BookSerializer(instance=book)
        return Response(serializer.data)

    def put(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        self.check_object_permissions(request, book)
        serializer = BookPostSerializer(data=request.data, instance=book)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        self.check_object_permissions(request, book)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

