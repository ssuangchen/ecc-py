from unittest import TestCase


class Point:
    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        if self.x is None and self.y is None:
            return
        if self.y ** 2 != self.x ** 3 + a * x + b:
            raise ValueError('({},{}) is not on the curve'.format(x, y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        # 同一条曲线
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {},{} are not on the same curve'.format(self, other))
        # self是无穷远点
        if self.x is None:
            return other
        # other是无穷远点
        if other.x is None:
            return self
        # 两点所在直线垂直X轴,x相同,y不同
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        # x不同
        if self.x != other.x:
            k = (other.y - self.y) / (other.x - self.x)  # 斜率
            x3 = k ** 2 - self.x - other.x
            y3 = k * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)
        # x相同,y相同
        if self == other:
            k = (3 * self.x ** 2 + self.a) / (2 * self.y)  # 斜率
            x3 = k ** 2 - 2 * self.x
            y3 = k * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)
        if self == other and self.y == 0:
            return self.__class__(None, None, self.a, self.b)


class PointTest(TestCase):
    def test_ne(self):
        a = Point(x=3, y=-7, a=5, b=7)
        b = Point(x=18, y=77, a=5, b=7)
        self.assertTrue(a != b)
        self.assertFalse(a != a)

    def test_add0(self):
        a = Point(x=None, y=None, a=5, b=7)
        b = Point(x=2, y=5, a=5, b=7)
        c = Point(x=2, y=-5, a=5, b=7)
        self.assertEqual(a + b, b)
        self.assertEqual(b + a, b)
        self.assertEqual(b + c, a)

    def test_add1(self):
        a = Point(x=3, y=7, a=5, b=7)
        b = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(a + b, Point(x=2, y=-5, a=5, b=7))

    def test_add2(self):
        a = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(a + a, Point(x=18, y=77, a=5, b=7))
