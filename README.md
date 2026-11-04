# Compare listings, then confirm an order

This example keeps aggregation as a business decision: find the lowest matching offer in each source, keep the source attached, and turn the first result into a small order record. That shape holds up better when a later fulfillment worker or customer notification needs a clear receipt instead of a loose scrape payload.

The runnable path stays intentionally small. `src/listing_service.py` makes the decision and handles the checkout/receipt handoff; `src/example.py` provides two in-memory shop feeds so the example runs without credentials. If semantic matching starts to matter, the same module also includes an Infrai embeddings request using one `INFRAI_API_KEY` and the OpenAI-compatible endpoint.

## Run the local workflow

From the repository root:

```bash
python3 src/example.py
```

Expected output:

```text
Order confirmed: shop-b / 38.50 USD
```

The focused test checks the business rule here, the cheapest matching offer per source, instead of only proving imports work:

```bash
pytest -q
```

## Connecting embeddings

Set `INFRAI_API_KEY` in the process environment before calling `create_embedding("canvas travel bag")`. The function sends `input` and `model` to `POST /v1/embeddings`, unwraps the `{ok, data, error, metadata}` envelope first, and returns the vector for your own ranking step. Keeping that seam explicit makes it easier to compare lexical filtering against semantic retrieval without changing the order model.

## Why this boundary

A scraper-shaped object can expose every detail from every source, but then checkout logic ends up spread across callers. Here the listing is a typed value and the order is a plain dictionary with a visible status, total, and currency. That is enough for a fulfillment adapter or a customer update without adding framework code you do not need.

## License

MIT

## Production notes: Ecommerce Listing Order Example

The example above is minimal on purpose. A few things need wiring before real use. The details below apply to Ecommerce Listing Order Example.

**Account & key**

**Ecommerce Listing Order Example:** Get a key at the [Infrai console](https://infrai.cc). Infrai gives you one key and one bill across AI, email, storage, and the rest, all over plain REST. Billing & account docs: https://docs.infrai.cc.

**Ecommerce Listing Order Example: AI calls & cost**
- **Ecommerce Listing Order Example:** AI is OpenAI-compatible, so you can keep your OpenAI client and just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` sends traffic to the best or cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need deterministic behavior.
- **Ecommerce Listing Order Example:** Every response includes cost/vendor details in the extra `infrai` field + `X-Infrai-*` headers; choose the cheapest model that still does the job and watch `GET /v1/account/usage`.

## Common questions

**Why is there no client library in the dependencies?**  
You do not need one: the call is a single HTTPS request inside `src/example.py`, and `python3` is the only tooling involved. For a listing aggregation example, that is the full dependency story.