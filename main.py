# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# @app.get("/Aman/Husain")
# def add(a:int,b:int):            # My input going to be consider as integer
#     return {"result":a + b}

# class substractmode(BaseModel):
#     a: int
#     b: int



# def substract(a:int,b:int):
#     return a-b


# @app.post('/substract')   #To move the particular method runninng in a particular system
# def substract_number(model: substractmode):
#     return substract(model.a,model.b)

# print(add(10,20))



from fastapi import FastAPI

app = FastAPI()


# Decorating
@app.get('/')   # FastAPI object

# TODO: Exposing this function to outer world
def test():
    return {"message":"Hello, Kamine!"}


@app.get("/Aman/test/amana")
def test1():
    return "My name is aman i am data scientist"


students = {1:"Aman",2:"Kiran",3:"Kishan"}
@app.get('/students')
def get_students():
    return students


# TODO: Paramterized API
@app.get("/students/{stud_id}")
def students_search(stud_id:int):    # Pydantic : Maintains Schema for schema validation 
    return {"id":stud_id,"name":students[stud_id]}


# TODO: 
@app.get('/add_student')
def add_student(stud_id:int,name:str):
    students[stud_id] = name
    return students

# TODO: Data is not exposed in the URL
@app.post('/add_student_difff')
def add_student_diff():
    students['new_id'] = 'new_name'
    return students


from pydantic import BaseModel

class newdata(BaseModel):
    stud_id:int
    name:str

@app.post('/add_student_new_valuee')
def add_student_new_value(newdata:newdata):
    students[newdata.stud_id] = newdata.name
    return students


# TODO: Restarting Server
# uvicorn file_name:app --reload