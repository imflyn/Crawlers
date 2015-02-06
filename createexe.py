# coding=utf-8
from distutils.core import setup
import py2exe

str = input("please input filename:")
setup(console=[str])