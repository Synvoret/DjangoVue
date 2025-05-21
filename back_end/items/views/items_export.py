# views.py
from django.http import HttpResponse
import openpyxl
from items.models import Item


def items_export(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Items"
    ws.append(["ID", "Name", "Description", "Author", "Created At"])
    for item in Item.objects.all():
        ws.append(
            [
                item.id,
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
