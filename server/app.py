from flask_restful import Api, Resource
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate

from models import db, Mentor, Cohort, Student
import models 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


# @app.route('/')
# def home():
#     return {"message": "Moringa Top 5 Mentors"}

# @app.route('/top-mentors')



# Error Handling
def not_found(resource="Resource"):
    return {"error": f"{resource} not found"}, 404


def bad_request(message="Bad request"):
    return {"error": message}, 400


class Mentors(Resource):
    def get(self):
        return [m.to_dict() for m in Mentor.query.all()], 200
    
    def post(self):
        data = request.get_json()
        if not data or not data.get("name"):
            return bad_request("Mentor name is required")

        mentor = Mentor(name=data['name'])
        db.session.add(mentor)
        db.session.commit()

        return mentor.to_dict(), 201


class MentorById(Resource):
    
    def get(self, id):
        mentor = Mentor.query.get(id)
        if not mentor:
            return not_found("Mentor")

        return mentor.to_dict(), 200

    def patch(self, id):
        mentor = Mentor.query.get(id)
        if not mentor:
            return not_found("Mentor")

        data = request.get_json()

        if "name" in data and not data["name"]:
            return bad_request("Name cannot be empty")

        mentor.name = data.get("name", mentor.name)
        db.session.commit()

        return mentor.to_dict(), 200

    def delete(self, id):
        mentor = Mentor.query.get(id)
        if not mentor:
            return not_found("Mentor")

        db.session.delete(mentor)
        db.session.commit()

        return {}, 204
    

class Cohorts(Resource):

    def get(self):
        return [c.to_dict() for c in Cohort.query.all()], 200

    def post(self):
        data = request.get_json()

        required = ["name", "start_date", "end_date"]
        if not all(field in data for field in required):
            return bad_request("Missing required cohort fields")

        cohort = Cohort(
            name=data["name"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            mentor_id=data.get("mentor_id")
        )

        db.session.add(cohort)
        db.session.commit()

        return cohort.to_dict(), 201


class CohortById(Resource):
    def get(self, id):
        cohort = Cohort.query.get(id)
        if not cohort:
            return not_found("Cohort")

        return cohort.to_dict(), 200

    def delete(self, id):
        cohort = Cohort.query.get(id)
        if not cohort:
            return not_found("Cohort")

        db.session.delete(cohort)
        db.session.commit()
        return {}, 204    


class Students(Resource):

    def get(self):
        students = Student.query.all()
        return [s.to_dict() for s in students], 200

    def post(self):
        data = request.get_json()
        if not data or not data.get("name"):
            return bad_request("Student name is required")

        student = Student(name=data["name"])
        db.session.add(student)
        db.session.commit()

        return student.to_dict(), 201
    
class StudentById(Resource):

    def get(self, id):
        student = Student.query.get(id)
        if not student:
            return not_found("Student")

        return student.to_dict(), 200

    def delete(self, id):
        student = Student.query.get(id)
        if not student:
            return not_found("Student")

        db.session.delete(student)
        db.session.commit()
        return {}, 204

api.add_resource(Mentors, "/mentors")
api.add_resource(MentorById, "/mentors/<int:id>")
api.add_resource(Cohorts, "/cohorts")
api.add_resource(CohortById, "/cohorts/<int:id>")
api.add_resource(Students, "/students")    

if __name__ == '__main__':
    app.run(port=5000, debug=True)















        # def top_mentors():
    # mentors = Mentor.query.all()

    # ranked = sorted(
    #     mentors,
    #     key=lambda m: m.student_count(),
    #     reverse=True
    # )[:5]

    # return jsonify([
    #     {
    #         "mentor": mentor.name,
    #         "students_trained": mentor.student_count()
    #     }
    #     for mentor in ranked
    # ])