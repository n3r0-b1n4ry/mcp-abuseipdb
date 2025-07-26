# Error Handling

HTTP status codes are the most reliable method of determining the status of the API response. After all, that is the sole purpose of the codes. When we encounter at least one application error, a JSON response with a collection of errors is returned. The structure conforms to the [JSON API spec](http://jsonapi.org/format/#errors):

At minimum, we will always include the the `detail` and `status` members. We may provide more members, as per the spec.

**Error Response:**

```
{
    "errors": [
        {
        "detail": "The max age in days must be between 1 and 365.",
        "status": 422
        }
    ]
}
```
