from setuptools import setup, Extension


module = Extension('immutable_namespace', sources=['namespace.c'])

setup(
    name='NamespaceModule',
    version='1.0',
    description='Immutable Namespace in C',
    ext_modules=[module],
)
