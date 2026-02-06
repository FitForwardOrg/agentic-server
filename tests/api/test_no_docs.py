def test_no_docs(client):
    # Verify docs are disabled
    response = client.get("/docs")
    assert response.status_code == 404

    response = client.get("/redoc")
    assert response.status_code == 404
