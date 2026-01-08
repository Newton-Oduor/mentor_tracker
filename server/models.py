from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


# =========================
# Mentor
# =========================
class Mentor(db.Model, SerializerMixin):
    __tablename__ = 'mentors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # One mentor -> one cohort
    cohort = db.relationship(
        'Cohort',
        back_populates='mentor',
        uselist=False
    )

    serialize_rules = (
        '-cohort.mentor',
        '-cohort.students.cohort',
        '-cohort.phases.cohort',
    )

    def student_count(self):
        return len(self.cohort.students) if self.cohort else 0


# =========================
# Cohort
# =========================
class Cohort(db.Model, SerializerMixin):
    __tablename__ = 'cohorts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.id'))
    mentor = db.relationship('Mentor', back_populates='cohort')

    # One cohort -> many students
    students = db.relationship(
        'Student',
        back_populates='cohort',
        cascade='all, delete-orphan'
    )

    # One cohort -> many phases
    phases = db.relationship(
        'Phase',
        back_populates='cohort',
        cascade='all, delete-orphan'
    )

    serialize_rules = (
        '-mentor.cohort',
        '-students.cohort',
        '-phases.cohort',
    )


# =========================
# Student
# =========================
class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Global grade (simple model)
    grade = db.Column(db.Float)

    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'))
    cohort = db.relationship('Cohort', back_populates='students')

    serialize_rules = (
        '-cohort.students',
        '-cohort.phases',
        '-cohort.mentor',
    )


# =========================
# Phase
# =========================
class Phase(db.Model, SerializerMixin):
    __tablename__ = 'phases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'))
    cohort = db.relationship('Cohort', back_populates='phases')

    serialize_rules = (
        '-cohort.phases',
        '-cohort.students',
        '-cohort.mentor',
    )