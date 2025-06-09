import asyncio
import json
import threading

from app.container import Container

container = Container()


async def worker_loop():
    await container.load_dependencies()
    while True:
        try:
            item = await container.redis_connection.client.blpop(
                container.settings.redis_fila, timeout=0
            )
            try:
                if item:
                    _, value = item
                    dados: str = json.loads(value)
                    dados = dados.split("_")
                    await container.consulta_service.start_consulta(dados[0], dados[1])
            except Exception as e:
                print(str(e))

        except Exception as e:
            print("Erro ao processar item da fila:", e)
            await asyncio.sleep(2)


def start_worker_in_thread():
    def run_worker():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(worker_loop())

    threading.Thread(target=run_worker, daemon=True).start()
