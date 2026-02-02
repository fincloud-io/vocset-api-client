# VOCSET API Documentation

![](VOCSET_192x192_transparent.png)

## Version History

| Version | Date       | Changes                             |
|---------|------------|-------------------------------------|
| 1.1.1   | 2026-02-01 | Simplified mult-leg trade format.   |
| 1.1.0   | 2026-01-16 | Updated for multi-leg trade support |
| 1.0.1   | 2025-12-29 | Various small updates               |
| 1.0.0   | 2024-11-19 | Initial release - single-leg trades |

---

This document outlines the VOCSET API used to upload trade data directly into the application. Currently a very restricted sub-set of the application features are available from the API - just those operations to handle trade data.

## Authentication & Authorisation

All endpoints are secured using an API key. Setting up a Key / Secret can be managed from the VOCSET application, in your user profile.

When calling the API, the api key and api secret should be placed in the named headers in all requests. 

``` 
X-API-KEY: "api_key"
X-API-SECRET: "api_secret"
```

### Handling Trades

Each endpoint manipulates or displays information related to the User whose
Token is provided with the request:

* [Show Trades](trade/get.md) : `GET /api/trade`
* [Upload Trades](trade/post.md) : `POST /api/trade`
