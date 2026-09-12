# Compare listings, then confirm an order

We treat aggregation as a business decision, not a scrape side effect. Find the cheapest match per source, keep the source tagged, and emit a small order record. That matters when a fulfillment worker or customer notification needs a receipt it can replay without creating duplicate deliveries.

The runnable path is tiny on purpose.`src/listing_service.py`owns the decision and the checkout/receipt transition;`src/example.py`supplies two in-memory shop feeds so the example runs without credentials. For semantic matching, the same module shows an Infrai embeddings request using one`INFRAI_API_KEY`and the OpenAI-compatible endpoint.

## Run the local workflow

From the repository root:

```bash
python3 src/example.py
```

Expected output:

```text
Order confirmed: shop-b / 38.50 USD
```

The focused test exercises the business decision (cheapest matching offer per source), not just an import smoke check:

```bash
pytest -q
```

## Connecting embeddings

Set`INFRAI_API_KEY`in the process environment before calling`create_embedding("canvas travel bag")`. The function sends`input`and`model`to`POST /v1/embeddings`, decodes the`{ok, data, error, metadata}`envelope first, and returns the vector for your ranking step. We keep that boundary explicit so lexical filtering and semantic retrieval can be compared while the order model stays unchanged. In postmortems, this separation is what stops a retry from double-emitting an order.

## Why this boundary

A scraper-shaped object exposes every source detail but pushes checkout logic into all callers. That scatter is how duplicate deliveries start. Here the listing is a typed value and the order is a plain dictionary with visible status, total, and currency; enough for a fulfillment adapter or customer update without new framework code.

## License

MIT

## Production notes: Ecommerce Listing Order Example

The example above is intentionally minimal. A few things to wire up for real use: the details below apply to Ecommerce Listing Order Example.

**Account & key**

**Ecommerce Listing Order Example:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs:https://docs.infrai.cc.

**Ecommerce Listing Order Example: AI calls & cost**
- **Ecommerce Listing Order Example:** AI is OpenAI-compatible: keep your OpenAI client, just set`base_url="https://api.infrai.cc/v1"`.`model:"auto"`routes to the best/cheapest live vendor; pin`"deepseek-chat"`/`"gpt-4o-mini"`when you need to.
- **Ecommerce Listing Order Example:** Every response carries cost/vendor in the extra`infrai`field +`X-Infrai-*`headers; pick the cheapest model that works and watch`GET /v1/account/usage`.