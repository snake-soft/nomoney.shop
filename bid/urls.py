""" urls for the bid module """
from django.urls import path
from .views import BidListView, BidCreateView, BidDetailView, BidDeleteView


urlpatterns = [
    path('', BidListView.as_view(), name='bid_list'),
    # path('partner/<int:partner_pk>/', BidListView.as_view(), name='bid_list'),
    #path('partner/<int:partner_pk>/new/', BidCreateView.as_view(), name='bid_create'),
    path('for/deal/<int:deal_pk>/new/', BidCreateView.as_view(), name='bid_create'),
    path('<int:pk>/', BidDetailView.as_view(), name='bid_detail'),
    path('<int:pk>/update/', BidDetailView.as_view(), name='bid_update'),
    path('<int:bid_pk>/delete/', BidDeleteView.as_view(), name='bid_delete'),
]
