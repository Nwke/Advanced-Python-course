import psycopg2 as pg


def create_db():
    with pg.connect(dbname='netology_db', user='denis') as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE student (
            id serial PRIMARY KEY,
            name varchar(100) NOT NULL ,
            gpa numeric(10, 2),
            birth timestamp with time zone );""")

            cur.execute("""CREATE TABLE course (
            id serial PRIMARY KEY,
            name varchar(100) NOT NULL );""")

            cur.execute("""CREATE TABLE student_course (
            id serial PRIMARY KEY,
            student_id integer REFERENCES student(id),
            course_id integer REFERENCES course(id));""")


def get_students(course_id):  # возвращает студентов определенного курса
    with pg.connect(dbname='netology_db', user='denis') as conn:
        with conn.cursor() as cur:
            cur.execute("""      
            select student.name, course.name from student
            join student_course on student_course.student_id = student.id
            join course on course.id = (%s)""", (str(course_id),))
            return cur.fetchall()


def add_students(course_id, students):  # создает студентов и
    with pg.connect(dbname='netology_db', user='denis') as conn:
        with conn.cursor() as cur:
            for student in students:
                add_student(student)
                id_last_student = _get_id_last_record()
                cur.execute("""insert into student_course (student_id, course_id) values (%s, %s)""",
                            (id_last_student, course_id))


def add_student(student):
    with pg.connect(dbname='netology_db', user='denis') as conn:
        with conn.cursor() as cur:
            cur.execute("""insert into student (name, gpa, birth) values (%s, %s, %s)""",
                        (student['name'], student['gpa'], student['birth']))


def get_student(student_id):
    with pg.connect(dbname='netology_db', user='denis') as conn:
        with conn.cursor() as cur:
            cur.execute("""select * from student where student.id = (%s)""", (str(student_id)))
            return cur.fetchall()


def _get_id_last_record():
    field_id_in_scheme = 0

    with pg.connect(dbname='netology_db', user='denis') as conn:
        with conn.cursor() as cur:
            cur.execute("""select * from student ORDER BY id desc""")
            user = cur.fetchall()
            return user[field_id_in_scheme][field_id_in_scheme]


if __name__ == "__main__":
    create_db()
    add_student({'name': 'Kiril', 'gpa': 5, 'birth': '1995-03-03'})
    add_student({'name': 'Vanya', 'gpa': 9, 'birth': '1935-03-03'})
    add_students(1, [{'name': 'Masha', 'gpa': 7, 'birth': '2995-03-03'}])
