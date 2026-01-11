# Home Dashboard

A lightweight, secure homepage dashboard for your self-hosted services. Built with FastAPI, TailwindCSS, and Docker.

## Features

- 🔒 **Secure Authentication**: Password-protected access with HTTP-only signed cookies
- 🎨 **Modern UI**: Clean, responsive design using TailwindCSS
- ⚙️ **Easy Configuration**: Simple YAML file to define your services
- 🐳 **Docker Ready**: Includes Dockerfile and docker-compose.yml for easy deployment
- 🚀 **Lightweight**: Minimal dependencies, fast startup

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone or download this repository**

2. **Edit `services.yaml`** to add your services:
   ```yaml
   services:
     - name: Sonarr
       url: https://sonarr.yourdomain.com
       icon: fa-solid fa-tv
       description: TV Series Management
   ```

3. **Set your password** in `docker-compose.yml`:
   ```yaml
   environment:
     - DASHBOARD_PASSWORD=your_secure_password_here
     - SECRET_KEY=generate_a_random_string_here
   ```

4. **Start the application**:
   ```bash
   docker-compose up -d
   ```

5. **Access the dashboard** at `http://localhost:8000`

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

## Nginx Reverse Proxy

Example Nginx configuration:

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