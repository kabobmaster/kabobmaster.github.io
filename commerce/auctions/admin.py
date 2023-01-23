from django.contrib import admin
from .models import listings, bids, comments

# Register your models here.
admin.site.register(listings)
admin.site.register(comments)
admin.site.register(bids)