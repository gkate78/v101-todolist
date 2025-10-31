#!/usr/bin/env python3
"""
Database Restore Script

This script restores the SQLite database from a backup file.

Usage:
    python restore_db.py [backup_filename]
    
    If no backup filename is provided, it will list available backups.
"""

import os
import shutil
import sys
from datetime import datetime

# Database paths
DATABASE_DIR = os.getenv("DATABASE_DIR", "/app/data")
DATABASE_FILE = os.path.join(DATABASE_DIR, "database.db")
BACKUP_DIR = os.path.join(DATABASE_DIR, "backups")

def list_backups():
    """List all available backup files."""
    try:
        if not os.path.exists(BACKUP_DIR):
            print("❌ No backups directory found.")
            return []
        
        backup_files = [
            f for f in os.listdir(BACKUP_DIR)
            if f.startswith("database_backup_") and f.endswith(".db")
        ]
        
        if not backup_files:
            print("❌ No backup files found.")
            return []
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: os.path.getmtime(os.path.join(BACKUP_DIR, x)), reverse=True)
        
        print("📦 Available backups:")
        print()
        for i, backup_file in enumerate(backup_files, 1):
            backup_path = os.path.join(BACKUP_DIR, backup_file)
            file_size = os.path.getsize(backup_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(backup_path))
            print(f"   {i}. {backup_file}")
            print(f"      Size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
            print(f"      Created: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
        
        return backup_files
    except Exception as e:
        print(f"❌ Error listing backups: {e}")
        return []

def restore_backup(backup_filename):
    """Restore database from a backup file."""
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    # Check if backup file exists
    if not os.path.exists(backup_path):
        print(f"❌ Error: Backup file not found at {backup_path}")
        return False
    
    # Create a backup of current database before restoring
    if os.path.exists(DATABASE_FILE):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        current_backup = os.path.join(BACKUP_DIR, f"pre_restore_{timestamp}.db")
        shutil.copy2(DATABASE_FILE, current_backup)
        print(f"💾 Backed up current database to: {os.path.basename(current_backup)}")
        print()
    
    try:
        # Copy backup file to database location
        shutil.copy2(backup_path, DATABASE_FILE)
        
        # Verify restore
        if os.path.exists(DATABASE_FILE):
            file_size = os.path.getsize(DATABASE_FILE)
            print(f"✅ Database restored successfully!")
            print(f"   Restored from: {backup_filename}")
            print(f"   Database size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
            print()
            print("⚠️  Note: You may need to restart the application for changes to take effect.")
            return True
        else:
            print("❌ Error: Restore completed but database file not found!")
            return False
    except Exception as e:
        print(f"❌ Error restoring backup: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Database Restore Tool")
    print(f"   Database: {DATABASE_FILE}")
    print(f"   Backup directory: {BACKUP_DIR}")
    print()
    
    # If backup filename provided, restore it
    if len(sys.argv) > 1:
        backup_filename = sys.argv[1]
        print(f"📥 Restoring from: {backup_filename}")
        print()
        restore_backup(backup_filename)
    else:
        # List available backups
        backups = list_backups()
        if backups:
            print("💡 To restore a backup, run:")
            print(f"   python restore_db.py <backup_filename>")
            print()
            print("   Example:")
            print(f"   python restore_db.py {backups[0]}")

