from rest_framework import permissions

class BookPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.has_perm("books.add_book")

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return request.user.has_perm('books.view_book')
        elif request.method == "PUT":
            return request.user.has_perm("books.change_book")
        elif request.method == "DELETE":
            return request.user.has_perm("books.delete_book")
        return False
