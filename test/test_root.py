def test_root(guest):
    response = guest.get("/")
    assert response.status_code == 404
