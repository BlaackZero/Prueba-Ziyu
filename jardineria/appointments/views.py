from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Client, VisitRequest
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Client, VisitRequest, Gardener

from django.shortcuts import render

def index(request):
    return render(request, "appointments/index.html")


def create_visit_request(request):
    if request.method == "POST":
        client_id = request.POST.get("client_id")
        address = request.POST.get("address")
        date = request.POST.get("date")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        # Obtener el cliente
        client = Client.objects.first()  # Puedes ajustarlo según la lógica actual

        # Crear la solicitud de visita
        VisitRequest.objects.create(
            client=client,
            address=address,
            date=date,
            latitude=latitude,
            longitude=longitude,
            status="pending"
        )

        return redirect("index")

    clients = Client.objects.all()
    return render(request, "appointments/create_visit_request.html", {"clients": clients})




def gardener_dashboard(request):
    # Obtener el jardinero predeterminado
    gardener = Gardener.objects.get(email="jardinero@prueba.com")
    
    # Mostrar las visitas asignadas al jardinero
    visits = VisitRequest.objects.filter(gardener=gardener)
    return render(request, "appointments/gardener_dashboard.html", {"visits": visits})



def confirm_service(request):
    # Filtrar visitas completadas que aún no hayan sido confirmadas por el cliente
    visits = VisitRequest.objects.filter(status="completed", client_confirmation=False)

    if request.method == "POST":
        visit_id = request.POST.get("visit_id")
        confirmation = request.POST.get("confirmation")

        # Obtener la visita y procesar la confirmación
        visit = get_object_or_404(VisitRequest, pk=visit_id)

        if confirmation == "yes":
            visit.client_confirmation = True  # Confirmar la visita
        elif confirmation == "no":
            visit.status = "cancelled"  # Cancelar la visita
        visit.save()

        return redirect(reverse("confirm_service"))  # Redirigir al listado nuevamente

    return render(request, "appointments/confirm_service.html", {"visits": visits})

def list_visit_requests(request):
    visits = VisitRequest.objects.all()  # O filtra según sea necesario
    return render(request, "appointments/list_visit_requests.html", {"visits": visits})


def update_visit_status(request, pk):
    if request.method == "POST":
        visit = get_object_or_404(VisitRequest, pk=pk)
        new_status = request.POST.get("status")

        # Actualizar el estado de la visita
        if new_status in ["in_progress", "completed"]:
            visit.status = new_status
            visit.save()

        return HttpResponseRedirect(reverse("gardener_dashboard"))
    
def assign_visit(request, pk):
    if request.method == "POST":
        # Obtener la visita
        visit = get_object_or_404(VisitRequest, pk=pk)
        
        # Verificar si la visita ya tiene un jardinero asignado
        if visit.gardener:
            return redirect(reverse("gardener_dashboard"))  # Redirigir si ya está asignada

        # Asignar el jardinero predeterminado
        gardener = Gardener.objects.get(email="jardinero@prueba.com")
        visit.gardener = gardener
        visit.status = "in_progress"  # Cambiar estado a "En Progreso"
        visit.save()

        return redirect(reverse("gardener_dashboard"))
