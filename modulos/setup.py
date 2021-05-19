from setuptools import setup
from Cython.Build import cythonize

print("Compilando encoder.pyx\n\n")
setup(ext_modules = cythonize("encoder.pyx"),)

print("\n\nCompilando conversor.pyx\n\n")
setup(ext_modules = cythonize("conversor.pyx"),)
