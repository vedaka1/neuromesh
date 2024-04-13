from domain.common.response import Response

test = Response(
    value="test! (test_) ```test```, *test* test! test_ ```test```, *test* test! test_ ```test```, *test*  test! test_ ```test```,\n *test* test! test_ ```test```, *test* test! test_ ```test```, *test*"
)
print(test.value)
