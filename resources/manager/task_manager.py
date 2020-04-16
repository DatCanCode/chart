
from . import *
import socket
from contextlib import closing
import subprocess as sp
import tempfile

class TaskManager(Resource):
    #get info of task by task_id
    def get(self, task_id):
        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            cursor.execute(query.show_task_by_id, (task_id,))
            row_headers = [x[0] for x in cursor.description]
            rs = cursor.fetchall()
            json_data = []
            for result in rs:
                json_data.append(dict(zip(row_headers, result)))

            result = jsonify({
                'return_code': '1',
                'return_msg': 'Success',
                'return_data': json_data
            })
            cursor.close()
            cnx.close()

        except Error as e:
            fr_logs.logger.info("-----showTaskByID")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })
        return result
    
       #start or stop task by task id
    #update
    def put(self, task_id):
        data = get_body_data()
        task_id = task_id
        task_name = data.get('task_name')
        stream_id = data.get('stream_id')
        unit_id = data.get('unit_id')
        config = data.get('config')

        if task_id is None or task_name is None or stream_id is None or unit_id is None or config is None:
            return jsonify({
                'return_code': '2',
                'return_msg': 'Biến truyền vào không hợp lệ.',
                'return_data': ''
            })

        if task_id == "" or task_name  == "" or stream_id  == "" or unit_id == "" or config  == "":
            return jsonify({
                'return_code': '2',
                'return_msg': 'Biến truyền vào không hợp lệ.',
                'return_data': ''
            })  
        
        try:
            # connect db
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()

            # Kiểm tra biến task_id có tồn tại không
            cursor.execute(query.check_exist_task, (task_id,))
            row_headers = [x[0] for x in cursor.description]
            check = cursor.fetchall()
            if(check):
                json_data = []
                for result in check:
                    json_data.append(dict(zip(row_headers, result)))

                if json_data[0]['STATUS'] != 1:
                    result = jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể cập nhật do task_id đang hoạt động hoặc đã xóa',
                        'return_data': json_data
                    })
                else:
                    dt = datetime.now()
                    setting_json = data['config']
                    setting_str = json.dumps(setting_json)
                    data_update = {
                        'task_id': task_id,
                        'task_name': task_name,
                        'stream_id': stream_id,
                        'dateupdate': dt,
                        'status': 1,
                        'setting': setting_str,
                        'unit_id': unit_id
                    }
                    cursor.execute(query.update_taskmanager, data_update)

                    # Make sure data is committed to the database
                    cnx.commit()
                    result = jsonify({
                        'return_code': '1',
                        'return_msg': 'Success',
                        'return_data': ''
                    })

                cursor.close()
                cnx.close()
            else:
                result = jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể cập nhật do task_id không tồn tại trong hệ thống',
                        'return_data': ''
                    })

        except Error as e:
            fr_logs.logger.info("-----UpdateTask")
            fr_logs.logger.error(e)
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })

        return result
    #delete task by task_id
    def delete(self, task_id):
        try:
            # connect db
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()

            # Kiểm tra biến task_id có tồn tại không
            cursor.execute(query.check_exist_task, (task_id,))
            row_headers = [x[0] for x in cursor.description]
            check = cursor.fetchall()

            if(check):
                json_data = []
                for result in check:
                    json_data.append(dict(zip(row_headers, result)))
                if json_data[0]['STATUS'] != 1:
                    result = jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể xóa do task_id đã xóa hoặc đang hoạt động.',
                        'return_data': json_data
                    })
                else:
                    dt = datetime.now()
                    data_update = {
                    'status': 0,
                    'dateupdate': dt,
                    'task_id': task_id
                }
                    cursor.execute(query.update_status_taskmanager, data_update)
                    # Make sure data is committed to the database
                    cnx.commit() 
                    result = jsonify({
                    'return_code': '1',
                    'return_msg': 'Success',
                    'return_data': ''
                })
            else:
                return jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể xóa do task_id không tồn tại trên hệ thống.',
                        'return_data': ''
                        })

            cursor.close()
            cnx.close()

        except Error as e:
            fr_logs.logger.info("-----DeleteTask")
            fr_logs.logger.error(e)
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })

        return result

class TaskManagerList(Resource):
    #get all task info
    def get(self):
        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            cursor.execute(query.show_all_task)
            row_headers = [x[0] for x in cursor.description]
            rs = cursor.fetchall()
            json_data = []
            for result in rs:
                json_data.append(dict(zip(row_headers, result)))

            result = jsonify({
                'return_code': '1',
                'return_msg': 'Success',
                'return_data': json_data
            })
            cursor.close()
            cnx.close()

        except Error as e:
            fr_logs.logger.info("-----showAllTask")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })
        return result

    #create task
    def post(self):
        data = get_body_data()
        task_id = find_free_port()
        task_name = data.get('task_name')
        stream_id = data.get('stream_id')
        unit_id = data.get('unit_id')
        config = data.get('config')

        if task_id is None or task_name is None or stream_id is None or unit_id is None or config is None:
            return jsonify({
                'return_code': '2',
                'return_msg': 'Biến truyền vào không hợp lệ.',
                'return_data': ''
            })
        if task_id == "" or task_name  == "" or stream_id  == "" or unit_id == "" or config  == "":
            return jsonify({
                'return_code': '2',
                'return_msg': 'Biến truyền vào không hợp lệ.',
                'return_data': ''
            })  
            
        try:
            # connect db
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()

            # Kiểm tra biến task_id có tồn tại không
            cursor.execute(query.check_exist_task, (task_id,))
            row_headers = [x[0] for x in cursor.description]
            check = cursor.fetchall()

            dt = datetime.now()
            setting_json = data['config']
            setting_str = json.dumps(setting_json)
            data_bd = {
                'task_id': task_id,
                'task_name': task_name,
                'stream_id': stream_id,
                'status': 1,
                'setting': setting_str,
                'unit_id': unit_id
            }

            if(check):
                json_data = []
                for result in check:
                    json_data.append(dict(zip(row_headers, result)))
                if json_data[0]['STATUS'] != 0:
                    result = jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể thêm mới do task_id đã tồn tại.',
                        'return_data': json_data
                    })
                else:
                    data_update = data_bd
                    data_update['dateupdate'] = dt
                    cursor.execute(query.update_taskmanager, data_update)
                    # Make sure data is committed to the database
                    cnx.commit()
                    result = jsonify({
                        'return_code': '1',
                        'return_msg': 'Success',
                        'return_data': ''
                    })
            else:
    
                data_add = data_bd
                data_add['datecreated'] = dt
                cursor.execute(query.create_taskmanager, data_add)
                # Make sure data is committed to the database
                cnx.commit()
                result = jsonify({
                    'return_code': '1',
                    'return_msg': 'Success',
                    'return_data': {"task_id":task_id}
                })

            cursor.close()
            cnx.close()

        except Error as e:
            fr_logs.logger.info("-----CreateTask")
            fr_logs.logger.error(e)
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })
        return result

#start stop

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

currentTask = {}

class Task():
    def __init__(self, task_id, task_name, stream_id, stream_url):
        self.task_id = task_id
        self.task_name = task_name
        self.stream_id = stream_id
        self.stream_url = stream_url

    def run(self):

        if self.task_name== 'recognition':
            print('start')
            self.tmf = tempfile.TemporaryFile()
            self.p = sp.Popen(["python","resources/face_activity/main_activity.py","-t", self.task_id,"-s", self.stream_id ,"-url", self.stream_url],stdout = self.tmf)
            #self.p = sp.Popen(["python","resources/face_activity/cam_stream.py","-i", "haha", "-u",self.stream_url ],stdout = self.tmf)
            #self.p = sp.Popen(["python","resources/face_activity/show_cam.py","-u", self.stream_url],stdout = self.tmf)

    def kill(self):
       self.p.kill()
       self.tmf.close()

def startTask(task_id, task_name, stream_id, stream_url):
    task = Task(task_id, task_name, stream_id, stream_url)
    task.run()
    currentTask[task_id] = task
    print('Running Task: ')
    print(currentTask)

def stopTask(task_id):
    currentTask[task_id].kill()
    del currentTask[task_id]
    print(currentTask)

class StartTask(Resource):
    def put(self, task_id):
        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            # Kiểm tra biến task_id có tồn tại không
            cursor.execute(query.check_exist_task, (task_id,))
            row_headers = [x[0] for x in cursor.description]
            check = cursor.fetchall()
            if(check):
                json_data = []
                for result in check:
                    json_data.append(dict(zip(row_headers, result)))

                if json_data[0]['STATUS'] != 1:
                    return jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể khởi động do task_id đang hoạt động hoặc đã xóa',
                        'return_data': json_data
                    })
                else:
                    stream_id = json_data[0]['STREAM_ID']
                    task_name =  json_data[0]['TASK_NAME']

                    cursor.execute(query.check_exist_stream, (stream_id,))
                    row_headers = [x[0] for x in cursor.description]
                    result =  cursor.fetchall()
                    data_stream = []
                    if result:
                        data_stream = dict(zip(row_headers,result[0]))
                        if data_stream['STATUS'] == 0:
                             return  jsonify({
                            'return_code': '0',
                            'return_msg': 'Không thể khởi động do stream_id không tồn tại hoặc đã xóa',
                            'return_data': data_stream
                        })
                        else:
                            stream_url = data_stream['STREAM_URL']
                    else:
                        return  jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể khởi động do stream_id không tồn tại hoặc đã xóa',
                        'return_data': data_stream
                    })
                    #runTask(thread_id, thread_url)
                    startTask(task_id, task_name, stream_id, stream_url)
                    dt = datetime.now()
                    data_query = {
                        'status': 2,
                        'dateupdate': dt,
                        'task_id': task_id
                    }
                    cursor.execute(query.update_status_taskmanager, data_query)

                    # Make sure data is committed to the database
                    cnx.commit()

                    cursor.close()
                    cnx.close()

                    return jsonify({
                        'return_code': '1',
                        'return_msg': 'Success',
                        'return_data': ''
                    })
            else:
                return jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể khởi động do task_id không tồn tại trên hệ thống.',
                        'return_data': ''
                        })
        except Error as e:
            print("Error: {}".format(e))
            fr_logs.logger.info("-----StartTask")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            return jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })

class StopTask(Resource):
    def put(self, task_id):
        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            # Kiểm tra biến task_id có tồn tại không
            cursor.execute(query.check_exist_task, (task_id,))
            row_headers = [x[0] for x in cursor.description]
            check = cursor.fetchall()
            if(check):
                json_data = []
                for result in check:
                    json_data.append(dict(zip(row_headers, result)))

                if json_data[0]['STATUS'] != 2:
                    return jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể dừng do task_id đang không hoạt động hoặc đã xóa',
                        'return_data': json_data
                    })
                else:
                    thread_id = json_data[0]['ID']
                    #Stop Task function
                    stopTask(thread_id)

                    dt = datetime.now()
                    data_query = {
                        'status': 1,
                        'dateupdate': dt,
                        'task_id': task_id
                    }
                    cursor.execute(query.update_status_taskmanager, data_query)

                    # Make sure data is committed to the database
                    cnx.commit()

                    cursor.close()
                    cnx.close()

                    return jsonify({
                        'return_code': '1',
                        'return_msg': 'Success',
                        'return_data': ''
                    })
            else:
                return jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể khởi dừng task_id không tồn tại trên hệ thống.',
                        'return_data': ''
                        })
        except Error as e:
            print("Error: {}".format(e))
            fr_logs.logger.info("-----StopTask")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            return jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })