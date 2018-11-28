# -*- encoding: utf8 -*-
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from flask import Blueprint, Response, flash, redirect, \
    render_template

blueprint = Blueprint('main', __name__, template_folder='templates')
route = blueprint.route


@route('/index')
@route('/')
def index():
    # type: () -> Response
    return render_template('index.html')
