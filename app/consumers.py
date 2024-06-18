import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .services import get_all_domains, get_domain_by_name
from .vm_list import get_os_logo


class VMListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.send_vm_list())
        await self.accept()

    async def disconnect(self, close_code):
        self.loop.stop()

    async def send_vm_list(self):
        while True:
            vms_list = get_all_domains()
            vms = []

            for vm_name in vms_list:
                vm_info = get_domain_by_name(vm_name)
                if vm_info:
                    vm_info['os_logo'] = get_os_logo(vm_info.get('os'))
                    vms.append(vm_info)

            await self.send(text_data=json.dumps({
                'vms': vms
            }))
            await asyncio.sleep(2)
