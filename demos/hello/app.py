# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import click
from flask import Flask

# 实例化 Flask类
app = Flask(__name__)


# the minimal Flask application
# 装饰器   传入URL规则作为参数
# 注册路由 路由负责管理URL和函数之前的映射  这个函数称为视图函数
# app.route()装饰器把根地址/和index()函数绑定起来 当用户访问这个URL时就会触发index()函数
# 这个视图函数可以像其他的普通函数一样执行任意操作，  最后视图函数的返回值将作为相应的主体
# 一般来说响应的主体就是呈现在浏览器窗口的HTML页面
@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'


# route()装饰器的第一个参数是URL规则，用字符串表示，必须是以斜杠/开始
# 这里的URL是相对URL（又称为内部URL），即不包含域名的URL

# bind multiple URL for one view function
# 为一个视图函数绑定多个URL
# 将/hi 和 /hello 都绑定到say_hello()函数上，当用户访问这两个URL时都会触发say_hello()函数，获得相同的响应
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'


# dynamic route, URL variable default
# 动态URL,不仅仅可以绑定多个URL,还可以在URL规则中添加变量部分  使用 <变量名>  形式表示
# Flask处理请求时会把变量传入视图函数，可以添加参数获取这个变量值
# 注：因为URL中可以包含变量，所以将传入app.route()的字符串称为URL规则，而不是URL
# Flask会解析请求并把请求的URL与视图函数的Url规则进行匹配
# 如greet视图中的URL规则是 /greet/<name>  类似/greet/foo  /greet/bar请求都会触发这个视图函数

# 当URL规则中包含变量时，如果用户请求的URL中没有添加变量，如 /greet ,Flask在匹配失败后会返回一个404错误响应
# 一个常见的解决方法是在app.route()装饰器中使用 参数default 设置URL变量的默认值，这个参数接收 字典 作为输入，存储URL变量和默认值的映射
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


# custom flask cli command
@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')
