# Upload Active Trades

Allow the user with valid API Key to upload their trades into the daily blotter, and
submit these to their clients.

**URL** : `/api/trade`

**Method** : `POST`

**Auth required** : YES (API Key)

**Permissions required** : None

**Data constraints**

```json
{
  "tradeID": "<MANDATORY>",
  "traceID": "<OPTIONAL>",
  "tradeDate": "YYYY-MM-DD <MANDATORY> cannot be in future",
  "side": "Buy|Sell <MANDATORY>",
  "quantity": "676 <MANDATORY> integer - limited to 32 digits - no decimals",
  "price": "2009 <MANDATORY> decimal - limited to 24 digits + 8 dps",
  "instrumentCode": "String <MANDATORY> contract code only, no maturity information",
  "maturity": "YYYY-MM-DD <MANDATORY>>",
  "strike": "Decimal <MANDATORY when assetClass=Option>",
  "optionType": "Call|Put <MANDATORY when assetClass=Option>",
  "mic": "String <MANDATORY>",
  "client": "String <MANDATORY>",
  "executingAccount": "String <OPTIONAL>",
  "executingBroker": "String <OPTIONAL> only necessary when firms need to use multiple broker codes",
  "productDescription": "String <OPTIONAL>>",
  "clearingAccount": "String <MANDATORY>",
  "clearingBroker": "String <MANDATORY>",
  "carryBroker": "String <OPTIONAL> only use when requested. Can be defaulted",
  "executionTime": "DateTime(ISO 8601) <MANDATORY> example: 2024-12-01T14:00:04-05:00",
  "giveupTime": "DateTime(ISO 8601) <OPTIONAL> example: 2024-12-01T14:01:00-05:00",
  "assetClass": "Future|Option <MANDATORY>"
}
```

Note for `Client, executingBroker, clearingBroker, executingAccount, clearingAccount` please
refer to the company codes visible in VOCSET gui.

**Data examples**

```json
[
  {
    "tradeID": "20241119-001",
    "tradeDate": "2024-11-19",
    "side": "Buy",
    "quantity": "676",
    "price": "2009",
    "instrumentCode": "CL",
    "maturity": "2024-12-01",
    "mic": "XNYM",
    "client": "CTCINC",
    "productDescription": "Brent Crude",
    "clearingAccount": "GC123",
    "clearingBroker": "DBAG",
    "executionTime": "2024-11-19T14:00:04-05:00",
    "giveupTime": "2024-11-19T14:01:00-05:00",
    "assetClass": "Future"
  },
  {
    "tradeID": "20241119-002",
    "tradeDate": "2024-11-19",
    "side": "Buy",
    "quantity": "47",
    "price": "1979",
    "instrumentCode": "NG",
    "maturity": "2024-12-01",
    "mic": "XNYM",
    "client": "CTCINC",
    "productDescription": "Natural Gas",
    "clearingAccount": "GC123",
    "clearingBroker": "DBAG",
    "executionTime": "2024-11-19T14:00:04-05:00",
    "giveupTime": "2024-11-19T14:01:00-05:00",
    "assetClass": "Future"
  },
  {
    "tradeID": "20241119-003",
    "tradeDate": "2024-11-19",
    "side": "Sell",
    "quantity": "1",
    "price": "77",
    "instrumentCode": "C",
    "maturity": "2025-03-01",
    "mic": "NDEX",
    "client": "CTCINC",
    "productDescription": "EUA Futures",
    "clearingAccount": "GC456",
    "clearingBroker": "DBAG",
    "executionTime": "2024-11-19T14:00:04-05:00",
    "giveupTime": "2024-11-19T14:01:00-05:00",
    "assetClass": "Future"
  },
  {
    "tradeID": "20241119-004",
    "tradeDate": "2024-11-19",
    "side": "Buy",
    "quantity": "50",
    "price": "50",
    "instrumentCode": "T",
    "maturity": "2025-03-01",
    "mic": "IFEU",
    "client": "CTCINC",
    "productDescription": "WTI Crude",
    "clearingAccount": "GC456",
    "clearingBroker": "DBAG",
    "executionTime": "2024-11-19T14:00:04-05:00",
    "giveupTime": "2024-11-19T14:01:00-05:00",
    "assetClass": "Future"
  },
  {
    "tradeID": "20241119-005",
    "tradeDate": "2024-11-19",
    "side": "Sell",
    "quantity": "1",
    "price": "100",
    "instrumentCode": "B",
    "maturity": "2025-06-01",
    "mic": "IFEU",
    "client": "CTCINC",
    "productDescription": "Brent Crude ICE",
    "clearingAccount": "GC123",
    "clearingBroker": "DBAG",
    "executionTime": "2024-11-19T14:00:04-05:00",
    "giveupTime": "2024-11-19T14:01:00-05:00",
    "assetClass": "Future"
  },
  {
    "tradeID": "20241119-006",
    "tradeDate": "2024-11-19",
    "side": "Sell",
    "quantity": "1",
    "price": "100",
    "instrumentCode": "B",
    "maturity": "2025-06-01",
    "strike": 100.1,
    "optionType": "Call",
    "mic": "IFEU",
    "client": "CTCINC",
    "productDescription": "Brent Crude ICE",
    "clearingAccount": "GC123",
    "clearingBroker": "DBAG",
    "executionTime": "2024-11-19T14:00:04-05:00",
    "giveupTime": "2024-11-19T14:01:00-05:00",
    "assetClass": "Option"
  }
]
```

## Success Responses

**Condition** : Data provided is valid and User is Authenticated.

**Code** : `200 OK` (response payload need to be examined for individual trade errors)

**Content example** : Response will reflect back the updated information. A
User with `id` of '1234' sets their name, passing `UAPP` header of 'ios1_2':

```json
{
  "timestamp": "2024-11-21T17:16:12.424011385Z",
  "status": 200,
  "result": [
    {
      "id": "20241119-001",
      "status": "OK",
      "message": ""
    },
    {
      "id": "20241119-002",
      "status": "OK",
      "message": ""
    },
    {
      "id": "20241119-003",
      "status": "OK",
      "message": ""
    },
    {
      "id": "20241119-004",
      "status": "OK",
      "message": ""
    },
    {
      "id": "20241119-005",
      "status": "OK",
      "message": ""
    },
    {
      "id": "20241119-006",
      "status": "OK",
      "message": ""
    }
  ],
  "path": "/api/trade"
}
```

## Success Response (Partial)

**Condition** : Data provided is correctly formatted but some trades may have invalid data

**Code** : `200 OK`

**Content example** :
```json
{
"timestamp": "2024-11-21T17:16:12.424011385Z",
"status": 200,
"result": [
    {
        "id": "20241119-001",
        "status": "ERROR",
        "message": "Trade ID [20241119-001] is not unique",
        "field": "tradeId",
        "value": "20241119-001"
    },
    {
        "id": "20241119-002",
        "status": "ERROR",
        "message": "Trade ID [20241119-002] is not unique",
        "field": "tradeId",
        "value": "20241119-002"
    },
    {
        "id": "20241119-006",
        "status": "OK",
        "message": ""
    }
  ]
}
```
## Notes

* Because some trades in the upload were valid, but the payload was formatted correctly,
  but some trades in the upload were correct, a partially successful upload is possible.
* In these instances, the return code will be 200, but the payload will indicate
  individual trade errors on the status field of each result element as indicated above.


## Error Response

**Condition** : Bad data has been supplied in the payload.

**Code** : `400 BAD REQUEST`


## Error Response

**Condition** : VOCSET encountered an unexpected / unhandled error while processing.

**Code** : `500 INTERNAL SERVER ERROR`
