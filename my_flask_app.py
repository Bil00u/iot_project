from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/debian/iot_project/light_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class LightData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    value = db.Column(db.Float)

class Threshold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        threshold = Threshold.query.get(1)
        threshold.value = request.form['threshold']
        db.session.commit()

    data = LightData.query.order_by(LightData.id.desc()).limit(100).all()
    threshold = Threshold.query.get(1)
    if not threshold:
        threshold = Threshold(id=1, value=0.0)
        db.session.add(threshold)
        db.session.commit()

    return render_template('index.html', data=data, threshold=threshold)

@app.route('/latest-data', methods=['GET'])
def latest_data():
    latest_data = LightData.query.order_by(LightData.id.desc()).first()
    if latest_data:
        return jsonify({'timestamp': latest_data.timestamp, 'value': latest_data.value})
    else:
        return jsonify({})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8082)

