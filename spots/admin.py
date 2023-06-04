from django.contrib import admin
from spots.models import Tag, Province, SpotLike, Spot

admin.site.register(Tag)
admin.site.register(Province)
admin.site.register(Spot)
admin.site.register(SpotLike)
