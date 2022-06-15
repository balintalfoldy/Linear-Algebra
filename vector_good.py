from __future__ import annotations
import math
from dataclasses import dataclass, field
from decimal import Decimal, getcontext

getcontext().prec = 30

@dataclass
class Vector:
    coordinates: list
    dimension: int = field(init=False)
    magnitude: float = field(init=False)

    def __post_init__(self) -> None:
        self.coordinates = tuple([Decimal(x) for x in self.coordinates])
        self.dimension = len(self.coordinates)
        self.magnitude = self.calc_magnitude()


    # def __init__(self, coordinates):
    #     try:
    #         if not coordinates:
    #             raise ValueError
    #         self.coordinates = tuple(coordinates)
    #         self.dimension = len(coordinates)
    #         self.magnitude = self.calc_magnitude()

    #     except ValueError:
    #         raise ValueError('The coordinates must be nonempty')

    #     except TypeError:
    #         raise TypeError('The coordinates must be an iterable')


    #def __str__(self) -> str:
        #return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v) -> bool:
        return self.coordinates == v.coordinates


    def add(self, v) -> Vector:
        assert self.dimension == v.dimension, "Dimensions must be the same!"

        sum = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        
        return Vector(sum)


    def subtract(self, v) -> Vector:
        assert self.dimension == v.dimension, "Dimensions must be the same!"

        sub = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        
        return Vector(sub)


    def multiply(self, scalar) -> Vector:

        mul = [num * Decimal(scalar) for num in self.coordinates]
        
        return Vector(mul)


    def calc_magnitude(self) -> float:
        return math.sqrt(sum([n*n for n in self.coordinates]))


    def calc_normalize(self) -> Vector:
        try:
            scalar = Decimal('1.0') / Decimal(self.magnitude)
            return self.multiply(scalar)

        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')


    def dot_product(self, v):
        assert self.dimension == v.dimension, "Dimensions must be the same!"
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])


    def angle(self, v, degree=False):
        assert self.dimension == v.dimension, "Dimensions must be the same!"
        try:
            u1 = self.calc_normalize()
            u2 = v.calc_normalize()
            angle = math.acos(round(u1.dot_product(u2), 5))

            if degree:
                return math.degrees(angle)
            else:
                return angle
        except ZeroDivisionError:
            raise ZeroDivisionError('Cannot compute the angle with zero vector')
        except Exception as e:
            raise e

my_vector1 = Vector([7.35, 0.221, 5.188])
my_vector2 = Vector([2.751, 8.259, 3.985])
print(my_vector1.dot_product(my_vector2))
print(my_vector1.angle(my_vector2, degree=True))
print(my_vector1)

# Continue from parallel and orthogonal vectors
