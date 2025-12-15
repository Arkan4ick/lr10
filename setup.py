from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    name="integrate_cython",
    ext_modules=cythonize("integrate_cython.pyx", language_level="3"),
    include_dirs=[np.get_include()],
)
