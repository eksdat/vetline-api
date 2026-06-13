from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import create_animal, delete_animal, get_animal, list_animals, update_animal
from app.database import get_session
from app.schemas import AnimalCreate, AnimalRead, AnimalUpdate


router = APIRouter(prefix="/animals", tags=["animals"])


@router.post("", response_model=AnimalRead, status_code=status.HTTP_201_CREATED)
def create_animal_route(
    animal_in: AnimalCreate,
    session: Session = Depends(get_session),
) -> AnimalRead:
    # A rota so valida a entrada e delega a persistencia para a camada de CRUD
    return create_animal(session, animal_in)


@router.get("", response_model=list[AnimalRead])
def list_animals_route(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    session: Session = Depends(get_session),
) -> list[AnimalRead]:
    return list_animals(session, skip=skip, limit=limit)


@router.get("/{animal_id}", response_model=AnimalRead)
def get_animal_route(
    animal_id: int,
    session: Session = Depends(get_session),
) -> AnimalRead:
    animal = get_animal(session, animal_id)
    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    return animal


@router.patch("/{animal_id}", response_model=AnimalRead)
def update_animal_route(
    animal_id: int,
    animal_in: AnimalUpdate,
    session: Session = Depends(get_session),
) -> AnimalRead:
    animal = get_animal(session, animal_id)
    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    return update_animal(session, animal, animal_in)


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal_route(
    animal_id: int,
    session: Session = Depends(get_session),
) -> None:
    animal = get_animal(session, animal_id)
    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    # Delete e definitivo, entao eu valido primeiro se o registro existe
    delete_animal(session, animal)