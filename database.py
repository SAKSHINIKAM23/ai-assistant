from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///tasks.db")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    done = Column(Boolean, default=False)

Base.metadata.create_all(engine)

def save_task(text):
    db = SessionLocal()
    task = Task(text=text)
    db.add(task)
    db.commit()
    db.close()

def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).filter(Task.done == False).all()
    db.close()
    return tasks

def mark_done(task_id):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.done = True
        db.commit()
    db.close()