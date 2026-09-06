from listing_service import Listing, aggregate_listings, checkout, receipt


def main() -> None:
    sources = {
        "shop-a": [Listing("shop-a", "Canvas travel bag", 42.0, "USD")],
        "shop-b": [Listing("shop-b", "Canvas travel bag", 38.5, "USD")],
    }
    choices = aggregate_listings("canvas", sources)
    order = checkout(choices[0])
    print(receipt(order))


if __name__ == "__main__":
    main()
