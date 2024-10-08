from rest_framework import permissions

class LoanPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.has_perm("loan.add_loan")
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return request.user.has_perm('loan.view_loan')
        elif request.method == "PUT":
            return request.user.has_perm("loan.change_loan")
        return False
