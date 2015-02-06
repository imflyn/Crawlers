# coding=utf-8
from distutils.core import setup
import py2exe

str = raw_input("please input filename:")
setup(console=[str])