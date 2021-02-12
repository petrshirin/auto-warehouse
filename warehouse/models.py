from django.db import models


class Cargo(models.Model):
    name = models.CharField(max_length=1024)
    cargo_model = models.CharField(max_length=255)
    producer = models.CharField(max_length=512)
    factory_io_id = models.PositiveIntegerField()
    place_x = models.PositiveSmallIntegerField()
    place_y = models.PositiveSmallIntegerField()
    shelving = models.PositiveSmallIntegerField()


class CargoMove(models.Model):
    factory_io_id = models.PositiveIntegerField()
    from_place_x = models.PositiveSmallIntegerField()
    from_place_y = models.PositiveSmallIntegerField()
    from_shelving = models.PositiveSmallIntegerField()
    to_place_x = models.PositiveSmallIntegerField()
    to_place_y = models.PositiveSmallIntegerField()
    to_shelving = models.PositiveSmallIntegerField()


