# -*- coding: utf-8 -*-

from {{ cookiecutter.app_name }}.views.index import index_router


routers = (
    (index_router, ''),
)
