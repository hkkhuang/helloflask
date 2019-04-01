# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import os

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from jinja2 import escape
from jinja2.utils import generate_lorem_ipsum
from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


# get name value from query string and cookie
@app.route('/')
@app.route('/hello', methods=['GET', 'POST'])  # 设置允许的请求方法
def hello():
    name = request.args.get('name')
    # 使用get() 方法获取数据原因
    # 从request对象的类型为MultiDict或者ImmutableMultiDict的属性（如form,files等）直接使用键作为索引获取对象
    # 如request.args['names'],如果没有对应的键，那么会返回HTTP 400错误（Bad Request，请求无效），而不是抛出KeyError异常
    # 使用get()方法获取数据，如果没有对应的值返回None
    # get()方法的第二个参数可以设置为默认值，如 request.args.get('name','Human')

    # 注：如果开启了调试模式，会抛出BadRequestKeyError异常，并显示对应的错误堆栈信息，不是常规的400响应

    if name is None:
        # 从Cookie中获取name值
        name = request.cookies.get('name', 'Human')
    response = '<h1>Hello, %s!</h1>' % escape(name)  # escape name to avoid XSS
    # return different response according to the user's authentication status
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


# redirect 重定向
# redirect() 函数生成重定向响应，重定向的目标URL作为第一个参数，默认的状态码是203，即临时重定向
# 若要修改状态码，在redirect()函数中作为第二个参数，或者使用code关键字传入
@app.route('/hi')
def hi():
    # 在程序内部重定向到其他的视图，只需要在redirect()函数中使用 url_for()函数生成目标URL即可
    return redirect(url_for('hello'))


# use int URL converter 转换器
# 不仅仅是转换变量类型，同时包括URL匹配
@app.route('/goback/<int:year>')
def go_back(year):
    return 'Welcome to %d!' % (2018 - year)


# use any URL converter 转换器
# <any(value1,value2,...)> 匹配一系列给定值中的一个元素
@app.route('/colors/<any(blue, white, red):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


# return error response 错误重定向
# 访问出错会得到一个状态码为418的错误响应
@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418)
    else:
        return 'A drop of tea.'


# 404
@app.route('/404')
def not_found():
    # 在abort()函数中传入状态码，就可以返回对应的错误信息
    # abort()函数前面不需要 return ,一旦abort()函数被调用，之后的代码将不会被执行
    abort(404)  # abort前面没有return


# return response with different formats 返回不同格式的响应
@app.route('/note', defaults={'content_type': 'text'})
@app.route('/note/<content_type>')
def note(content_type):
    content_type = content_type.lower()
    if content_type == 'text':
        body = '''Note-text
                to: Peter
                from: Jane
                heading: Reminder
                body: Don't forget the party!
                '''
        response = make_response(body)
        response.mimetype = 'text/plain'
    elif content_type == 'html':
        body = '''<!DOCTYPE html>
                <html>
                <head></head>
                <body>
                  <h1>Note-html</h1>
                  <p>to: Peter</p>
                  <p>from: Jane</p>
                  <p>heading: Reminder</p>
                  <p>body: <strong>Don't forget the party!</strong></p>
                </body>
                </html>
                '''
        response = make_response(body)
        response.mimetype = 'text/html'
    elif content_type == 'xml':
        body = '''<?xml version="1.0" encoding="UTF-8"?>
                <note>
                  <to>Peter</to>
                  <from>Jane</from>
                  <heading>Reminder</heading>
                  <body>Don't forget the party!</body>
                </note>
                '''
        response = make_response(body)
        response.mimetype = 'application/xml'
    elif content_type == 'json':
        body = {"note": {
            "to": "Peter",
            "from": "Jane",
            "heading": "Remider",
            "body": "Don't forget the party!"
        }
        }
        response = jsonify(body)
        # equal to:
        # response = make_response(json.dumps(body))
        # response.mimetype = "application/json"
    else:
        abort(400)
    return response


# set cookie 设置cookie
# 在响应中添加一个cookie,最方便的方法是在Response类提供的set_cookie()方法
@app.route('/set/<name>')
def set_cookie(name):
    # 首先是使用 make_response()方法手动生成一个响应对象，传入响应主题作为参数
    # 这个响应对象默认实例化内置的Response类
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)  # 该方法的参数 P47
    return response


# log in user
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


# protect view
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'


# log out user 用户登出 session.pop()
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


# AJAX
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)


# redirect to last page
@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/do-something')
def do_something():
    # do something here
    return redirect_back()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
