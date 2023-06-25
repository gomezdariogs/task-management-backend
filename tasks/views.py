import json
import base64

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task, Board, Assignee, Column, User
from django.core.files.base import ContentFile


def decode_base64(string_to_decode: str):
    format, imgstr = string_to_decode.split(';base64,')
    ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(imgstr), name='temp.' + ext)


@csrf_exempt
def create_assignee(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(username=body['user'])
        img = decode_base64(body['picture'])
        new_boards = []
        for board_id in body['boards']:
            if Board.objects.filter(id=board_id).exists():
                board = Board.objects.get(id=board_id)
                new_boards.append(board)
            else:
                return JsonResponse({'status': '404', 'message': f'Board with id {board_id} not found'},
                                    status=404)
        assignee = Assignee(name=body['name'], picture=img, user=user)
        assignee.save()
        assignee.boards.set(new_boards)
        del body['picture']
        return JsonResponse({'status': '200', 'response': f'Assignee {body} created successfully'})
    except User.DoesNotExist:
        return JsonResponse({'status': '404', 'message': f'User with username {body["user"]} not found'}, status=404)


@csrf_exempt
def delete_assignee(request, id):
    try:
        obj = Assignee.objects.get(id=id)
        obj.delete()
        return JsonResponse({'status': 200, 'response': f'Assignee with id {id} was deleted successfully'})
    except Assignee.DoesNotExist:
        return JsonResponse({'status': 404, 'message': f'Assignee with id {id} not found'}, status=404)


@csrf_exempt
def edit_assignee(request, id):
    new_body = json.loads(request.body.decode('utf-8'))
    img = decode_base64(new_body['picture'])
    user = User.objects.get(username=new_body['user'])  # must be an unassigned user
    assignee = Assignee.objects.get(id=id)
    new_boards = []
    try:
        for board_id in new_body['boards']:
            if Board.objects.filter(id=board_id).exists():
                board = Board.objects.get(id=board_id)
                new_boards.append(board)
            else:
                return JsonResponse({'status': 404, 'message': f'Board with id {board} not found'}, status=404)
        assignee.boards.set(new_boards)
        assignee.name = new_body['name']
        assignee.picture = img
        assignee.user = user
        assignee.save()
        return JsonResponse({'status': 200, 'response': f'Assignee with id {id} was updated successfully'})
    except Assignee.DoesNotExist:
        return JsonResponse({'status': 404, 'message': f'Assignee with id {id} not found'}, status=404)


@csrf_exempt
def retrieve_all_assignees(request):
    assignees = serializers.serialize('json', Assignee.objects.all())
    return HttpResponse(assignees, content_type="application/json")


@csrf_exempt
def retrieve_assignee(request, id):
    try:
        assignee = Assignee.objects.get(id=id)
        data = assignee.get_details()
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Assignee.DoesNotExist:
        return JsonResponse({'status': '404', 'message': f'Assignee with id {id} not found'}, status=404)


@csrf_exempt
def create_board(request):
    body = json.loads(request.body.decode('utf-8'))
    board = Board(name=body['name'], description=body['description'])
    board.save()
    return JsonResponse({'status': '200', 'response': f'Board {body} was created successfully'})


@csrf_exempt
def delete_board(request, id):
    try:
        board = Board.objects.get(id=id)
        board.delete()
        return JsonResponse({'status': 200, 'response': f'Board with id {id} was deleted successfully'})
    except Board.DoesNotExist:
        return JsonResponse({'status': 404, 'message': f'Board with id {id} not found'}, status=404)


@csrf_exempt
def edit_board(request, id):
    new_body = json.loads(request.body.decode('utf-8'))
    board = Board.objects.filter(id=id)
    if board.exists():
        board.update(name=new_body['name'], description=new_body['description'])
        return JsonResponse({'status': '200', 'response': f'Board with id {id} was updated successfully'})
    else:
        return JsonResponse({'status': '404', 'message': f'Board with id {id} not found'}, status=404)


@csrf_exempt
def retrieve_all_boards(request):
    boards = serializers.serialize('json', Board.objects.all())
    return HttpResponse(boards, content_type="application/json")


@csrf_exempt
def retrieve_board(request, id):
    try:
        board = Board.objects.get(id=id)
        data = board.get_details()
        return HttpResponse(json.dumps(data), content_type="application/json")
    except Board.DoesNotExist:
        return JsonResponse({'status': '404', 'message': f'Board with id {id} not found'}, status=404)


@csrf_exempt
def create_task(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        assignee = Assignee.objects.get(id=body['assignee'])
        board = Board.objects.get(id=body['board'])
        column = Column.objects.get(id=body['column'])
        task = Task(name=body['name'], description=body['description'], assignee=assignee, board=board, column=column)
        task.save()
        return JsonResponse({'status': '200', 'response': f'Task {body} created successfully'})
    except Assignee.DoesNotExist:
        return JsonResponse({'status': '404', 'message': f'Assignee with id {body["assignee"]} not found'}, status=404)
    except Board.DoesNotExist:
        return JsonResponse({'status': '404', 'message': f'Board with id {body["board"]} not found'}, status=404)
    except Column.DoesNotExist:
        return JsonResponse({'status': '404', 'message': f'Column with id {body["column"]} not found'}, status=404)


@csrf_exempt
def delete_task(request, id):
    try:
        obj = Task.objects.get(id=id)
        obj.delete()
        return JsonResponse({'status': 200, 'response': f'Task with id {id} was deleted successfully'})
    except Task.DoesNotExist:
        return JsonResponse({'status': 404, 'message': f'Task with id {id} not found'}, status=404)


@csrf_exempt
def edit_task(request, id):
    try:
        new_body = json.loads(request.body.decode('utf-8'))
        assignee = Assignee.objects.get(id=new_body['assignee'])
        board = Board.objects.get(id=new_body['board'])
        column = Column.objects.get(id=new_body['column'])
        task = Task.objects.filter(id=id)
        if task.exists():
            task.update(name=new_body['name'], description=new_body['description'], assignee=assignee, board=board,
                        column=column)
            return JsonResponse({'status': '200', 'response': f'Task with id {id} was updated successfully'})
        else:
            return JsonResponse({'status': '404', 'message': f'Task with id {id} not found'}, status=404)
    except Assignee.DoesNotExist:
        return JsonResponse({'status': '404', 'message': f'Assignee with id {new_body["assignee"]} not found'},
                            status=404)
    except Board.DoesNotExist:
        return JsonResponse({'status': '404', 'message': f'Board with id {new_body["board"]} not found'}, status=404)
    except Column.DoesNotExist:
        return JsonResponse({'status': '404', 'message': f'Column with id {new_body["column"]} not found'}, status=404)


@csrf_exempt
def retrieve_all_tasks(request):
    boards = serializers.serialize('json', Task.objects.all())
    return HttpResponse(boards, content_type="application/json")


@csrf_exempt
def retrieve_task(request, id):
    try:
        task = Task.objects.get(id=id)
        data = task.get_details()
        return HttpResponse(json.dumps(data), content_type="application/json")
    except Task.DoesNotExist:
        return JsonResponse({'status': '404', 'message': f'Task with id {id} not found'}, status=404)


def custom400(request, exception=None):
    return JsonResponse({
        'status_code': 400,
        'error': 'Bad request'
    }, status=400)


def custom403(request, exception=None):
    return JsonResponse({
        'status_code': 403,
        'error': 'Permission denied'
    }, status=403)


def custom404(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'error': 'Page not found'
    }, status=404)


def custom500(request):
    return JsonResponse({
        'status_code': 500,
        'error': 'Server error'
    }, status=500)
