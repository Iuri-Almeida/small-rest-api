from typing import Callable, List, Tuple
from routes import home, not_found


def app(environ: dict, start_response: Callable[[str, List[Tuple[str, str]]], None]) -> List[bytes]:

    path: str = environ.get('PATH_INFO')

    if path.endswith('/'):
        path = path[:-1]

    if path == '':  # index
        data = home()
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
