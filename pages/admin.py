from django.contrib import admin

from .models import Page, BreadcrumbParents, Widget


class BreadcrumbInline(admin.TabularInline):
    model = BreadcrumbParents
    extra = 0


class WidgetInline(admin.StackedInline):
    model = Widget
    extra = 0


class PageAdmin(admin.ModelAdmin):
    inlines = [WidgetInline, BreadcrumbInline]
    save_on_top = True


admin.site.register(Page, PageAdmin)
