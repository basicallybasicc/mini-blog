#!/usr/bin/env python3

import os
from flask import Flask
from . import db
from flaskr.templates.__blueprints.auth import bp as auth_bp
from flaskr.templates.__blueprints.blog import bp as blog_bp

def create_app (test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'masterdb.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.add_url_rule('/', endpoint = 'index')

    return app