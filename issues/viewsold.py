# import json
# from django.http import JsonResponse
# from django.views import View
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from issues.storage import db

# @method_decorator(csrf_exempt, name='dispatch')
# class ReporterListCreateView(View):
#     def get(self, request):
#         return JsonResponse([r.to_dict() for r in db.list_reporters()], safe=False)

#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             reporter = db.add_reporter(
#                 name=data.get('name'),
#                 email=data.get('email'),
#                 team=data.get('team')
#             )
#             return JsonResponse(reporter.to_dict(), status=201)
#         except ValueError as e:
#             return JsonResponse({"error": str(e)}, status=400)
#         except Exception:
#             return JsonResponse({"error": "Malformed request payload body"}, status=400)

# @method_decorator(csrf_exempt, name='dispatch')
# class IssueListCreateView(View):
#     def get(self, request):
#         return JsonResponse([i.to_dict() for i in db.list_issues()], safe=False)

#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             issue = db.add_issue(
#                 title=data.get('title'),
#                 description=data.get('description'),
#                 reporter_id=data.get('reporter_id'),
#                 status=data.get('status', 'open'),
#                 priority=data.get('priority', 'medium')
#             )
#             return JsonResponse(issue.to_dict(), status=201)
#         except ValueError as e:
#             return JsonResponse({"error": str(e)}, status=400)
#         except Exception:
#             return JsonResponse({"error": "Malformed request payload body"}, status=400)

# @method_decorator(csrf_exempt, name='dispatch')
# class IssueDetailView(View):
#     def get(self, request, pk):
#         issue = db.get_issue(pk)
#         if not issue:
#             return JsonResponse({"error": f"Issue with ID {pk} not found"}, status=404)
#         return JsonResponse(issue.to_dict())

#     def put(self, request, pk):
#         try:
#             data = json.loads(request.body)
#             issue = db.update_issue(pk, data)
#             if not issue:
#                 return JsonResponse({"error": f"Issue with ID {pk} not found"}, status=404)
#             return JsonResponse(issue.to_dict())
#         except ValueError as e:
#             return JsonResponse({"error": str(e)}, status=400)
