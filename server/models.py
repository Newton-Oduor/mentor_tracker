from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


class Mentor(db.Model):
    __tablename__ = 'mentors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    cohort = db.relationship(
        'Cohort',
        back_populates='mentor',
        uselist=False
    )

    def student_count(self):
        if not self.cohort:
            return 0

        student_ids = {sp.student_id for sp in self.cohort.student_phases}
        return len(student_ids)


class Cohort(db.Model):
    __tablename__ = 'cohorts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.id'))
    mentor = db.relationship('Mentor', back_populates='cohort')

    phases = db.relationship('Phase', back_populates='cohort')
    student_phases = db.relationship('StudentPhase', back_populates='cohort')


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    student_phases = db.relationship('StudentPhase', back_populates='student')


class Phase(db.Model):
    __tablename__ = 'phases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'))
    cohort = db.relationship('Cohort', back_populates='phases')

    student_phases = db.relationship('StudentPhase', back_populates='phase')


class StudentPhase(db.Model):
    __tablename__ = 'student_phase'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    phase_id = db.Column(db.Integer, db.ForeignKey('phases.id'))
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'))
    grade = db.Column(db.Float)

    student = db.relationship('Student', back_populates='student_phases')
    phase = db.relationship('Phase', back_populates='student_phases')
    cohort = db.relationship('Cohort', back_populates='student_phases')