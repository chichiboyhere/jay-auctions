from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Winner)
admin.site.register(ContactMessage)

