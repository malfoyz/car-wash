from rest_framework import permissions


class IsAdministratorOrReadOnly(permissions.BasePermission):
    """
    Глобальное разрешение делать любые операции администратору
    и просматривать записи пользователю.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        else:
            return request.user.groups.filter(name='Администратор').exists()



class IsAdministrator(permissions.BasePermission):
    """
    Глобальное разрешение позволяет выполнять любые операции
    над объектами пользователю, состоящему в группу Администратор.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Администратор').exists()

