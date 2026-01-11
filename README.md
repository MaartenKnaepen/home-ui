# Home Dashboard

A lightweight, secure homepage dashboard for your self-hosted services. Built with FastAPI, TailwindCSS, and Docker.

## Features

- 🔒 **Secure Authentication**: Password-protected access with HTTP-only signed cookies
- 🎨 **Modern UI**: Clean, responsive design using TailwindCSS
- ⚙️ **Easy Configuration**: Simple YAML file to define your services
- 🐳 **Docker Ready**: Includes Dockerfile and docker-compose.yml for easy deployment
- 🚀 **Lightweight**: Minimal dependencies, fast startup

## Quick Start

### Production Deployment (Git Pull & Run)

This is the recommended workflow for deploying on your server:

1. **Clone the repository on your server:**
   ```bash
   git clone <repository-url>
   cd home-ui
   ```

2. **Create your environment configuration:**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your secure password and secret key
   ```

   Generate a secure secret key:
   ```bash
   openssl rand -hex 32
   ```

3. **Edit `services.yaml`** to match your services (already configured with common services)

4. **Build and start the application:**
   ```bash
   docker-compose up -d --build
   ```

5. **Access the dashboard** at `http://localhost:8000`

6. **Configure Nginx** for SSO (see [Deployment with Single Sign-On](#deployment-with-single-sign-on-sso) section below)

### Local Development / Testing

1. **Clone or download this repository**

2. **Start with defaults** (password: `changeme`):
   ```bash
   docker-compose up -d
   ```

3. **Access the dashboard** at `http://localhost:8000`

### Manual Installation

1. **Install dependencies** (requires Python 3.10+):
   ```bash
   uv pip install -e .
   # or
   pip install -e .
   ```

2. **Set environment variables**:
   ```bash
   export DASHBOARD_PASSWORD=your_password
   export SECRET_KEY=your_secret_key
   ```

3. **Run the application**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Configuration

### Environment Variables

- `DASHBOARD_PASSWORD`: Password to access the dashboard (default: `changeme`)
- `SECRET_KEY`: Secret key for signing cookies (default: `change-this-to-a-random-string`)
- `CONFIG_PATH`: Path to services configuration file (default: `services.yaml`)

### Services Configuration

Edit `services.yaml` to add your services. Each service requires:

- `name`: Display name
- `url`: URL to the service
- `icon`: FontAwesome icon class (e.g., `fa-solid fa-tv`)
- `description`: (optional) Short description

**Example:**
```yaml
services:
  - name: Portainer
    url: https://portainer.yourdomain.com
    icon: fa-brands fa-docker
    description: Container Management
  
  - name: Home Assistant
    url: https://hass.yourdomain.com
    icon: fa-solid fa-house
    description: Home Automation
```

### Finding Icons

Browse available icons at [FontAwesome](https://fontawesome.com/icons). Use the full class name (e.g., `fa-solid fa-server`, `fa-brands fa-github`).

## Deployment with Single Sign-On (SSO)

This application supports **Single Sign-On** via Nginx's `auth_request` module. Once you log into the dashboard, you can access all protected services without re-authenticating.

### How SSO Works

1. **The Dashboard** acts as the authentication gatekeeper with the `/auth/verify` endpoint
2. **Nginx** intercepts requests to your services (Sonarr, Radarr, etc.) and checks authentication status
3. **If authenticated**: Request passes through to the service
4. **If not authenticated**: User is redirected to the login page

### Step-by-Step SSO Setup

#### 1. Deploy the Dashboard

Start the dashboard with Docker Compose:

```bash
docker-compose up -d
```

#### 2. Configure Nginx

Copy the provided `nginx-setup.conf` to your Nginx configuration:

```bash
sudo cp nginx-setup.conf /etc/nginx/sites-available/home
sudo ln -s /etc/nginx/sites-available/home /etc/nginx/sites-enabled/
```

**Important:** Edit the configuration file to:
- Change `home.yourdomain.com` to your actual domain
- Adjust service ports to match your Docker setup
- Configure SSL certificates (recommended: use Let's Encrypt)

Test and reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

#### 3. Configure Your Services

**CRITICAL:** Each service must be configured to work behind a reverse proxy with a base URL.

For **Sonarr** (repeat for each Sonarr/Radarr instance):

1. Open Sonarr web interface directly (e.g., `http://localhost:8989`)
2. Go to **Settings → General**
3. Set **URL Base**: `/sonarr-1080p` (or `/sonarr-4k` for 4K instance)
4. Set **Authentication**: `None` or `External` (Nginx handles auth now)
5. Click **Save** and restart the container:
   ```bash
   docker restart sonarr-1080p
   ```

For **Radarr**:
- Set **URL Base**: `/radarr-1080p` or `/radarr-4k`
- Set **Authentication**: `None` or `External`

For **Prowlarr**:
- Set **URL Base**: `/prowlarr`
- Set **Authentication**: `None` or `External`

For **qBittorrent**:
- Go to **Tools → Options → Web UI**
- Uncheck **Enable Host header validation** (required for reverse proxy)
- Under **Authentication**, you can disable it since Nginx protects access

For **Overseerr**:
- Set **URL Base**: `/overseerr` in Settings → General

For **Jellyfin**:
- Go to **Dashboard → Networking**
- Set **Base URL**: `/jellyfin`
- Set **Known proxies**: Your Nginx server IP (usually `172.x.x.x` for Docker)

#### 4. Update services.yaml

The provided `services.yaml` already uses relative URLs:

```yaml
services:
  - name: Sonarr (1080p)
    url: /sonarr-1080p
    icon: fa-solid fa-tv
    description: TV Series (Standard)
```

These URLs will work seamlessly with the Nginx configuration.

#### 5. Test the Setup

1. Visit `https://home.yourdomain.com`
2. Log in with your dashboard password
3. Click on any service - it should open **without asking for credentials**
4. In a private/incognito window, try accessing `https://home.yourdomain.com/sonarr-1080p` directly
   - You should be redirected to the login page

### Port Reference

Default ports used in `nginx-setup.conf` (adjust to match your setup):

| Service | Default Port | Nginx Location |
|---------|--------------|----------------|
| Home Dashboard | 8000 | `/` |
| Overseerr | 5055 | `/overseerr` |
| Jellyfin | 8096 | `/jellyfin` |
| Sonarr (1080p) | 8989 | `/sonarr-1080p` |
| Sonarr (4K) | 8990 | `/sonarr-4k` |
| Radarr (1080p) | 7878 | `/radarr-1080p` |
| Radarr (4K) | 7879 | `/radarr-4k` |
| Prowlarr | 9696 | `/prowlarr` |
| Qbittorrent | 8080 | `/qbit` |

### Troubleshooting SSO

**Service shows blank page or errors:**
- Make sure the service's Base URL matches the Nginx location
- Check that the service container is running: `docker ps`
- View service logs: `docker logs <container-name>`

**Authentication not working:**
- Test the auth endpoint directly: `curl -I http://localhost:8000/auth/verify` (should return 401)
- After logging in, test again with cookies to verify it returns 200
- Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`

**Service doesn't recognize the base URL:**
- Some services require a container restart after changing the base URL
- Make sure to save settings and restart: `docker restart <container-name>`

## Basic Nginx Setup (Without SSO)

If you prefer a simple reverse proxy without SSO, use this minimal configuration:

```nginx
server {
    listen 80;
    server_name home.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Security Notes

- Always change the default password in production
- Use a strong, random `SECRET_KEY` (generate with `openssl rand -hex 32`)
- Consider using HTTPS in production (Let's Encrypt recommended)
- The session cookie is valid for 7 days by default

## Development

The project follows these standards (see `AGENTS.md`):
- Python 3.10+ with modern type hints
- PEP 8 compliance
- FastAPI for web framework
- Pydantic for data validation
- TailwindCSS for styling

## License

MIT

## Support

For issues or questions, please open an issue on the repository.