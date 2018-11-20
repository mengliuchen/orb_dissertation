import os
import pickle
import uuid
from flask import Flask, render_template, make_response, request, json
from sqlalchemy.orm import create_session

from ai.orb import compute_orb, compute_orb_percent
from db import db
from db.Records import insert_or_update_record, get_all_records

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/mys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/upload_file', methods=["POST"])
def update_file():
    img = request.files['img']
    if not img:
        return make_response("error", 400)
    filename = img.filename
    filename = str(uuid.uuid1()).replace("-", "") + "." + filename.rsplit('.', 1)[1].lower()
    img.save(os.path.join("./static/uploads", filename))
    return make_response(filename)


@app.route('/result/<string:id>')
def result(id):
    id_dest = compute_orb(id)
    records = get_all_records()
    max_match = 0
    max_img = None
    for record in records:
        hits = compute_orb_percent(id_dest, pickle.loads(record.des))
        print(hits)
        if hits > max_match:
            max_img = record
            max_match = hits
    if max_img is None:
        return render_template("result.html", q_img=id, max_img=None)
    return render_template("result.html", q_img=id, max_img=max_img, per=max_match)


@app.route('/add_new_record', methods=["POST"])
def add():
    img_path = request.form["img"]
    pos_x = request.form['pos_x']
    pos_y = request.form['pos_y']
    label = request.form['label']
    des = compute_orb(img_path)
    insert_or_update_record(img_path, pickle.dumps(des), pos_x, pos_y, label)
    return make_response("success")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
