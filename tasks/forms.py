from django import forms
from .models import Assignee, Task, Board, Column

class BoardForm(forms.ModelForm):
    class Meta:
        model: Board
        fields = "__all__"
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

class AssigneeForm(forms.ModelForm):
    class Meta:
        model = Assignee
        fields = "__all__"

class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = "__all__"