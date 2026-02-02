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

Details of a `CalendarSpread` multi-leg trade on `IFEU` exchange.

```json
[{
  "tradeID": "ML-20250116-001",
  "userID": "jj@java2go.com",
  "strategyName": "CalendarSpread",
  "side": "Buy",
  "quantity": 10,
  "price": 0.00000000,
  "tradeDate": "2025-01-16",
  "currency": "USD",
  "mic": "IFEU",
  "assetClass": "Future",
  "instrumentCode": "B",
  "instrumentCodeType": "Ticker",
  "optionType": "None",
  "maturity": "2025-03-01",
  "client": "CTCLTD",
  "executingBroker": "DBAG",
  "executingAccount": "",
  "clearingBroker": "DBAG",
  "clearingAccount": "GC123",
  "executionTime": "2025-01-16T10:00:00Z",
  "reportedTime": "2025-01-16T10:00:01.123456Z",
  "legs": [
    {
      "tradeID": "ML-20250116-001-L1",
      "side": "Buy",
      "quantity": 10,
      "price": 76.00000000,
      "mic": "IFEU",
      "assetClass": "Future",
      "instrumentCode": "B",
      "maturity": "2025-03-01",
      "executionTime": "2025-01-16T10:00:00Z"
    },
    {
      "tradeID": "ML-20250116-001-L2",
      "side": "Sell",
      "quantity": 10,
      "price": 75.50000000,
      "mic": "IFEU",
      "assetClass": "Future",
      "instrumentCode": "B",
      "maturity": "2025-04-01",
      "executionTime": "2025-01-16T10:00:00Z"
    }
  ]
}]
```

Details of a `Butterfly` options multi-leg trade on `IFEU` exchange.

```json
[{
  "tradeID": "ML-20250116-003",
  "userID": "jj@java2go.com",
  "strategyName": "Butterfly",
  "side": "Buy",
  "quantity": 10,
  "price": 0.00000000,
  "tradeDate": "2025-01-16",
  "currency": "USD",
  "mic": "IFEU",
  "assetClass": "Option",
  "instrumentCode": "B",
  "instrumentCodeType": "Ticker",
  "strike": 75.00,
  "optionType": "Call",
  "maturity": "2025-06-01",
  "client": "CTCLTD",
  "executingBroker": "DBAG",
  "executingAccount": "",
  "clearingBroker": "DBAG",
  "clearingAccount": "GC123",
  "executionTime": "2025-01-16T10:00:00Z",
  "reportedTime": "2025-01-16T10:00:01.123456Z",
  "legs": [
    {
      "tradeID": "ML-20250116-003-L1",
      "side": "Buy",
      "quantity": 10,
      "price": 5.00000000,
      "mic": "IFEU",
      "assetClass": "Option",
      "instrumentCode": "B",
      "maturity": "2025-06-01",
      "strike": 70.00,
      "optionType": "Call",
      "executionTime": "2025-01-16T10:00:00Z"
    },
    {
      "tradeID": "ML-20250116-003-L2",
      "side": "Sell",
      "quantity": 20,
      "price": 3.00000000,
      "mic": "IFEU",
      "assetClass": "Option",
      "instrumentCode": "B",
      "maturity": "2025-06-01",
      "strike": 75.00,
      "optionType": "Call",
      "executionTime": "2025-01-16T10:00:00Z"
    },
    {
      "tradeID": "ML-20250116-003-L3",
      "side": "Buy",
      "quantity": 10,
      "price": 1.50000000,
      "mic": "IFEU",
      "assetClass": "Option",
      "instrumentCode": "B",
      "maturity": "2025-06-01",
      "strike": 80.00,
      "optionType": "Call",
      "executionTime": "2025-01-16T10:00:00Z"
    }
  ]
}]
```

## Notes

* The fields `strike` and `optionType` are only returned for `Option` trades.
* Multi-leg trades include a `strategyName` field and a `legs` array containing individual leg trades.
* Legs inherit `client`, `tradeDate`, `clearingBroker`, `clearingAccount`, `executingBroker`, and `executingAccount` from the parent trade.
