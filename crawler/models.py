from django.db import models

class Domain(models.Model):
    domain_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Page(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    url = models.URLField()
    status_code = models.IntegerField()
    crawled_at = models.DateTimeField(auto_now_add=True)

class Insight(models.Model):
    page = models.OneToOneField(Page, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    h1 = models.JSONField(default=list)
    h2 = models.JSONField(default=list)
    h3 = models.JSONField(default=list)
    p_count = models.IntegerField(default=0)
    image_count = models.IntegerField(default=0)
    internal_links = models.IntegerField(default=0)
    external_links = models.IntegerField(default=0)
    keywords = models.JSONField(default=list)