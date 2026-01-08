from flask import Flask, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from datetime import datetime

from models import db, Mentor, Cohort, Student


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)



def not_found(resource="Resource"):
    return {"error": f"{resource} not found"}, 404


def bad_request(message="Bad request"):
    return {"error": message}, 400



class Mentors(Resource):
    def get(self):
        return [mentor.to_dict() for mentor in Mentor.query.all()], 200

    def post(self):
        data = request.get_json()

        if not data or not data.get("name"):
            return bad_request("Mentor name is required")

        mentor = Mentor(name=data["name"])
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
        return [cohort.to_dict() for cohort in Cohort.query.all()], 200

    def post(self):
        data = request.get_json()

        required = ["name", "start_date", "end_date"]
        if not data or not all(field in data for field in required):
            return bad_request("Missing required cohort fields")

        try:
            start_date = parse_date(data["start_date"], "start_date")
            end_date = parse_date(data["end_date"], "end_date")
        except ValueError as e:
            return bad_request(str(e))

        mentor_id = data.get("mentor_id")
        if mentor_id:
            mentor = Mentor.query.get(mentor_id)
            if not mentor:
                return bad_request("Mentor does not exist")
            if mentor.cohort:
                return bad_request("Mentor already assigned to a cohort")

        cohort = Cohort(
            name=data["name"],
            start_date=start_date,
            end_date=end_date,
            mentor_id=mentor_id
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
        return [student.to_dict() for student in Student.query.all()], 200

    def post(self):
        data = request.get_json()

        if not data or not data.get("name"):
            return bad_request("Student name is required")

        cohort_id = data.get("cohort_id")
        if cohort_id and not Cohort.query.get(cohort_id):
            return bad_request("Cohort does not exist")

        student = Student(
            name=data["name"],
            grade=data.get("grade"),
            cohort_id=cohort_id
        )

        db.session.add(student)
        db.session.commit()

        return student.to_dict(), 201


class StudentById(Resource):
    def get(self, id):
        student = Student.query.get(id)
        if not student:
            return not_found("Student")

        return student.to_dict(), 200

    def patch(self, id):
        student = Student.query.get(id)
        if not student:
            return not_found("Student")

        data = request.get_json()

        if "name" in data and not data["name"]:
            return bad_request("Name cannot be empty")

        if "cohort_id" in data and data["cohort_id"]:
            if not Cohort.query.get(data["cohort_id"]):
                return bad_request("Cohort does not exist")

        student.name = data.get("name", student.name)
        student.grade = data.get("grade", student.grade)
        student.cohort_id = data.get("cohort_id", student.cohort_id)

        db.session.commit()
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
api.add_resource(StudentById, "/students/<int:id>")
   

if __name__ == '__main__':
    app.run(port=5000, debug=True)

