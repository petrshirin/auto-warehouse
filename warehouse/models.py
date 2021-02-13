from django.db import models


class WarehousePoint(models.Model):
    point_num = models.PositiveSmallIntegerField(default=0)
    type = models.CharField(max_length=10, choices=[
        ("RESERVED", "RESERVED"),
        ("FILLED", "FILLED"),
        ("VOID", "VOID")
    ], default='VOID')
    last_action = models.CharField(max_length=10, choices=[
        ("LOAD", "LOAD"),
        ("UNLOAD", "UNLOAD"),
        ("TRANSFER", "TRANSFER")], null=True, blank=True, default=None)
    shelving = models.PositiveSmallIntegerField(default=-1)


class Cargo(models.Model):
    name = models.CharField(max_length=1024)
    cargo_model = models.CharField(max_length=255)
    producer = models.CharField(max_length=512)
    place = models.ForeignKey(WarehousePoint, on_delete=models.CASCADE, null=True)
    factory_io_id = models.PositiveIntegerField(null=True, blank=True)


class CargoMove(models.Model):
    factory_io_id = models.PositiveIntegerField(null=True, blank=True)
    from_point = models.ForeignKey(WarehousePoint, null=True, on_delete=models.SET_NULL, related_name='from_point')
    to_point = models.ForeignKey(WarehousePoint, null=True, on_delete=models.SET_NULL, related_name='to_point')


class CargoUnloadTimeSheet(models.Model):
    factory_io_id = models.PositiveIntegerField()
    date_unload = models.DateTimeField()
    completed = models.BooleanField(default=False)


class CargoLoadTimeSheet(models.Model):
    factory_io_id = models.PositiveIntegerField()
    date_load = models.DateTimeField()
    completed = models.BooleanField(default=False)


def create_warehouse(count_shelving=4, count_x=9, count_y=6):
    for z in range(count_shelving):
        for y in range(count_y):
            for x in range(count_x):
                WarehousePoint.objects.create(shelving=z+1, point_num=(y+1) * (x+1))




