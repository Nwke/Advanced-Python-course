import psycopg2 as pg
import sys

from config import DB_NAME, USER, USER_ID, ERROR_COURSE_EXIST


def create_db():
    with pg.connect(dbname=DB_NAME, user=USER) as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS student (
            id serial PRIMARY KEY,
            name varchar(100) NOT NULL ,
            gpa numeric(10, 2),
            birth timestamp with time zone );""")

            cur.execute("""CREATE TABLE IF NOT EXISTS course (
            id serial PRIMARY KEY,
            name varchar(100) NOT NULL );""")

            cur.execute("""CREATE TABLE IF NOT EXISTS student_courses (
            id serial PRIMARY KEY,
            student_id integer REFERENCES student(id)  ON DELETE CASCADE,
            course_id integer REFERENCES course(id)  ON DELETE CASCADE);""")


def get_students(course_id):  # возвращает студентов определенного курса
    with pg.connect(dbname=DB_NAME, user=USER) as conn:
        with conn.cursor() as cur:
            cur.execute("""      
            select student.name, course.name from student
            join student_courses on student_courses.student_id = student.id
            join course on course.id = (%s)""", (str(course_id),))
            return cur.fetchall()


def add_students(course_id, students):
    with pg.connect(dbname=DB_NAME, user=USER) as conn:
        with conn.cursor() as cur:

            cur.execute("""select * from course where course.id = (%s)""", (str(course_id),))
            if cur.fetchone() is None:
                message = f'course with id as {course_id} does not exist'
                return (ERROR_COURSE_EXIST, message)

            for student in students:
                id_last_student = add_student(student)
                cur.execute("""insert into student_courses (student_id, course_id) values (%s, %s)""",
                            (id_last_student, course_id))


def add_student(student):
    with pg.connect(dbname=DB_NAME, user=USER) as conn:
        with conn.cursor() as cur:
            cur.execute("""insert into student (name, gpa, birth) values (%s, %s, %s) RETURNING id;""",
                        (student['name'], student['gpa'], student['birth']))
            return cur.fetchone()[USER_ID]


def get_student(student_id):
    with pg.connect(dbname=DB_NAME, user=USER) as conn:
        with conn.cursor() as cur:
            cur.execute("""select * from student where student.id = (%s)""", str(student_id))


if __name__ == "__main__":
    create_db()
    add_student({'name': 'Kiril', 'gpa': 5, 'birth': '1995-03-03'})
    add_student({'name': 'Vanya', 'gpa': 9, 'birth': '1935-03-03'})

    add_students(1, [{'name': 'Evgen', 'gpa': 7, 'birth': '2995-03-03'}])
    add_students(1, [{'name': 'Evgen', 'gpa': 7, 'birth': '2995-03-03'}])
