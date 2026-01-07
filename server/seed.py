from app import app
from models import db, Mentor, Cohort, Student, Phase, StudentPhase
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


    phases = []
    for cohort in cohorts:
        for i in range(1, 6):
            phases.append(
                Phase(name=f"Phase {i}", cohort=cohort)
            )

    db.session.add_all(phases)


    students = [
        Student(name=f"Student {i}") for i in range(1, 31)
    ]

    db.session.add_all(students)
    db.session.flush()

 
    for cohort in cohorts:
        cohort_phases = [p for p in phases if p.cohort == cohort]

        # each cohort gets 2–6 students (uneven on purpose)
        cohort_students = sample(students, randint(2, 6))

        for student in cohort_students:
            # student completes 2–5 phases
            taken_phases = sample(cohort_phases, randint(2, 5))

            for phase in taken_phases:
                db.session.add(
                    StudentPhase(
                        student=student,
                        cohort=cohort,
                        phase=phase,
                        grade=randint(60, 95)
                    )
                )

    db.session.commit()

