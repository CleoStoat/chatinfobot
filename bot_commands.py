from helpers.command_helpers import CommandData
from service_layer.commands_handlers.broadcast import broadcast_cmd
from service_layer.commands_handlers.infogroup import infogroup_cmd
from service_layer.commands_handlers.plot import (
    report_today_by_hour,
    report_thisweek_by_hour,
    report_thisweek_by_weekday,
    report_month_by_hour,
    report_month_by_weekday,
    report_month_by_date,
    report_alltime_by_hour,
    report_alltime_by_weekday,
    report_alltime_by_date,
    report_alltime_by_month,
    report_today_by_users,
    report_thisweek_by_users,
    report_month_by_users,
    report_alltime_by_users,
)

COMMANDS = [
    CommandData(
        callback=infogroup_cmd,
        name="mensajes_info",
        description="Muestra la cantidad de mensajes que se enviaron en este chat",
    ),
    CommandData(
        callback=broadcast_cmd,
        name="broadcast",
        description="Enviar mensaje a todos los grupos",
    ),
    CommandData(
        callback=report_today_by_hour,
        name="informe_hoy_por_hora",
        description="Reporte de mensajes del día de hoy por hora",
    ),
    CommandData(
        callback=report_thisweek_by_hour,
        name="informe_semanal_por_hora",
        description="Reporte de mensajes de la semana actual por hora",
    ),
    CommandData(
        callback=report_thisweek_by_weekday,
        name="informe_semanal_por_diasem",
        description="Reporte de mensajes de la semana actual por día de la semana",
    ),
    CommandData(
        callback=report_month_by_hour,
        name="informe_mensual_por_hora",
        description="Reporte de mensajes del mes por hora",
    ),
    CommandData(
        callback=report_month_by_weekday,
        name="informe_mensual_por_diasem",
        description="Reporte de mensajes del mes por día de la semana",
    ),
    CommandData(
        callback=report_month_by_date,
        name="informe_mensual_por_fecha",
        description="Reporte de mensajes del mes por fecha",
    ),
    CommandData(
        callback=report_alltime_by_hour,
        name="informe_todoeltiempo_por_hora",
        description="Reporte de mensajes de todo el tiempo por hora",
    ),
    CommandData(
        callback=report_alltime_by_weekday,
        name="informe_todoeltiempo_por_diasem",
        description="Reporte de mensajes de todo el tiempo por día de la semana",
    ),
    CommandData(
        callback=report_alltime_by_date,
        name="informe_todoeltiempo_por_fecha",
        description="Reporte de mensajes de todo el tiempo por fecha",
    ),
    CommandData(
        callback=report_alltime_by_month,
        name="informe_todoeltiempo_por_mes",
        description="Reporte de mensajes de todo el tiempo por mes",
    ),
    CommandData(
        callback=report_today_by_users,
        name="informe_hoy_por_usuario",
        description="Reporte de mensajes de hoy por usuario",
    ),
    CommandData(
        callback=report_thisweek_by_users,
        name="informe_semanal_por_usuario",
        description="Reporte de mensajes de esta semana por usuario",
    ),
    CommandData(
        callback=report_month_by_users,
        name="informe_mensual_por_usuario",
        description="Reporte de mensajes de este mes por usuario",
    ),
    CommandData(
        callback=report_alltime_by_users,
        name="informe_todoeltiempo_por_usuario",
        description="Reporte de mensajes de todo el tiempo por usuario",
    ),
]
