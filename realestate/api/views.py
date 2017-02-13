from rest_framework import viewsets
from realestate.listing.models import Listing, Attribute, AttributeListing
from realestate.api.serializers import ListingSerializer
from rest_framework.response import Response
import json
import geocoder


class PaginationMixin(object):
    paginate_by = 15
    paginate_by_param = 'limit'
    max_paginate_by = 100


class ListingViewSet(PaginationMixin, viewsets.ModelViewSet):  # viewsets.ReadOnlyModelViewSet):
    model = Listing
    serializer_class = ListingSerializer
    queryset = Listing.objects.none()

    def get_queryset(self):
        queryset = Listing.objects.active()

        last_modified = self.request.query_params.get('modified_from')
        if last_modified is not None:
            queryset = queryset.filter(last_modified__gt=last_modified)

        return queryset

    def create(self, request, *args, **kwargs):
        new_listing = Listing.objects.create(active=True)
        new_listing.title = request.data['title']
        new_listing.description = request.data['description']
        new_listing.coords = request.data['coords']

        # files
        for name, img in request.FILES.items():
            i = new_listing.images.create(name=name)
            i.image.save(name, img)

        # features
        for feat in json.loads(request.data['features']):
            feature_name = feat.get('featureDescription')
            feature, _created = Attribute.objects.get_or_create(name=feature_name, validation='realestate.listing.utils.validation_simple')
            AttributeListing.objects.get_or_create(listing=new_listing, attribute=feature)

        # gis
        coords = list(map(float, new_listing.coords.split(',')))
        location = geocoder.google(coords,method='reverse')

        print unicode(location)

        #print("LOCATION_STREET: {}".format(house.street))
        #print("LOCATION_SECTOR: {}".format(house.postal))
        #print("LOCATION_CITY: {}".format(house.city))
        #print("LOCATION_STATE: {}".format(house.state))

        new_listing.save()

        serializer = ListingSerializer(new_listing, many=False, context={'request': request})
        return Response(serializer.data)


