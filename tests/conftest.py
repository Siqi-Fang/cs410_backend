from flask import Flask, url_for
import pytest
import sys

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_gen_scrape_request(client):
    url = url_for('gen_scrape_request')
    response = client.post(url, data={
        "social-media" : "truth-social",
        "username": 'dummyuser',
        "password": 'hehe',
        "terms":['t1', 't2', 't3']
    })
    assert response.status_code == 200