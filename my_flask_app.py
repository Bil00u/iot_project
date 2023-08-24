# Importing necessary modules from the Flask and SQLAlchemy libraries
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Creating a new Flask application
app = Flask(__name__)

# Setting the configuration for the Flask application to use a SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/debian/iot_project/light_data.db'
# Disabling SQLAlchemy's event system
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initializing an SQLAlchemy object which provides an interface to the database
db = SQLAlchemy(app)

# Defining a model for light data in the database
class LightData(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Each reading has a unique id
    timestamp = db.Column(db.Integer) # The time the reading was taken
    value = db.Column(db.Float) # The light sensor value

# Defining a model for the light threshold in the database
class Threshold(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Each threshold has a unique id
    value = db.Column(db.Float) # The threshold value

# Define the main route for the Flask application
@app.route('/', methods=['GET', 'POST'])
def home():
	# If the request is a POST request
    if request.method == 'POST':
# Fetch the first (and only) threshold from the database
        threshold = Threshold.query.get(1)
# Update its value with the value from the form
        threshold.value = request.form['threshold']
# Commit the changes to the database
        db.session.commit()
# Fetching the last 100 light data readings from the database
    data = LightData.query.order_by(LightData.id.desc()).limit(100).all()
# Fetching the threshold from the database
    threshold = Threshold.query.get(1)
# If there is no threshold in the database yet, create one with a default value of 0.0
    if not threshold:
        threshold = Threshold(id=1, value=0.0)
# Adding the new threshold to the database and commit the changes
        db.session.add(threshold)
        db.session.commit()
# Rendering the index.html template, passing in the light data and threshold
    return render_template('index.html', data=data, threshold=threshold)

@app.route('/latest-data', methods=['GET'])
def latest_data():
    latest_data = LightData.query.order_by(LightData.id.desc()).first()
    if latest_data:
        return jsonify({'timestamp': latest_data.timestamp, 'value': latest_data.value})
    else:
        return jsonify({})
# If the script is being run directly
if __name__ == '__main__':
# Create all database tables according to the defined models
    with app.app_context():
        db.create_all()

# Start the Flask application, listening on all IP addresses on port 8082
    app.run(host='0.0.0.0', port=8082)

