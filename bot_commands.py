from helpers.command_helpers import CommandData
from service_layer.commands_handlers.infogroup import infogroup_cmd
from service_layer.commands_handlers.plot import plot_cmd, plot_active_hours_cmd, plot_active_weekdays_cmd, plot_month_cmd

COMMANDS = [
    CommandData(
        callback=infogroup_cmd,
        name="mensajes_info",
        description="Muestra la cantidad de mensajes que se enviaron en este chat",
    ),
    CommandData(
        callback=plot_cmd,
        name="plot",
        description="Plotear",
    ),
    CommandData(
        callback=plot_active_hours_cmd,
        name="plot_h",
        description="Plotear horas",
    ),
    CommandData(
        callback=plot_active_weekdays_cmd,
        name="plot_d",
        description="Plotear dias",
    ),
    CommandData(
        callback=plot_month_cmd,
        name="plot_m",
        description="Plotear ultimos 31 dias",
    ),
]
