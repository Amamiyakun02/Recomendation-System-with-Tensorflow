from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
# Deklarasi base untuk model SQLAlchemy
Base = declarative_base()

# Definisi model Sector
class Sector(Base):
    __tablename__ = 'sektor'  # Nama tabel

    id_sektor = Column(Integer, primary_key=True, autoincrement=True)
    nama_sektor = Column(String(255), nullable=False)
    url_gambar = Column(String(255), nullable=False)
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp())

    # def __repr__(self):
    #     return f"<Sector(id={self.id_sektor}, name='{self.nama_sektor}', image_url={self.url_gambar})>"
