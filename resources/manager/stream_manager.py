from . import *

class StreamManager(Resource):
    #select one stream id
    def get(self, stream_id):
        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            cursor.execute(query.show_stream_by_id, (stream_id,))
            row_headers = [x[0] for x in cursor.description]
            rs = cursor.fetchall()
            json_data = []
            for result in rs:
                json_data.append(dict(zip(row_headers, result)))
            if json_data == []:
                result = jsonify({
                    'return_code': '2',
                    'return_msg': 'Stream_id không tồn tại',
                    'return_data': ''
                })
            else:
                result = jsonify({
                'return_code': '1',
                'return_msg': 'Success',
                'return_data': json_data
            })
            cursor.close()
            cnx.close()

        except Error as e:
            fr_logs.logger.info("-----showStream")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })
        return result
    #delete
    def delete(self, stream_id):
        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            dt = datetime.now()
            # Kiểm tra stream có tồn tại không
            cursor.execute(query.check_exist_stream,(stream_id,))
            row_headers = [x[0] for x in cursor.description]
            stream = cursor.fetchall()
            if(stream):
                json_data = []
                for result in stream:
                    json_data.append(dict(zip(row_headers, result)))
                if(json_data[0]['STATUS'] == 2):
                    result = jsonify({
                        'return_code': '2',
                        'return_msg': 'Camera đang chạy tính năng AI, không thể xóa.',
                        'return_data': ''
                    })
                else:
                    data_query= {
                        'status': 0,
                        'dateupdate': dt,
                        'stream_id': stream_id
                    }
                    cursor.execute(query.update_status_streammanager, data_query)
                    # Make sure data is committed to the database
                    cnx.commit()
                    result = jsonify({
                        'return_code': '1',
                        'return_msg': 'Xóa Stream thành công.',
                        'return_data': ''
                    })
                cursor.close()
                cnx.close()
            else:
                result = jsonify({
                    'return_code': '2',
                    'return_msg': 'Stream không tồn tại.',
                    'return_data': ''
                })
        except Error as e:
            fr_logs.logger.info("-----deleteStream")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })
        return result
    #update
    def put(self, stream_id):
        data = get_body_data()
        stream_id = stream_id
        unit_id = data.get('unit_id')
        stream_url = data.get('stream_url')
        stream_name = data.get('stream_name')
        if stream_id == "" or unit_id == "" or stream_url == "" or stream_name == "":
            return jsonify({
                'return_code': '2',
                'return_msg': 'Biến truyền vào không hợp lệ.',
                'return_data': ''
            })
        if stream_id is None or unit_id is None or stream_url is None or stream_name is None:
            return jsonify({
                'return_code': '2',
                'return_msg': 'Biến truyền vào không hợp lệ.',
                'return_data': ''
            })

        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            cursor.execute(query.check_exist_stream, (stream_id,))
            row_headers = [x[0] for x in cursor.description]
            result = cursor.fetchall()
            if(result):
                data = dict(zip(row_headers, result[0]))
                
                if data['STATUS'] != 1:
                    return jsonify({
                    'return_code': '0',
                    'return_msg': 'Không thể cập nhật do stream_id đang hoạt động hoặc đã xóa',
                    'return_data': ''
                })
                else:
                    dt = datetime.now()
                    data_update_streammanager = {
                        'stream_name': stream_name,
                        'stream_url': stream_url,
                        'dateupdate': dt,
                        'unit_id': unit_id,
                        'stream_id':stream_id
                    }
                    cursor.execute(query.update_streammanager, data_update_streammanager)
                    # Make sure data is committed to the database
                    cnx.commit()
                    result = jsonify({
                        'return_code': '1',
                        'return_msg': 'Cập nhật Stream thành công.',
                        'return_data': ''
                    })

                cursor.close()
                cnx.close()
            else:
                result = jsonify({
                    'return_code': '2',
                    'return_msg': 'Stream không tồn tại.',
                    'return_data': ''
                })
        except Error as e:
            fr_logs.logger.info("-----updateStream")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })
        return result

class StreamList(Resource):
    #select all stream Id
    def get(self):
        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            cursor.execute(query.show_all_stream)
            row_headers = [x[0] for x in cursor.description]
            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))
            result = jsonify({
                'return_code': '1',
                'return_msg': 'Success',
                'return_data': json_data
            })
            cursor.close()
            cnx.close()
        except Error as e:
            fr_logs.logger.info("-----showStream")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })
        return result

    #create
    def post(self):
        data = get_body_data()
        stream_id = data.get('stream_id')
        unit_id = data.get('unit_id')
        stream_url = data.get('stream_url')
        stream_name = data.get('stream_name')
        if stream_id == "" or unit_id == "" or stream_url == "" or stream_name == "":
            return jsonify({
                'return_code': '2',
                'return_msg': 'Biến truyền vào không hợp lệ.',
                'return_data': ''
            })
        if stream_id is None or unit_id is None or stream_url is None or stream_name is None:
            return jsonify({
                'return_code': '2',
                'return_msg': 'Biến truyền vào không hợp lệ.',
                'return_data': ''
            })
        try:
            # kết nối db
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()

            # Kiểm tra biến stream_id và stream_url có tồn tại không
            cursor.execute(query.check_exist_stream_url, (stream_id, stream_url))
            row_headers = [x[0] for x in cursor.description]
            check = cursor.fetchall()
            dt = datetime.now()
            data_add_streammanager = {
                'stream_id':stream_id,
                'stream_name': stream_name,
                'stream_url': stream_url,
                'datecreated': dt,
                'status': 1,
                'unit_id': unit_id
            }
            if(check):
                json_data = []
                for result in check:
                    json_data.append(dict(zip(row_headers, result)))
                if json_data[0]['STATUS'] != 0:
                    result = jsonify({
                        'return_code': '0',
                        'return_msg': 'Không thể thêm mới do stream_id và stream_url đã tồn tại.',
                        'return_data': json_data
                    })
                else:
                    cursor.execute(query.update_create_streammanager, data_add_streammanager)
                    # Make sure data is committed to the database
                    cnx.commit() 
                    result = jsonify({
                    'return_code': '1',
                    'return_msg': 'Success',
                    'return_data': ''
                })
            else:
                cursor.execute(query.add_streammanager, data_add_streammanager)
                # Make sure data is committed to the database
                cnx.commit()
                result = jsonify({
                    'return_code': '1',
                    'return_msg': 'Success',
                    'return_data': ''
                })
            cursor.close()
            cnx.close()
            
        except Error as e:
            fr_logs.logger.info("-----addStream")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })
        return result 