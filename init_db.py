"""
Database Initialization Script

This script initializes the database for the FitCode application.
It creates all necessary tables and populates them with initial data.
"""

from application import app, db, init_db

print("Initializing the database...")
# Use the application context
with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    # Initialize the database
    init_db()
print("Database initialization complete!") 