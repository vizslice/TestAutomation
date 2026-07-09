# Student Guide - Testing the Posts API with Postman

## Step 1 - Start the Server

Make sure you have the dependencies installed:

```
pip install -r requirements.txt
```

Then run:

```
uvicorn main:app --reload
```

You should see: `Uvicorn running on http://127.0.0.1:8000`

---

## Step 2 - Set Up Postman Environment

1. Open Postman
2. Click **Environments** → **Add**
3. Name it `Local API`
4. Add a variable:
   - Key: `baseUrl`
   - Value: `http://127.0.0.1:8000`
5. Save and select `Local API` as the active environment

---

## Step 3 - Import the Collection

1. Click **Import** in Postman
2. Select `postman_collection.json`
3. Run each request in order (0 → 5)

---

## Step 4 - Explore Swagger UI

FastAPI generates interactive docs automatically.
Open your browser and visit:

```
http://127.0.0.1:8000/docs
```

From here you can:
- See all available endpoints
- Send requests directly from the browser
- View request/response schemas

---

## Step 5 - Understand the Auth Settings

There are two independent switches, one in each project, and they must agree with each other:

| Setting | Where | Values | What it controls |
|---|---|---|---|
| `AUTH_MODE` | `main.py`, near the top | `api_key` / `jwt` / `jwt_refresh` | Which auth mechanism the server actually enforces |
| `authMode` | Postman collection variable | `api_key` / `jwt` / `jwt_refresh` | Which auth mechanism the collection's scripts *assume* the server is using |
| `autoRefresh` | Postman collection variable | `true` / `false` | Whether Postman silently gets you a new token when the old one expires, or just lets requests fail |

To try a different combination: change `AUTH_MODE` in `main.py`, save (the server reloads itself), then open the collection's variables tab in Postman and set `authMode` to match. No script edits needed — the same collection handles all 3 x 2 = 6 combinations.

### The three `AUTH_MODE` options

**`api_key`** - simplest possible auth. Every request needs header `X-API-Key: student-api-key-123`. There's no `/login` step (it returns 404) and no concept of expiry — the key is valid forever until you change it in the code. This is the easiest to reason about but the weakest to demonstrate expiry behavior with.

**`jwt`** - run `0. Login - Get Token` with `username: student`, `password: student123`. You get back a signed token good for **3 days** (`ACCESS_TOKEN_EXPIRE_DAYS` in `main.py`). Every protected request sends `Authorization: Bearer <token>`. When the 3 days are up, the token itself becomes invalid — the server doesn't need to track anything, it just checks the `exp` field packed inside the token.

**`jwt_refresh`** - same as `jwt`, but `0. Login - Get Token` also returns a `refresh_token` valid for 30 days. When the access token expires, you don't need to log in again with a username/password — instead call `0b. Refresh Token`, which trades the refresh token for a brand-new 3-day access token. This mirrors how most real-world APIs (OAuth2-style) actually work.

### The two `autoRefresh` strategies

**`autoRefresh = true`** (automatic) - the collection's pre-request script checks the stored token's expiry before every request. If it's missing or expired, the script quietly calls `/login` (or `/token/refresh` in `jwt_refresh` mode) *before* sending your actual request, and stores the new token. You never see a 401 for an expired token — it just works. This is realistic client behavior but hides what's happening under the hood.

**`autoRefresh = false`** (manual) - nothing runs automatically. Once your token expires, every protected request returns `401 Unauthorized`, and the console prints a hint telling you to run `0. Login - Get Token` (or `0b. Refresh Token`) yourself before retrying. This is more tedious but makes the expiry/401/re-auth cycle explicit and easy to observe.

---

## What Actually Happens When the Token Expires Every 3rd Day

This is the scenario the whole demo is built around. Assume `AUTH_MODE = "jwt"` (or `jwt_refresh`) and you logged in on Day 0.

1. **Day 0-2:** `accessToken` is valid. Every request the collection sends includes it and gets a normal `200`/`201` response.
2. **Day 3, first request after expiry:** the token's `exp` claim is now in the past. FastAPI's token check rejects it with `401 Unauthorized`, `{"detail": "Token has expired, please login again"}`. The server never "pushes" this to you — it only notices when the next request arrives carrying the stale token.
3. **What happens next depends on `autoRefresh`:**
   - **`true`:** you never actually see that 401. Before the request was even sent, the pre-request script noticed `Date.now() >= accessTokenExpiry`, silently fetched a new token (via `/login` or `/token/refresh`), and attached the new one. The request that goes out over the wire already carries a valid token.
   - **`false`:** the 401 above is exactly what you see in the response, plus a console warning. You then manually run `0. Login - Get Token` (or `0b. Refresh Token` in `jwt_refresh` mode) to get a fresh token, and re-run the request that failed.
4. **`jwt` vs `jwt_refresh` on expiry day:** in plain `jwt` mode, recovering means sending username/password again (a full login). In `jwt_refresh` mode, recovering means sending the still-valid refresh token (no password needed) — that's the main practical benefit of the refresh-token pattern, and it's why real APIs use it: the short-lived access token limits damage if it leaks, while the refresh token avoids repeatedly transmitting the password.
5. **`api_key` mode has none of this** - there's no expiry, so nothing changes on day 3. That contrast is the point: static keys are simple but don't expire on their own, while JWTs enforce their own expiry without any server-side bookkeeping.

---

## Expected Results

| Request                              | Expected Status |
|---------------------------------------|-----------------|
| POST /login (api_key mode)            | 404 Not Found   |
| POST /login (jwt / jwt_refresh mode)  | 200 OK          |
| POST /token/refresh (jwt_refresh mode)| 200 OK          |
| POST /token/refresh (other modes)     | 404 Not Found   |
| GET /posts/1 (valid/attached token)   | 200 OK          |
| GET /posts/1 (missing/expired token)  | 401 Unauthorized|
| POST /posts                           | 201 Created     |
| PUT /posts/1                          | 200 OK          |
| DELETE /posts/1                       | 200 OK          |
| GET /posts/{non-existent-id}          | 404 Not Found   |

---

## Common Issues

**Server not running**
Make sure `uvicorn main:app --reload` is running in your terminal before sending requests.

**baseUrl not set**
Make sure you selected the `Local API` environment in Postman.

**Every protected request returns 401**
Check that `authMode` in the Postman collection variables matches `AUTH_MODE` in `main.py`. If they're both `jwt`/`jwt_refresh`, run `0. Login - Get Token` first — the token variables start out empty.

**404 on PUT or DELETE**
Post with ID 1 is deleted after the DELETE request. Restart the server to reset the data.

**`0b. Refresh Token` returns 404**
That's expected outside `jwt_refresh` mode — refresh tokens only exist in that mode.
