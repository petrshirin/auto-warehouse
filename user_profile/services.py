from typing import Union, Dict

from django.contrib.auth.password_validation import validate_password, ValidationError
from django.db.models import Q, QuerySet
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from .exceptions import UniqueUser
from .models import UserRegistrationCode, UserProfile
from .serializers import UserProfileSerializer, UserProfilePostSerializer


def check_registration_code(request: Request) -> bool:
    """
    Check user's code in login form
    :param request:
    :return: True/False
    """
    user_code = request.data.get('code')
    if not user_code:
        return False
    code: UserRegistrationCode = UserRegistrationCode.objects.filter(user=request.user).first()
    if not code:
        return False
    if code.code == user_code:
        request.user.userprofile.is_active = True
        request.user.userprofile.save()
        code.is_used = True
        code.save()
        return True
    else:
        return False


def process_registration(request: Request) -> Dict:
    """
        This controller get data in request and register new user.
        If user was created successfully - return info about current user with id
        :param request:
        :return:
    """
    try:
        check_password(request.data.get('password1', 1), request.data.get('password2', 2))
        validate_password(request.data.get('password1', ''))
    except ValueError as err:
        return {'errors': str(err), 'success': False}
    except ValidationError as err:
        return {'errors': err, 'success': False}

    try:
        check_user_from_db(request.data.get('username'), request.data.get('email'))
    except UniqueUser as err:
        return {'errors': str(err), 'success': False}
    user = User.objects.create_user(username=request.data.get('email'),
                                    password=request.data.get('password1'),
                                    email=request.data.get('email'))
    key = generate_token(user)
    UserProfile.objects.create(user=user)

    if key is not None:
        return {'success': True, 'key': key}
    else:
        return {'success': False,
                'errors': "Токен не сгенерирован, используйте форму логина"}


def check_user_from_db(username: str, email: str) -> bool:
    """
    function check username in db
    if username or email are not unique - raise Exception UniqueUser
    :param email:
    :param username:
    :return: True
    """
    if User.objects.filter(Q(username=username) | Q(email=email)).first():
        raise UniqueUser("Пользователь уже существует")
    else:
        return True


def check_password(password1: str, password2: str) -> bool:
    """
    Check two password on match or raise Exception ValueError
    :param password1:
    :param password2:
    :return: True
    """
    if password1 == password2:
        return True
    else:
        raise ValueError('Пароли не совпадают')


def generate_token(user: User) -> Union[str, None]:
    token = Token.objects.create(user=user)
    if token.created:
        return token.key
    else:
        return None


def get_user_info(user: User) -> ReturnDict:
    user_profile: UserProfile = user.userprofile
    ser = UserProfileSerializer(user_profile)
    return ser.data


def search_users(search_str: str) -> ReturnList:

    user_profiles: QuerySet[UserProfile] = UserProfile.objects.filter(fio__contains=search_str).all()
    ser = UserProfileSerializer(user_profiles, many=True)
    return ser.data


def change_user_info(user: User, data: Dict) -> Dict:
    ser = UserProfilePostSerializer(data=data)
    if ser.is_valid():
        data = dict(ser.validated_data)
        email = data['email']
        del data['email']
        user.email = email
        user.save()
        UserProfile.objects.filter(user=user).update(**data)
        return {"success": True, "data": UserProfileSerializer(user.userprofile).data}
    else:
        return {"success": False, "errors": ser.errors}