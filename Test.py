# coding=utf-8

from string import Template


str = Template('打印出了${a}')
print(str.substitute(a='''Hello,World'''))


