import math
import timeit
from integrate_cython_v2 import integrate_sin_fast, integrate_cos_fast


def integrate_python(f, a, b, n_iter=100000):
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


if __name__ == "__main__":
    print("ИТЕРАЦИЯ 4: Cython")
    
    t_python = timeit.timeit(lambda: integrate_python(math.sin, 0, math.pi, 100000), number=5) / 5
    t_cython = timeit.timeit(lambda: integrate_sin_fast(0, math.pi, 100000), number=5) / 5
    
    print(f"Python: {t_python:.6f}s")
    print(f"Cython: {t_cython:.6f}s")
    print(f"Ускорение: {t_python/t_cython:.1f}x")
