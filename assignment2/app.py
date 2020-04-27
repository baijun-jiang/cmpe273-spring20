from flask import Flask, escape, request, Response, send_from_directory

import sqlite3
import json
import os.path

from os import path
from collections import OrderedDict

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files'

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/files/<file_name>')
def get_scantron_file(file_name):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=file_name)

@app.route('/api/tests', methods=['POST'])
def save_test():
    payload = request.get_json()
    is_valid = valid_test(payload.get("answer_keys", None))

    if not is_valid:
        return "Invalid test format", 400
    
    connection = sqlite3.connect("test_db.db")

    cursor = connection.cursor()

    cursor.execute("INSERT INTO tests (subject, answer_keys) VALUES (?, ?)", 
        (payload.get("subject", None), json.dumps(payload.get("answer_keys", None))))

    test = Test()

    test.set_id(cursor.lastrowid)
    test.set_subject(payload.get("subject", None))
    test.set_answers(payload.get("answer_keys", None))

    connection.commit()
    connection.close()

    return test.__dict__, 201


@app.route('/api/tests/<id>', methods=['GET'])
def get_test(id):
    connection = sqlite3.connect("test_db.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tests where id=?", (id, ))

    tuple_item = cursor.fetchone()

    test = Test()
    test.set_id(tuple_item[0])
    test.set_subject(tuple_item[1])
    answers = json.loads(tuple_item[2])
    test.set_answers(OrderedDict(sorted((int(key), value) for key, value in answers.items())))

    submissions = []

    cursor.execute("SELECT * FROM scantrons where test_id = ?", (id, ))
    tupled_items = cursor.fetchall()

    for item in tupled_items:
        submission = Scantron()
        submission.set_id(item[0])
        submission.set_name(item[1])
        submission.set_subject(item[2])
        submission.set_subject(item[4])
        submission.set_url("http://localhost:5000/files/scantron-%s.json" % item[0])
        submission.set_result(
            OrderedDict(sorted((int(key), value) for key, value in json.loads(item[3]).items()))
        )

        submissions.append(submission.__dict__)
    
    test.set_submissions(submissions)

    
    return test.__dict__, 201


def valid_test(tests):
    for key in tests:
        if not key.isdigit():
            return False
    
    return True


@app.route('/api/tests/<test_id>/scantrons', methods=['POST'])
def save_scantron(test_id):

    if 'scantron' not in request.files:
        return "missing scantron upload file", 400
    
    f = request.files['scantron']

    if f.filename == '':
        return "missing file name", 400
    
    try:
        scantron = json.load(f)
    except Exception as e:
        return "input file is not in correct json format", 400
    
    scantron_anwsers = scantron.get("answers", None)

    connection = sqlite3.connect("test_db.db")
    cursor = connection.cursor()
    cursor.execute("SELECT subject, answer_keys FROM tests where id=?", (test_id, ))
    tuple_item = cursor.fetchone()

    if scantron.get('subject', None) == None or scantron.get('subject', None) != tuple_item[0]:
        return "submitted wrong subject", 400

    test_answers = json.loads(tuple_item[1])
    scanctron_with_score = grade_scantron(test_answers, scantron_anwsers)

    if not scanctron_with_score[2]:
        return "invalid scantron, scantron has different format from the test", 400

    score = scanctron_with_score[1]

    cursor.execute("INSERT INTO scantrons (subject, name, score, answers, test_id) VALUES(?, ?, ?, ?, ?)", (
        scantron.get("subject", None), scantron.get("name", None), score, 
        json.dumps(scanctron_with_score[0]), test_id))
    
    scantron_id = cursor.lastrowid

    connection.commit()
    connection.close()

    graded_scantron = {
        "scantron_id": scantron_id,
        "scantron_url": "http://localhost:5000/files/scantron-%s.json" % scantron_id,
        "subject": scantron.get("subject", None),
        "name": scantron.get("name", None),
        "score": score,
        "result": scanctron_with_score[0]
    }

    scantron_path = "files/scantron-%s.json" % scantron_id
    with open(scantron_path, 'w') as f:
        json.dump(graded_scantron, f)

    return graded_scantron, 201

def grade_scantron(test_keys, actual_keys):
    score = 0
    result = {}
    is_valid = True

    for key in test_keys:

        if key not in actual_keys:
            is_valid = False
            continue

        expect_answer = test_keys.get(key, None)
        actual_answer = actual_keys.get(key, None)

        if actual_answer is not None and expect_answer == actual_answer:
            score = score + 1
        
        result[key] = {
            "actual": actual_answer,
            "expected": expect_answer
        }

    result = OrderedDict(sorted((int(key), value) for key, value in result.items()))
    return (result, score, is_valid) 


class Test:
    def __init__(self):
        self.test_id = None
        self.subject = None
        self.answer_keys = None
        self.submissions = []
    
    def get_id(self):
        return self.test_id
    
    def set_id(self, id):
        self.test_id = id
    
    def get_subject(self):
        return self.subject
    
    def set_subject(self, subject):
        self.subject = subject
    
    def get_answers(self):
        return self.answer_keys
    
    def set_answers(self, anwsers):
        self.answer_keys = anwsers
    
    def get_submissions(self):
        return self.submissions
    
    def set_submissions(self, submissions):
        self.submissions = submissions


class Scantron:
    def __init__(self):
        self.id = None
        self.scantron_url = None
        self.name = None
        self.subject = None
        self.score = None
        self.result = None
    
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id

    def get_subject(self):
        return self.subject
    
    def set_subject(self, subject):
        self.subject = subject
    
    def get_score(self):
        return self.score
    
    def set_score(self, score):
        self.score = score
    
    def get_result(self):
        return self.result
    
    def set_result(self, result):
        self.result = result
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def get_url(self):
        return self.scantron_url
    
    def set_url(self, url):
        self.scantron_url = url