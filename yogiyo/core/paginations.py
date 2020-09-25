from rest_framework import pagination


class Pagination(pagination.CursorPagination):
    ordering = 'id'


class ReversePagination(pagination.CursorPagination):
    ordering = '-id'
