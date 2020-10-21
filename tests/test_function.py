import json
from typing import List

from . import TestGramex


def yielder(*items):
    for i in items:
        yield i


def total(*items: float) -> float:
    return sum(items)


def total_list(items: List[int], start: float) -> float:
    return sum(items, start)


def strtotal(*items: str) -> str:
    s = ''
    for i in items:
        s += i
    return s


def name_age(name, age):
    return f'{name} is {age} years old.'


def urlparse_hinted(name: str, age: int) -> str:
    return f'{name} is {age} years old.'


def native_types(a: int, b: float, c: bool, d: None):
    return {'msg': f'{a} items @ {b} each together cost {a * b}.', 'c': c, 'd': d}


def greet(name="Stranger"):
    return f'Hello, {name}!'


class TestFunction(TestGramex):

    def test_yield(self):
        self.check('/func/yielder?items=a&items=b&items=c', text="abc")

    def test_add_handler_get(self):
        self.check('/func/total/40/2', text="42.0")
        self.check('/func/name/johndoe/age/42', text="johndoe is 42 years old.")
        self.check('/func/foo?name=johndoe&age=42', text="johndoe is 42 years old.")
        # When type hints are violated:
        self.check('/func/hints?name=johndoe&age=42.3', code=500)
        # When multiple arguments are passed:
        self.check('/func/multi?items=1&items=2&items=3', text="6.0")
        self.check('/func/multilist?items=1&items=2&items=3&start=1', text="7.0")
        # Positional args with types
        self.check('/func/strtotal?items=a&items=b&items=c', text='abc')
        # Test native types:
        self.check(
            '/func/nativetypes?a=3&b=1.5&c=false&d=null',
            text='{"msg": "3 items @ 1.5 each together cost 4.5.", "c": false, "d": "null"}')
        self.check('/func/defaultNamed', text="Hello, Stranger!")
        self.check('/func/defaultNamed?name=gramex', text="Hello, gramex!")
        self.check('/func/multilist?items=1&items=2&items=3&start=1', text="7.0")

    def test_add_handler_delete(self):
        self.check('/func/total/40/2', text="42.0", method='delete')

    def test_add_handler_post(self):
        self.check(
            '/func/foo', method='post', data={'name': 'johndoe', 'age': '42'},
            text="johndoe is 42 years old.")
        self.check(
            '/func/foo', method='post', data=json.dumps({'name': 'johndoe', 'age': '42'}),
            text="johndoe is 42 years old.")
        # When type hints are violated:
        self.check('/func/hints', method='post', data={'name': 'johndoe', 'age': '42.3'},
                   code=500)
        # Check typecasting
        self.check(
            '/func/nativetypes', method='post',
            data=json.dumps({'a': 3, 'b': 1.5, 'c': False, 'd': None}),
            text='{"msg": "3 items @ 1.5 each together cost 4.5.", "c": false, "d": null}')
        self.check('/func/defaultNamed', text="Hello, Stranger!")
        # Check if POSTing urlparams and path args works
        self.check('/func/foo?name=johndoe&age=42', method='post', text="johndoe is 42 years old.")
        self.check('/func/name/johndoe/age/42', text="johndoe is 42 years old.")
