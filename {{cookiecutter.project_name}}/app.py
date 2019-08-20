# -*- coding: utf-8 -*-

import os

from {{ cookiecutter.app_name }} import create_app

config_name = os.getenv('{{cookiecutter.app_name}}') or "local"
app = create_app(config_name)
