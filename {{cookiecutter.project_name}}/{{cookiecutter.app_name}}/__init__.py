# -*- coding: utf-8 -*-

import importlib

from flask import Flask, request

from {{ cookiecutter.app_name }}.extensions import db, user_cache, error_logger
from {{ cookiecutter.app_name }}.urls import routers
from {{ cookiecutter.app_name }}.util.jsonpify import JsonpResp


def load_config_class(config_name):
    """导入config配置"""
    config_class_name = "%sConfig" % config_name.capitalize()
    app_name = __name__
    mod = importlib.import_module('%s.config.%s' % (app_name, config_name))
    config_class = getattr(mod, config_class_name, None)
    return config_class


def create_app(config_name):
    """创建app"""
    app = Flask(__name__)
    config_class = load_config_class(config_name)
    app.config.from_object(config_class)
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_blueprint(app)
    if app.debug:
        configure_process(app)

    return app


def configure_process(app):
    @app.before_request
    def before_request_process():
        app.logger.error(request.headers)
        app.logger.error("request.data: %s" % request.data)


def configure_blueprint(app):
    for blueprint, url_prefix in routers:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def configure_extensions(app):
    db.init_app(app)
    user_cache.init_app(app)


def configure_errorhandlers(app):
    @app.errorhandler(401)
    def unauthorized(error):
        callback = request.args.get("callback")
        return JsonpResp(callback).error("401", msg=str(error))

    @app.errorhandler(403)
    def forbidden(error):
        callback = request.args.get("callback")
        first_error_message = error.exc.messages.items()[0][1]
        first_error_message = first_error_message[0] \
            if isinstance(first_error_message, list) \
            else first_error_message
        return JsonpResp(callback).error("403", msg=first_error_message)

    @app.errorhandler(404)
    def page_not_found(error):
        callback = request.args.get("callback")
        return JsonpResp(callback).error("404", msg=str(error))

    @app.errorhandler(422)
    def error_request_argument(error):
        callback = request.args.get("callback")
        first_error_message = error.exc.messages.items()[0][1]
        first_error_message = first_error_message[0] \
            if isinstance(first_error_message, list) \
            else first_error_message
        return JsonpResp(callback).error("422", msg=first_error_message)

    @app.errorhandler(500)
    def server_error(error):
        error_logger.error(error)
        callback = request.args.get("callback")
        return JsonpResp(callback).error("500", msg=str(error))
