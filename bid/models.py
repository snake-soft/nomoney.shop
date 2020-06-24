from django.db import models
from django.utils.timezone import now
from config.settings import AUTH_USER_MODEL


class BidPositionBase(models.Model):
    listing = None
    deal = models.ForeignKey('deal.Deal', on_delete=models.CASCADE)
    bid = models.ForeignKey(
        'Bid',
        on_delete=models.CASCADE,
        )
    quantity = models.PositiveIntegerField()
    unit = models.ForeignKey(
        'listing.Unit',
        on_delete=models.CASCADE,
        )

    @property
    def push(self):
        return self.listing

    @property
    def pull(self):
        return self.listing

    class Meta:
        abstract = True


class BidPush(BidPositionBase):
    listing = models.ForeignKey(
        'listing.Push',
        on_delete=models.CASCADE,
        )


class BidPull(BidPositionBase):
    listing = models.ForeignKey(
        'listing.Pull',
        on_delete=models.CASCADE,
        )


class StatusCode:
    UNSEEN = 0, 'unseen'
    SEEN = 10, 'seen'
    ACCEPTED = 20, 'accepted'
    ANSWERED = 30, 'answered'
    REJECTED = 40, 'rejected'

    @classmethod
    def choices(cls):
        return (cls.UNSEEN, cls.SEEN, cls.ACCEPTED, cls.ANSWERED, cls.REJECTED)


class Bid(models.Model):
    deal = models.ForeignKey('deal.Deal', on_delete=models.CASCADE)

    pushs = models.ManyToManyField(
        'listing.Push',
        through=BidPush,
        through_fields=('bid', 'listing'),
        )

    pulls = models.ManyToManyField(
        'listing.Pull',
        through=BidPull,
        through_fields=('bid', 'listing'),
        )

    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )

    datetime = models.DateTimeField(default=now, editable=False)

    status = models.PositiveSmallIntegerField(
        default=StatusCode.UNSEEN[0],
        choices=StatusCode.choices(),
        )

    @property
    def push_positions(self):
        return self.bidpush_set.all()

    @property
    def pull_positions(self):
        return self.bidpull_set.all()

    @property
    def is_latest(self):
        return self.get_latest() == self

    def get_latest(self):
        return self.deal.bid_set.latest()  # .order_by('datetime')

    def get_users(self):
        return self.deal.users.all()

    def same_constellation(self):
        print("Rework")
        return self.deal.bid_set.all()

    @classmethod
    def by_user(cls, user):
        return user.bid_set.all()

    def __lt__(self, other):
        return self.datetime < other.datetime

    class Meta:
        ordering = ['-datetime']
        get_latest_by = ['-datetime']
