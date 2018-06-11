
from django.contrib import admin
from django.db import models
from app.models import Countrytable, Category, Subcategory, Subgroup, Reference, Sitetable, Speciestable, PenguinnessPhotos


admin.site.register(Countrytable)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Subgroup)
admin.site.register(Reference)
admin.site.register(Sitetable)
admin.site.register(Speciestable)
admin.site.register(PenguinnessPhotos)


