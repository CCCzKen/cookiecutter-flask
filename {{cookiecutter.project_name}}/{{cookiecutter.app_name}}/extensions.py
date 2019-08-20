# -*-coding: utf-8 -*-

import logging

from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
user_cache = FlaskRedis(config_prefix="USER_REDIS")

error_logger = logging.getLogger("gunicorn.error")
