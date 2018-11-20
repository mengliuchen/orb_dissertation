from db import db


class Records(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # kp = db.Column(db.Text())
    des = db.Column(db.Text())
    img_path = db.Column(db.String)
    position_x = db.Column(db.String)
    position_y = db.Column(db.String)
    label = db.Column(db.String)


def get_all_records():
    return Records.query.all()


def get_record_by_img(img_path):
    return Records.query.filter_by(img_path=img_path).first()


def insert_or_update_record(img_path, des, pos_x, pos_y, label):
    record = get_record_by_img(img_path)
    if record is None:
        # record = Records(img_path=img_path, kp=kp, des=des, position_x=pos_x, position_y=pos_y, label=label)
        record = Records(img_path=img_path, des=des, position_x=pos_x, position_y=pos_y, label=label)
        db.session.add(record)
        db.session.commit()
    else:
        record.img_path = img_path
        record.des = des
        record.pos_x = pos_x
        record.pos_y = pos_y
        record.label = label
        db.session.commit()
