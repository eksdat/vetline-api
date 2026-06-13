from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Animal
from app.schemas import AnimalCreate, AnimalUpdate


def create_animal(session: Session, animal_in: AnimalCreate) -> Animal:
    # Separar CRUD da rota facilita teste e deixa a regra de acesso ao banco mais limpa
    animal = Animal(**animal_in.model_dump())
    session.add(animal)
    session.commit()
    session.refresh(animal)
    return animal


def list_animals(session: Session, skip: int = 0, limit: int = 50) -> list[Animal]:
    # Uso paginacao basica para nao carregar tudo de uma vez
    statement = select(Animal).offset(skip).limit(limit).order_by(Animal.id)
    return list(session.scalars(statement))


def get_animal(session: Session, animal_id: int) -> Animal | None:
    return session.get(Animal, animal_id)


def update_animal(session: Session, animal: Animal, animal_in: AnimalUpdate) -> Animal:
    # Atualizo apenas os campos que vieram na requisicao
    updates = animal_in.model_dump(exclude_unset=True)
    for field_name, value in updates.items():
        setattr(animal, field_name, value)

    session.commit()
    session.refresh(animal)
    return animal


def delete_animal(session: Session, animal: Animal) -> None:
    session.delete(animal)
    session.commit()