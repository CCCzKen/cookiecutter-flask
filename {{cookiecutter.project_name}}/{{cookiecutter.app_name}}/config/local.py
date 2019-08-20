# -*- coding: utf-8 -*-


class LocalConfig(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_BINDS = {
        "master": "postgresql://postgres:@127.0.0.1:5432/postgres",
    }

    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_BINDS["master"]
    USER_REDIS_URL = "redis://@127.0.0.1:6379/0"
