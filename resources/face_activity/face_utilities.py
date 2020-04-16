import mysql.connector
from tool import db
from tool import fare

def load_data_people():
	known_name = []
	known_encodings = []
	known_id = {}
	known_name_to_cburl = {}

	known_id['Unknown'] = 'Unknown'
	try:
		cnx = mysql.connector.connect(**db.face_recognition_local)
		cursor = cnx.cursor()
		cursor.execute(("SELECT * from data_people"))
		row_headers = [x[0] for x in cursor.description]
		rv = cursor.fetchall()
		json_data = []
		for result in rv:
			json_data.append(dict(zip(row_headers, result)))

		for data in json_data:
			known_name.append(data['DP_ID'])
			known_id[data['DP_ID']] = data['DP_NAME']
			known_name_to_cburl[data['DP_ID']] = str(data['DP_CB_URL'])
			b_new = json.loads(data['DP_IMAGE_ENCODING'])
			a_new = np.array(b_new)
			known_encodings.append(a_new)

		print("Load data nhan dien thanh cong!")
		# fr_logs.logger.info("--- Khoi Dong: load du lieu tren database")
		cursor.close()
		cnx.close()
		print (known_name, known_id)
		return known_name, known_encodings, known_id, known_name_to_cburl

	except:
		# fr_logs.logger.error(sys.exc_info()[0])
		print("loi query")
		return known_name, known_encodings, known_id, known_name_to_cburl

def load_setting_task(task_id):
	cnx = mysql.connector.connect(**db.face_recognition_local)
	cursor = cnx.cursor()
	cursor.execute(fare.get_setting_camera, (task_id,))
	row_headers = [x[0] for x in cursor.description]
	results = cursor.fetchall()
	json_data = []
	for result in results:
		json_data.append(dict(zip(row_headers, result)))
	cursor.close()
	cnx.close()
	return json_data