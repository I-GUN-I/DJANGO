from django.urls import path
from .views import LoanListView, LoanAddView, LoanReturnView, LoanListAPI, LoanDetailAPI

urlpatterns = [
    path('', LoanListView.as_view(), name='loan-list'),
    path('<int:book_id>/add/', LoanAddView.as_view(), name='loan-add'),
    path('return/<int:loan_id>', LoanReturnView.as_view(), name='loan-return'),
    path('api/', LoanListAPI.as_view(), name='loan-api-list'),
    path('api/<int:loan_id>/', LoanDetailAPI.as_view(), name='loan-api-detail'),
]
