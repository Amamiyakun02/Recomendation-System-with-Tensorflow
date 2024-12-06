import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# Deklarasi base untuk model SQLAlchemy
Base = declarative_base()

class University(Base):
    __tablename__ = 'universitas'

    id_universitas = Column(Integer, primary_key=True, autoincrement=True)
    universitas = Column(String(100), nullable=False)
    jurusan = Column(String(100), nullable=False)
    id_sektor = Column(Integer, ForeignKey('sektor.id_sektor'), nullable=False)
    deskripsi = Column(Text, nullable=True)
    url_website = Column(Text, nullable=True)
    updated_at = Column(DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)
    sektor = sqlalchemy.orm.relationship('Sector', backref='universities')
