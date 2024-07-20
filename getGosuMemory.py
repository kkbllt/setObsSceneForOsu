import json
import time
import asyncio

from aiowebsocket.converses import AioWebSocket as AioWs
from multiprocessing import shared_memory

class app():

    osuMemoryData = ["_play_state","".zfill(1024),"allGosumemoryData".zfill(2949120)]

    def __init__(self, url="ws://127.0.0.1:24050/ws"):
        self.wsurl = url
        try:
            self.p = shared_memory.ShareableList(self.osuMemoryData,name='osumemory')
        except FileExistsError as e:
            self.p = shared_memory.ShareableList(name='osumemory')
        
        asyncio.get_event_loop().run_until_complete(self.connectWsServer())


    async def connectWsServer(self):

        async def getWsRes():
            async with AioWs(self.wsurl) as ws:
                converse = ws.manipulator
                while True:
                    wsRes = await converse.receive()
                    asyncio.ensure_future(self.setOsuData(wsRes))

        while True:
            try:
                await getWsRes()
            except Exception as e:
                print(e)
                continue


    async def setOsuData(self, wsRes):
        self.p[2] = wsRes
        wsRes = json.loads(wsRes)
        _mapdata = wsRes.get('menu', dict).get('bm', None)
        _mapselectmod = wsRes.get('menu', dict).get('mods', dict).get('str', None)
        _play_state = wsRes.get('menu', dict).get('state', None)
        if None not in (_mapdata, _play_state):
            _metadata = _mapdata['metadata']
            _map_stats = _mapdata['stats']
            _osutext = f"{_metadata.get('artist')} - {_metadata['title']}[{_metadata['difficulty']}]\nMapper:{_metadata['mapper']}  url: b/{_mapdata['id']}\nstar:{round(_map_stats['fullSR'],2)} AR:{_map_stats['AR']} CS:{_map_stats['CS']} OD:{_map_stats['OD']} HP:{_map_stats['HP']}{f'  +{_mapselectmod}' if _mapselectmod not in ('NM',None) else ''}"

            if _play_state != self.p[0] or _osutext != self.p[1]:
                self.p[0] = _play_state
                self.p[1] = _osutext


if __name__ == '__main__':
    app()