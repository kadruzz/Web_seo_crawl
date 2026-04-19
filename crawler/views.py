from rest_framework import generics
from .models import Domain, Page, Insight
from .serializers import DomainSerializer, PageSerializer, InsightSerializer



class DomainListView(generics.ListAPIView):
    queryset = Domain.objects.all().order_by('-created_at')
    serializer_class = DomainSerializer

class PageListView(generics.ListAPIView):
    serializer_class = PageSerializer

    def get_queryset(self):
        domain_id = self.kwargs.get('domain_id')
        return Page.objects.filter(domain_id=domain_id).order_by('-crawled_at')



class InsightView(generics.RetrieveAPIView):
    queryset = Insight.objects.all()
    serializer_class = InsightSerializer
    lookup_field = 'page_id'