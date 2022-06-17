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


    def is_parallel(self, v):
        return (self.is_zero() or v.is_zero() or self.angle(v, degree=True) in [0, 180, 360])
    

    def is_orthogonal(self, v, tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance


    def is_zero(self, tolerance=1e-10):
        return self.magnitude < tolerance


    def component_parallel_to(self, basis):
        try:
            u = basis.calc_normalize()
            weight = self.dot_product(u)
            return u.multiply(weight)
        except Exception as e:
            raise e


    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.subtract(projection)
        except Exception as e:
            raise e


    def cross_product(self, v):
        assert self.dimension == v.dimension, "Dimensions must be the same!"

        c1 = self.coordinates[1] * v.coordinates[2] - v.coordinates[1] * self.coordinates[2]
        c2 = (self.coordinates[0] * v.coordinates[2] - v.coordinates[0] * self.coordinates[2]) * Decimal('-1.0')
        c3 = self.coordinates[0] * v.coordinates[1] - v.coordinates[0] * self.coordinates[1]

        return Vector([c1, c2, c3])


    def area_parallelogram(self, v):
        product = self.cross_product(v)
        return product.magnitude


    def area_triangle(self, v):
        product = self.cross_product(v)
        return product.magnitude / Decimal('2.0')



my_vector1 = Vector([-8.987, -9.838, 5.031])
my_vector2 = Vector([-4.268, -1.861, -8.866])
print(my_vector1.area_parallelogram(my_vector2))



