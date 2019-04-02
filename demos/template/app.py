# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import os
from flask import Flask, render_template, flash, redirect, url_for, Markup

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/watchlist')
def watchlist():
    # 渲染模板 使用Flask提供的渲染函数 render_template()
    # 首先出入模板的文件名作为参数，Flask会在程序根目录下面的templates文件夹寻找模板文件，传入的文件路径是相对于templates根目录
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/')
def index():
    return render_template('index.html')


# register template context handler
# 模板全局变量 Flask提供一个app.context_processor装饰器，可以用来注册模板上下文处理函数
@app.context_processor
def inject_info():
    foo = 'I am foo.'
    # 模板上下文处理函数需要返回一个包含变量键值对的字典
    return dict(foo=foo)  # equal to: return {'foo': foo}
# 当调用render_template()函数渲染任意一个模板时，所有使用app.context_processor装饰器注册的模板上下文处理函数都会被执行
# 这些函数值会被添加到模板中，如上面示例，可以再模板中直接使用foo变量


# register template global function 自定义全局函数
# 将函数直接注册为模板全局函数，app.template_global()仅能用于注册全局函数，不能注册全局变量
@app.template_global()
def bar():
    return 'I am bar.'


# 在Jinja2中，过滤器 filter 是一些可以用来修改和过滤变量值的特殊函数，过滤器和变量值用一个竖线（管道符号）隔开
# register template filter 自定义过滤器
# 可以使用name关键字设置过滤器的名称，默认会使用函数名称
@app.template_filter()
def musical(s):  # 过滤器接收被处理的值作为参数，输出处理后的值
    return s + Markup(' &#9835;')  # 过滤器会在被过滤的变量字符后面添加一个音符图标，音符图标通过HTML实体 &#9835表示


# 测试器Test 是一些用来测试变量或者表达式，返回布尔值的特殊函数
# register template test  自定义测试器
# 使用 app.template_test()装饰器来注册一个测试器
# 测试器的名称默认是函数名称，可是使用name关键字指定自定义名称
# 测试器接收需要被测试的值作为输入参数，返回布尔值
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


@app.route('/watchlist2')
def watchlist_with_static():
    return render_template('watchlist_with_static.html', user=user, movies=movies)


# message flashing 消息闪现
# Flask 提供一个flash()函数,用来“闪现”需要显示给用户的消息
@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    return redirect(url_for('index'))


# 404 error handler
# 错误处理函数，需要添加app.errorhandler()装饰器，传入错误代码作为参数
@app.errorhandler(404)
def page_not_found(e):
    # 错误处理函数本身需要接受异常类作为参数，并在返回值中注明对应的HTTP状态码
    return render_template('errors/404.html'), 404


# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
