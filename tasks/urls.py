from django.urls import path

from . import views

urlpatterns = [
    path("tasks/", views.retrieve_all_tasks, name="retrieve_all_tasks"),
    path("task/<int:id>", views.retrieve_task, name="retrieve_task"),
    path("create-task", views.create_task, name="create_task"),
    path("edit-task/<int:id>", views.edit_task, name="edit_task"),
    path("delete-task/<int:id>", views.delete_task, name="delete_task"),
    path("boards/", views.retrieve_all_boards, name="retrieve_all_boards"),
    path("board/<int:id>", views.retrieve_board, name="retrieve_board"),
    path("create-board/",  views.create_board, name="create_board"),
    path("edit-board/<int:id>", views.edit_board, name="edit_board"),
    path("delete-board/<int:id>", views.delete_board, name="delete_board"),
    path("assignees/", views.retrieve_all_assignees, name="retrieve_all_assignees"),
    path("assignee/<int:id>", views.retrieve_assignee, name="retrieve_assignee"),
    path("create-assignee/", views.create_assignee, name='create_assignee'),
    path("delete-assignee/<int:id>", views.delete_assignee, name='delete_assignee'),
    path("edit-assignee/<int:id>", views.edit_assignee, name='edit_assignee'),
]
