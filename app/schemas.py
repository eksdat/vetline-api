from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import LifeStageEnum, SexEnum


def _strip_text(value: str) -> str:
    # Pequena normalizacao para remover espacos extras vindos do formulario ou JSON
    return value.strip()


class AnimalBase(BaseModel):
    # Este schema concentra os campos comuns entre criacao e leitura
    common_name: str = Field(min_length=2, max_length=120)
    scientific_name: str = Field(min_length=2, max_length=120)
    genus: str = Field(min_length=2, max_length=80)
    sex: SexEnum = SexEnum.unknown
    life_stage: LifeStageEnum = LifeStageEnum.adult
    is_pregnant: bool = False
    is_neutered: bool = False
    notes: str | None = Field(default=None, max_length=500)

    @field_validator("common_name", "scientific_name", "genus")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return _strip_text(value)

    @field_validator("notes")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        return _strip_text(value) if value is not None else value


class AnimalCreate(AnimalBase):
    pass


class AnimalUpdate(BaseModel):
    # No update eu deixo tudo opcional para editar so o que mudou
    common_name: str | None = Field(default=None, min_length=2, max_length=120)
    scientific_name: str | None = Field(default=None, min_length=2, max_length=120)
    genus: str | None = Field(default=None, min_length=2, max_length=80)
    sex: SexEnum | None = None
    life_stage: LifeStageEnum | None = None
    is_pregnant: bool | None = None
    is_neutered: bool | None = None
    notes: str | None = Field(default=None, max_length=500)

    @field_validator("common_name", "scientific_name", "genus")
    @classmethod
    def normalize_text(cls, value: str | None) -> str | None:
        return _strip_text(value) if value is not None else value

    @field_validator("notes")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        return _strip_text(value) if value is not None else value


class AnimalRead(AnimalBase):
    # Aqui eu incluo campos gerados pelo banco para retornar a resposta completa
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime