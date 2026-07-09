# Posts API - FastAPI Backend

A simple REST API built with FastAPI for students to practice API testing with Postman, now including a switchable token-auth demo.

## Requirements

```
pip install -r requirements.txt
```

## Run the Server

```
uvicorn main:app --reload
```

Server starts at: `http://127.0.0.1:8000`

## Swagger UI (Auto-generated Docs)

FastAPI automatically generates interactive API documentation.
Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

You can test all endpoints directly from the browser — no Postman needed. Note that `/docs` doesn't run the Postman pre-request scripts, so for protected endpoints you'll need to call `/login` first and paste the token in yourself (use the "Authorize" button).

## Auth Modes

`main.py` supports three interchangeable auth mechanisms, controlled by one line near the top of the file:

```python
AUTH_MODE = "jwt"  # "api_key" | "jwt" | "jwt_refresh"
```

Change it and restart the server (`--reload` picks it up automatically) to compare:

| Mode          | How it works                                                                 | Expiry                                                                 |
|---------------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| `api_key`     | Send header `X-API-Key: student-api-key-123` on every request.               | None — a static key doesn't expire on its own; you'd have to build rotation yourself. |
| `jwt`         | `POST /login` with username/password returns a signed access token.          | Baked into the token (`exp` claim) — stops working after 3 days automatically. |
| `jwt_refresh` | Same as `jwt`, plus `/login` also returns a long-lived refresh token.         | Access token expires after 3 days; `POST /token/refresh` trades the refresh token for a new one without re-sending credentials. Refresh token itself expires after 30 days. |

Demo credentials: `username: student`, `password: student123`.

**Important:** the Postman collection's `authMode` variable must match `AUTH_MODE` in `main.py` — they are two independent settings that both need to agree, since Postman has no way to see what mode the server is running in. See `STUDENT_GUIDE.md` for details.

## Endpoints

| Method | Endpoint          | Auth required        | Description                          |
|--------|-------------------|-----------------------|---------------------------------------|
| POST   | /login            | no                    | Get an access token (disabled in `api_key` mode) |
| POST   | /token/refresh    | no (needs refresh token) | Exchange a refresh token for a new access token (only in `jwt_refresh` mode) |
| GET    | /posts/{id}       | yes                   | Fetch a post by ID                   |
| POST   | /posts            | yes                   | Create a new post                    |
| PUT    | /posts/{id}       | yes                   | Update a post by ID                  |
| DELETE | /posts/{id}       | yes                   | Delete a post by ID                  |

## Notes

- Data is stored in memory — resets when the server restarts
- A default post with ID `1` is pre-loaded so GET works immediately
- `SECRET_KEY` in `main.py` is a hardcoded demo value — fine for local practice, never use it as-is in a real deployment
