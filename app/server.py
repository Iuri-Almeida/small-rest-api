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


def app(environ: dict, start_response: Callable[[str, List[Tuple[str, str]]], None]) -> List[bytes]:

    path: str = environ.get('PATH_INFO')

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

    data = data.encode('utf-8')

    status = '200 OK'
    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, headers)

    return [data]
