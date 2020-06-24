from django import forms
from .models import Bid, BidPush, BidPull

BID_POSITION_FIELDS = ['quantity', 'unit']


class BidForm(forms.ModelForm):

    def __init__(self, deal, *args, **kwargs):
        self.deal = deal
        super().__init__(*args, **kwargs)

    class Meta:
        model = Bid
        fields = []
        #fields = ['comment']


class BidPositionFormBase(forms.ModelForm):

    def __init__(self, listing, *args, **kwargs):
        self.listing = listing
        super().__init__(*args, **kwargs)

    def get_initial_for_field(self, field, field_name):
        if field_name == 'quantity':
            return 0  # Vorheriges gebot
        elif field_name == 'unit':
            return self.listing.unit.pk

    def save(self, bid, commit=True):
        obj = super().save(commit=False)
        obj.listing = self.listing
        obj.bid = bid
        obj.save()


class BidPushForm(BidPositionFormBase, forms.ModelForm):

    class Meta:
        model = BidPush
        fields = BID_POSITION_FIELDS


class BidPullForm(BidPositionFormBase, forms.ModelForm):

    class Meta:
        model = BidPull
        fields = BID_POSITION_FIELDS
