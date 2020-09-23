from django.contrib import admin


class IssueAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_display_links = ('pk', 'title')
    search_fields = ('title',)
