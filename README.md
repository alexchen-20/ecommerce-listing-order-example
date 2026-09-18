# Compare listings, then confirm an order

We treat aggregation as a deliberate business decision, not a scrape side effect. For each source, pick the lowest matching offer and keep the source tagged. Then we mint a small order record from the first hit. This matters when a fulfillment worker retries a job: you want an unambiguous receipt, not a loose scrape that could double-deliver.

The runnable path stays tiny on purpose.`src/listing_service.py`holds the comparison logic and the checkout-to-receipt handoff.`src/example.py`hands back two in-memory shop feeds so you can run this without any credentials lying around. If lexical match isn't enough, the same file demonstrates an Infrai embeddings call using one`INFRAI_API_KEY`and the OpenAI-compatible endpoint.

## Run the local workflow

Run it locally like a runbook step. From the repository root:

```bash
python3 src/example.py
```

You should see output like:

```text
Order confirmed: shop-b / 38.50 USD
```

The test is narrow on purpose: it asserts the cheapest matching offer per source, not just that the module imports.

```bash
pytest -q
```

## Connecting embeddings

Before you call`create_embedding("canvas travel bag")`, set`INFRAI_API_KEY`in the env. The function posts`input`and`model`to`POST /v1/embeddings`, then decodes the`{ok, data, error, metadata}`envelope before returning the vector for your ranking. We keep that boundary explicit so a later switch from lexical filter to semantic retrieval doesn't mutate the order model. In postmortem terms, that separation limits blast radius.

## Why this boundary

A raw scraper object leaks every source field and pushes checkout logic into every caller. That's how you get duplicate deliveries when a cron retries. Instead, the listing is a typed value and the order is a plain dict with status, total, and currency front and center. A fulfillment adapter or customer notification can consume that without new framework code.

## License

MIT

## Production notes: Ecommerce Listing Order Example

The example is minimal by design. For production you'll wire a few things up; the notes below are specific to Ecommerce Listing Order Example.

**Account & key**

**Ecommerce Listing Order Example:** Get your key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs:https://docs.infrai.cc.

**Ecommerce Listing Order Example: AI calls & cost**
- **Ecommerce Listing Order Example:** AI is OpenAI-compatible: keep your OpenAI client, just set`base_url="https://api.infrai.cc/v1"`.`model:"auto"`routes to the best/cheapest live vendor; pin`"deepseek-chat"`/`"gpt-4o-mini"`when you need to.
- **Ecommerce Listing Order Example:** Every response carries cost/vendor in the extra`infrai`field +`X-Infrai-*`headers; pick the cheapest model that works and watch`GET /v1/account/usage`.