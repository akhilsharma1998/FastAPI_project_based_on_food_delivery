from fastapi import APIRouter, status, Depends
from database import Session, engine
from schemas import SignupModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix = "/auth",
    tags = ['auth']
)

session = Session(bind=engine)

@auth_router.get("/")
async def hello(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return {"message":"hello world"}

# signup route

@auth_router.post("/signup", response_model = SignupModel, status_code = status.HTTP_201_CREATED)
async def signup(userss:SignupModel):
    db_email = session.query(User).filter(User.email==userss.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail = "user with this email is already exist")

    db_username = session.query(User).filter(User.username==userss.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail = "user with this username is already exist")

    new_user = User(
        username = userss.username,
        email = userss.email,
        passwored = generate_password_hash(userss.passwored),
        is_active = userss.is_active,
        is_staff = userss.is_staff
    )

    session.add(new_user)

    session.commit()

    return new_user

# login route

@auth_router.post("/login", status_code=200)
async def login(userss:LoginModel, Authorize:AuthJWT=Depends()):
    db_user = session.query(User).filter(User.username == userss.username).first()

    if db_user and check_password_hash(db_user.passwored, userss.passwored):
        access_token = Authorize.create_access_token(subject = db_user.username)
        refresh_token = Authorize.create_refresh_token(subject = db_user.username)

        response ={
            "access_token":access_token,
            "refresh_token":refresh_token
        }
        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    detail = "invalid username or password. please enter a valid email or password"
    )

@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "please provide a valid refresh token"
        )
    current_user=Authorize.get_jwt_subject()
    access_token=Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access":access_token})





    
