import os
import json
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db=SQLAlchemy(app)

ma=Marshmallow(app)

class Student(db.Model):
   __tablename__='students'
   id=db.Column(db.Integer, primary_key=True)
   fname=db.Column(db.String(40))

   def __init__(self, fname):
      self.fname = fname

class StudentSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
      model = Student

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@app.get('/')
def welcome():
   return 'Hello World'

@app.post('/student')
def addStudent():
   result = request.get_json()
   student = Student(result["fname"])
   db.session.add(student)
   db.session.commit()
   # return student_schema.jsonify(student)
   return jsonify(student_schema.dump(student))

@app.get('/student')
def viewgetAllStudents():
   all_students = Student.query.all()
   # return jsonify(students_schema.dump(all_students))
   return students_schema.jsonify(all_students)
