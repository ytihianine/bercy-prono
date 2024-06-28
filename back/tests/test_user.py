def test_user_registration(client, user_enregistrement):
    response = client.post(
        "/api/v1/user/enregistrement",
        data=user_enregistrement,
        content_type="application/json",
    )
    assert response.status_code == 201
