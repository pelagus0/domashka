from fastapi import FastAPI

from appbooster_app.api import router
from appbooster_app.db import Base, engine

# Import models so SQLAlchemy knows about them:
from appbooster_app import models  # noqa: WPS433

app = FastAPI(title="AppBooster experiments API")
app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)

