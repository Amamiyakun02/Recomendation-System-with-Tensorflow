from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Deklarasi base untuk model SQLAlchemy
Base = declarative_base()

# Definisi model Sector
class Sector(Base):
    __tablename__ = 'sector'  # Nama tabel

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    index = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Sector(id={self.id}, name='{self.name}', index={self.index})>"
