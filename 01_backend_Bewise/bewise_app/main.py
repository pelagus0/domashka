from fastapi import FastAPI

from bewise_app.api import router
from bewise_app.db import Base, engine

# Import models so SQLAlchemy knows about them:
from bewise_app import models  # noqa: WPS433

app = FastAPI(title="Bewise quiz API")
app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)

