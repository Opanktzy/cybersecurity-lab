from fastapi import FastAPI, Header, HTTPException

app = FastAPI(
    title="CyberLab Vulnerable API",
    description="An intentionally vulnerable API for security research in a local lab.",
    version="1.0.0",
)

users = [
    {
        "id": 1,
        "username": "alice",
        "role": "user",
        "token": "alice-token",
    },
    {
        "id": 2,
        "username": "bob",
        "role": "user",
        "token": "bob-token",
    },
    {
        "id": 3,
        "username": "admin",
        "role": "admin",
        "token": "admin-token",
    },
]


@app.get("/")
def root():
    return {
        "message": "CyberLab Vulnerable API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/login")
def login(username: str):
    for user in users:
        if user["username"] == username:
            return {
                "message": "Login successful",
                "token": user["token"],
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid username",
    )


@app.get("/users")
def get_users():
    return [
        {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
        }
        for user in users
    ]


@app.get("/users/me")
def get_current_user(x_token: str = Header(...)):
    for user in users:
        if user["token"] == x_token:
            return {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid token",
    )


@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    x_token: str = Header(...),
):
    current_user = None

    for user in users:
        if user["token"] == x_token:
            current_user = user
            break

    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
 
    # Authorization check
    if current_user["id"] != user_id and current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

    for user in users:
        if user["id"] == user_id:
            return {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
            }

    raise HTTPException(
        status_code=404,
        detail="User not found",
    )
