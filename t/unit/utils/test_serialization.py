import base64
import json as _json
import pytest
from typing import Mapping
from hypothesis import given
from hypothesis.strategies import binary, dictionaries, text
from faust.utils.compat import want_str
from faust.utils.serialization import (
    loads, dumps, json, binary as _binary, text_encoding,
)

DATA = {'a': 1, 'b': 'string'}


@pytest.mark.parametrize('serializer', ['json', 'pickle'])
def test_json_subset(serializer: str) -> None:
    assert loads(serializer, dumps(serializer, DATA)) == DATA


@given(binary())
def test_binary(input: bytes) -> None:
    assert loads('binary', dumps('binary', input)) == input


@given(text())
def test_text(input: str) -> None:
    assert loads('text', dumps('text', input)) == input


@given(dictionaries(text(), text()))
def test_combinators(input: Mapping[str, str]) -> None:
    s = json() | _binary() | text_encoding('utf-32')
    assert (repr(s).replace("u'", "'") ==
            "json() | binary() | text_encoding('utf-32')")

    d = s.dumps(input)
    assert isinstance(d, bytes)
    assert _json.loads(want_str(base64.b64decode(d))) == input
