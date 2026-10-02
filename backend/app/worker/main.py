from app.config import get_settings
from app.worker.tasks import (
    run_flashcards_task,
    run_ingest_index_task,
    run_topic_map_task,
)
from redis import Redis
from rq import Connection, Worker

if __name__ == "__main__":
    settings = get_settings()
    conn = Redis.from_url(settings.redis_url)
    with Connection(conn):
        Worker(["default"]).work()
