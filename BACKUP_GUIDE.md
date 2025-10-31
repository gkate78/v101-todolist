# Database Backup Guide

## Automated Backups

The backup system creates timestamped copies of your SQLite database and stores them in the same Fly.io volume.

### Backup Scripts

- **`app/utils/backup_db.py`** - Creates a timestamped backup
- **`app/utils/restore_db.py`** - Restores from a backup

### Backup Location

Backups are stored in: `/app/data/backups/`

Format: `database_backup_YYYYMMDD_HHMMSS.db`

### Manual Backup

**Create a backup manually:**
```bash
fly ssh console --app v101-todolist -C "python /app/app/utils/backup_db.py"
```

**List available backups:**
```bash
fly ssh console --app v101-todolist -C "python /app/app/utils/restore_db.py"
```

**Restore from a backup:**
```bash
fly ssh console --app v101-todolist -C "python /app/app/utils/restore_db.py database_backup_20231101_020000.db"
```

### Automated Weekly Backups

Fly.io doesn't have built-in cron jobs, but you can set up automated backups using:

#### Option 1: GitHub Actions (Recommended)

A GitHub Actions workflow is already configured in `.github/workflows/backup.yml`.

**Setup:**
1. Go to your GitHub repository settings → Secrets → Actions
2. Add a secret: `FLY_API_TOKEN` (get token from `fly auth token`)
3. The workflow will run automatically every Sunday at 2 AM UTC
4. You can also trigger it manually from the Actions tab

**Manual trigger:**
- Go to Actions tab in GitHub
- Select "Weekly Database Backup" workflow
- Click "Run workflow"

#### Option 2: External Cron Service

Use services like:
- **cron-job.org** (free)
- **EasyCron** (free tier available)
- Your own server with cron

Set up a cron job that runs:
```bash
fly ssh console --app v101-todolist -C "python /app/app/utils/backup_db.py"
```

#### Option 3: Manual Weekly Reminder

Set a calendar reminder to run the backup command weekly.

### Backup Management

**View backups:**
```bash
fly ssh console --app v101-todolist -C "ls -lh /app/data/backups/"
```

**Download a backup to local machine:**
```bash
fly sftp get /app/data/backups/database_backup_20231101_020000.db backup.db --app v101-todolist
```

**Clean up old backups:**
The backup script automatically keeps the last 10 backups. To manually clean up:
```bash
fly ssh console --app v101-todolist -C "rm /app/data/backups/database_backup_OLD_DATE.db"
```

### Restore Process

1. **List available backups:**
   ```bash
   fly ssh console --app v101-todolist -C "python /app/app/utils/restore_db.py"
   ```

2. **Restore from backup:**
   ```bash
   fly ssh console --app v101-todolist -C "python /app/app/utils/restore_db.py database_backup_20231101_020000.db"
   ```

3. **Restart the app:**
   ```bash
   fly apps restart v101-todolist
   ```

### Important Notes

- Backups are stored in the same volume as the database
- The backup script automatically keeps the last 10 backups
- Each backup creates a timestamped copy
- Before restoring, the current database is automatically backed up as `pre_restore_TIMESTAMP.db`
- Backups persist across deployments (stored in volume)

### Testing the Backup

Test the backup system:

```bash
# Create a test backup
fly ssh console --app v101-todolist -C "python /app/app/utils/backup_db.py"

# Verify backup was created
fly ssh console --app v101-todolist -C "ls -lh /app/data/backups/"

# List backups
fly ssh console --app v101-todolist -C "python /app/app/utils/restore_db.py"
```

