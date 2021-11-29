from cgi import FieldStorage
from hashlib import md5
from typing import Callable, List, Tuple

from errors.api_error import ApiError
from json import loads, dumps


def get_users() -> List[dict]:
    with open('users.json', 'r') as file:
        return loads(file.read())


def get_user_by_id(user_id: str) -> dict:
    with open('users.json', 'r') as file:
        users: List[dict] = loads(file.read())

        for user in users:
            if user_id == user['id']:
                return user

    raise ApiError(f'No user found with id `{user_id}`.')


def get_user_hash(user: dict) -> str:
    return md5(f'{user["name"]}{user["age"]}{user["city"]}'.encode('utf-8')).hexdigest()


def user_exists(user: dict) -> bool:
    try:
        get_user_by_id(user['id'])
        return True
    except (ApiError, KeyError):
        return False


def add_user(user: dict) -> None:
    if user['name'] is None or user['age'] is None or user['city'] is None:
        raise ApiError('Missing user data.')

    if not user['name'].replace(' ', '').isalnum() or not user['city'].replace(' ', '').isalnum():
        raise ApiError('User name and city must be alphanumeric.')

    if not user['age'].isnumeric():
        raise ApiError('User age must be int type.')

    user['name'] = user['name'].title()
    user['age'] = int(user['age'])
    user['city'] = user['city'].title()

    new_user = {'id': get_user_hash(user)}
    new_user.update(user)

    if user_exists(new_user):
        raise ApiError('User already there.')

    users = get_users()
    users.append(new_user)

    with open('users.json', 'w') as file:
        file.write(dumps(users))


def update_user(user: dict) -> None:
    if user['id'] is None:
        raise ApiError('Missing user id.')

    if not user_exists(user):
        raise ApiError('User does not exists.')

    for key in user.copy().keys():
        if user[key] is None:
            del user[key]

    if 'name' in user.keys():
        if not user['name'].replace(' ', '').isalnum():
            raise ApiError('User name must be alphanumeric.')

        user['name'] = user['name'].title()

    if 'age' in user.keys():
        if not user['age'].isnumeric():
            raise ApiError('User age must be int type.')

        user['age'] = int(user['age'])

    if 'city' in user.keys():
        if not user['city'].replace(' ', '').isalnum():
            raise ApiError('User city must be alphanumeric.')

        user['city'] = user['city'].title()

    users = get_users()

    for u in users:
        if u['id'] == user['id']:
            u.update(user)
            u['id'] = get_user_hash(u)

    with open('users.json', 'w') as file:
        file.write(dumps(users))


def delete_user(user: dict) -> None:
    if user['id'] is None:
        raise ApiError('Missing user id.')

    if not user_exists(user):
        raise ApiError('User does not exists.')

    users = get_users()

    for u in users:
        if u['id'] == user['id']:
            users.remove(u)

    with open('users.json', 'w') as file:
        file.write(dumps(users))


def find_path(path: str) -> str:
    if path.endswith('/'):
        path = path[:-1]

    if path == '' or path == '/users':  # all users
        data = dumps(get_users())

    elif '/users/' in path:  # specific user
        try:
            user_id = path.split('/')[2]
            data = dumps(get_user_by_id(user_id))
        except ApiError:
            data = f'Not found `{path}` path'

    else:  # other pages
        data = f'Not found `{path}` path'

    return data


def post(post_data: FieldStorage) -> None:
    user = {
        'name': post_data.getvalue('name'),
        'age': post_data.getvalue('age'),
        'city': post_data.getvalue('city')
    }

    add_user(user)


def put(put_data: FieldStorage) -> None:
    user = {
        'id': put_data.getvalue('id'),
        'name': put_data.getvalue('name'),
        'age': put_data.getvalue('age'),
        'city': put_data.getvalue('city')
    }

    update_user(user)


def delete(delete_data: FieldStorage) -> None:
    user = {
        'id': delete_data.getvalue('id'),
    }

    delete_user(user)


def choosing_method(environ: dict) -> (str, bytes):
    status_code = '200'

    method = environ['REQUEST_METHOD']
    request_data = FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
    )

    data = find_path('/users')

    if method == 'GET':
        path: str = environ.get('PATH_INFO')
        data = find_path(path)

    elif method == 'POST':
        try:
            post(request_data)
        except ApiError:
            status_code = '400'

    elif method == 'PUT':
        try:
            put(request_data)
        except ApiError:
            status_code = '404'

    elif method == 'DELETE':
        try:
            delete(request_data)
        except ApiError:
            status_code = '404'

    else:
        status_code = '400'

    return status_code, data.encode('utf-8')


def app(environ: dict, start_response: Callable[[str, List[Tuple[str, str]]], None]) -> List[bytes]:
    status_code, data = choosing_method(environ)
    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status_code, headers)

    return [data]
