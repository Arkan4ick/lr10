import sys
import math
import timeit
from concurrent.futures import ThreadPoolExecutor


def integrate(f, a, b, n_iter=100000):
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_thread(args):
    f, a, b, n = args
    return integrate(f, a, b, n)


def integrate_threads(f, a, b, n_iter=100000, n_jobs=4):
    part_size = n_iter // n_jobs
    tasks = [(f, a + (b-a)*i/n_jobs, a + (b-a)*(i+1)/n_jobs, part_size) for i in range(n_jobs)]
    
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        results = list(executor.map(integrate_thread, tasks))
    
    return sum(results)


if __name__ == "__main__":
    print(f"Python версия: {sys.version}")
    print(f"noGIL доступен: {sys.flags.nogil if hasattr(sys.flags, 'nogil') else 'Нет'}")
    
    print("\nОдин поток (базовое время):")
    t1 = timeit.timeit(lambda: integrate(math.sin, 0, math.pi, 100000), number=5) / 5
    print(f"  {t1:.6f}s")
    
    print("\nМножество потоков (4 потока):")
    t4 = timeit.timeit(lambda: integrate_threads(math.sin, 0, math.pi, 100000, 4), number=5) / 5
    print(f"  {t4:.6f}s")
    
    print(f"\nИтоги: потоки {'помогли' if t4 < t1 else 'не помогли'} (GIL в Python < 3.13)")
