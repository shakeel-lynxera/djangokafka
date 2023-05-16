from rest_framework import permissions
from djangokafka.settings import USER_AUTH


class AllowUserAuth(permissions.BasePermission):
    message = "unauthorized user."
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        try:
            user_auth = str(request.META.get("HTTP_USER_AUTH"))
            if user_auth == USER_AUTH:
                return True
            return False
        except Exception as err:
            print(f"Error in AllowCOBRequest: {err}")
            return False
