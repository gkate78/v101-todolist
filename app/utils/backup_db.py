#!/usr/bin/env python3
"""
Database Backup Script

This script creates a backup of the SQLite database with a timestamp.
It can be run manually or scheduled to run automatically.

Usage:
    python backup_db.py
"""

import os
import shutil
from datetime import datetime

# Database paths
DATABASE_DIR = os.getenv("DATABASE_DIR", "/app/data")
DATABASE_FILE = os.path.join(DATABASE_DIR, "database.db")
BACKUP_DIR = os.path.join(DATABASE_DIR, "backups")

def create_backup():
    """Create a timestamped backup of the database."""
    # Create backups directory if it doesn't exist
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Generate timestamp for backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"database_backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    # Check if database file exists
    if not os.path.exists(DATABASE_FILE):
        print(f"Error: Database file not found at {DATABASE_FILE}")
        return False
    
    try:
        # Copy database file to backup location
        shutil.copy2(DATABASE_FILE, backup_path)
        
        # Get file size
        file_size = os.path.getsize(backup_path)
        
        print(f"✅ Backup created successfully!")
        print(f"   Backup file: {backup_filename}")
        print(f"   Size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
        print(f"   Location: {backup_path}")
        
        # Clean up old backups (keep last 10)
        cleanup_old_backups()
        
        return True
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False

def cleanup_old_backups(keep=10):
    """Remove old backups, keeping only the most recent ones."""
    try:
        # Get all backup files
        backup_files = [
            os.path.join(BACKUP_DIR, f)
            for f in os.listdir(BACKUP_DIR)
            if f.startswith("database_backup_") and f.endswith(".db")
        ]
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Remove backups beyond the keep limit
        if len(backup_files) > keep:
            for old_backup in backup_files[keep:]:
                os.remove(old_backup)
                print(f"   🗑️  Removed old backup: {os.path.basename(old_backup)}")
    except Exception as e:
        print(f"   ⚠️  Warning: Could not clean up old backups: {e}")

if __name__ == "__main__":
    print("🔄 Starting database backup...")
    print(f"   Database: {DATABASE_FILE}")
    print(f"   Backup directory: {BACKUP_DIR}")
    print()
    
    success = create_backup()
    
    if success:
        print()
        print("✅ Backup completed successfully!")
    else:
        print()
        print("❌ Backup failed!")
        exit(1)

