from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
# Assuming root user and localhost. 
# NOTE: In production, use environment variables!
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Mithun1701@localhost/dualkey_db"

# Create Engine
# pool_recycle is important for MySQL to prevent connection timeouts
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
