import os
import json
from issues.models import Reporter, Issue, CriticalIssue, LowPriorityIssue

DB_FILE = 'db.json'

class JSONDatabase:
    def __init__(self):
        self._initialize_db()

    def _initialize_db(self):
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, 'w') as f:
                json.dump({"reporters": {}, "issues": {}, "reporter_counter": 1, "issue_counter": 1}, f)

    def _read(self):
        with open(DB_FILE, 'r') as f:
            return json.load(f)

    def _write(self, data):
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def add_reporter(self, name, email, team):
        state = self._read()
        rid = state["reporter_counter"]
        
        reporter = Reporter(id=rid, name=name, email=email, team=team)
        reporter.validate()
        
        state["reporters"][str(rid)] = reporter.to_dict()
        state["reporter_counter"] += 1
        self._write(state)
        return reporter

    def list_reporters(self):
        state = self._read()
        return [Reporter(**r) for r in state["reporters"].values()]

    def _instantiate_issue(self, **kwargs):
        # Drop calculated field key if present in file to prevent init breakdown signatures
        kwargs.pop('description_text', None)
        priority = kwargs.get('priority', 'medium')
        if priority == 'critical':
            return CriticalIssue(**kwargs)
        elif priority == 'low':
            return LowPriorityIssue(**kwargs)
        return Issue(**kwargs)

    def add_issue(self, title, description, reporter_id, status='open', priority='medium'):
        state = self._read()
        if str(reporter_id) not in state["reporters"]:
            raise ValueError(f"Foreign Key Error: Reporter ID {reporter_id} does not exist.")
        
        iid = state["issue_counter"]
        issue = self._instantiate_issue(
            id=iid, title=title, description=description, 
            reporter_id=reporter_id, status=status, priority=priority
        )
        issue.validate()
        
        state["issues"][str(iid)] = issue.to_dict()
        state["issue_counter"] += 1
        self._write(state)
        return issue

    def get_issue(self, iid):
        state = self._read()
        issue_data = state["issues"].get(str(iid))
        if not issue_data:
            return None
        return self._instantiate_issue(**issue_data)

    def list_issues(self):
        state = self._read()
        return [self._instantiate_issue(**i) for i in state["issues"].values()]

    def update_issue(self, iid, data):
        state = self._read()
        issue_data = state["issues"].get(str(iid))
        if not issue_data:
            return None
        
        # Build live entity object to parse incoming data and run validation check constraints
        issue = self._instantiate_issue(**issue_data)
        if 'title' in data: issue.title = data['title']
        if 'description' in data: issue.description = data['description']
        if 'status' in data: issue.status = data['status']
        if 'priority' in data: issue.priority = data['priority']
        issue.validate()
        
        # Re-save the updated issue object back into the JSON file
        state["issues"][str(iid)] = issue.to_dict()
        self._write(state)
        return issue

# Core instantiated tracking data worker singleton access hook points
db = JSONDatabase()
