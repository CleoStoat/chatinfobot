from helpers import CommandData
from service_layer.commands_handlers.infogroup import infogroup_cmd

COMMANDS = [
    CommandData(
        callback=infogroup_cmd,
        name="mensajes_info",
        description="Muestra la cantidad de mensajes que se enviaron en este chat",
    ),
]
