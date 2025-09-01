from apscheduler.schedulers.background import BackgroundScheduler
from database import SessionLocal
from models import Scheduler, Config
from . import pinger

def job_ping():
    with SessionLocal() as db:
        # Vérifie si le scheduler est activé
        config = db.query(Config).filter(Config.key == "scheduler").first()
        if not config or config.value == "0":
            print("[INFO] Scheduler désactivé, aucun ping exécuté.")
            return

        # Sinon on lance les pings
        schedulers = db.query(Scheduler).all()
        for scheduler in schedulers:
            host = scheduler.url.url
            ok = pinger.main(host)
            print(f"[{'OK' if ok else 'FAIL'}] Ping {host}")

scheduler = BackgroundScheduler()
scheduler.add_job(job_ping, 'interval', seconds=10)
scheduler.start()
