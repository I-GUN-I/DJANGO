from rest_framework import permissions

class CategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.has_perm("category.add_category")

class CategoryDetailPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return request.user.has_perm('category.view_category')
        elif request.method == "PUT":
            return request.user.has_perm("category.change_category")
        elif request.method == "DELETE":
            return request.user.has_perm("category.delete_category")
        return False
