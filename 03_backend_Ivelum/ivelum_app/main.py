from __future__ import annotations

from fastapi import FastAPI, Response
from sqlalchemy.orm import Session

import httpx

from ivelum_app.db import Base, SessionLocal, engine
from ivelum_app.html_proxy import rewrite_links_to_proxy
from ivelum_app.models import ProxyRequestLog
from ivelum_app.settings import settings

app = FastAPI(title="Ivelum HN proxy")


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


def _log_request(path: str) -> None:
    db_session: Session = SessionLocal()
    try:
        db_session.add(ProxyRequestLog(path=path))
        db_session.commit()
    finally:
        db_session.close()


@app.get("/{full_path:path}")
def proxy(full_path: str) -> Response:
    path = "/" + full_path
    _log_request(path)

    upstream_url = settings.upstream_base_url + path
    with httpx.Client() as client:
        upstream = client.get(upstream_url, timeout=20.0)

    content_type = upstream.headers.get("content-type", "")
    if "text/html" in content_type:
        html = upstream.text
        rewritten = rewrite_links_to_proxy(html, current_path=path)
        return Response(
            content=rewritten,
            status_code=upstream.status_code,
            media_type="text/html",
        )

    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        media_type=content_type or None,
    )

