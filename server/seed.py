from app import app
from models import db, Mentor, Cohort, Student, Phase
from datetime import date
from random import randint, sample


with app.app_context():

    db.drop_all()
    db.create_all()


    mentor_names = [
        "Tom Mboya",
        "Alex Muiruri",
        "Sarah Wanjiru",
        "Kevin Mutua",
        "Linda Achieng",
        "Joseph Karanja",
        "Mary Wambui",
        "Brian Otieno",
        "Faith Njeri",
        "Daniel Kiptoo"
    ]

    mentors = [Mentor(name=name) for name in mentor_names]
    db.session.add_all(mentors)
    db.session.flush()

 
    cohorts = []
    for index, mentor in enumerate(mentors, start=1):
        cohort = Cohort(
            name=f"SDF FT-{index:02}",
            start_date=date(2024, 1, 10),
            end_date=date(2024, 6, 10),
            mentor=mentor
        )
        cohorts.append(cohort)

    db.session.add_all(cohorts)
    db.session.flush()


    phases = []
    for cohort in cohorts:
        for i in range(1, 6):
            phases.append(
                Phase(
                    name=f"Phase {i}",
                    cohort=cohort
                )
            )

    db.session.add_all(phases)
    db.session.flush()

 
    students = [
        Student(
            name=f"Student {i}",
            grade=randint(60, 95)
        )
        for i in range(1, 31)
    ]

    db.session.add_all(students)
    db.session.flush()


    remaining_students = students.copy()

    for cohort in cohorts:
        # Each cohort gets 2–6 students (uneven by design)
        cohort_students = sample(
            remaining_students,
            min(randint(2, 6), len(remaining_students))
        )

        for student in cohort_students:
            student.cohort = cohort
            remaining_students.remove(student)

        if not remaining_students:
            break

    db.session.commit()

