#TASKMANAGER
check_exist_task = ("SELECT * FROM taskmanager WHERE TASK_ID = %s")
update_status_taskmanager = ("UPDATE taskmanager "
                    "SET STATUS = %(status)s, DATEUPDATE = %(dateupdate)s "
                    "WHERE TASK_ID = %(task_id)s")
update_taskmanager = ("UPDATE taskmanager "
                    "SET TASK_NAME =%(task_name)s, STREAM_ID =%(stream_id)s, STATUS = %(status)s, DATEUPDATE = %(dateupdate)s, SETTING = %(setting)s "
                    "WHERE TASK_ID = %(task_id)s")
create_taskmanager = ("INSERT INTO taskmanager "
                    "(TASK_ID, TASK_NAME, STREAM_ID, DATECREATED,STATUS,SETTING,DV_ID) "
                    "VALUES (%(task_id)s, %(task_name)s, %(stream_id)s, %(datecreated)s,"
                     " %(status)s, %(setting)s, %(unit_id)s)")
show_all_task = ("SELECT * FROM taskmanager WHERE STATUS <> 0")
show_task_by_id = ("SELECT * FROM taskmanager WHERE TASK_ID = %s ")
#STREAMMANAGER
check_exist_stream = ("SELECT * FROM streammanager WHERE STREAM_ID = %s")
check_exist_stream_url = ("SELECT * FROM streammanager WHERE (STREAM_ID = %s AND STREAM_URL = %s)")
update_status_streammanager = ("UPDATE streammanager "
                    "SET STATUS = %(status)s, DATEUPDATE = %(dateupdate)s "
                    "WHERE STREAM_ID = %(stream_id)s")

update_streammanager = ("UPDATE streammanager"
                        " SET STREAM_NAME = %(stream_name)s, STREAM_URL = %(stream_url)s, DATEUPDATE = %(dateupdate)s,"
                        " DV_ID = %(unit_id)s"
                        " WHERE STREAM_ID = %(stream_id)s")

update_create_streammanager = ("UPDATE streammanager"
                        " SET STREAM_NAME = %(stream_name)s, STREAM_URL = %(stream_url)s, DATECREATED = %(datecreated)s, "
                        " STATUS = %(status)s,DV_ID = %(unit_id)s"
                        " WHERE STREAM_ID = %(stream_id)s")
add_streammanager = ("INSERT INTO streammanager "
                    "(STREAM_ID, STREAM_NAME, STREAM_URL, DATECREATED,STATUS,DV_ID) "
                    "VALUES (%(stream_id)s, %(stream_name)s, %(stream_url)s, %(datecreated)s,"
                     " %(status)s, %(unit_id)s)")
show_all_stream = ("SELECT * FROM streammanager WHERE STATUS NOT IN (0)")
show_stream_by_id = ("SELECT * FROM streammanager WHERE STREAM_ID = %s")
#UNITMANAGER
check_exist_unit = ("SELECT * FROM unitmanager WHERE UNIT_ID = %s ")
add_unit = ("INSERT INTO unitmanager (UNIT_ID, UNIT_NAME, DATECREATED, STATUS)"
             " VALUES (%(unit_id)s,  %(unit_name)s, %(datecreated)s, %(status)s)")
update_unit = ("UPDATE unitmanager SET UNIT_NAME =%(unit_name)s, DATEUPDATE =%(dateupdate)s"
                "WHERE UNIT_ID =%(unit_id)s")
update_add_unit = ("UPDATE unitmanager SET UNIT_NAME =%(unit_name)s, DATECREATED =%(datecreated)s,"
                    "STATUS =%(status)s WHERE UNIT_ID =%(unit_id)s")

update_status_unit = ("UPDATE unitmanager SET STATUS = 0")
show_all_unit = ("SELECT * FROM unitmanager WHERE STATUS = 1")
show_unit_by_id = ("SELECT * FROM unitmanager WHERE UNIT_ID = %s")
#recognition activity
add_camera_people = ("INSERT INTO camera_people "
                     "(STREAM_ID, FACES, IMAGE, FACE_RECTANGLE, AMOUNT_OF_PEOPLE, NUMBER_OF_IDENTIFYERS, GENDER, AGE, CREATEAT, CREATEAT_TICKS) "
                    "VALUES (%(stream_id)s, %(name)s, %(image)s, %(location)s, %(num_of_people)s, %(num_of_known)s, %(genders)s, %(ages)s, %(dt)s, %(dt_ticks)s)")