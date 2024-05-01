from rest_framework import serializers
from auctions.models import Bids, Listing

class BidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bids
        fields = '__all__'


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'