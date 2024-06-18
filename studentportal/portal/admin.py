from django.contrib import admin
from .models import *
# Register your models here.

class NotesAdmin(admin.ModelAdmin):
	empty_value_display = '-empty-'
	list_display = ('user', 'title')
	list_display_links = ('title',)
admin.site.register(Notes, NotesAdmin)


admin.site.register(Homework)
admin.site.register(Todo)
admin.site.register(Diary)