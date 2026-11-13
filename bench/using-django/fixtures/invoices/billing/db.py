import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.environ.get("DATABASE_URL", "postgresql+psycopg://localhost/invoices"))
session = scoped_session(sessionmaker(bind=engine))
