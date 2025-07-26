# REPORT Endpoint

Reporting IP addresses is the core feature of AbuseIPDB. When you report what you observe, everyone benefits, including yourself. To report an IP address, send a POST request. At least one category is required, but you may add additional categories using commas to separate the integer IDs. Related details can be included in the comment field.

> ⚠️ STRIP ANY PERSONALLY IDENTIFIABLE INFORMATION (PII); WE ARE NOT RESPONSIBLE FOR PII YOU REVEAL.

In the body, we get the updated abuseConfidenceScore.

## Report Parameters

| Field | Default | Restrictions | Description |
|-------|---------|-------------|-------------|
| ip | required | | A valid IPv4 or IPv6 address. |
| categories | required | 30 | Comma separated values; Reference |
| comment | | | A descriptive text of the attack i.e. server logs, port numbers, etc. |
| timestamp | current time | | ISO 8601 datetime of the attack or earliest observance of attack. |

## Example Request

**POST the submission.**

```
curl https://api.abuseipdb.com/api/v2/report \
--data-urlencode "ip=127.0.0.1" \
-d categories=18,22 \
--data-urlencode "comment=SSH login attempts with user root." \
--data-urlencode "timestamp=2023-10-18T11:25:11-04:00" \
-H "Key: YOUR_OWN_API_KEY" \
-H "Accept: application/json"
```

**Response:**

```
{
  "data": {
    "ipAddress": "127.0.0.1",
    "abuseConfidenceScore": 52
  }
}
```

