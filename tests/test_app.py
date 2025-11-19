from http import HTTPStatus


def test_index_should_return_ok(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK


def test_index_should_return_welcome_message(client):
    response = client.get("/")

    assert response.json() == {"message": "welcome to the weather api v1."}
