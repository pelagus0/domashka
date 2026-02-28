from fastapi import FastAPI

from mstroy_app.api import router
from mstroy_app.db import Base, engine

# Import models so SQLAlchemy knows about them:
from mstroy_app import models  # noqa: WPS433

app = FastAPI(title="MStroy TreeStore API")
app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)

