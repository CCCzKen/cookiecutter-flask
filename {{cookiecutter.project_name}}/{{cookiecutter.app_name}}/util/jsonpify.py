# -*- coding: utf-8 -*-

import simplejson as json
from flask import jsonify, Response


class JsonpResp(object):
    def __init__(self, *args):
        self.callback = args[0] if len(args) >= 1 else None

    def _build(self, jsonify_result):
        reponse = Response(jsonify_result)
        if self.callback:
            reponse = Response(
                "%s(%s)" % (self.callback, jsonify_result),
                mimetype="application/javascript"
            )
        return reponse

    def success(self, data):
        """处理成功状态下的jsonp请求"""
        return self._build(json.dumps({"state": 1, "code": "200", "data": data}))

    def error(self, code, msg):
        """处理错误状态下的jsonp请求"""
        return self._build(json.dumps({"state": 0, "code": code, "msg": msg}))
