from __future__ import annotations

from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from ivelum_app.settings import settings
from ivelum_app.text_transform import add_trademark_to_six_letter_words


def _is_upstream_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc in {"", urlparse(settings.upstream_base_url).netloc}


def rewrite_links_to_proxy(html: str, current_path: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(["a", "link", "script", "img"]):
        attr = "href" if tag.name in {"a", "link"} else "src"
        value = tag.get(attr)
        if not value:
            continue

        absolute = urljoin(settings.upstream_base_url + "/", value)
        if not _is_upstream_url(absolute):
            continue

        absolute_parsed = urlparse(absolute)
        proxy_url = settings.proxy_base_url + absolute_parsed.path
        if absolute_parsed.query:
            proxy_url = f"{proxy_url}?{absolute_parsed.query}"
        tag[attr] = proxy_url

    # Transform visible text:
    for text_node in soup.find_all(string=True):
        if text_node.parent and text_node.parent.name in {"script", "style"}:
            continue
        transformed = add_trademark_to_six_letter_words(str(text_node))
        text_node.replace_with(transformed)

    return str(soup)

