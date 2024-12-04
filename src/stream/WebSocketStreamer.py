import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol
import cv2
import base64
import json
import logging
from datetime import datetime
from typing import Set
import threading

"""
Bu modül, OpenCV karelerini WebSocket üzerinden yayınlamak için kullanılır.
"""

class WebSocketStreamer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
        self.server = None
        self._stop = False
        self.loop = None

    async def unregister(self, websocket: WebSocketServerProtocol):
        """Bağlantıyı sonlandır"""
        if websocket in self.clients:
            self.clients.discard(websocket)
            await self.broadcast_viewer_count()

    async def register(self, websocket: WebSocketServerProtocol):
        """Yeni bağlantıyı kaydet"""
        self.clients.add(websocket)
        await self.broadcast_viewer_count()

    async def broadcast_viewer_count(self):
        """Tüm istemcilere güncel izleyici sayısını gönder"""
        message = json.dumps({
            'type': 'viewer_count',
            'count': len(self.clients)
        })

        for websocket in self.clients.copy():
            try:
                await websocket.send(message)
            except:
                pass

    async def broadcast_frame(self, frame):
        """Tüm bağlı istemcilere kareyi gönder"""
        if not self.clients:
            return

        try:
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            message = json.dumps({
                'type': 'frame',
                'data': jpg_as_text,
                'timestamp': datetime.now().isoformat()
            })

            clients = self.clients.copy()
            for websocket in clients:
                try:
                    await websocket.send(message)
                except websockets.exceptions.ConnectionClosed:
                    self.clients.discard(websocket)
                    await self.broadcast_viewer_count()
                except Exception as e:
                    logging.error(f"Mesaj gönderilirken hata oluştu: {str(e)}")
                    self.clients.discard(websocket)

        except Exception as e:
            logging.error(f"Frame yayınlanırken hata oluştu: {str(e)}")

    async def ws_handler(self, websocket: WebSocketServerProtocol):
        """WebSocket bağlantı"""
        await self.register(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get('type') == 'disconnect':
                        await self.unregister(websocket)
                        break
                except json.JSONDecodeError:
                    pass
        except websockets.exceptions.ConnectionClosed:
            await self.unregister(websocket)
        finally:
            await self.unregister(websocket)


    async def _run_server(self):
        """server çalıştırma"""
        async with websockets.serve(self.ws_handler, self.host, self.port):
            self.server = True
            print(f"ws://{self.host}:{self.port}")
            await asyncio.Future()  # run forever

    def start_server(self):
        """WebSocket sunucusunu çalıştır"""

        def run_async_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self._run_server())

        self.server_thread = threading.Thread(target=run_async_loop, daemon=True)
        self.server_thread.start()

    def stop_server(self):
        """WebSocket sunucuyu durdur"""
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
            logging.info("WebSocket sunucusu durduruldu")

    def update_frame(self, frame):
        """Yeni bir kareyi yayınla"""
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.broadcast_frame(frame), self.loop)