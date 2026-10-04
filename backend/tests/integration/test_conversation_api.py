from fastapi.testclient import (
    TestClient,
)

from app.main import app


client = TestClient(app)


def test_text_to_gloss():
    response = client.post(
        "/api/v1/conversation/text-to-gloss",
        params={
            "text": "Where is the pain?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["glosses"] == [
        "WHERE",
        "PAIN",
    ]


def test_conversation_message():
    response = client.post(
        "/api/v1/conversation/message",
        json={
            "id": "test-1",
            "source": "speech",
            "text": "I have pain",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["source"] == "speech"
    assert "PAIN" in data["glosses"]
