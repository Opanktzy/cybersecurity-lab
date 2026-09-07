from fastapi import FastAPI

app = FastAPI(
    title="CyberLab Vulnerable API",
    description="An intentionally vulnerable API for security research in a local lab.",
    version="1.0.0",
)


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
users = [
    {
        "id": 1,
        "username": "alice",
        "role": "user",
    },
    {
        "id": 2,
        "username": "bob",
        "role": "user",
    },
    {
        "id": 3,
        "username": "admin",
        "role": "admin",
    },
]


@app.get("/users")
def get_users():
    return users
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

    return {
        "error": "User not found",
    }
