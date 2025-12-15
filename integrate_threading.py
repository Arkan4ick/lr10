import math
from typing import Callable
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import timeit


def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100000) -> float:
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_task(args):
    f, a, b, n = args
    return integrate(f, a, b, n_iter=n)


def integrate_threads(f: Callable, a: float, b: float, n_iter: int = 100000, n_jobs: int = 4) -> float:
    """Интегрирование с потоками"""
    part_size = n_iter // n_jobs
    tasks = [(f, a + (b-a)*i/n_jobs, a + (b-a)*(i+1)/n_jobs, part_size) for i in range(n_jobs)]
    
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        results = list(executor.map(integrate_task, tasks))
    
    return sum(results)


def integrate_processes(f: Callable, a: float, b: float, n_iter: int = 100000, n_jobs: int = 4) -> float:
    """Интегрирование с процессами"""
    part_size = n_iter // n_jobs
    tasks = [(f, a + (b-a)*i/n_jobs, a + (b-a)*(i+1)/n_jobs, part_size) for i in range(n_jobs)]
    
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        results = list(executor.map(integrate_task, tasks))
    
    return sum(results)


if __name__ == "__main__":
    print("ИТЕРАЦИЯ 2: Потоки")
    for n_jobs in [2, 4, 8]:
        t = timeit.timeit(lambda: integrate_threads(math.sin, 0, math.pi, 100000, n_jobs), number=3) / 3
        print(f"  n_jobs={n_jobs}: {t:.6f}s")
    
    print("\nИТЕРАЦИЯ 3: Процессы")
    for n_jobs in [2, 4, 8]:
        t = timeit.timeit(lambda: integrate_processes(math.sin, 0, math.pi, 100000, n_jobs), number=3) / 3
        print(f"  n_jobs={n_jobs}: {t:.6f}s")
    
    print("\nСравнение чистый Python vs Потоки vs Процессы:")
    t_pure = timeit.timeit(lambda: integrate(math.sin, 0, math.pi, n_iter=100000), number=3) / 3
    t_threads = timeit.timeit(lambda: integrate_threads(math.sin, 0, math.pi, 100000, 4), number=3) / 3
    t_process = timeit.timeit(lambda: integrate_processes(math.sin, 0, math.pi, 100000, 4), number=3) / 3
    
    print(f"  Python: {t_pure:.6f}s")
    print(f"  Потоки: {t_threads:.6f}s")
    print(f"  Процессы: {t_process:.6f}s")
