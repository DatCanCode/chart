from . import *

#có bug k lấy theo dv_id được haha
class UnitManager(Resource):
    #select
    def get(self, unit_id):
        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            cursor.execute(query.show_unit_by_id, (unit_id,))
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
            fr_logs.logger.info("-----loadDonVi")
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
    def delete(self, unit_id):
        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            cursor.execute(query.check_exist_unit, (unit_id,))
            row_headers = [x[0] for x in cursor.description]
            rs = cursor.fetchall()
            if(rs):
                data = dict(zip(row_headers, rs[0]))
                if data['STATUS'] == 0:
                    return jsonify({
                        'return_code': '0',
                        'return_msg': 'Không xóa được vì đơn vị đã xóa',
                        'return_data': ''
                    })
                else:
                    data = {
                        
                    }
                    cursor.execute(query.update_status_unit)
                    cnx.commit()
                    cursor.close()
                    cnx.close()
                    return jsonify({
                        'return_code': '1',
                        'return_msg': 'Xoá đơn vị thành công',
                        'return_data': ''
                    })
            else:
                result = jsonify({
                    'return_code': '2',
                    'return_msg': 'Đơn vị không tồn tại.',
                    'return_data': ''
                })
        except Error as e:
            fr_logs.logger.info("-----deleteUnit")
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
    def put(self, unit_id):
        data = get_body_data()
        unit_name = data.get('unit_name')
        if unit_name == "" or unit_name is None:
            return jsonify({
                'return_code': '2',
                'return_msg': 'Biến truyền vào không hợp lệ.',
                'return_data': ''
            })
        try:
            dt = datetime.now()
            data_query = {
                'unit_id': unit_id,
                'unit_name': unit_name,
                'dateupdate': dt,
            }
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            cursor.execute(query.check_exist_unit,(unit_id,))
            row_headers = [x[0] for x in cursor.description]
            result = cursor.fetchall()
            if result:
                data_cr = dict(zip(row_headers,result[0]))
                if data_cr['STATUS'] == 0:
                    result = jsonify({
                    'return_code': '0',
                    'return_msg': 'Unit_id đã xóa',
                    'return_data': ''
                })
                else:
                    cursor.execute(query.update_unit, data_query)
                    result = jsonify({
                        'return_code': '1',
                        'return_msg': 'Success',
                        'return_data': ''
                    })
            else:
                result = jsonify({
                    'return_code': '0',
                    'return_msg': 'Unit_id không tồn tại',
                    'return_data': ''
                })
            # Make sure data is committed to the database
            cnx.commit()
            cursor.close()
            cnx.close()
        except Error as e:
            fr_logs.logger.info("-----UpdateUnit")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })
        return result

class UnitList(Resource):
    #select
    def get(self):
        try:
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor= cnx.cursor()
            cursor.execute(query.show_all_unit)
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
            fr_logs.logger.info("-----ShowAllUnit")
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
        unit_id = data.get('unit_id')
        unit_name = data.get('unit_name')
        if unit_id == "" or unit_name == "" or unit_id is None or unit_name is None:
            return jsonify({
                'return_code': '2',
                'return_msg': 'Biến truyền vào không hợp lệ.',
                'return_data': ''
            })
        try:
            dt = datetime.now()
            data_query = {
                'unit_id': unit_id,
                'unit_name': unit_name,
                'datecreated': dt,
                'status': 1
            }
            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            cursor.execute(query.check_exist_unit,(unit_id,))
            row_headers = [x[0] for x in cursor.description]
            result = cursor.fetchall()
            if result:
                data_cr = dict(zip(row_headers,result[0]))
                if data_cr['STATUS'] == 0:
                    cursor.execute(query.update_add_unit, data_query)
                else:
                    return jsonify({
                    'return_code': '0',
                    'return_msg': 'Unit_id đã tồn tại',
                    'return_data': ''
                })
            cursor.execute(query.add_unit, data_query)
            # Make sure data is committed to the database
            cnx.commit()
            cursor.close()
            cnx.close()
            result = jsonify({
                'return_code': '1',
                'return_msg': 'Success',
                'return_data': ''
            })
            cursor.close()
            cnx.close()
        except Error as e:
            fr_logs.logger.info("-----CreateUnit")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Vui lòng liên hệ quản trị viên.',
                'return_data': ''
            })
        return result