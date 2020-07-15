from statistics import mean
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models
from chat.models import Chat
from listing.models import ListingStatus
from category.models import Category
from _collections import defaultdict


def image_path(instance, filename):
    suffix = filename.split('.')[-1]
    return 'user/{}/avatar.{}'.format(instance.pk, suffix)


class UserConfig(models.Model):
    hint_step = models.PositiveSmallIntegerField(default=0)


class User(AbstractUser):
    """
    first_name, last_name, email, is_staff, is_active, date_joined
    REQUIRED_FIELDS = ['email']
    """
    config = models.OneToOneField(
        UserConfig,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('config'),
        )
    image = models.ImageField(
        blank=True,
        upload_to=image_path,
        verbose_name=_('image'),
        )
    description = models.TextField(
        blank=True,
        verbose_name=_('description'),
        )

    @property
    def chats(self):
        lobby = [Chat.get_lobby().pk]
        user_chats = [chat.pk for chat in self.chat_set.all()]
        market_chats = [market.chat.pk for market in self.markets]
        pks = set(lobby + user_chats + market_chats)
        return Chat.objects.filter(pk__in=pks)

    @property
    def locations(self):
        return self.location_set.all()

    @property
    def other_users(self):
        return self.__class__.objects.exclude(pk=self.pk)

    @property
    def pushs(self):
        return self.push_set.exclude(status=ListingStatus.DELETED)

    @property
    def pulls(self):
        return self.pull_set.exclude(status=ListingStatus.DELETED)

    @property
    def markets(self):
        return self.market_set.all()

    @property
    def listings(self):
        """ returns list of listings (pushs and pulls) """
        return list(self.pushs) + list(self.pulls)

    @property
    def score(self):
        """ self.taken_feedbacks.aggregate(Avg('score'))['score__avg'] """
        scores = []
        for feedback in self.feedback_for.all():
            if feedback.score:
                scores.append(feedback.score)
        if scores:
            return mean(scores)

    def get_unseen_messages(self):
        return self.unseen_messages.all()

    def get_unseen_by_chat(self):
        unseen_messages = defaultdict(list)
        for message in self.get_unseen_messages():
            unseen_messages[message.chat.pk].append(message)
        return unseen_messages

    @property
    def open_feedback(self):
        return list(self.userfeedback_set.filter(status=0)) + \
            list(self.pushfeedback_set.filter(status=0))

    @property
    def deals(self):
        deals = self.user1_deals.all().union(self.user2_deals.all())
        for deal in deals:
            deal.set_pov(self)
        return deals

    def get_chat_with(self, *users):
        return Chat.by_users(self, *users, create=True)

    def objects_to_prove(self):
        if self.is_staff:
            objects = {}
            objects['categories'] = Category.get_unproved()
            return objects

    def __str__(self):
        return self.username or self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


@receiver(pre_save, sender=User)
def create_user_config(sender, instance, **kwargs):
    instance.config = UserConfig.objects.create()
