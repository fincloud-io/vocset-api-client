# Rotate API Key

Allow a client holding a **valid** API key + secret to programmatically mint a
**new** key + secret without logging into the VOCSET GUI or entering a TOTP code.
The current credential is used to authenticate the request; on success the old
key/secret is **burned immediately** and the newly minted pair is returned in the
response.

This enables headless / server-to-server clients to renew their own credentials
before the 60-day expiry, replacing the previous GUI-only flow.

**URL** : `/api/auth/apiKey/rotate`

**Method** : `POST`

**Auth required** : YES — the *current* API key + secret (presented in the standard
headers). No JWT, session, or TOTP is required.

**Permissions required** : None (the credential authorises rotating **only itself**).

**Request headers**

```
X-API-KEY: "<current_api_key>"
X-API-SECRET: "<current_api_secret>"
```

**Request body** : None.

## Behaviour

* The presented key + secret are validated. If either is wrong the request is
  rejected with a generic authentication error (the response does **not** reveal
  which of the two was invalid).
* A new key and secret are generated using a secure random source:
  * `apiKey` — prefixed `vk_` (a non-secret handle)
  * `apiSecret` — prefixed `vs_` (128-bit key / 256-bit secret respectively)
* The `apiLabel` is preserved; the key creation date is reset to the time of
  rotation, restarting the 60-day validity period.
* The old credential stops authenticating **the instant the call commits** — there
  is no overlap window.
* A rotation notification email is sent to the key owner, and the rotation is
  recorded in the audit log (never the secret itself).

### Expiry grace period

A key may be rotated up to **7 days past** its 60-day expiry (configurable). Beyond
this grace window, rotation is refused and the key must be re-issued via the GUI
(session + TOTP) flow.

### Restrictions

* **Service accounts** cannot hold API keys and are refused rotation.
* **Inactive users** are refused rotation.

## Success Response

**Condition** : The presented key + secret are valid and within the (expiry + grace)
window.

**Code** : `200 OK`

**Headers** : `Cache-Control: no-store` is set so the secret is not cached by
intermediaries.

**Content example** :

```json
{
  "timestamp": "2026-07-21T17:16:12.424011385Z",
  "status": 200,
  "result": {
    "apiKey": "vk_8Qw3nR1tZ7yKpL0aB2cD4e",
    "apiSecret": "vs_Nf9Xk2Lp7Qw3nR1tZ7yKpL0aB2cD4eG6hJ8mN0oP2q",
    "apiLabel": "cron-uploader",
    "apiKeyCreationDate": "2026-07-21T17:16:12.424011385Z"
  },
  "path": "/api/auth/apiKey/rotate"
}
```

> **Important** : The response is the **only** copy of the new secret — it is
> returned once and cannot be retrieved again. Persist it before making any further
> calls. The old key/secret is invalid immediately, so the client must switch to the
> new pair for all subsequent requests.

## Error Response

**Condition** : Missing headers, or the presented key/secret is invalid (including a
credential that has already been burned by a previous rotation).

**Code** : `401 UNAUTHORIZED`

**Content example** :

```json
{
  "timestamp": "2026-07-21T17:16:12.424011385Z",
  "status": 401,
  "reason": "AUTHENTICATION_FAILED",
  "message": "Invalid API key or secret",
  "path": "/api/auth/apiKey/rotate"
}
```

## Error Response

**Condition** : The credential belongs to a service account or an inactive user.

**Code** : `403 FORBIDDEN`

**Content example** :

```json
{
  "timestamp": "2026-07-21T17:16:12.424011385Z",
  "status": 403,
  "reason": "ACTION_UNAUTHORIZED",
  "message": "Service accounts cannot hold API keys",
  "path": "/api/auth/apiKey/rotate"
}
```

## Error Response

**Condition** : The key has no creation date, or is expired beyond the rotation grace
window. The key must be re-issued via the GUI.

**Code** : `400 BAD REQUEST`

**Content example** :

```json
{
  "timestamp": "2026-07-21T17:16:12.424011385Z",
  "status": 400,
  "reason": "API_KEY_EXPIRED",
  "message": "API key expired beyond rotation grace",
  "path": "/api/auth/apiKey/rotate"
}
```

## Error Response

**Condition** : VOCSET encountered an unexpected / unhandled error while processing.

**Code** : `500 INTERNAL SERVER ERROR`

## Example

```bash
# Rotate -> 200 with new key/secret/creationDate
curl -sS -X POST https://api.vocset.net/api/auth/apiKey/rotate \
  -H "X-API-KEY: $OLD_KEY" \
  -H "X-API-SECRET: $OLD_SECRET"

# Old creds are now rejected on protected endpoints -> 401
curl -sS -o /dev/null -w "%{http_code}\n" https://api.vocset.net/api/trade \
  -H "X-API-KEY: $OLD_KEY" -H "X-API-SECRET: $OLD_SECRET"

# New creds authenticate -> 200
curl -sS -o /dev/null -w "%{http_code}\n" https://api.vocset.net/api/trade \
  -H "X-API-KEY: $NEW_KEY" -H "X-API-SECRET: $NEW_SECRET"
```

## Notes

* Rotation is **self-scoped**: a credential can only rotate itself and the new key
  inherits the same user, role, and privileges. There is no way to rotate another
  user's key.
* Concurrent rotations of the same key are **last-write-wins**; the losing caller is
  left holding a dead secret. Serialise rotations for a given key.
* If a client crashes after the server commits but before it stores the new secret,
  the old key is already burned and the new secret is lost — recover by re-issuing
  the key via the GUI (session + TOTP).
* Browser clients should not use API-key authentication; API keys are intended for
  server-to-server use.
</content>
</invoke>
