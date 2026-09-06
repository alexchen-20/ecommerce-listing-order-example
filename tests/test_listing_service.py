import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from listing_service import Listing, aggregate_listings


def test_aggregate_keeps_cheapest_match_from_each_source() -> None:
    sources = {
        "alpha": [Listing("alpha", "Canvas bag", 41, "USD"), Listing("alpha", "Canvas bag", 39, "USD")],
        "beta": [Listing("beta", "Canvas bag", 40, "USD")],
    }
    result = aggregate_listings("canvas", sources)
    assert [(item.source, item.price) for item in result] == [("alpha", 39), ("beta", 40)]
