from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from datetime import date, datetime, timedelta
from mysql.connector.errors import Error
from gevent.pywsgi import WSGIServer
from PIL import Image
from io import BytesIO
import urllib.request
import base64
import time
import mysql.connector
# import json
import db
import fare
import ast
import sys
import fr_logs
import requests

def auto_start_stream():
    cnx = mysql.connector.connect(**db.face_recognition_local)
    base64_image_search = cnx.cursor()
    try:
        query = ("SELECT * FROM streammanager WHERE STATUS IN (2)")
        base64_image_search.execute(query)
        row_headers = [x[0] for x in base64_image_search.description]
        stream = base64_image_search.fetchall()
        # print(stream)
        # stream = 1
    except Error as e:
        fr_logs.logger.info("-----addthread")
        fr_logs.logger.debug(e)
        fr_logs.logger.debug(sys.exc_info()[0])
        print("Unexpected error:", sys.exc_info()[0])

    if(stream):
        try:
            print('Auto Start Stream')
            json_data = []
            for result in stream:
                json_data.append(dict(zip(row_headers, result)))
            for item in json_data:
                # start nhận diện trên camera
                thread_id = item['STREAM_ID']
                thread_url = item['STREAM_URL']
                print(thread_id)
                # urllib.request.urlopen(thread_url)

                #face_reco.runThreadFaceRecognition(thread_id, thread_url)
                params = {
                "stream_id":thread_id
                }
                r = requests.post(
                'http://127.0.0.1:5002/api/stopStream',
                json=params)
                #print(r.text)
                r = requests.post(
                'http://127.0.0.1:5002/api/startStream',
                json=params)
                #print(r.text)
                cnx.close()
            
        except Error as e:
            fr_logs.logger.info("-----addthread")
            fr_logs.logger.error(e)
            fr_logs.logger.error(sys.exc_info()[0])
            print("Error: {}".format(e))
            print("Unexpected error:", sys.exc_info()[0])
            result = jsonify({
                'return_code': '2',
                'return_msg': 'Không thể bật nhận dạng trên camera. Vui lòng kiểm tra lại camera.',
                'return_data': ''
            })

if __name__ == "__main__":
    time.sleep(30)
    auto_start_stream()