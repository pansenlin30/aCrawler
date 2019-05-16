from acrawler.http import Request
import sys
import logging
import webbrowser
from importlib import import_module
from pathlib import Path



def request_to_dict(request: Request):

    d = {
        'url': request.url,
        'callback': request.callback,
        'method': request.method,
        'request_config': request.request_config,
        'dont_filter': request.dont_filter,
        'meta': request.meta,
        'priority': request.priority
    }
    return d


def request_from_dict(d):
    return Request(**d)


def config_from_setting(module):
    context = {}
    for key in dir(module):
        if not key.startswith('__'):
            context[key] = getattr(module, key)
    request_config = context.pop('REQUEST_CONFIG', {})
    middleware_config = context.pop('MIDDLEWARE_CONFIG', {})
    config = context
    return config, request_config, middleware_config


def merge_config(*configs):
    r = {}
    for config in configs:
        r = {**r, **config}
    return r


def check_import(name: str):
    if not name in sys.modules:
        mod = import_module(name)
        return mod
    else:
        return sys.modules[name]


def open_html(html, path=None):
    if not path:
        path = Path.home()/'.temp.html'
    url = 'file://' + str(path)
    with open(path, 'w') as f:
        f.write(html)
    webbrowser.open(url)


def get_logger(name: str = 'user'):
    if not name.startswith('acrawler.'):
        name = 'acrawler.'+name
    return logging.getLogger(name)