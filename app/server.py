from typing import Callable, List, Tuple

from app.errors.api_error import ApiError
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


def user_exists(user: dict) -> bool:
    try:
        get_user_by_id(user['id'])
        return True
    except (ApiError, KeyError):
        return False


def add_user(user: dict) -> None:
    if not user_exists(user):
        users = get_users()
        users.append(user)

        with open('users.json', 'w') as file:
            file.write(dumps(users))


def update_user(user: dict) -> None:
    if user_exists(user):
        users = get_users()

        for u in users:
            if u['id'] == user['id']:
                u.update(user)

        with open('users.json', 'w') as file:
            file.write(dumps(users))


def delete_user(user: dict) -> None:
    if user_exists(user):
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


def post(environ: dict) -> None:
    post_data: str = environ['wsgi.input'].readline().decode('utf-8')
    info_list = post_data.split('&')

    user = {'id': f'{abs(hash(str(info_list)))}'}

    for info in info_list:
        aux = info.split('=')

        key = aux[0]
        value = aux[1].replace('+', ' ')

        if key == 'age':
            value = int(value)

        if key == 'name':
            value = value.title()

        if key == 'name' or key == 'age' or key == 'city':
            user[key] = value

    add_user(user)


def put(environ: dict) -> None:
    put_data: str = environ['wsgi.input'].readline().decode('utf-8')
    info_list = put_data.split('&')

    user = {}

    for info in info_list:
        aux = info.split('=')

        key = aux[0]
        value = aux[1].replace('+', ' ')

        if key == 'age':
            value = int(value)

        if key == 'name':
            value = value.title()

        if key == 'id' or key == 'name' or key == 'age' or key == 'city':
            user[key] = value

    update_user(user)


def delete(environ: dict) -> None:
    delete_data: str = environ['wsgi.input'].readline().decode('utf-8')
    info_list = delete_data.split('&')

    user = {}

    for info in info_list:
        aux = info.split('=')

        key = aux[0]
        value = aux[1].replace('+', ' ')

        if key == 'id' or key == 'name' or key == 'age' or key == 'city':
            user[key] = value

    delete_user(user)


def app(environ: dict, start_response: Callable[[str, List[Tuple[str, str]]], None]) -> List[bytes]:
    method = environ['REQUEST_METHOD']

    if method == 'GET':
        path: str = environ.get('PATH_INFO')
        data = find_path(path)

    elif method == 'POST':
        post(environ)
        data = find_path('/users')

    elif method == 'PUT':
        put(environ)
        data = find_path('/users')

    elif method == 'DELETE':
        delete(environ)
        data = find_path('/users')

    else:
        raise ApiError(f'Did not understand `{method}` method.')

    data = data.encode('utf-8')

    status = '200 OK'
    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, headers)

    return [data]
