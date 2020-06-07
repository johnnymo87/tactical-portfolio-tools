from hypothesis import given
import hypothesis.strategies as s
from lib.hello import Hello

def test_world():
    assert Hello.world() == 'world'

@given(s.lists(s.integers()))
def test_hypothesis(xs):
    ys = xs.copy()
    ys.reverse()
    ys.reverse()
    assert ys == xs
