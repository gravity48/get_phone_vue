import asyncio
import json
import os
import concurrent.futures
import socket
import typing
import websockets
from logging_ import main_log
from logging_.log_decorators import event_logger
from settings import INTERFACE, PORT, base_configuration
from server import ProjectWrapper


PROJECT_RUNNING: typing.Dict[int, ProjectWrapper] = {}


def dict2msg(dict_):
    return json.dumps(dict_, ensure_ascii=False).encode('utf8')


@event_logger(main_log)
def sync_db(data: dict):
    host, port = data['db_ip'].split(':')
    data['db_ip'] = host
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)
        sock.connect((host, int(port)))
    base_configuration.update_db_info(**data)
    return dict2msg({'success': True})


@event_logger(main_log)
def start_project(data: dict):
    """
    Запуск проекта согласно его типа
    """
    global PROJECT_RUNNING
    id_ = data['id']
    proj_type = data['proj_type']
    alias = data['options']['alias']
    PROJECT_RUNNING[id_] = ProjectWrapper(alias)
    PROJECT_RUNNING[id_].start_proj(proj_type, data)
    context = {
        'status': 'success'
    }
    return dict2msg(context)


def status_project(data: dict):
    global PROJECT_RUNNING
    context = {}
    try:
        id_ = data['id']
        status = PROJECT_RUNNING[id_].status()
        context['status'] = status
    except KeyError:
        context['status'] = 'Project not initialize'
    return dict2msg(context)


@event_logger(main_log)
def stop_proj(data: dict):
    global PROJECT_RUNNING
    try:
        id_ = data['id']
        proj_ = PROJECT_RUNNING.pop(id_, None)
        if proj_:
            proj_.stop()
            del proj_
    finally:
        context = {
            'status': 'Project Stopped'
        }
        return dict2msg(context)


async def get_phone_view(websocket, path):
    """Шина событий сервера"""
    func_event = {
        'sync_db': sync_db,
        'start_project': start_project,
        'status_proj': status_project,
        'stop_proj': stop_proj,
    }
    loop = asyncio.get_running_loop()
    try:
        message = await websocket.recv()
        json_response = json.loads(message)
        event = json_response['event']
        data = json_response['data']
        response = await loop.run_in_executor(pool, func_event[event], data)
        await websocket.send(response)
    except Exception as e:
        context = {
            'error': f'Error {e!r}',
        }
        await websocket.send(dict2msg(context))


async def start():
    async with websockets.serve(get_phone_view, INTERFACE, PORT):
        await asyncio.Future()


if __name__ == '__main__':
    pool = concurrent.futures.ThreadPoolExecutor((os.cpu_count() or 1))

    asyncio.run(start())
