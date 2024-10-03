import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .services import get_all_domains, get_domain_by_name
from .vm_list import get_os_logo

"""
Channels consumer pour la liste des VMs, qui envoie la liste des VMs toutes les 2 secondes via WebSocket.
"""


class VMListConsumer(AsyncWebsocketConsumer):
    DELAY = 2

    # Méthodes de connexion et de déconnexion
    async def connect(self):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.send_vm_list())
        await self.accept()

    async def disconnect(self, close_code):
        self.loop.stop()

    # Récupère la liste des VMs et l'envoie via WebSocket en fonction du délai défini
    async def send_vm_list(self):
        while True:
            vms_list = get_all_domains(request)
            vms = []

            for vm_name in vms_list:
                vm_info = get_domain_by_name(request, vm_name)
                if vm_info:
                    vm_info['os_logo'] = get_os_logo(vm_info.get('os'))
                    vms.append(vm_info)

            await self.send(text_data=json.dumps({
                'vms': vms
            }))
            await asyncio.sleep(self.DELAY)
