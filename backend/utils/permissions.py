from rest_framework.permissions import BasePermission


class OwnerOrStaff(BasePermission):
    """Allow access to staff users or the owner of an object.

    - For non-object-level checks, requires an authenticated user.
    - For object-level checks, returns True if the requesting user is staff
      or is the object's owner. Common owner attribute names are supported
      (`owner`, `user`, `created_by`, `author`). If the object is a user
      instance, the object itself is compared to `request.user`.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_staff:
            return True

        # If the object is a user instance
        if obj == user:
            return True

        # Common owner attribute names
        for attr in ('owner', 'user', 'created_by', 'author'):
            owner = getattr(obj, attr, None)
            if owner == user:
                return True

        return False
