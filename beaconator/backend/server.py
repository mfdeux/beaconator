import os
import typing
import uuid

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import dao, models, schemas
from .database import SessionLocal, engine
from .utils.http import SingletonAiohttp
from .utils.images import image_queries
from .utils.other import current_http_datetime
from .utils.secrets import (
    JWT_SECRET,
    TEMP_PASSWORD,
    InvalidToken,
    generate_jwt_token,
    validate_jwt_token,
)

beacon_url = "https://ssl.google-analytics.com/collect"
DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../..", "data")
STATIC_DIR = os.path.join(DATA_DIR, "static")


def get_auth_token(*, authorization: str = Header(None)) -> None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    scheme, token = get_authorization_scheme_param(authorization)
    if scheme.lower() != "bearer":
        raise credentials_exception

    try:
        validate_jwt_token(token, JWT_SECRET)
    except InvalidToken:
        raise credentials_exception


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def static_file(filename: str) -> str:
    return os.path.join(STATIC_DIR, filename)


def make_analytics_payload(
    tracking_id: str,
    property_code: str,
    client_id: str = None,
    user_agent: str = None,
    title: str = None,
    ip_address: str = None,
    referer: str = None,
    query: typing.Dict = None,
) -> typing.Dict:
    payload = {
        "v": "1",  # Protocol Version
        "t": "pageview",  # Type
        "tid": tracking_id,  # TrackingID
        "cid": client_id,  # ClientId
        "dp": f"/images/{property_code}",  # Document Path
        "dt": title,  # Document title
        "ua": user_agent,  # User Agent
        "uip": ip_address,  # User IP
        "aip": 1,  # Anonymize IP
        "ds": "beaconator",  # Data Source,
        "property_code": property_code,
        "referer": referer,
    }

    # for key, value in query.items():
    #     payload[key] = value

    return payload


async def send_analytics_payload(
    ga_code: str,
    property_code: str,
    client_id: str,
    user_agent: str = None,
    title: str = None,
    ip_address: str = None,
    referer: str = None,
) -> None:
    payload = make_analytics_payload(
        tracking_id=ga_code,
        property_code=property_code,
        client_id=client_id,
        user_agent=user_agent,
        title=title,
        ip_address=ip_address,
        referer=referer,
    )
    await SingletonAiohttp.post_payload(beacon_url, payload)


async def on_start_up() -> None:
    models.Base.metadata.create_all(bind=engine)
    SingletonAiohttp.get_aiohttp_client()


async def on_shutdown() -> None:
    await SingletonAiohttp.close_aiohttp_client()


app = FastAPI(
    docs_url=None, redoc_url=None, on_startup=[on_start_up], on_shutdown=[on_shutdown]
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter()

SERVE_ADMIN = True

if SERVE_ADMIN:
    app.mount(
        "/admin",
        StaticFiles(
            directory="/Users/mfdeux/dev/projects/github.com/mfdeux/beaconator/beaconator/frontend/dist"  # noqa: E501
        ),
        name="admin",
    )


@app.get("/images/{property_code}")
async def get_image(
    property_code: str,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> FileResponse:
    property = dao.get_property_by_code(db, code=property_code)
    if property is None:
        raise HTTPException(status_code=404, detail="Requested image does not exist")
    if not property.active:
        raise HTTPException(status_code=404, detail="Requested image does not exist")

    try:
        image_resp = image_queries[property.image]
    except KeyError:
        image_resp = image_queries["other"]

    user_agent = request.headers.get("user-agent")
    referer = request.headers.get("referer")
    ip_address = request.client[0]
    if not request.cookies.get("cid"):
        cid = str(uuid.uuid4())
    else:
        cid = request.cookies.get("cid")

    response = FileResponse(
        static_file(image_resp["filename"]), media_type=image_resp["media_type"]
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
    response.headers["Expires"] = current_http_datetime()
    response.set_cookie("cid", cid, path="/", expires=60 * 60 * 24 * 365)

    background_tasks.add_task(
        send_analytics_payload,
        ga_code=property.ga_code.code,
        property_code=property.code,
        client_id=cid,
        user_agent=user_agent,
        title=property.image,
        ip_address=ip_address,
        referer=referer,
    )

    return response


@app.post("/api/login", response_model=schemas.AuthToken, tags=["api"])
async def post_login(item: schemas.Login) -> typing.Dict:
    """
    Login to the API and return JWT token
    """
    if item.password == TEMP_PASSWORD:
        return {"token": generate_jwt_token(JWT_SECRET)}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@api.get("/codes", response_model=typing.List[schemas.GACode])
async def get_ga_codes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):  # noqa: ANN201
    ga_codes = dao.get_ga_codes(db, skip=skip, limit=limit)
    return ga_codes


@api.post("/codes", response_model=schemas.GACode)
async def post_ga_code(
    item: schemas.GACodeChange, db: Session = Depends(get_db)
):  # noqa: ANN201
    return dao.create_ga_code(db=db, item=item)


@api.get("/codes/{code_id}", response_model=schemas.GACode)
async def get_ga_code(code_id: int, db: Session = Depends(get_db)):  # noqa: ANN201
    code = dao.get_ga_code(db, id=code_id)
    if code is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return code


@api.patch("/codes/{code_id}", response_model=schemas.GACode)
async def patch_ga_code(
    code_id: int, item: schemas.GACodeChange, db: Session = Depends(get_db)
):  # noqa: ANN201
    returned = dao.update_ga_code(db, id=code_id, item=item)
    if returned < 1:
        raise HTTPException(status_code=404, detail="Code not found")
    return dao.get_ga_code(db, id=code_id)


@api.delete("/codes/{code_id}", response_model=dict)
async def delete_ga_code(code_id: int, db: Session = Depends(get_db)):  # noqa: ANN201
    returned = dao.delete_ga_code(db, id=code_id)
    if returned < 1:
        raise HTTPException(status_code=404, detail="Code not found")
    return {"deleted": returned}


@api.get("/properties", response_model=typing.List[schemas.Property])
async def get_ga_properties(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):  # noqa: ANN201
    properties = dao.get_properties(db, skip=skip, limit=limit)
    return properties


@api.post("/properties", response_model=schemas.Property)
async def post_ga_property(
    item: schemas.PropertyChange, db: Session = Depends(get_db)
):  # noqa: ANN201
    return dao.create_property(db=db, item=item)


@api.get("/properties/{property_id}", response_model=schemas.Property)
async def get_ga_property(
    property_id: int, db: Session = Depends(get_db)
):  # noqa: ANN201
    property = dao.get_property(db, id=property_id)
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property


@api.patch("/properties/{property_id}", response_model=schemas.Property)
async def patch_ga_property(
    property_id: int, item: schemas.PropertyChange, db: Session = Depends(get_db)
):  # noqa: ANN201
    returned = dao.update_property(db, id=property_id, item=item)
    if returned < 1:
        raise HTTPException(status_code=404, detail="Property not found")
    return dao.get_property(db, id=property_id)


@api.delete("/properties/{property_id}", response_model=dict)
async def delete_ga_property(
    property_id: int, db: Session = Depends(get_db)
):  # noqa: ANN201
    returned = dao.delete_property(db, id=property_id)
    if returned < 1:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"deleted": returned}


@app.get("/api/other/images", tags=["api"])
async def get_images(type: typing.Optional[str] = "other") -> FileResponse:
    try:
        image_resp = image_queries[type]
    except KeyError:
        image_resp = image_queries["other"]

    return FileResponse(
        static_file(image_resp["filename"]), media_type=image_resp["media_type"]
    )


app.include_router(
    api, prefix="/api", tags=["api"], dependencies=[Depends(get_auth_token)]
)
