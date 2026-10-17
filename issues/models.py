from abc import ABC, abstractmethod
from datetime import datetime

class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        # We invoke describe() dynamically to expose the formatted description text string inside JSON arrays
        data = {key: value for key, value in self.__dict__.items()}
        if hasattr(self, 'describe'):
            data['description_text'] = self.describe()
        return data

class Reporter(BaseEntity):
    def __init__(self, id, name, email, team):
        self.id = int(id)
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not self.name or str(self.name).strip() == "":
            raise ValueError('Name cannot be empty')
        if '@' not in str(self.email):
            raise ValueError('Invalid email address')

class Issue(BaseEntity):
    def __init__(self, id, title, description, reporter_id, status='open', priority='medium', created_at=None):
        self.id = int(id)
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = int(reporter_id)
        self.created_at = created_at if created_at else str(datetime.now())

    def validate(self):
        if not self.title or str(self.title).strip() == "":
            raise ValueError('Title cannot be empty')
        if not self.description or str(self.description).strip() == "":
            raise ValueError('Description cannot be empty')
            
        valid_statuses = ['open', 'in_progress', 'resolved', 'closed']
        if self.status not in valid_statuses:
            raise ValueError(f"Invalid status. Choose from: {valid_statuses}")
            
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if self.priority not in valid_priorities:
            raise ValueError(f"Invalid priority. Choose from: {valid_priorities}")

    def describe(self):
        return f"{self.title} [{self.priority}]"

class CriticalIssue(Issue):
    def describe(self):
        return f"[URGENT] {self.title} — needs immediate attention"

class LowPriorityIssue(Issue):
    def describe(self):
        return f"{self.title} — low priority, handle when free"
