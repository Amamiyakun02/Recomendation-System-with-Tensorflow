from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Definisi model Sector
class Sector(Base):
    __tablename__ = 'sektor'

    id_sektor = Column(Integer, primary_key=True, autoincrement=True)
    nama_sektor = Column(String(100), nullable=False)
    url_gambar = Column(String(255), nullable=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    universitas = relationship('Universitas', backref='sektor')

    # def __repr__(self):
    #     return f"<Sector(id={self.id_sektor}, name='{self.nama_sektor}', image_url={self.url_gambar})>"
class Universitas(Base):
    __tablename__ = 'universitas'

    id_universitas = Column(Integer, primary_key=True, autoincrement=True)
    universitas = Column(String(100), nullable=False)
    jurusan = Column(String(100), nullable=False)
    id_sektor = Column(Integer, ForeignKey('sektor.id_sektor'), nullable=False)
    deskripsi = Column(Text, nullable=True)
    url_website = Column(Text, nullable=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
