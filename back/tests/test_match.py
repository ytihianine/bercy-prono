def test_match_info(client, match_informations):
    response = client.get("/api/v1/match/information")
    assert match_informations == response.data
