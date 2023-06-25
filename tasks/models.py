from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

class Board(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f' {str(self.id)}:  {self.name}'

    def get_details(self):
        data = model_to_dict(self)
        assignees = self.assignee_set.all()
        tasks = self.task_set.all()
        columns = self.column_set.all()
        assignees_list = []
        tasks_list = []
        columns_list = []
        for assignee in assignees: assignees_list.append(assignee.get_details())
        for task in tasks: tasks_list.append(task.get_details())
        for column in columns: columns_list.append(column.get_details())
        data['assignees'] = assignees_list
        data['tasks'] = tasks_list
        data['columns'] = columns_list
        return data


class Column(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    position = models.IntegerField()
    size = models.IntegerField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return f' {str(self.id)}:  {self.name}'

    def get_details(self):
        data = model_to_dict(self)
        data['board'] = model_to_dict(self.board)
        return data


class Assignee(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='images/', default='images/default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    boards = models.ManyToManyField(Board)

    def __str__(self):
        return f' {str(self.id)}:  {self.name}'

    def get_boards(self):
        return f'[{", ".join([b.name for b in self.boards.all()])}]'

    def get_details(self):
        data = model_to_dict(self)
        data['picture'] = self.picture.url
        data['boards'] = list(self.boards.values())
        return data


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    assignee = models.ForeignKey(Assignee, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)

    def __str__(self):
        return f' {str(self.id)}: {self.name}'

    def get_details(self):
        data = model_to_dict(self)
        data['assignee'] = self.assignee.get_details()
        data['board'] = model_to_dict(self.board)
        data['column'] = self.column.get_details()
        return data

class Permission(models.Model):
    PERMISSION_CHOICES = [('W', 'write'), ('R', 'read')]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50,choices=PERMISSION_CHOICES) #Has to be one of Permission Enum class
    assignee = models.ManyToManyField(Assignee)

    def __str__(self):
        return f' {str(self.id)}: {self.name}'

    def get_assignees(self):
        return f'[{", ".join([b.name for b in self.assignee.all()])}]'