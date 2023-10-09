from django.contrib import admin
from treeview.models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
	list_display = ('name', 'service_name')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'parent', 'menu')
	list_filter = ('menu',)

