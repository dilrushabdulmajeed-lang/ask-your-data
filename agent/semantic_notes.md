## Business notes

### Google Ads (paid search and display advertising)
- `ads_daily`: one row per date × campaign × ad group × device. Loaded daily, so the latest date moves; check `max(date)` when a question says "latest" or "recent". It is a ReplacingMergeTree, so read it with `FINAL` or use `ads_performance`.
- `campaigns`: campaign attributes (type, objective, market). `ads_performance` is a view joining both, the easiest source.
- Metrics: spend = sum(cost); ROAS = sum(conversion_value) / sum(cost); CPA = sum(cost) / sum(conversions);
  CTR = sum(clicks) / sum(impressions); CPC = sum(cost) / sum(clicks); conversion rate = sum(conversions) / sum(clicks).
  Always compute ratios from sums, never by averaging daily ratios.
- "Search | Lead Gen | Qatar" records no conversion value, so its ROAS is 0 by design.

### E-commerce store (GCC electronics, 15 Oct 2025 – 15 Oct 2026)
- `ecom_events`: one row per event; `event_type` is one of view_product, add_to_cart, begin_checkout, purchase. A session (`session_id`) is one visit.
- `ecom_orders`: one row per order; `revenue` is the amount paid after discount (AED).
- `ecom_users`: every visitor (not only buyers), with first visit date and acquisition channel. Customers are users with at least one order.
- `ecom_rfm`: one row per customer with recency (days), frequency (orders), monetary (AED spend), 1–5 scores and a segment
  (Champions, Loyal, New / Promising, Needs Attention, At Risk, Lost).
- Repeat purchase rate = share of customers with more than one order. AOV = revenue / orders.

### A/B test: mobile checkout redesign (7 Sep – 4 Oct 2026)
- `ab_checkout_experiment`: one row per user assigned to `control` or `treatment` among mobile users who started checkout.
  `completed` = 1 if they finished checkout; `revenue` is the order value (0 if not completed).
- Known data-quality issue: some assignments were logged twice (exact duplicate rows). Count users with `uniqExact(user_id)`
  or deduplicate (`SELECT DISTINCT *`) before computing rates.

### Not in the data
No costs of goods or profit, no inventory, no customer names, emails, phone numbers or demographics, no non-Google ad
platform spend, and nothing before October 2025.
