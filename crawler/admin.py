from django.contrib import admin
from .models import Domain, Page, Insight


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain_name', 'created_at')
    search_fields = ('domain_name',)
    ordering = ('-created_at',)



@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'url', 'status_code', 'crawled_at')
    list_filter = ('status_code', 'domain')
    search_fields = ('url',)
    ordering = ('-crawled_at',)



@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = (
    'page',
    'title',
    'p_count',
    'image_count',
    'internal_links',
    'external_links'
    )


search_fields = ('page__url', 'title')
list_filter = ('p_count', 'image_count')

def short_title(self, obj):
    return obj.title[:50] + "..." if obj.title else ""
short_title.short_description = "Title"
