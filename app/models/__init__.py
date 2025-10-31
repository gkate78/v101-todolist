# This makes the models directory a Python package
# We'll import our Todo model here so it's easy to access from other parts of the app
from app.models.todo import Todo

__all__ = ["Todo"]

