from rest_framework import pagination


class Pagination(pagination.CursorPagination):
    ordering = '-id'
