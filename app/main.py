import logging
from fastapi import FastAPI, Request, Response, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeTimedSerializer, BadSignature
from app.config import Settings, load_services

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Home Dashboard")

# Initialize templates
templates = Jinja2Templates(directory="app/templates")

# Load settings
settings = Settings()

# Initialize serializer for secure cookies
serializer = URLSafeTimedSerializer(settings.secret_key)

COOKIE_NAME = "session"


def get_current_user(request: Request) -> str | None:
    """Dependency to check if user is authenticated via signed cookie."""
    cookie_value = request.cookies.get(COOKIE_NAME)
    if not cookie_value:
        return None
    
    try:
        # Verify and decode the signed cookie
        username = serializer.loads(cookie_value, max_age=86400 * 7)  # 7 days
        return username
    except BadSignature:
        return None


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render the login page."""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, password: str = Form(...)):
    """Handle login form submission."""
    if password == settings.dashboard_password:
        # Create signed cookie
        token = serializer.dumps("user")
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            httponly=True,
            max_age=86400 * 7,  # 7 days
            samesite="lax"
        )
        return response
    else:
        # Log failed login attempt for security monitoring
        logger.warning(f"Failed login attempt from {request.client.host}")
        # Return to login page with error
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid password"},
            status_code=401
        )


@app.get("/logout")
async def logout():
    """Clear session and redirect to login."""
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(COOKIE_NAME)
    return response


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, user: str | None = Depends(get_current_user)):
    """Render the dashboard page (requires authentication)."""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    # Load services from configuration
    services = load_services(settings.config_path)
    
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "services": services}
    )


@app.get("/auth/verify")
@app.head("/auth/verify")
async def auth_verify(request: Request, user: str | None = Depends(get_current_user)):
    """
    Auth verification endpoint for Nginx auth_request.
    Returns 200 if authenticated, 401 if not.
    """
    if user:
        return Response(status_code=200)
    else:
        return Response(status_code=401)


@app.get("/favicon.ico", include_in_schema=False)
@app.head("/favicon.ico", include_in_schema=False)
async def favicon():
    """Return empty response for favicon to avoid 404 errors in logs."""
    return Response(status_code=204)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
