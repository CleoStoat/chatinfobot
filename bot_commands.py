from helpers import CommandData
from service_layer.commands_handlers.infogroup import infogroup_cmd
from service_layer.commands_handlers.plot import plot_cmd

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
]
