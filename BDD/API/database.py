from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion PostgreSQL
DATABASE_URL = "postgresql://postgres:BTS2425@localhost/campus_db"

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création d'une session locale
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base pour les modèles SQLAlchemy
Base = declarative_base()
