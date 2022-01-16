from django.contrib import admin
from core.models import Catagory,Video
# Register your models here.
admin.site.register(Catagory)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    # list_display = ('title','slug','dscription', '', 'created','updated')
    search_fields = ('title','slug')
    prepopulated_fields = {"slug": ("title",)}
    # raw_id_fields = ('author',)
    date_hierachy = 'created'
    
