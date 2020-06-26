from user.models import User
from abc import ABC
from django.db.models import Q


class Result:
    quality = 0
    value = 'value'
    title = 'title'
    owner = 'owner'
    date = 'date'

    def __init__(self, obj):
        self.object = obj


class SearchBase(ABC):
    model = None

    def __init__(self, search_string):
        self.search_string = search_string
        self.query_set = self.get_query_set()
        self.objects = self.get_result_objects()
        self.sorted_objects = self.get_sorted_objects()

    def get_query_set(self):
        """ returns QuerySet """
        return self.model.objects.all()

    def get_result_objects(self):
        """ returns List of Objects """
        return [Result(obj) for obj in self.query_set]

    def get_sorted_objects(self):
        """ List of sorted Objects """
        return self.objects

    def get_results(self):
        return self.sorted_objects


class UserSearch(SearchBase):
    model = User

    def get_query_set(self):
        return User.objects.filter(
            Q(first_name__contains=self.search_string) |
            Q(last_name__contains=self.search_string) |
            Q(email__contains=self.search_string) |
            Q(username__contains=self.search_string)
            )


class SearchEngine:
    modules = [UserSearch]

    def __init__(self, search_string):
        self.results = []
        self.search_string = search_string
        self.search_modules()
        self.sort_results()

    def search_modules(self):
        for module in self.modules:
            self.results.append(*module(self.search_string).get_results())

    def sort_results(self):
        return 

    def get_results(self):
        return self.results
