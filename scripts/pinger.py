from datetime import datetime
import models
from database import SessionLocal
import requests

def main(url: str):
    db = SessionLocal()
    try:
        resp = requests.get(url, timeout=5)

        response_content = resp.status_code

        pingerCreate = models.Ping(url=url, date=datetime.now(), result=response_content)
        db.add(pingerCreate)
        db.commit()
        db.refresh(pingerCreate)

        if resp.ok:
            return "ping great"
        else:
            return f"ping failed with status code: {resp.status_code}"

    except requests.ConnectionError:
        return "ping not available (connection error)"
    except requests.Timeout:
        return "ping not available (timeout)"
    except requests.RequestException as e:
        return f"ping not available (error: {e})"
    finally:
        db.close()
