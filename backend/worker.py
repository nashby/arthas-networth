from rq import Connection, Worker
from redis import Redis

from config import Config

def run_worker():
    redis = Redis.from_url(Config.REDIS_URL)

    with Connection(redis):
        worker = Worker('arthas_networth_import')
        worker.work()

if __name__ == '__main__':
    run_worker()
