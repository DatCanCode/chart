
# Copyright 2020 AI R&D Team Authors, Pavel Yakubovskiy. All Rights Reserved.
from flask_restful import Resource
from flask import json, jsonify
VERSION = (1, 5, 0)

__version__ = ".".join(map(str, VERSION))
class Info(Resource):
    def get(self):
        return jsonify({'1.Info': 'VNPT.IT2 R&D - Python Web AI-engine',
                            '2.Version': __version__,
                            '3.Features':'Face Recognition, Traffic Surveillance'
                            })
    def post(self):
        return self.get()
    def put(self):
        return self.get()
    def delete(self):
        return self.get()