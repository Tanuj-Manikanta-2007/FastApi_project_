import fastapi
import pydantic 

app = fastapi.FastAPI()
users = {}
class storage(pydantic.BaseModel):
  id : str
  name : str
  email : str
  age : int
  
@app.post('/add')
def new_dict(user : storage):
  if user.id in users:
    raise fastapi.HTTPException(statuc_code = 400,detail = "User ID already exists")
  users[user.id] = {
    "name" : user.name,
    "email" : user.email,
    "age" : user.age
  }
  return {"message" : "User added successfull", "user" : users[user.id]}
@app.get('/all_users')
def all_user_data():
  for i in users:
    return {"users" : users }
