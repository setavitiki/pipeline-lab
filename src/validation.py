# Task Validation Module
import re
from datetime import datetime

def validate_task_title(title):
    """Validate task title"""
    if not title or len(title.strip()) == 0:
        return False, "Title cannot be empty"
    
    if len(title) > 100:
        return False, "Title cannot exceed 100 characters"
    
    if not re.match(r'^[a-zA-Z0-9\s\-_.]+$', title):
        return False, "Title contains invalid characters"
    
    return True, "Valid title"

def validate_task_priority(priority):
    """Validate task priority"""
    valid_priorities = ['low', 'medium', 'high', 'critical']
    if priority not in valid_priorities:
        return False, f"Priority must be one of: {valid_priorities}"
    return True, "Valid priority"

def validate_task_due_date(due_date):
    """Validate task due date"""
    try:
        due = datetime.fromisoformat(due_date)
        if due < datetime.now():
            return False, "Due date cannot be in the past"
        return True, "Valid due date"
    except ValueError:
        return False, "Invalid date format. Use ISO format: YYYY-MM-DD"
