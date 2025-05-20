from app.db.session import engine
from app.db.base_class import Base
from app.db.models import user

def init_db():
    """
    Initialize the database by creating all tables.
    """
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)