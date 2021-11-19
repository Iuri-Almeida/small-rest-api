from typing import Callable, List, Tuple, Optional
from routes import home, not_found
from json import loads, dumps


def get_users() -> List[dict]:

    with open('users.json', 'r') as file:
        return loads(file.read())


def get_user_by_name(name: str) -> Optional[dict]:

    with open('users.json', 'r') as file:
        users: List[dict] = loads(file.read())

        for user in users:
            if name.title() in user['name'].split():
                return user

    return None


def app(environ: dict, start_response: Callable[[str, List[Tuple[str, str]]], None]) -> List[bytes]:

    path: str = environ.get('PATH_INFO')

    if path.endswith('/'):
        path = path[:-1]

    if path == '':  # index
        user = get_user_by_name('Pedro')

        data = home({'user': dumps(user)})
    else:  # other pages
        data = not_found({'path': path})

    data = data.encode('utf-8')

    status = '200 OK'
    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, headers)

    return [data]
