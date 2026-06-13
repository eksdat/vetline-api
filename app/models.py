from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now() -> datetime:
    # Guardar horario em UTC evita confusao quando o projeto crescer
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class SexEnum(str, Enum):
    male = "male"
    female = "female"
    unknown = "unknown"


class LifeStageEnum(str, Enum):
    newborn = "newborn"
    cub = "cub"
    juvenile = "juvenile"
    adult = "adult"
    senior = "senior"


class Animal(Base):
    __tablename__ = "animals"

    # Aqui eu guardo os dados principais do animal que quero controlar no CRUD
    id: Mapped[int] = mapped_column(primary_key=True)
    common_name: Mapped[str] = mapped_column(String(120), nullable=False)
    scientific_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    genus: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    sex: Mapped[SexEnum] = mapped_column(SAEnum(SexEnum), nullable=False, default=SexEnum.unknown)
    life_stage: Mapped[LifeStageEnum] = mapped_column(
        SAEnum(LifeStageEnum), nullable=False, default=LifeStageEnum.adult
    )
    is_pregnant: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_neutered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )