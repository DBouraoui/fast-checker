from database import SessionLocal, Base, engine
import models

def load_fixtures():
    db = SessionLocal()
    if db.query(models.Url).count() == 0:
        db.add_all([
            models.Url(name="Google", url="https://www.google.com"),
            models.Url(name="Youtube", url="https://youtube.com")
        ])
    if db.query(models.Config).count() == 0:
        db.add_all([
            models.Config(key="scheduler", value="0"),
        ])
    db.commit()
    db.close()

if __name__ == "__main__":
    load_fixtures()
