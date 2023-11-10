class Base:
    __slots__ = ()
    __truediv__ = lambda self, other: tuple(self // other)
    __divmod__ = lambda self, other: (self / other, self.temp)
    __gt__ = lambda self, item: True
    def __rdivmod__(self, other: int):
        r = self / other
        return self.temp, r


class Constant(Base):
    """please see oft/doc/constant"""


class Repeat(Base):
    """please see oft/doc/repeat"""
    __slots__ = "v"
    v: int
    def __init__(self, v: int):
        self.v = v
    
    def __floordiv__(self, other: int):
        while True:
            other, v = divmod(other, self.v)
            v: int
            yield v
    
    def __mul__(self, other: tuple) -> int:
        c = 0
        for p, i in enumerate(other):
            c += i * self.v ** p
        return c
    
    def __gt__(self, item: tuple) -> bool:
        return all(map(lambda x: x < self.v, item))


class Repeat_(Repeat):
    """please see oft/doc/spacial repeat"""
    __slots__ = "v", "m", "temp"
    v: int
    temp: int
    def __init__(self, v: int, m: int):
        self.v = v
        self.m = m
    
    def __floordiv__(self, other: int):
        for _ in range(self.m):
            other, v = divmod(other, self.v)
            v: int
            yield v
        self.temp = other
    
    def __int__(self) -> int:
        return int(self.v) ** self.temp
    
    def __gt__(self, item: tuple) -> bool:
        return super().__gt__(item) and len(item) < self.m


class Number(Repeat):
    """please see oft/doc/number"""
    def __floordiv__(self, other: int):
        while True:
            if not other:
                self.temp = other
                return
            other, v = divmod(other, self.v)
            v: int
            yield v


class Struct(Base):
    """please see oft/doc/struct"""
    __slots__ = "ft", "temp"
    ft: tuple
    temp: int
    def __init__(self, *ft: int):
        self.ft = ft
    
    def __floordiv__(self, other: int):
        for x in self.ft:
            other, a = divmod(other, x)
            yield a
        self.temp = other
    
    def __int__(self) -> int:
        i = 1
        for item in self.ft:
            i *= int(item)
        return i
    
    def __mul__(self, other: tuple):
        c = 0
        p = 1
        for i, j in zip(other, self.ft):
            c += i * p
            p *= j
        return c
    
    def __gt__(self, other: tuple):
        return all(map(lambda x, y: x < y, other, self.ft)) and len(other) == len(self.ft)


class Compress(Repeat):
    """please see oft/doc/compress"""
    __slots__ = "v"
    v: int
    def __init__(self, v: int):
        self.v = v
    
    def __floordiv__(self, other: int):
        pos = 0
        while True:
            pairs = int(self.v) ** pos
            if pairs > other:
                break
            other -= pairs
            pos += 1
        yd = super().__floordiv__(other)
        yield from (next(yd) for _ in range(pos))
    
    def __mul__(self, other: tuple) -> int:
        c = 0
        for p, i in enumerate(other):
            pairs = self.v ** p
            c += pairs
            c += i * pairs
        return c


class Concat(Base):
    """please see oft/doc/concat"""
    __slots__ = "ft", "temp"
    ft: tuple
    def __init__(self, *ft: int):
        self.ft = ft
    
    def __int__(self):
        return sum(map(int, self.ft))
    
    def __floordiv__(self, other: int):
        for ft in self.ft:
            size = int(ft)
            if other < size:
                yield from ft // other
                return
            other -= size
        self.temp = other
    
    def __mul__(self, other: tuple):
        p = 0
        for i in self.ft:
            if other < i:
                return p + i * other
            p += int(i)
        raise ValueError
    
    def __gt__(self, item: tuple):
        return any(map(lambda x: item < x, self.ft))


class Two(Base):
    """please see oft/doc/two"""
    __slots__ = "one", "two"
    def __init__(self, one: int, two: int):
        self.one = one
        self.two = two
    
    def __floordiv__(self, other: tuple):
        return self.one // (self.two * other)
    
    def __mod__(self, other: tuple):
        return self.two // (self.one * other)
            
    def __mul__(self, other: tuple):
        return self.two / (self.one * other)
