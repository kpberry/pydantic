try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

import pytest

from pydantic import BaseModel, ValidationError
from pydantic.errors import DictMissingKeysError


def test_basic_typed_dict():
    TD = TypedDict('TD', {'a': int, 'b': str})

    class Model(BaseModel):
        td: TD

    d = {'a': 123, 'b': 'foo'}
    m = Model(td=d)

    assert m.td == d


def test_typed_dict_non_dict_value():
    TD = TypedDict('TD', {'a': int, 'b': str})

    class Model(BaseModel):
        td: TD

    with pytest.raises(ValidationError):
        Model(td='123')


def test_typed_dict_extra_keys():
    TD = TypedDict('TD', {'a': int, 'b': str})

    class Model(BaseModel):
        td: TD

    d = {'a': 123, 'b': 'foo', 'c': 'bar'}
    m = Model(td=d)

    # c should get dropped since it's not part of the type
    assert m.td == {'a': 123, 'b': 'foo'}


def test_typed_dict_missing_keys():
    TD = TypedDict('TD', {'a': int, 'b': str})

    class Model(BaseModel):
        td: TD

    d = {'a': 123}
    with pytest.raises(DictMissingKeysError):
        Model(td=d)


def test_typed_dict_missing_keys_and_extra_keys():
    TD = TypedDict('TD', {'a': int, 'b': str})

    class Model(BaseModel):
        td: TD

    d = {'a': 123, 'c': 123}
    with pytest.raises(DictMissingKeysError):
        Model(td=d)


def test_typed_dict_invalid_value():
    TD = TypedDict('TD', {'a': int, 'b': str})

    class Model(BaseModel):
        td: TD

    d = {'a': 'bar', 'b': 'foo'}
    with pytest.raises(ValidationError):
        Model(td=d)


def test_typed_dict_in_nested_model():
    TD = TypedDict('TD', {'a': int, 'b': str})

    class A(BaseModel):
        td: TD

    class B(BaseModel):
        a: A

    d = {'a': 123, 'b': 'foo'}
    m = B(a=A(td=d))

    assert m.a.td == d
