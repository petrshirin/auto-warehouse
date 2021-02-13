from django.db.models import Q, QuerySet
from typing import Union, Dict
from .models import WarehousePoint, CargoMove
from .rabbitMQ import start_connection, send_message
import json


def cargo_load(cords: Dict) -> Dict:
    ware_point = check_point('LOAD', cords['point'], cords['shelving'])
    if ware_point:
        ware_point.type = 'RESERVED'
        ware_point.last_action = 'LOAD'
        ware_point.save()
        connection, channel = start_connection()
        message = {
            "type": "LOAD",
            "cords": {
                "point": cords['point'],
                "shelving": cords['shelving']
            }
        }
        send_message(channel, json.dumps(message))
        connection.close()
        return {"success": True, 'data': "ok"}
    else:
        return {"success": False, 'data': "Действие для этой ячейки недоступно"}


def cargo_transfer(cords_from: Dict, cords_to: Dict) -> Dict:
    ware_point_from = check_point('UNLOAD', cords_from['point'], cords_from['shelving'])
    ware_point_to = check_point('UNLOAD', cords_to['point'], cords_to['shelving'])
    if ware_point_from and ware_point_to:
        ware_point_from.type = 'RESERVED'
        ware_point_from.last_action = 'TRANSFER'
        ware_point_from.save()
        ware_point_to.type = 'RESERVED'
        ware_point_to.last_action = 'TRANSFER'
        ware_point_to.save()
        connection, channel = start_connection()
        message = {
            "type": "UNLOAD",
            "from": {
                "point": cords_from['point'],
                "shelving": cords_from['shelving']
            },
            "to": {
                "point": cords_to['point'],
                "shelving": cords_to['shelving']
            }
        }
        send_message(channel, json.dumps(message))
        connection.close()
        return {"success": True, 'data': "ok"}
    else:
        return {"success": False, 'data': "Действие для этой ячейки недоступно"}


def cargo_unload(cords: Dict) -> Dict:
    ware_point = check_point('UNLOAD', cords['point'], cords['shelving'])
    if ware_point:
        ware_point.type = 'RESERVED'
        ware_point.last_action = 'UNLOAD'
        ware_point.save()
        connection, channel = start_connection()
        message = {
            "type": "UNLOAD",
            "cords": {
                "point": cords['point'],
                "shelving": cords['shelving']
            }
        }
        send_message(channel, json.dumps(message))
        connection.close()
        return {"success": True, 'data': "ok"}
    else:
        return {"success": False, 'data': "Действие для этой ячейки недоступно"}


def check_point(event_type: str, point: int, shelving: int) -> Union[WarehousePoint, None]:
    ware_point: WarehousePoint = WarehousePoint.objects.filter(point_num=point, shelving=shelving).first()
    if not ware_point:
        return
    if event_type == 'LOAD':
        if ware_point.type == 'FILLED':
            return
        elif ware_point.type == 'VOID':
            return ware_point
    elif event_type == 'UNLOAD':
        if ware_point.type == 'FILLED':
            return ware_point
        elif ware_point.type == 'VOID':
            return






