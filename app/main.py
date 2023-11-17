from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import Session
from . import database, models_and_schemas, crud, auth, sendmail
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv(find_dotenv())

app = FastAPI(
    title="Andreas Lagocki | DigitalArt",
)


@app.on_event("startup")
def startup_event():
    database.create_db_and_tables()


@app.post("/register", tags=["Default"])
def register_user(user: models_and_schemas.UserSchema, db: Session = Depends(database.get_db)):
    db_user = crud.create_user(db=db, user=user)
    token = auth.create_access_token(user=db_user)
    #sendmail.send_mail(to=user.email, token=token, username=user.username)
    return db_user


@app.post("/login", tags=["Default"])
def login(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = crud.get_user_by_username(db=db, username=form_data.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Anmeldeinformationen nicht korrekt")
    if auth.verify_password(form_data.password, db_user.hashed_password):
        token = auth.create_access_token(db_user)
        return {"access_token": token, "token_typ": "Bearer"}
    raise HTTPException(status_code=401, detail="Anmeldeinformationen nicht korrekt")


@app.get("/verify/{token}", response_class=HTMLResponse, tags=["Default"])
def verify_user(token: str, db: Session = Depends(database.get_db)):
    claims = auth.decode_token(token)
    username = claims.get('sub')
    db_user = crud.get_user_by_username(db=db, username=username)
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return f"""
    <html>
        <head>
            <title>Bestätigung der Registrierung</title>
        </head>
        <body>
            <h2>Aktivierung von {username} erfolgreich!</h2>
            <a href="https://www.lagocki.de">
                Zurück
            </a>
        </body>
    </html>
    """

# @app.get("/users")
def get_all_user(db: Session = Depends(database.get_db), tags=["Default"]):
    users = crud.get_users(db=db)
    return users


@app.get("/customer/{id}", dependencies=[Depends(auth.check_active)], tags=["Customer"], description="Get Customer Data by ID")
def get_customer(id:int, db: Session = Depends(database.get_db)):
    users = crud.get_user_by_id(db=db, userid=id)
    return users


@app.get("/admin", dependencies=[Depends(auth.check_admin)], tags=["Admin"])
def secured(db: Session = Depends(database.get_db)):
    users = crud.get_users(db=db)
    return users
