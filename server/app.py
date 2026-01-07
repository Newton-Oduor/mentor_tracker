from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Mentor
import models 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return {"message": "Moringa Mentor Impact Tracker API"}


@app.route('/top-mentors')
def top_mentors():
    mentors = Mentor.query.all()

    ranked = sorted(
        mentors,
        key=lambda m: m.student_count(),
        reverse=True
    )[:5]

    return jsonify([
        {
            "mentor": mentor.name,
            "students_trained": mentor.student_count()
        }
        for mentor in ranked
    ])


if __name__ == '__main__':
    app.run(debug=True)