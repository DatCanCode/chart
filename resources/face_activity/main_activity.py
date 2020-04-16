
#import phase
from arcface_fd import FaceDetector
from arcface_fr import FaceRecognition
from arcface_fga import FaceGenderage
import os
import argparse
import cv2
import time
import json
import mxnet as mx
import numpy as np
from numpy.linalg import norm
from face_utilities import load_data_people, load_setting_task
from tool import fr_logs , query, db
import mysql.connector  
from datetime import datetime
import sys

# construct the argument parser and parse command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t","--task_id", type=str,required=True,
	help="Task ID")
ap.add_argument("-s", "--stream_id", type=str, required=True,
help="Stream URL to get frame")
ap.add_argument("-url", "--stream_url", type=str, required=True,
	help="Stream URL to get frame")
args = vars(ap.parse_args())
task_id = args['task_id']
stream_url = args['stream_url']
stream_id = args['stream_id']

#load model
ROOT_DIR = os.path.abspath(os.curdir)
ROOT_DIR = ROOT_DIR + '/resources/face_activity'
path = ROOT_DIR +'/model'

def gpu_device(gpu_number=0):
    try:
        _ = mx.nd.array([1, 2, 3], ctx=mx.gpu(gpu_number))
    except mx.MXNetError:
        return -1
    return gpu_number
ctx = -1#gpu_device()
if ctx == -1:
    print('Run with CPU....')
else:
    print('Run with GPU....')
    
fd = FaceDetector({'prefix':path+'/rentina-net/model','epoch':0000})
fd.prepare(ctx)

fr = FaceRecognition({'prefix':path+'/r100-arcface-net/model','epoch':0000})
fr.prepare(ctx)

fga = FaceGenderage({'prefix':path+'/gender-age-net/model','epoch':0000})
fga.prepare(ctx)

#load database
base = []
label = []

class stackPeople():
    def __init__(self):
        self.currentPeople = set([])
        self.baseUnknown = []
        self.baseUnknownName = []
    def clean(self):
        self.currentPeople = set([])
    def push(self,temp):
        if temp == "Unknown":
            self.currentPeople.add(temp+str(len(self.currentPeople)))
        else:
            self.currentPeople.add(temp)
    def check(self,temp):
        if temp in self.currentPeople:
            return True
        else:
            return False
            
def train_data_local(path):
    img_names = os.listdir(path)

    for img_name in img_names:
        image = cv2.imread(path+img_name)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image,(640,480))
        #image = imutils.resize(image, width=480)
        results, lm  = fd.detect(image)
        
        # loop over the detections
        for dets in results:
            startX = int(dets[0])
            startY = int(dets[1])
            endX = int(dets[2])
            endY = int(dets[3])
            scores = dets[4]

            if scores > 0.9:
                emd = fr.get_embedding(image[startY:endY,startX:endX])[0]
                base.append(emd)
                label.append(img_name.split('.')[0])
#print('train data.....')

# train_data_local(ROOT_DIR+'/known_people/')
# print('Done')
# print(label)

def recognition(ebd, base):
    confi = 0.6
    result = -1
    for i,emd in enumerate(base):
        cos_sim = np.dot(ebd, emd)/(norm(ebd)*norm(emd))
        if cos_sim > confi:
            confi = cos_sim
            #print(confi)
            result = i
    return result
#main processing

known_dp_id, known_encodings, map_id_name, known_name_to_cburl = load_data_people()

json_data = load_setting_task(task_id)
print(json_data)
donvi_id = json_data[0]['DV_ID']
unknown_alarm = 0
unknown_alarm_cb_url = ''
if json_data[0]['SETTING']:
    setting_stream = json_data[0]['SETTING']
    print(setting_stream)
    setting_json = json.loads(setting_stream)
    face = setting_json['face']
    platenumber = setting_json['platenumber']
    unknown_alarm = setting_json['unknown_alarm']
    unknown_alarm_cb_url = setting_json['unknown_alarm_cb_url']

cap = cv2.VideoCapture(0)
checkCamError = False
currentPeople = stackPeople()

while True:
    t = time.time()
    key = cv2.waitKey(1)

    try:
        _ , frame = cap.read()
        #frame = imutils.resize(frame, width=700)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        checkCamError = False
    except:
        if not checkCamError:
            print("Camera error read()")
            fr_logs.logger.debug("Camera error read()")
            checkCamError = True
    
    results, lm  = fd.detect(rgb_frame)
    if results  == []:
        continue

    n = 0
    n_known_people = 0
    people_in_frame = []

    known_people_in_frame = []
    unknown_people_in_frame = []

    location = []
    lst_face = []
    lst_location =[]
    ages = []
    genders = []

    # loop over the detections
    for dets in results:
        startX = int(dets[0])
        startY = int(dets[1])
        endX = int(dets[2])
        endY = int(dets[3])
        scores = dets[4]
        left, top, right, bottom = startX, startY, endX, endY
        if scores > 0.9:
            if startX < 0 or startY <0:
                continue
                
            face = rgb_frame[startY:endY, startX:endX]
            gender, age = fga.get(face)
            genders.append(str(gender))
            ages.append(str(age))
            emd = fr.get_embedding(face)[0]
            best_matched = recognition(emd, known_encodings)

            n += 1
            dp_id = -1
            name = "Unknown"

            if best_matched != -1: #known
                dp_id = known_dp_id[best_matched] # it will return id - not name
                n_known_people += 1
                name = map_id_name[dp_id]
                known_people_in_frame.append({'name':name, 'cb_url': known_name_to_cburl[dp_id]})
            else: #unknown
                idx = recognition(emd, currentPeople.baseUnknown)
                if idx == -1:
                    id_temp = "Unknown"+str(len(currentPeople.baseUnknown))
                    currentPeople.baseUnknown.append(emd)
                    currentPeople.baseUnknownName.append(id_temp)
                else:
                    dp_id = currentPeople.baseUnknownName[idx]
                unknown_people_in_frame.append("Unknown")
            
            lst_face.append(name)
            lst_location.append((left, top, right, bottom))
            
            if not currentPeople.check(dp_id):
                currentPeople.push(dp_id)
                people_in_frame.append(name)
                location.append((left,top,right,bottom))
            #Draw face into frame
            cv2.rectangle(frame, (left, top), (right,bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom + 37), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom + 15), font, 0.8, (255, 128, 0), 1)

    if people_in_frame != [] and len(lst_face) != 1:
        people_in_frame = lst_face
        location = lst_location

    if people_in_frame != []:
        dt = datetime.now()
        dt_ticks = datetime.now() #time.time()
        str_people_in_frame = json.dumps(known_people_in_frame)
        str_location = json.dumps(location)
        str_genders = json.dumps(genders)
        str_ages = json.dumps(ages)

        try:
            data = {
                'stream_id': stream_id,
                'name': str_people_in_frame,
                'image': '',
                'location': str_location,
                'num_of_people': n,
                'num_of_known': n_known_people,
                'genders': str_genders,
                'ages': str_ages,
                'dt': dt,
                'dt_ticks': dt_ticks
            }

            cnx = mysql.connector.connect(**db.face_recognition_local)
            cursor = cnx.cursor()
            cursor.execute(query.add_camera_people, data)
            cnx.commit()
            idlast = cursor.lastrowid
            cursor.close()
            cnx.close()

            # # check alarm
            # for face in data_face:
            #     params = {
            #         'label': face['name'],
            #         'stream_id': id_stream,
            #         'identified_id': idlast
            #     }
            #     try:
            #         #print(params)
            #         r = requests.post(face['cb_url'], json=params)
            #         #print(r.headers)
            #         #print(r.json())
            #     except:
            #         #print("Lỗi callback identifiedImagePeople")
            #         fr_logs.logger.error("*** Threading: loi callback people")
            #         fr_logs.logger.error(stream_id)
            #         fr_logs.logger.error(stream_url)
            #         fr_logs.logger.error(sys.exc_info()[0])

            # # check alarm Unknown
            # if unknown_alarm == "1":
            #     for a_name in name_face:
            #         if a_name == "Unknown":
            #             params = {
            #                 'label': 'Unknown',
            #                 'stream_id': id_stream,
            #                 'identified_id': idlast
            #             }
            #             try:
            #                 #print(unknown_alarm_cb_url)
            #                 #print(params)
            #                 r = requests.post(unknown_alarm_cb_url, json=params)
            #                 #print(r.headers)
            #                 #print(r.json())
            #             except:
            #                 fr_logs.logger.error("*** Threading: loi callback unknown")
            #                 fr_logs.logger.error(stream_id)
            #                 fr_logs.logger.error(stream_url)
            #                 fr_logs.logger.error(sys.exc_info()[0])
            #         break
        except:
            print(sys.exc_info()[0])
    
    #show FPS
    cv2.putText(frame, str(int(1/(time.time()-t))), (40, 40), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# do a bit of cleanup
cv2.destroyAllWindows()