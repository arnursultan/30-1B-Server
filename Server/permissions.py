from rest_framework.permissions import BasePermission
from .serializers import calculate_age

class IsAdult(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        age = calculate_age(user.date_of_birth)
        return bool(age is not None and age >= 18)

