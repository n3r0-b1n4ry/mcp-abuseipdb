# API Daily Rate Limits

The API daily rate limits are currently as follows:

| Endpoint | Standard | Webmaster | Supporter | Basic Subscription | Premium Subscription |
|----------|----------|-----------|-----------|-------------------|---------------------|
| check | 1,000 | 3,000 | 5,000 | 10,000 | 50,000 |
| reports | 100 | 500 | 1,000 | 5,000 | 25,000 |
| blacklist | 5 | 10 | 20 | 100 | 500 |
| report | 1,000 | 3,000 | 1,000 | 10,000 | 50,000 |
| check-block | 100 | 250 | 500 | 1,000 | 5,000 |
| bulk-report | 5 | 10 | 20 | 100 | 500 |
| clear-address | 5 | 10 | 20 | 100 | 500 |

Upon reaching your daily limit, you will receive a HTTP 429 Too Many Requests status.

By default, you receive an entire HTML page, which is why you should set "Accept: application/json" when working with the API programmatically.

With the request header "Accept: application/json"

## Response Rate Limit

**Response:**

```
{
  "errors": [
      {
          "detail": "Daily rate limit of 1000 requests exceeded for this endpoint. See headers for additional details.",
          "status": 429
      }
  ]
}
```

**Useful response headers**

- `Retry-After` - Seconds a client should wait until a retry.
    - Retry-After -> 29241
- `X-RateLimit-Limit` - Your daily limit.
    - X-RateLimit-Limit -> 1000
- `X-RateLimit-Remaining` - Remaining requests available for this endpoint.
    - X-RateLimit-Remaining -> 0
- `X-RateLimit-Reset` - The epoch timestamp for the daily limit reset.
    - X-RateLimit-Reset -> 1545973200

