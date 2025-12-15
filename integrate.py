import math
from typing import Callable
import doctest
import unittest
import timeit


def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100000) -> float:
    """
    Численное интегрирование методом прямоугольников.
    
    Args:
        f: функция для интегрирования
        a: левая граница
        b: правая граница
        n_iter: количество итераций
    
    Returns:
        приближённое значение интеграла
    
    Examples:
        >>> integrate(math.sin, 0, math.pi, n_iter=10000)
        2.0...
        
        >>> integrate(lambda x: x**2, 0, 2, n_iter=10000)
        2.6...
    """
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


class TestIntegrate(unittest.TestCase):
    
    def test_sin(self):
        result = integrate(math.sin, 0, math.pi, n_iter=50000)
        self.assertAlmostEqual(result, 2.0, places=2)
    
    def test_cos(self):
        result = integrate(math.cos, 0, math.pi / 2, n_iter=50000)
        self.assertAlmostEqual(result, 1.0, places=2)
    
    def test_quadratic(self):
        result = integrate(lambda x: x**2, 0, 2, n_iter=50000)
        self.assertAlmostEqual(result, 8/3, places=2)
    
    def test_linear(self):
        result = integrate(lambda x: x, 0, 1, n_iter=50000)
        self.assertAlmostEqual(result, 0.5, places=2)
    
    def test_constant(self):
        result = integrate(lambda x: 3, 0, 5, n_iter=50000)
        self.assertAlmostEqual(result, 15, places=1)
    
    def test_stability(self):
        r1 = integrate(lambda x: x, 0, 1, n_iter=1000)
        r2 = integrate(lambda x: x, 0, 1, n_iter=10000)
        r3 = integrate(lambda x: x, 0, 1, n_iter=100000)
        self.assertAlmostEqual(r1, 0.5, places=1)
        self.assertAlmostEqual(r2, 0.5, places=2)
        self.assertAlmostEqual(r3, 0.5, places=3)


if __name__ == "__main__":
    print("DOCTEST:")
    doctest.testmod()
    
    print("\nUNITTEST:")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\nTIMEIT профилирование:")
    for n in [1000, 10000, 100000]:
        t = timeit.timeit(lambda: integrate(math.sin, 0, math.pi, n_iter=n), number=5) / 5
        print(f"n_iter={n}: {t:.6f}s")
