from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

from __version__ import Info
from resources.manager.stream_manager import StreamManager, StreamList
from resources.manager.unit_manager import UnitManager, UnitList
from resources.manager.task_manager import TaskManager, TaskManagerList, StartTask, StopTask

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api.add_resource(Info, '/', '/api/', '/api/info', '/api/version')

api.add_resource(StreamManager,'/api/stream/<stream_id>')
api.add_resource(StreamList,'/api/stream')

api.add_resource(TaskManager, '/api/task/<task_id>')
api.add_resource(TaskManagerList,'/api/task')

api.add_resource(StartTask, '/api/task/<task_id>/start')
api.add_resource(StopTask, '/api/task/<task_id>/stop')

api.add_resource(UnitManager,'/api/unit/<unit_id>')
api.add_resource(UnitList,'/api/unit')

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host="0.0.0.0", port="5000")
    # http_server = WSGIServer(('0.0.0.0', 5002), app)
    # http_server.serve_forever()