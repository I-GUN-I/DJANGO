from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.contrib.auth.models import Permission
from django.db import transaction
from .models import Loan
from .form import LoanForm
from books.models import Book
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoanSerializer, LoanPostSerializer, LoanReturnSerializer

class LoanListView(LoginRequiredMixin, View):
    login_url = "/auth/"

    def get(self, request):
        if request.user.has_perm('loan.view_loan'):
            loans = Loan.objects.all()
        else:
            loans = Loan.objects.filter(user=request.user)

        for i in loans:
            if i.return_date < timezone.now().date() and not i.is_returned:
                i.is_overdue = True
                i.save()
            else:
                i.is_overdue = False
                i.save()

        return render(request, 'loan_list.html', {'loans': loans})

class LoanAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/"
    permission_required = ["loan.add_loan"]

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        form = LoanForm(initial={'book': book})
        return render(request, 'loan_add.html', {'form': form})

    def post(self, request, book_id):
        form = LoanForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                loan = form.save(commit=False)
                loan.user = request.user
                loan.borrow_date = timezone.now().date()
                loan.save()
                loan.book.status = 'Unavailable'
                loan.book.save()
            return redirect('loan-list')
        return render(request, 'loan_add.html', {'form': form})


class LoanReturnView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/"
    permission_required = ["loan.change_loan"]
    
    def get(self, request, loan_id):
        with transaction.atomic():
            loan = get_object_or_404(Loan, pk=loan_id)

            loan.is_returned = True
            loan.is_overdue = False
            loan.return_date = timezone.now().date()
            loan.save()

            loan.book.status = 'Available'
            loan.book.save()

            return redirect('loan-list')

### API ###
class LoanListAPI(APIView):
    def get(self, request):
        loans = Loan.objects.all()
        for i in loans:
            if i.return_date < timezone.now().date() and not i.is_returned:
                i.is_overdue = True
                i.save()
            else:
                i.is_overdue = False
                i.save()
        serializer = LoanSerializer(instance=loans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LoanPostSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                book = serializer.validated_data['book']
                book.status = 'Unavailable'
                book.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanDetailAPI(APIView):
    def get(self, request, loan_id):
        loan = get_object_or_404(Loan, pk=loan_id)
        serializer = LoanSerializer(instance=loan)
        return Response(serializer.data)

    def put(self, request, loan_id):
        loan = get_object_or_404(Loan, pk=loan_id)
        serializer = LoanReturnSerializer(data=request.data, instance=loan)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                book = serializer.validated_data['book']
                if serializer.validated_data['is_returned']:
                    book.status = 'Available'
                else:
                    book.status = 'Unavailable'
                book.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)