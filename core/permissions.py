from rest_framework.permissions import BasePermission


class IsReviewer(BasePermission):
    """
    Allows access only to users in the 'Reviewers' group.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="Reviewers").exists()
