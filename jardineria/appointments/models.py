from django.db import models

class Client(models.Model):
    """
    Modelo para los clientes que solicitan servicios de jardinería.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    phone = models.CharField(max_length=15, verbose_name="Teléfono", blank=True, null=True)

    def __str__(self):
        return self.name


class Gardener(models.Model):
    """
    Modelo para los jardineros que realizan los servicios.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre del Jardinero")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    phone = models.CharField(max_length=15, verbose_name="Teléfono", blank=True, null=True)

    def __str__(self):
        return self.name


class VisitRequest(models.Model):
    """
    Modelo para las solicitudes de visitas y servicios de jardinería.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="visit_requests")
    gardener = models.ForeignKey(
        Gardener,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_visits",
        verbose_name="Jardinero Asignado"
    )
    address = models.CharField(max_length=255, verbose_name="Dirección")
    date = models.DateTimeField(verbose_name="Fecha y Hora de la Visita")
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name="Latitud", null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name="Longitud", null=True, blank=True
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default='pending', verbose_name="Estado"
    )
    client_confirmation = models.BooleanField(default=False, verbose_name="Confirmación del Cliente")

    def __str__(self):
        return f"{self.client.name} - {self.address} ({self.get_status_display()})"
