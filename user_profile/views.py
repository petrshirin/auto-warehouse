from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .services import process_registration, check_registration_code, \
    get_user_info, change_user_info, search_users
from rest_framework.authtoken.admin import User


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user_view(request: Request) -> Response:
    data = process_registration(request)
    if data.get('errors'):
        return Response(data, 422)
    else:
        return Response(data, 201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_registration_code_view(request: Request) -> Response:
    if check_registration_code(request):
        return Response({'success': True, 'data': "ok"}, 201)
    else:
        return Response({'success': False, 'errors': "Неверный код пользователя"}, 400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_self_info_view(request: Request) -> Response:
    data = get_user_info(request.user)
    return Response({"success": True, "data": data})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def self_info_view(request: Request) -> Response:
    if request.method == 'PUT':
        return change_self_info_view(request)
    else:
        return get_self_info_view(request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_self_info_view(request: Request) -> Response:
    data = request.data
    answer = change_user_info(request.user, data)
    if not answer.get('errors'):
        return Response(answer, 201)
    else:
        return Response(answer, 400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users_view(request: Request) -> Response:
    search_str = request.query_params.get('search_str')
    return Response(search_users(search_str), 200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_view(request: Request, pk: int) -> Response:
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"success": False, "error": 'user not found'}, 400)

    data = get_user_info(user)
    return Response({"success": True, "data": data}, 200)



