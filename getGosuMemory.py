import json
import time
import asyncio
import websockets

from multiprocessing import shared_memory

class app():

    osuMemoryData = ['play_state',"_play_state",'mapstr', "".zfill(1024),"allGosumemoryData".zfill(6144)]
    appState = 0

    def __init__(self, url="ws://127.0.0.1:24050/ws"):
        self.wsurl = url
        try:
            self.p = shared_memory.ShareableList(self.osuMemoryData,name='osumemory')
        except FileExistsError as e:
            self.p = shared_memory.ShareableList(name='osumemory')
        
        asyncio.get_event_loop().run_until_complete(self.connectWsServer())


    async def connectWsServer(self):
        while True:
            try:
                async with websockets.connect(self.wsurl) as ws:
                    wsRes = await ws.recv()
                    asyncio.ensure_future(self.setOsuData(wsRes))
            except:
                print(f'无法连接{self.wsurl}')
                await asyncio.sleep(1)
                continue


    async def setOsuData(self, wsRes):
        wsRes = json.loads(wsRes)
        _mapdata = wsRes.get('menu', dict).get('bm', None)
        _mapselectmod = wsRes.get('menu', dict).get('mods', dict).get('str', None)
        _play_state = wsRes.get('menu', dict).get('state', None)
        if None not in (_mapdata, _play_state):
            _metadata = _mapdata['metadata']
            _map_stats = _mapdata['stats']
            _osutext = f"{_metadata.get('artist')} - {_metadata['title']}[{_metadata['difficulty']}]\nMapper:{_metadata['mapper']}  url: b/{_mapdata['id']}\nstar:{round(_map_stats['SR'],1)} AR:{_map_stats['AR']} CS:{_map_stats['CS']} OD:{_map_stats['OD']} HP:{_map_stats['HP']}{f'  +{_mapselectmod}' if _mapselectmod not in ('NM',None) else ''}"
            osuMemoryData = ['play_state',_play_state,'mapstr', _osutext]

            if _play_state != self.p[1] or _osutext != self.p[3]:
                self.p[1] = _play_state
                self.p[3] = _osutext
            print(f'{time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())}:{self.p}')


if __name__ == '__main__':
    app()