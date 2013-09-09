from django.contrib import admin
from chat.models import Room

class RoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(Room, RoomAdmin)
