from flask import request, json, jsonify
from flask_restful import Resource
import mysql.connector
from mysql.connector.errors import Error
from datetime import datetime
from .tool import fr_logs
from .tool import db
from .tool import query
from .tool import fare
import sys 
import ast

def get_body_data():
    body_data = request.data
    if body_data:
        body_data = str(body_data.decode('utf-8', errors='ignore'))
        return ast.literal_eval(body_data)
    else:
        return {}