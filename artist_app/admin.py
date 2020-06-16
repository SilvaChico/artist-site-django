from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.

# the module name is app_name.models
from artist_app.models import Artist, Project, ArtWork, MyProfile

class MyProfileAdmin(admin.ModelAdmin):
    if MyProfile.objects.exists():
        def has_add_permission(self, request):
            return False
        def has_delete_permission(self, request, obj=None):
             return False

class ArtWorkInline(admin.TabularInline):
    model = ArtWork

class ProdjectAdmin(admin.ModelAdmin):
    inlines = [ArtWorkInline]

# Register your models to admin site, then you can add, edit, delete and search your models in Django admin site.
admin.site.register(MyProfile, MyProfileAdmin)
admin.site.register(Project, ProdjectAdmin)
admin.site.register(ArtWork)
admin.site.unregister(Group)
admin.site.register(Artist)


