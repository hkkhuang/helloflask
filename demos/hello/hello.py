#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : hello.py.py
# @Author: huangkeke
# @Date  : 2019/3/7
# @Contact : hkkhuang@163.com

from app import app

if __name__ == '__main__':
    app.run(debug=True, port=5000)
# 这种方式是 旧的启动开发服务器的方式，目前已经不推荐使用
