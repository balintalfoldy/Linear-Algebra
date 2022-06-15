
import math
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(Decimal(x) for x in coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates
    

    def __add__(self, v):
        assert self.dimension == v.dimension, "Dimensions must be the same!"

        sum = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        
        return Vector(sum)


    def __sub__(self, v):
        assert self.dimension == v.dimension, "Dimensions must be the same!"

        sub = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        
        return Vector(sub)

    def __mul__(self, scalar):

        mul = [num * Decimal(scalar) for num in self.coordinates]
        
        return Vector(mul)

    def magnitude(self):
        return math.sqrt(sum(list(map(lambda n: n*n, self.coordinates))))

    def normalize(self):
        try:
            return self * (1. / self.magnitude())

        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def dot_product(self, v):
        assert self.dimension == v.dimension, "Dimensions must be the same!"
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def angle(self, v, degree=False):
        assert self.dimension == v.dimension, "Dimensions must be the same!"
        try:
            u1 = self.normalize()
            u2 = v.normalize()
            angle = math.acos(round(u1.dot_product(u2), 5))

            if degree:
                return math.degrees(angle)
            else:
                return angle
        except ZeroDivisionError:
            raise ZeroDivisionError('Cannot compute the angle with zero vector')
        except Exception as e:
            raise e

    def if_parallel(self, v):
        return (self.is_zero() or v.is_zero() or self.angle(v, degree=True) in [0, 180, 360])
    
    def if_orthogonal(self, v, tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_parallel_to(self, basis):
        try:
            u = basis.normalize()
            return u * self.dot_product(u)
        except Exception as e:
            raise e
    
    def cross_product(self, v):
        assert self.dimension == v.dimension, "Dimensions must be the same!"

        c1 = self.coordinates[1] * v.coordinates[2] - v.coordinates[1] * self.coordinates[2]
        c2 = (self.coordinates[0] * v.coordinates[2] - v.coordinates[0] * self.coordinates[2]) * -1.
        c3 = self.coordinates[0] * v.coordinates[1] - v.coordinates[0] * self.coordinates[1]

        return Vector([c1, c2, c3])

    def area_parallelogram(self, v):
        product = self.cross_product(v)
        return product.magnitude()

    def area_triangle(self, v):
        product = self.cross_product(v)
        return product.magnitude() * 1./2


v1 = Vector([1,2,5])
v2 = Vector([1,2,5])
