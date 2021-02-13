from django_cron import CronJobBase, Schedule
from .models import CargoUnloadTimeSheet, CargoLoadTimeSheet, WarehousePoint, Cargo
from django.utils.timezone import now
from .services import cargo_load, cargo_unload
from django.db.models import Q, QuerySet


class LoadJob(CronJobBase):

    schedule = Schedule(run_every_mins=1)
    code = 'warehouse.load_job'

    def do(self):
        need_to_loaded_cargo: QuerySet[CargoLoadTimeSheet] = CargoLoadTimeSheet.objects.get(date_load__lt=now(), completed=False).all()
        for cargo_sheet in need_to_loaded_cargo:
            ware_point: WarehousePoint = WarehousePoint.objects.filter(type='VOID').first()
            cargo: Cargo = Cargo.objects.filter(factory_io_id=cargo_sheet.factory_io_id).first()
            answ = cargo_load({"point": ware_point.point_num, "shelving": ware_point.shelving})
            if answ.get('error'):
                cargo_sheet.completed = True
                cargo.place = ware_point
                cargo_sheet.save()
                cargo.save()


class UnLoadJob(CronJobBase):

    schedule = Schedule(run_every_mins=1)
    code = 'warehouse.unload_job'

    def do(self):
        need_to_loaded_cargo: QuerySet[CargoLoadTimeSheet] = CargoLoadTimeSheet.objects.get(date_load__lt=now(), completed=False).all()
        for cargo_sheet in need_to_loaded_cargo:
            ware_point: WarehousePoint = WarehousePoint.objects.filter(type='VOID').first()
            cargo: Cargo = Cargo.objects.filter(factory_io_id=cargo_sheet.factory_io_id).first()
            answ = cargo_unload({"point": ware_point.point_num, "shelving": ware_point.shelving})
            if answ.get('error'):
                cargo_sheet.completed = True
                cargo.place = ware_point
                cargo_sheet.save()
                cargo.save()