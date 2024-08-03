from . import Base
from sqlalchemy import (
    Column, 
    Integer,
    DateTime, 
    Time, 
    ForeignKey, 
    String
)
from sqlalchemy.orm import relationship

class Absensi(Base):
    __tablename__ = "absensi"
    
    id = Column("id", Integer, nullable=False, autoincrement=True, primary_key=True)
    tanggal_absen = Column("tanggal_absen", DateTime)
    jam_masuk = Column("jam_absen_masuk", Time)
    jam_keluar = Column("jam_absen_keluar", Time)
    keterangan = Column("keterangan", String(100))
    user_id = Column("user_id", ForeignKey("user.id"))
    shift_id = Column("shift_id", ForeignKey("shift.id"))
    kehadiran_id = Column("kehadiran_id", ForeignKey("kehadiran.id"))

    # Relation
    absen_user = relationship(
        "AbsenUser",
        backref="absen_user_id",
        foreign_keys=[user_id]
    )

    absen_shift = relationship(
        "AbsenShift",
        backref="absen_shift_id",
        foreign_keys=[shift_id]
    )

    absen_kehadiran = relationship(
        "AbsenKehadiran",
        backref="absen_kehadiran_id",
        foreign_keys=[kehadiran_id]
    )