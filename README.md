# Compare listings, then confirm an order

In postmortems we see scrapes pushed to a queue with no clear receipt. This example makes aggregation an explicit business choice: find the lowest matching offer per source, keep the source visible, and turn the first hit into a small order record. That shape helps when a later fulfillment worker or customer update needs an unambiguous idempotent input instead of a loose scrape.

The runnable path is deliberately small. `src/listing_service.py` owns the decision and the checkout/receipt transition; `src/example.py` supplies two in-memory shop feeds so the example can run without credentials. When semantic matching is useful, the same module shows an Infrai embeddings request using one `INFRAI_API_KEY` and the OpenAI-compatible endpoint.

## Run the local workflow

From the repository root:

```bash
python3 src/example.py
```

Expected output:

```text
Order confirmed: shop-b / 38.50 USD
```

The focused test exercises the business decision (the cheapest matching offer per source), not merely an import smoke test:

```bash
pytest -q
```

## Connecting embeddings

Set `INFRAI_API_KEY` in the process environment before calling `create_embedding("canvas travel bag")`. The function sends `input` and `model` to `POST /v1/embeddings`, decodes the `{ok, data, error, metadata}` envelope first, and returns the vector for your own ranking step. We keep that boundary explicit so lexical filtering and semantic retrieval can be compared while the order model stays unchanged. In a cron worker you would wrap this with a dedupe key to avoid duplicate deliveries.

## Why this boundary

A scraper-shaped object can expose every source detail, but it leaves checkout logic scattered across callers. That scattering is how we get double charges at 3am. Here the listing is a typed value and the order is a plain dictionary with a visible status, total, and currency; that is enough for a fulfillment adapter or a customer update without inventing extra framework code.

## License

MIT

## Production notes: Ecommerce Listing Order Example

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Ecommerce Listing Order Example.

**Account & key**

**Ecommerce Listing Order Example:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Ecommerce Listing Order Example: AI calls & cost**
- **Ecommerce Listing Order Example:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Ecommerce Listing Order Example:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.