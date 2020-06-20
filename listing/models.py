from decimal import Decimal
from itertools import chain
from django.db import models
from django.core.validators import MinValueValidator
from config.settings import AUTH_USER_MODEL
from user.models import User


class Review(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    score = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class Unit(models.Model):
    title = models.CharField(max_length=20)
    short = models.CharField(max_length=5)

    def __str__(self):
        return self.title


class ListingBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    title = models.CharField(max_length=50)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._actions = {0: set(), 1: set(), 2: set(), 3: set()}

    @property
    def opposite_class(self):
        return {'push': Pull, 'pull': Push}.get(self.type)

    def get_matches(self):
        cls = self.opposite_class
        return cls.objects.filter(category=self.category
                                  ).exclude(user=self.user)

    def __eq__(self, other):
        try:
            return self.category == other.category  # and self.type == other.type
        except AttributeError as e:
            print(e)

    def __str__(self):
        return '{} {} {}'.format(self.user.username, self.type, self.title)

    class Meta:
        abstract = True


class Push(ListingBase):
    type = 'push'


class Pull(ListingBase):
    type = 'pull'
