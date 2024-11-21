# VOCSET API Documentation

This document outlines the VOCSET API used to upload trade data directly into the application. Currently a very limited sub-set of the application features are available from the API - just those operations to handle trade data.

## Authentication & Authorisation

All endpoints are secured using an API key. Setting up an API Key can be managed from the VOCSET application, in your user profile.

When calling the API, the api key and api secret should be placed in the request headers. 

``` 
X-API-KEY: "api_key"
X-API-SECRET: "api_secret"
```

### Handling Trades

Each endpoint manipulates or displays information related to the User whose
Token is provided with the request:

* [Show Trades](trade/get.md) : `GET /api/trade`
* [Upload Trades](trade/put.md) : `PUT /api/trade`
