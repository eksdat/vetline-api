# Vetline API

Projeto de estudo para montar um portfolio backend com fundamentos de ciência da computação, código limpo e uma API pensada para crescer.

## Objetivo

Gerenciar animais com foco em dados úteis para clínica, resgate ou zoológico.

Campos já previstos:

- nome comum
- nome científico
- gênero/taxonomia
- sexo
- fase de vida como filhote ou adulto
- status de prenhez
- castração
- observações

## Stack inicial

- FastAPI
- SQLite
- SQLAlchemy
- Pydantic

## Como rodar

1. Instale as dependências listadas em `dep.txt`.
2. Execute a aplicação com `uvicorn app.main:app --reload`.
3. Abra `http://127.0.0.1:8000/docs`.

## Próximos passos sugeridos

- criar validações de domínio mais fortes
- adicionar filtros por espécie, sexo e fase de vida
- separar camadas de serviço e repositório
- criar testes automatizados
