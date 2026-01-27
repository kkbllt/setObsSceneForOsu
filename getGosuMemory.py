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
            _metadata = _mapdata
            _map_stats = _mapdata['stats']
            now_star = f'{"Star"}:{round(_map_stats['stars']["total"],2)}'
            
            if not bool(_Art := _metadata.get('artistUnicode',"")):
                _Art = _metadata['artist']
            if not bool(_Title := _metadata.get('titleUnicode',"")):
                _Title = _metadata['title']

            _osutext = f"{_Art} - {_Title}[{_metadata['version']}]\nMapper:{_metadata['mapper']}  url: b/{_mapdata['set']}\n{now_star} AR:{_map_stats['ar']['converted']} CS:{_map_stats['cs']['converted']} OD:{_map_stats['od']['converted']} HP:{_map_stats['hp']['converted']}{f'  +{_mapselectmod}' if _mapselectmod not in ('NM',None,"") else ''}"
            
            if _play_state != self.p[0] or _osutext != self.p[1]:
                self.p[0] = _play_state
                self.p[1] = _osutext


if __name__ == '__main__':
    app()