#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/03/06
# @Author  : PandaTofu

from fish_pound.app.application import create_app

if __name__ == '__main__':
    app = create_app('product')
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
