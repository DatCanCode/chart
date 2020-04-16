# query sql face recognition
import datetime
import threading


add_thread_manager = ("INSERT INTO thread_manager (THREAD_ID,STREAM_ID,STATUS) VALUES (%(thread_id)s,%(stream_id)s,%(status)s)")

update_thread_manager = ("UPDATE thread_manager SET STATUS = %(status)s")

add_streammanager = ("INSERT INTO streammanager "
                    "(STREAM_ID, STREAM_NAME, STREAM_URL, DATECREATED,STATUS,SETTING,DV_ID) "
                    "VALUES (%(stream_id)s, %(stream_name)s, %(stream_url)s, %(datecreated)s,"
                     " %(status)s, %(setting)s, %(donvi_id)s)")

data_add_streammanager = {
                            'stream_id': '',
                            'stream_name': '',
                            'stream_url': '',
                            'datecreated': '',
                            'status': '',
                            'setting': ''
                            }

update_streammanager = ("UPDATE streammanager"
                        " SET STREAM_NAME = %(stream_name)s, STREAM_URL = %(stream_url)s, DATEUPDATE = %(dateupdate)s,"
                        " SETTING = %(setting)s, DV_ID = %(donvi_id)s"
                        " WHERE STREAM_ID = %(stream_id)s")

update_donvi = "UPDATE dm_donvi SET DV_MA = %(ma_donvi)s, DV_TEN = %(ten_donvi)s WHERE DV_ID = %(id_donvi)s"

data_update_streammanager = {
                            'stream_id': '',
                            'stream_name': '',
                            'stream_url': '',
                            'dateupdate': '',
                            'setting': '',
                            'id': ''
                            }

deleta_streammanager = ("UPDATE streammanager "
                    "SET STATUS = %(status)s, DATEUPDATE = %(dateupdate)s "
                    "WHERE STREAM_ID = %(stream_id)s")

delete_donvi = ("UPDATE dm_donvi SET DV_TRANGTHAI = %(trangthai)s WHERE DV_ID = %(donvi_id)s")

data_delete_streammanager = {
                            'status': '',
                            'dateupdate': '',
                            'stream_id': ''
                            }

query_streammanager_showstream = ("SELECT * FROM streammanager WHERE STREAM_ID = %(stream_id)s AND STATUS NOT IN (0)")

query_streammanager_showallstream = ("SELECT * FROM streammanager WHERE STATUS NOT IN (0)")

query_donvi = ("SELECT * FROM dm_donvi WHERE DV_TRANGTHAI NOT IN (2)")

query_donvi_by_id = ("SELECT * FROM dm_donvi WHERE DV_ID= %(dv_id)s AND DV_TRANGTHAI NOT IN (0)")

add_donvi = ("INSERT INTO dm_donvi (DV_MA, DV_TEN, DV_NGAYTAO, DV_TRANGTHAI)"
             " VALUES (%(ma)s,  %(ten)s, %(ngay_tao)s, %(trang_thai)s)")

add_camera_people = ("INSERT INTO camera_people "
                     "(CAMERA, STREAM_ID, FACES, IMAGE, FACE_RECTANGLE, AMOUNT_OF_PEOPLE, NUMBER_OF_IDENTIFYERS, GENDER, AGE, CREATEAT, CREATEAT_TICKS) "
                    "VALUES (%(camera)s,  %(stream_id)s, %(ten)s, %(hinhanh)s, %(toado)s, %(songuoi)s, %(songuoibiet)s, %(gioitinh)s, %(tuoi)s, %(thoigian)s, %(thoigianticks)s)")

# query_nhandang = ("SELECT * FROM camera_people WHERE CAMERA = %(id)s ORDER BY CREATEAT DESC LIMIT %(batdau)s, %(soluong)s")
query_nhandang = "SELECT * FROM camera_people WHERE CAMERA = %(id)s LIMIT %(batdau)s, %(soluong)s"

query_nhandangv2 = "CALL API_showNhanDang(%(id)s, %(batdau)s, %(soluong)s)"

data_query_nhandang = {
                        'id': '',
                        'batdau': '',
                        'soluong': ''
                        }

# Hien edit 2019-12-03
# query_nhandang_bytime = ("SELECT * FROM camera_people WHERE CAMERA = %(id)s AND CREATEAT_TICKS >= %(from_time_ticks)s AND CREATEAT_TICKS <= %(to_time_ticks)s ORDER BY CREATEAT_TICKS DESC ")
query_nhandang_bytime = ("SELECT ID,CAMERA,AREA,FACES,AMOUNT_OF_PEOPLE,NUMBER_OF_IDENTIFYERS,GENDER,AGE,COUNTRY,MASK,"
                         "WEAPONS,VALIDITY,VIOLATE,VIDEO,VIDEOSTARTTIME,VIDEOENDTIME,VIDEOTIME,CREATEAT,CREATEAT_TICKS,"
                         "CREATEUSER,UPDATEAT,DELETED "
                         "FROM camera_people "
                         "WHERE CAMERA = %(id)s AND CREATEAT_TICKS >= %(from_time_ticks)s "
                         "AND CREATEAT_TICKS <= %(to_time_ticks)s ORDER BY CREATEAT_TICKS DESC ")
query_trackingIdentifiedByTime = ("CALL API_trackingIdentifiedByTime(%(identified_id)s, %(from_time_ticks)s, %(to_time_ticks)s)")
# end Hien edit 2019-12-03
add_data_people = ("INSERT INTO data_people (DP_NAME, DP_IMAGE_ENCODING, DP_DATE_CREATE, DP_ALARM, DP_CB_URL, DP_IMAGE_FACE, DV_ID)"
                   " VALUES (%(name)s, %(image_en)s, %(ngaytao)s, %(i_alarm)s, %(i_cb_url)s, %(image_face)s, %(donvi_id)s)")
data_add_data_people = {
    'name': '',
    'image_en': '',
    'ngaytao': '',
    'i_alarm': '',
	'i_cb_url': '',
    'image_face': ''
}
query_data_people = "SELECT * FROM data_people WHERE DP_STATUS = 1"
query_load_data_people = "SELECT DP_ID,DP_IMAGE_ENCODING FROM data_people WHERE DP_STATUS = 1"
load_data_train_people = ("SELECT DP_ID,DP_NAME,DP_DATE_CREATE,DP_IMAGE_FACE,DP_ALARM,DP_CB_URL,DV_ID,DP_STATUS,DV_ID FROM data_people WHERE DV_ID = %(donvi_id)s AND DP_STATUS = 1")
edit_data_train_people = ("UPDATE data_people SET DP_ALARM = %(alarm)s, DP_CB_URL = %(cb_url)s, DV_ID = %(donvi_id)s "
"WHERE DP_NAME = %(label)s")
# edit_data_train_people = ("UPDATE data_people SET DP_NAME = %(label)s, DP_ALARM = %(alarm)s, DP_CB_URL = %(cb_url)s, DV_ID = %(donvi_id)s "
#                           "WHERE DP_ID = %(dp_id)s")

data_edit_data_train_people = {
    'label': '',
    'alarm': '',
    'cb_url': '',
    'dp_id': ''
}

update_face_data_train_people = ("UPDATE data_people SET DP_IMAGE_ENCODING = %(face_en)s, DP_IMAGE_FACE = %(face64)s "
                                 "WHERE DP_ID = %(dp_id)s")

delete_data_train_people = ("UPDATE data_people SET DP_STATUS = %(status)s "
                            "WHERE DP_ID = %(dp_id)s")
delete_data_train_people_label = ("UPDATE data_people SET DP_STATUS = %(status)s "
                                  "WHERE DP_NAME = %(dp_name)s AND DV_ID= %(dv_id)s")

data_delete_data_train_people = {
    'status': '',
    'dp_id': ''
}

get_setting_camera = "SELECT * FROM streammanager WHERE ID = %s"

data_get_setting_camera = {
    'id': ''
}
