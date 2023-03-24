import asyncio
import json
import websockets
import sys
import wave

port = '4849'


def connection_error(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except ConnectionRefusedError:
            return {'status': 'no connection'}
    return wrapper


class WebSocketClient:

    def __init__(self):
        self.cnt_str = f'ws://localhost:{port}'

    @staticmethod
    async def _send_data(uri: str, data: dict):
        data = json.dumps(data, ensure_ascii=False).encode('utf8')
        async with websockets.connect(uri) as websocket:
            await websocket.send(data)
            response = await websocket.recv()
        return response

    def start_project(self, data, db):
        ip_db, port_db = db['db_ip'].split(':')
        data['db'] = {
            'path2db': db['db_path'],
            'server_ip': ip_db,
            'port': port_db,
            'login': db['db_login'],
            'password': db['db_password'],
        }
        context = {
            'event': 'start_project',
            'data': data,
        }
        response = asyncio.run(self._send_data(self.cnt_str, context))
        response = json.loads(response)
        return response

    @connection_error
    def stop_proj(self, data):
        context = {
            'event': 'stop_proj',
            'data': data,
        }
        response = asyncio.run(self._send_data(self.cnt_str, context))
        response = json.loads(response)
        return response

    @connection_error
    def status_proj(self, data):
        context = {
            'event': 'status_proj',
            'data': data,
        }
        response = asyncio.run(self._send_data(self.cnt_str, context))
        response = json.loads(response)
        return response

    @connection_error
    def sync_database(self, data):
        context = {
            'event': 'sync_db',
            'data': data,
        }
        response = asyncio.run(self._send_data(self.cnt_str, context))
        response = json.loads(response)
        return response['success']


