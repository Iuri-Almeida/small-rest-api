"""
    Project: Small Rest Api

    Author: Iuri Lopes Almeida

    GitHub: https://github.com/Iuri-Almeida

    Goal: Create an rest api
"""
from abc import ABC
from gunicorn.app.base import BaseApplication
from server import app
from typing import Callable, List, Tuple


class Application(BaseApplication, ABC):

    def __init__(
            self,
            application: Callable[[dict, Callable[[str, List[Tuple[str, str]]], None]], List[bytes]],
            options: dict = None):
        self.application = application
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {}
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                config[key] = value
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    params = {
        'bind': '127.0.0.1:8000',
    }
    Application(app, params).run()
