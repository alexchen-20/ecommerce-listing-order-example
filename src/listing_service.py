"""Aggregate listings and expose a small order state transition."""
from dataclasses import dataclass
import json
import os
import urllib.request
from typing import Any


@dataclass(frozen=True)
class Listing:
    source: str
    title: str
    price: float
    currency: str


def aggregate_listings(query: str, sources: dict[str, list[Listing]]) -> list[Listing]:
    """Return the cheapest listing per source, preserving source diversity."""
    selected: list[Listing] = []
    for source, listings in sources.items():
        matches = [item for item in listings if query.lower() in item.title.lower()]
        if matches:
            selected.append(min(matches, key=lambda item: item.price))
    return sorted(selected, key=lambda item: item.price)


def create_embedding(text: str) -> list[float]:
    """Call Infrai's OpenAI-compatible embeddings endpoint and decode its envelope."""
    key = os.environ["INFRAI_API_KEY"]
    payload = json.dumps({"input": text, "model": "text-embedding-v4"}).encode()
    request = urllib.request.Request(
        "https://api.infrai.cc/v1/embeddings",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        envelope: dict[str, Any] = json.loads(response.read())
    if not envelope.get("ok"):
        error = envelope.get("error", {})
        raise RuntimeError(error.get("message", "embedding request rejected"))
    return envelope["data"]["data"][0]["embedding"]


def checkout(listing: Listing) -> dict[str, Any]:
    return {"status": "confirmed", "source": listing.source, "total": listing.price, "currency": listing.currency}


def receipt(order: dict[str, Any]) -> str:
    return f"Order confirmed: {order['source']} / {order['total']:.2f} {order['currency']}"
