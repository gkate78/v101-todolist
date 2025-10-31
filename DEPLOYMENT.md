# Deployment Guide - Fly.io
## Deploying Your Todo List App to Production

This guide walks you through deploying your FastAPI application to Fly.io, making it accessible on the internet.

### Prerequisites

1. **Fly.io Account**: Sign up at [fly.io](https://fly.io)
2. **Fly CLI**: Install the Fly.io command-line tool
   ```bash
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   
   # Windows (using PowerShell)
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```
3. **GitHub Account**: Your code should be in a GitHub repository
4. **Docker**: Fly.io uses Docker (automatically handled, but good to understand)

### Step-by-Step Deployment

#### Step 1: Install Fly.io CLI

Make sure the Fly CLI is installed and authenticated:

```bash
# Login to Fly.io
fly auth login

# Verify you're logged in
fly auth whoami
```

#### Step 2: Initialize Fly.io App (First Time Only)

If this is the first time deploying this app:

```bash
# Initialize Fly.io in your project
fly launch --no-deploy

# Follow the prompts:
# - App name: v101-todolist (or your choice)
# - Region: Choose closest to you (e.g., sin for Singapore)
# - PostgreSQL: No (we're using SQLite)
# - Redis: No
# - Deploy now: No (we'll deploy from GitHub)
```

**Note:** The `fly.toml` file should already exist in your project. If Fly asks to overwrite it, choose "No" to keep our configured version.

#### Step 3: Create a Volume for Database Persistence

SQLite needs a persistent volume to store the database file across deployments:

```bash
# Create a 1GB volume (enough for SQLite)
fly volumes create todo_db --size 1 --region sin

# Replace "sin" with your chosen region if different
# The volume name "todo_db" matches the mount in fly.toml
```

#### Step 4: Configure Environment Variables

Set the database directory for production:

```bash
# Set environment variable to use the volume mount
fly secrets set DATABASE_DIR=/app/data
```

#### Step 5: Deploy from GitHub

Fly.io can automatically deploy from GitHub. Here's how:

**Option A: Connect GitHub Repository (Recommended)**

1. Go to [Fly.io Dashboard](https://fly.io/dashboard)
2. Select your app (or create new app)
3. Go to "Settings" → "GitHub"
4. Click "Connect GitHub Repository"
5. Authorize Fly.io to access your repositories
6. Select your repository (`VibecampAU/v101-todolist`)
7. Choose the branch (usually `main`)
8. Enable "Deploy on Push" (optional, auto-deploys on every push)

**Option B: Deploy via CLI from Local Machine**

If you prefer to deploy from your local machine:

```bash
# Make sure you're on the main branch
git checkout main

# Deploy to Fly.io
fly deploy

# This will:
# 1. Build the Docker image
# 2. Push to Fly.io registry
# 3. Deploy and start your app
```

#### Step 6: Verify Deployment

After deployment, check your app status:

```bash
# Check app status
fly status

# View logs (to see if it's running correctly)
fly logs

# Open your app in browser
fly open
```

### Understanding the Deployment Files

#### Dockerfile

The `Dockerfile` tells Docker how to build your application:
- Uses Python 3.12 base image
- Installs dependencies from `requirements.txt`
- Copies your code
- Creates data directory for database
- Runs uvicorn server on port 8000

#### fly.toml

The `fly.toml` configures Fly.io:
- App name and region
- HTTP service configuration
- Volume mount for database persistence
- Health checks
- Auto-start/stop machines (saves money when idle)

#### Volume Mount

The volume mount ensures your database persists:
```toml
[[mounts]]
  source = "todo_db"           # Volume name
  destination = "/app/data"   # Where it's mounted in container
```

### Post-Deployment

#### View Your App

```bash
# Get your app URL
fly info

# Open in browser
fly open
```

#### Monitor Your App

```bash
# View real-time logs
fly logs

# Check app status
fly status

# View app metrics
fly metrics
```

#### Update Your App

When you make changes:

1. **Push to GitHub** (if using GitHub deployment):
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```
   Fly.io will automatically deploy (if auto-deploy is enabled)

2. **Or deploy manually**:
   ```bash
   fly deploy
   ```

### Troubleshooting

#### App Won't Start

```bash
# Check logs for errors
fly logs

# Common issues:
# - Database initialization errors
# - Missing environment variables
# - Port configuration issues
```

#### Database Not Persisting

```bash
# Verify volume is attached
fly volumes list

# Check if volume mount is in fly.toml
# Verify DATABASE_DIR environment variable is set
```

#### Can't Connect to Database

```bash
# Check volume is mounted correctly
fly ssh console -C "ls -la /app/data"

# Verify database file exists
fly ssh console -C "ls -la /app/data/database.db"
```

### Important Notes

1. **Database Persistence**: The volume ensures your database survives deployments and restarts
2. **Environment Variables**: Use `fly secrets set` for sensitive data
3. **Scaling**: Fly.io can scale your app if needed (configure in fly.toml)
4. **Costs**: Free tier includes 3 shared VMs. The volume may have costs (check Fly.io pricing)

### Next Steps

- Add custom domain: `fly domains add yourdomain.com`
- Set up monitoring and alerts
- Configure backups (for production apps)
- Add CI/CD pipeline for automatic testing

### Quick Reference Commands

```bash
# Deploy
fly deploy

# View logs
fly logs

# Open app
fly open

# Check status
fly status

# SSH into container (for debugging)
fly ssh console

# View secrets
fly secrets list

# Set secret
fly secrets set KEY=value

# List volumes
fly volumes list

# View app info
fly info
```

---

**Happy Deploying!** 🚀

