import json
from pathlib import Path
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from issues.models import Reporter, Issue, CriticalIssue, LowPriorityIssue

# 🌟 Using Path objects instead of os.path strings
BASE_DIR = Path(__file__).resolve().parent.parent
REPORTERS_FILE = BASE_DIR / 'reporters.json'
ISSUES_FILE = BASE_DIR / 'issues.json'

def load_file_data(file_path: Path):
    """Loads a JSON file. Returns a clean tracking layout if the file doesn't exist."""
    # 🌟 Pathlib substitution for: if not os.path.exists(filepath)
    if not file_path.exists():
        return {"counter": 1, "data": {}}
        
    # 🌟 Pathlib opens and reads files using context managers directly
    try:
        with file_path.open('r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"counter": 1, "data": {}}

def save_file_data(file_path: Path, storage_dict):
    """Saves updated dictionary data back to its dedicated file location."""
    # 🌟 Pathlib alternative to open(filepath, 'w')
    with file_path.open('w') as f:
        json.dump(storage_dict, f, indent=4)


@method_decorator(csrf_exempt, name='dispatch')
class ReporterListCreateView(View):
    def get(self, request):
        db_reporters = load_file_data(REPORTERS_FILE)
        return JsonResponse(list(db_reporters["data"].values()), safe=False)

    def post(self, request):
        try:
            payload = json.loads(request.body)
            db_reporters = load_file_data(REPORTERS_FILE)
            
            next_id = db_reporters["counter"]
            
            reporter = Reporter(
                id=next_id,
                name=payload.get('name'),
                email=payload.get('email'),
                team=payload.get('team')
            )
            reporter.validate()
            
            db_reporters["data"][str(next_id)] = reporter.to_dict()
            db_reporters["counter"] = next_id + 1
            save_file_data(REPORTERS_FILE, db_reporters)
            
            return JsonResponse(reporter.to_dict(), status=201)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception:
            return JsonResponse({"error": "Malformed request payload"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class IssueListCreateView(View):
    def get(self, request):
        db_issues = load_file_data(ISSUES_FILE)
        serialized_list = []
        
        for record in db_issues["data"].values():
            priority = record.get('priority', 'medium')
            if priority == 'critical':
                issue_obj = CriticalIssue(**record)
            elif priority == 'low':
                issue_obj = LowPriorityIssue(**record)
            else:
                issue_obj = Issue(**record)
                
            out = issue_obj.to_dict()
            out['description_text'] = issue_obj.describe()
            serialized_list.append(out)
            
        return JsonResponse(serialized_list, safe=False)

    def post(self, request):
        try:
            payload = json.loads(request.body)
            db_reporters = load_file_data(REPORTERS_FILE)
            db_issues = load_file_data(ISSUES_FILE)
            
            reporter_id = payload.get('reporter_id')
            if not reporter_id or str(reporter_id) not in db_reporters["data"]:
                return JsonResponse({"error": f"Reporter ID {reporter_id} does not exist in records."}, status=400)
            
            next_id = db_issues["counter"]
            priority = payload.get('priority', 'medium')
            
            issue_args = {
                "id": next_id,
                "title": payload.get('title'),
                "description": payload.get('description'),
                "reporter_id": reporter_id,
                "status": payload.get('status', 'open'),
                "priority": priority
            }
            
            # Explicitly instantiate the correct subclass based on priority
            if priority == 'critical':
                issue = CriticalIssue(**issue_args)
            elif priority == 'low':
                issue = LowPriorityIssue(**issue_args)
            else:
                issue = Issue(**issue_args)
                
            issue.validate()
            
            db_issues["data"][str(next_id)] = issue.to_dict()
            db_issues["counter"] = next_id + 1
            save_file_data(ISSUES_FILE, db_issues)
            
            response = issue.to_dict()
            response['description_text'] = issue.describe()
            return JsonResponse(response, status=201)
            
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception:
            return JsonResponse({"error": "Malformed request payload"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class IssueDetailView(View):
    def get(self, request, pk):
        db_issues = load_file_data(ISSUES_FILE)
        record = db_issues["data"].get(str(pk))
        if not record:
            return JsonResponse({"error": f"Issue with ID {pk} not found"}, status=404)
            
        priority = record.get('priority')
        if priority == 'critical':
            issue_obj = CriticalIssue(**record)
        elif priority == 'low':
            issue_obj = LowPriorityIssue(**record)
        else:
            issue_obj = Issue(**record)
            
        out = issue_obj.to_dict()
        out['description_text'] = issue_obj.describe()
        return JsonResponse(out)