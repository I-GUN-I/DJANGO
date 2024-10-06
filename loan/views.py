from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.contrib.auth.models import Permission
from .models import Loan
from .form import LoanForm
from books.models import Book
from django.utils import timezone

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
        book = get_object_or_404(Book, id=book_id)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.borrow_date = timezone.now().date()

            book.status = 'Unavailable'

            loan.book = book
            book.save()
            loan.save()
            return redirect('loan-list')

        return render(request, 'loan_add.html', {'form': form})


class LoanReturnView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/auth/"
    permission_required = ["loan.change_loan"]
    
    def get(self, request, book_id, loan_id):
        loan = get_object_or_404(Loan, pk=loan_id)
        book = get_object_or_404(Book, pk=book_id)

        loan.is_returned = True
        loan.is_overdue = False
        loan.return_date = timezone.now().date()
        loan.save()

        book.status = 'Available'
        book.save()

        return redirect('loan-list')