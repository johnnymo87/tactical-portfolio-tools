import hypothesis.strategies as s
from hypothesis import given

from lib.hello_world import HelloWorld


def test_world():
    assert HelloWorld.hello_world() == "hello world"


@given(s.lists(s.integers()))
def test_hypothesis(xs):
    ys = xs.copy()
    ys.reverse()
    ys.reverse()
    assert ys == xs
