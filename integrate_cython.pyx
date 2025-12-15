# integrate_cython.pyx

from libc.math cimport sin, cos

def integrate_cython(f, double a, double b, int n_iter=100000):
    """Интегрирование на Cython"""
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_sin_fast(double a, double b, int n_iter=100000):
    """Быстрое интегрирование sin без GIL"""
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    
    for i in range(n_iter):
        acc += sin(a + i * step) * step
    return acc


def integrate_cos_fast(double a, double b, int n_iter=100000):
    """Быстрое интегрирование cos без GIL"""
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    
    for i in range(n_iter):
        acc += cos(a + i * step) * step
    return acc
