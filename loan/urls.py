from django.urls import path
from .views import LoanListView, LoanAddView, LoanReturnView

urlpatterns = [
    path('', LoanListView.as_view(), name='loan-list'),
    path('<int:book_id>/add/', LoanAddView.as_view(), name='loan-add'),
    path('return/<int:book_id>/<int:loan_id>/', LoanReturnView.as_view(), name='loan-return'),
]