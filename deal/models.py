from django.db import models
from django.db.models import Q
from config.settings import AUTH_USER_MODEL
from feedback.models import PushFeedback, UserFeedback


class DealStatus(models.IntegerChoices):
    VIRTUAL = 0, 'virtual'
    STARTED = 10, 'started'
    PLACED = 20, 'placed'
    ACCEPTED = 100, 'accepted'
    CANCELED = 110, 'canceled'


class Deal(models.Model):
    user1 = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user1_deals'
        )
    user2 = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user2_deals'
        )
    guild = models.ForeignKey(
        'guild.Guild', on_delete=models.CASCADE, null=True, blank=True
        )
    status = models.PositiveSmallIntegerField(
        default=DealStatus.STARTED,
        choices=DealStatus.choices,
        )

    pov_user = None
    _level = None
    _quality = None

    #===========================================================================
    # def __init__(self, pov_user=None, *args, **kwargs):
    #     if pov_user:
    #         self.pov_user = pov_user
    #     super().__init__(*args, **kwargs)
    #===========================================================================

    @property
    def user(self):
        if self.pov_user and self.pov_user == self.user2:
            return self.user2
        return self.user1

    @property
    def partner(self):
        if self.user == self.user2:
            return self.user1
        return self.user2

    def set_pov(self, pov_user):
        self.pov_user = pov_user
        return self

    @property
    def bids(self):
        return self.bid_set.filter()

    @property
    def pushs(self):
        # pylint: disable=no-member
        return list(self.intersection(self.user.pushs, self.partner.pulls))

    @property
    def pulls(self):
        # pylint: disable=no-member
        return list(self.intersection(self.user.pulls, self.partner.pushs))

    @property
    def level(self):
        """ Levels:
            0 - No Deal match
            1 - One side Match
            2 - Two side Match
            3 - Deal between three users
            4 - Deal between four users
        users represent all users taking part at this deal
        """
        if self._level:
            return self._level
        level = 0
        if self.pushs:
            level += 1
        if self.pulls:
            level += 1
        self._level = level
        return self._level

    @property
    def quality(self):
        if self._quality:
            return self._quality
        self._quality = len(self.pushs + self.pulls)
        return self._quality

    def get_users(self):
        return self.user, self.partner

    def get_latest_bid(self):
        bids = self.bids
        return bids.latest() if bids else None

    def can_accept(self, user):
        latest_bid = self.get_latest_bid()
        if not latest_bid:
            return False
        if latest_bid.creator != user:
            return True
        return False

    def can_bid(self, user):
        latest_bid = self.get_latest_bid()
        if not latest_bid:
            return True
        if latest_bid.creator != user:
            return True
        return False

    @classmethod
    def by_users(cls, user1, user2, create=False):
        existing = cls.objects.filter(
            Q(user1=user1, user2=user2) |
            Q(user2=user1, user1=user2)
            )
        if create and not existing:
            cls.objects.create(user1=user1, user2=user2)
        else:
            return existing

    @classmethod
    def get_or_create(cls, users):
        return cls.by_users(*users, create=True)

    @staticmethod
    def intersection(lst1, lst2):
        """ returns intersecting elements """
        for element in lst1:
            if element in lst2:
                yield element

    def save(self, *args, **kwargs):
        models.Model.save(self, *args, **kwargs)
        if self.status == DealStatus.ACCEPTED:
            UserFeedback.objects.create(creator=self.user, user=self.partner)
            UserFeedback.objects.create(creator=self.partner, user=self.user)

    class Meta:
        get_latest_by = ['pk']



class VirtualDeal(Deal):
    status = 0

    @classmethod
    def by_users(cls, me_, other_users, level=2):
        deals = []
        # Calculate possible Deals
        for user in other_users:
            deal = cls(user1=me_, user2=user)
            if deal.level == level:
                deals.append(deal)

        # Calculate max Quality
        max_quality = max(
                (deal.quality for deal in deals)
            ) if deals else 0

        # Calculate Quality Percentage of each deal (for view/css)
        for deal in deals:
            deal.max_quality = max_quality
            deal.quality_pct = int(deal.quality / max_quality * 100 + 0.5)

        return sorted(deals, key=lambda x: x.quality, reverse=True)

    @classmethod
    def by_user(cls, me_, partner, level=2):
        deals = cls.by_users(me_, [partner], level=level)
        return deals[0] if deals else None

    def save(self):
        pass

    class Meta:
        proxy = True
