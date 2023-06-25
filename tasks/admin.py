from django.contrib import admin
from .models import Board, Assignee, Task, Column, Permission


class BoardAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ['id','name',]

class AssigneeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ['id','name','picture','user','get_boards']

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ['id','name','assignee','board','column']

class ColumnAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ['id', 'name', 'position', 'size', 'board']

class PermissionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ['id', 'name', 'get_assignees']

admin.site.register(Board, BoardAdmin)
admin.site.register(Assignee, AssigneeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Permission, PermissionAdmin)
