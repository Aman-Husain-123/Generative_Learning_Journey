from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Database URL
db_url = "postgresql://neondb_owner:npg_secD4wZKdO3k@ep-flat-dew-a413066u-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


# Pydantic model
class Student(BaseModel):
    id: int
    name: str
    age: int


# DB Connection
def get_connection():
    return psycopg2.connect(db_url, cursor_factory=RealDictCursor)


# --------------------------- API Endpoints ---------------------------

@app.post("/student/local/save")
def create_student_local(data: Student):
    """Save student inside a local file."""
    with open("students.txt", "a") as f:
        f.write(f"{data.id},{data.name},{data.age}\n")
    
    return {"message": "Student saved locally"}


@app.post("/student/db/insert")
def insert_student_db(student: Student):
    """Insert a student into PostgreSQL database."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO student (id, name, age) VALUES (%s, %s, %s)",
            (student.id, student.name, student.age)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Student inserted successfully"}


@app.put("/student/db/update")
def update_student_db(student: Student):
    """Update an existing student record."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM student WHERE id=%s", (student.id,))
    record = cursor.fetchone()

    if not record:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    cursor.execute(
        "UPDATE student SET name=%s, age=%s WHERE id=%s",
        (student.name, student.age, student.id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Student updated successfully"}


@app.get("/student/{student_id}")
def get_student(student_id: int):
    """Fetch a student by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM student WHERE id=%s", (student_id,))
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.delete("/student/db/delete/{student_id}")
def delete_student(student_id: int):
    """Delete student record from DB."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM student WHERE id=%s", (student_id,))
    record = cursor.fetchone()

    if not record:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    cursor.execute("DELETE FROM student WHERE id=%s", (student_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": f"Student with ID {student_id} deleted successfully"}
