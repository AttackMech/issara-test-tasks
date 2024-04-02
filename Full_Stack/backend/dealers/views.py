from rest_framework import viewsets, filters
from rest_framework.pagination import CursorPagination
from django.db.models import Q
from .models import Dealer
from .serializers import DealerSerializer

class DealerPagination(CursorPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    ordering = 'id'

class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    pagination_class = DealerPagination
    
    def get_queryset(self):
        queryset = Dealer.objects.all()
        name = self.request.query_params.get('name')
        city = self.request.query_params.get('city')

        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(name_en__icontains=name))
        if city:
            queryset = queryset.filter(city__iexact=city)

        return queryset
