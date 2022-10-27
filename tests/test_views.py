import pytest
from flask import url_for


def test_gen_scrape_request(client):

    response = client.post('/gen_scrape_request', data={
        "social-media" : "truth-social",
        "username": 'dummy user',
        "password": 'hehe',
        "terms":['t1', 't2', 't3']
    })
    assert response.status_code == 200