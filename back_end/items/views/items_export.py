import openpyxl
from django.http import HttpResponse, HttpResponseForbidden

from items.models import Item


# @login_required
def items_export(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Items"
    ws.append(["Index", "Name", "Description", "Author", "Created At"])
    for index, item in enumerate(Item.objects.all(), start=1):
        ws.append(
            [
                index,
                item.name,
                item.description,
                str(item.author) if item.author else "No Author",
                item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            ]
        )
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=items.xlsx"
    wb.save(response)
    return response
