# Show Active Trades

Gets an `Array` of `Trade` objects representing the currently active trades in the blotter
for the API key owner's company.

**URL** : `/api/trades`

**Method** : `GET`

**Auth required** : YES (API Key)

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

Details of a `Futures` trade on `IFEU` exchange.

```json
[{
  "tradeID": "20241119-005",
  "userID": "jj@java2go.com",
  "side": "Sell",
  "quantity": 1,
  "price": 100.00000000,
  "tradeDate": "2024-11-19",
  "currency": "USD",
  "mic": "IFEU",
  "assetClass": "Future",
  "instrumentCode": "B",
  "instrumentCodeType": "Ticker",
  "optionType": "None",
  "maturity": "2025-06-01",
  "client": "CTCINC",
  "executingBroker": "JJFUTLTD",
  "executingAccount": "",
  "clearingBroker": "DBAG",
  "clearingAccount": "GC123",
  "executionTime": "2024-11-19T23:33:00.895319Z",
  "reportedTime": "2024-11-19T23:33:01.492583Z"
}]
```

Details of an `Option` trade on `XNYM` exchange.

```json
[{
  "tradeID": "119934867",
  "userID": "jj@java2go.com",
  "side": "Sell",
  "quantity": 200,
  "price": 0.09600000,
  "tradeDate": "2024-10-27",
  "currency": "USD",
  "mic": "XNYM",
  "assetClass": "Option",
  "instrumentCode": "ON",
  "instrumentCodeType": "Ticker",
  "strike": 3.20,
  "optionType": "Call",
  "maturity": "2024-12-01",
  "client": "CTCINC",
  "executingBroker": "JJFUTLTD",
  "executingAccount": "",
  "clearingBroker": "JPMLLC",
  "clearingAccount": "CTC123",
  "executionTime": "2024-10-27T13:27:33Z",
  "giveupTime": "2024-10-28T13:32:01Z",
  "reportedTime": "2024-10-31T14:54:07.630565Z"
}]
```

## Notes

* The fields `strike` and `optionType` are only returned for `Option` orders.

