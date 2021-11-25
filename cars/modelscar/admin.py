from django.contrib import admin

from .models import Color, Cars, Equipment, ImageCar


admin.site.register(Color)
admin.site.register(Equipment)

class ImageCarAdmin(admin.StackedInline):
    model = ImageCar

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    inlines = [ImageCarAdmin]
    list_display = (
        'title',
        'text',
        )
    search_fields = (
        'title',
        'year')
    list_filter = (
        'title',
        'year')

    class Meta:
       model = Cars

@admin.register(ImageCar)
class ImageCarAdmin(admin.ModelAdmin):
    pass
