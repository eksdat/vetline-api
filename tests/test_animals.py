from fastapi.testclient import TestClient

BASE = "/api/v1/animals"

LION = {
    "common_name": "Leão",
    "scientific_name": "Panthera leo",
    "genus": "Panthera",
    "sex": "male",
    "life_stage": "adult",
    "is_pregnant": False,
    "is_neutered": False,
}


# POST /animals


def test_create_animal_returns_201(client: TestClient) -> None:
    response = client.post(BASE, json=LION)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["common_name"] == "Leão"
    assert "created_at" in data
    assert "updated_at" in data


def test_create_animal_strips_whitespace(client: TestClient) -> None:
    response = client.post(BASE, json={**LION, "common_name": "  Tigre  "})
    assert response.status_code == 201
    assert response.json()["common_name"] == "Tigre"


def test_create_animal_common_name_too_short_returns_422(client: TestClient) -> None:
    response = client.post(BASE, json={**LION, "common_name": "X"})
    assert response.status_code == 422


def test_create_animal_invalid_sex_returns_422(client: TestClient) -> None:
    response = client.post(BASE, json={**LION, "sex": "masculino"})
    assert response.status_code == 422


def test_create_animal_invalid_life_stage_returns_422(client: TestClient) -> None:
    response = client.post(BASE, json={**LION, "life_stage": "baby"})
    assert response.status_code == 422


def test_create_animal_missing_required_field_returns_422(client: TestClient) -> None:
    payload = {k: v for k, v in LION.items() if k != "common_name"}
    response = client.post(BASE, json=payload)
    assert response.status_code == 422



# GET /animals


def test_list_animals_empty(client: TestClient) -> None:
    response = client.get(BASE)
    assert response.status_code == 200
    assert response.json() == []


def test_list_animals_returns_created(client: TestClient) -> None:
    client.post(BASE, json=LION)
    response = client.get(BASE)
    assert len(response.json()) == 1


def test_list_animals_skip(client: TestClient) -> None:
    client.post(BASE, json=LION)
    client.post(BASE, json={**LION, "common_name": "Tigre", "scientific_name": "Panthera tigris"})
    response = client.get(f"{BASE}?skip=1")
    assert len(response.json()) == 1
    assert response.json()[0]["common_name"] == "Tigre"


def test_list_animals_limit(client: TestClient) -> None:
    for i in range(3):
        client.post(BASE, json={**LION, "common_name": f"Animal {i}", "scientific_name": f"Species {i}"})
    response = client.get(f"{BASE}?limit=2")
    assert len(response.json()) == 2


def test_list_animals_limit_above_max_returns_422(client: TestClient) -> None:
    response = client.get(f"{BASE}?limit=201")
    assert response.status_code == 422


def test_list_animals_limit_zero_returns_422(client: TestClient) -> None:
    response = client.get(f"{BASE}?limit=0")
    assert response.status_code == 422


def test_list_animals_negative_skip_returns_422(client: TestClient) -> None:
    response = client.get(f"{BASE}?skip=-1")
    assert response.status_code == 422


# GET /animals/{id}


def test_get_animal_found(client: TestClient) -> None:
    client.post(BASE, json=LION)
    response = client.get(f"{BASE}/1")
    assert response.status_code == 200
    assert response.json()["scientific_name"] == "Panthera leo"


def test_get_animal_not_found_returns_404(client: TestClient) -> None:
    response = client.get(f"{BASE}/999")
    assert response.status_code == 404


# PATCH /animals/{id}


def test_patch_animal_updates_only_provided_fields(client: TestClient) -> None:
    client.post(BASE, json=LION)
    response = client.patch(f"{BASE}/1", json={"is_neutered": True})
    assert response.status_code == 200
    data = response.json()
    assert data["is_neutered"] is True
    assert data["common_name"] == "Leão"  # campo não enviado permanece intacto


def test_patch_animal_not_found_returns_404(client: TestClient) -> None:
    response = client.patch(f"{BASE}/999", json={"is_neutered": True})
    assert response.status_code == 404


def test_patch_animal_invalid_field_returns_422(client: TestClient) -> None:
    client.post(BASE, json=LION)
    response = client.patch(f"{BASE}/1", json={"common_name": "X"})
    assert response.status_code == 422


def test_patch_animal_notes_field(client: TestClient) -> None:
    client.post(BASE, json=LION)
    response = client.patch(f"{BASE}/1", json={"notes": "Observado em campo aberto"})
    assert response.status_code == 200
    assert response.json()["notes"] == "Observado em campo aberto"


# DELETE /animals/{id}


def test_delete_animal_returns_204(client: TestClient) -> None:
    client.post(BASE, json=LION)
    response = client.delete(f"{BASE}/1")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_animal_not_found_returns_404(client: TestClient) -> None:
    response = client.delete(f"{BASE}/999")
    assert response.status_code == 404


def test_delete_animal_removes_from_list(client: TestClient) -> None:
    client.post(BASE, json=LION)
    client.delete(f"{BASE}/1")
    assert client.get(BASE).json() == []


def test_delete_animal_get_after_delete_returns_404(client: TestClient) -> None:
    client.post(BASE, json=LION)
    client.delete(f"{BASE}/1")
    assert client.get(f"{BASE}/1").status_code == 404
