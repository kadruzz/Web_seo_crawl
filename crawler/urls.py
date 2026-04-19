from django.urls import path
from .views import DomainListView, PageListView, InsightView

urlpatterns = [
    path('domains/', DomainListView.as_view()),
    path('domains/<int:domain_id>/pages/', PageListView.as_view()),
    path('pages/<int:page_id>/insights/', InsightView.as_view()),
]