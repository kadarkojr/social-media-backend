from fastapi import FastAPI
from src import models, schemas, utils
from database import engine
from routers import post,user,auth,vote
from config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#class Post(BaseModel):
 #   name : str


'''
while True:


    try:
        conn = psycopg2.connect(host = 'localhost', database = 'testingknowledge', user = 'postgres', password = 'ebemenoor', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection succesful")
        break

    except Exception as error:
        print("Database connection failed")
        print("Error is ", error)
        time.sleep(4)

@app.post('/api')
def create_person(post: Post):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""SELECT * from peops where name = %s""",(post.name,))
        existing_record = cursor.fetchone()

        if existing_record:
            raise HTTPException(status_code=400, detail="Name already registered")


        cursor.execute(""" INSERT into peops (name) values (%s) returning * """, (post.name,))
        new_post = cursor.fetchone()

    conn.commit()
    return {"data" : new_post}


@app.get('/api/{id}')
def get_person(id : int):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(""" Select * from peops where id = %s """, (str(id),))
        new_post = cursor.fetchone()

    if not new_post:
        raise HTTPException(status_code = 400, detail= f"user with id {id} not found")

    return {"data" : new_post}

@app.delete('/api/{id}')
def delete_person(id : int):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(""" Select * from peops where id = %s""", (str(id),))
        existing_record = cursor.fetchone()

        if existing_record:
            cursor.execute(""" DELETE FROM peops where id = %s returning *""", (str(id),))
            deleted_post = cursor.fetchone()
        conn.commit()

        if not existing_record:
            raise HTTPException(status_code=404, detail=f"User with id {id} not found in list")

        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/api/{id}")
def update_user(id : int, post: Post):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(""" SELECT id FROM peops WHERE id = %s""", (str(id),))
        existing_record = cursor.fetchone()
    
    
        if existing_record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")

        
        cursor.execute(""" UPDATE peops SET name = %s WHERE id = %s RETURNING *""", (post.name, str(id),))
        updated_post = cursor.fetchone()
    
    conn.commit()
    
    return {"data" : updated_post}



@app.post('/users',status_code=status.HTTP_201_CREATED, response_model=schemas.Userout)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/users/{id}', response_model=schemas.Userout)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=400, detail=f"User with id {id} not found")

    return user
'''
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def getter():
    return {"message" : "hello world!!!!!!"}