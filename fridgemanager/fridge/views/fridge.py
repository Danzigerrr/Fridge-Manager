from django.shortcuts import render, redirect
from ..models import Product, Fridge
from ..forms import FridgeForm
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator


# generate pdf file
def fridges_export_as_pdf(request):
    # create bytestream buffer
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    fridges = Fridge.objects.all()
    lines = []
    for fridge in fridges:
        lines.append(str(fridge.id))
        lines.append(fridge.name)
        lines.append(fridge.created_date.strftime("%Y-%m-%d %H:%M:%S"))
        lines.append(fridge.description)

        owners = fridge.owners.all()  # Retrieve all related owners
        owner_names = []
        for owner in owners:
            owner_names.append(f"{owner.first_name} {owner.last_name}")

        lines.append(", ".join(owner_names))  # Join owner names with commas

        lines.append(" ")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='fridges.pdf')


# generate csv file
def fridges_export_as_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=fridges.csv'

    writer = csv.writer(response)

    # column names
    writer.writerow(['id', 'fridge_name', 'created_date', 'description', 'owners'])

    fridges = Fridge.objects.all()

    for fridge in fridges:
        writer.writerow([fridge.id,
                         fridge.name,
                         fridge.created_date,
                         fridge.description,
                         fridge.owners])

    return response


# generate text file
def fridges_export_as_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=fridges.txt'

    fridges = Fridge.objects.all()

    lines = []
    for fridge in fridges:
        lines.append(f"{fridge.id}\n"
                     f"{fridge.name}\n"
                     f"{fridge.created_date}\n"
                     f"{fridge.description}\n"
                     f"{fridge.owners}\n\n")

    response.writelines(lines)
    return response


def fridge_add(request):
    submitted = False
    if request.method == "POST":
        form = FridgeForm(request.POST)
        if form.is_valid():
            fridge = form.save(commit=False)
            fridge.save()
            fridge.owners.set([request.user])
            return HttpResponseRedirect('/fridges/add?submitted=True')
    else:
        form = FridgeForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'fridge/fridge_add.html',
                  {'form': form, 'submitted': submitted})


def fridge_list(request):
    fridges = Fridge.objects.all().order_by('name')
    return render(request, 'fridge/fridge_list.html', {'fridges': fridges})


def fridge_detail(request, fridge_id):
    fridge = Fridge.objects.get(pk=fridge_id)
    return render(request, 'fridge/fridge_details.html', {'fridge': fridge})


def fridge_update(request, fridge_id):
    fridge = Fridge.objects.get(pk=fridge_id)
    form = FridgeForm(request.POST or None, instance=fridge)
    if form.is_valid():
        form.save()
        return redirect('fridge_list')

    return render(request, 'fridge/fridge_update.html',
                  {'fridge': fridge,
                   "form": form})


def fridge_delete(request, fridge_id):
    fridge = Fridge.objects.get(pk=fridge_id)
    fridge.delete()
    return redirect('fridge_list')


def fridge_products(request, fridge_id):
    fridge = Fridge.objects.get(pk=fridge_id)
    products_in_database = Product.objects.filter(fridge=fridge)

    p = Paginator(products_in_database, 2)  # 2nd arg --> objects per page
    page = request.GET.get('page')
    products_to_show = p.get_page(page)

    return render(request, 'product/products_list.html',
                  {'products': products_to_show, 'products_len': len(products_in_database)})
