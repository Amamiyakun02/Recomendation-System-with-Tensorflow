from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Deklarasi base untuk model SQLAlchemy
Base = declarative_base()

# Definisi model Sector
class Sector(Base):
    __tablename__ = 'sektor'  # Nama tabel

    id_sektor = Column(Integer, primary_key=True, autoincrement=True)
    nama_sektor = Column(String(255), nullable=False)
    # index = Column(Integer, nullable=False)
    url_gambar = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Sector(id={self.id_sektor}, name='{self.nama_sektor}', image_url={self.url_gambar})>"
  # def __repr__(self):
  #       return f"<Sector(id={self.id}, name='{self.name}', index={self.index})>"
