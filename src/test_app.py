import pytest
from flask import json

from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_returns_matching_isbn(client):
    response = client.get("/books/140003065X")

    assert response.status == "200 OK"

    data = json.loads(response.data)

    assert_resp_equal(
        {"title": "A Fine Balance", "isbn": "140003065X"}, data,
    )


def test_returns_404_if_not_found(client):
    response = client.get("/books/NaN")

    assert response.status == "404 NOT FOUND"


def test_returns_book_with_author_present(client):
    response = client.get("/books/140003065X?includeAuthor=1")

    assert response.status == "200 OK"

    data = json.loads(response.data)

    assert_resp_equal(
        {
            "isbn": "140003065X",
            "title": "A Fine Balance",
            "author": {"id": "B000AQTH1C", "name": "Rohinton Mistry"},
        },
        data,
    )


def test_returns_book_with_author_absent(client):
    response = client.get("/books/0061624268?includeAuthor=1")

    assert response.status == "200 OK"

    data = json.loads(response.data)

    assert_resp_equal(
        {
            "title": "Microserfs",
            "isbn": "0061624268",
            "author": {},  # note: intentiontionally absent; author data not available
        },
        data,
    )


def test_returns_book_with_1_level_of_related_books_present(client):
    response = client.get("/books/140003065X?includeRelated=1")

    assert response.status == "200 OK"

    data = json.loads(response.data)

    assert_resp_equal(
        {
            "title": "A Fine Balance",
            "isbn": "140003065X",
            "related": [{"isbn": "0061624268", "title": "Microserfs"}],
        },
        data,
    )


def test_returns_book_with_2_levels_of_related_books_present_part_1_of_2(client):
    response = client.get("/books/140003065X?includeRelated=2")

    assert response.status == "200 OK"

    data = json.loads(response.data)

    assert_resp_equal(
        {
            "title": "A Fine Balance",
            "isbn": "140003065X",
            "related": [
                {"isbn": "0061624268", "title": "Microserfs"},
                {"isbn": "031205436X", "title": "Generation X"},
            ],
        },
        data,
    )


def test_returns_book_with_2_levels_of_related_books_present_part_2_of_2(client):
    response = client.get("/books/0061624268?includeRelated=2")

    assert response.status == "200 OK"

    data = json.loads(response.data)

    assert_resp_equal(
        {
            "title": "Microserfs",
            "isbn": "0061624268",
            "related": [
                {"isbn": "140003065X", "title": "A Fine Balance"},
                {"isbn": "031205436X", "title": "Generation X"},
                {"isbn": "1503214133", "title": "Anne of Green Gables"},
            ],
        },
        data,
    )


def test_returns_book_with_1_level_of_related_books_including_authors(client):
    response = client.get("/books/140003065X?includeRelated=1&includeAuthor=1")

    assert response.status == "200 OK"

    data = json.loads(response.data)

    assert_resp_equal(
        {
            "title": "A Fine Balance",
            "isbn": "140003065X",
            "related": [{"isbn": "0061624268", "title": "Microserfs", "author": {}}],
            "author": {"id": "B000AQTH1C", "name": "Rohinton Mistry"},
        },
        data,
    )


def assert_resp_equal(expected, data):
    expected_related = expected.pop("related", None)
    data_related = data.pop("related", None)
    assert expected == data

    if expected_related is None:
        assert data_related is None
    elif isinstance(expected_related, list):
        key = lambda data: data["isbn"]
        assert isinstance(data_related, list)
        assert sorted(expected_related, key=key) == sorted(data_related, key=key)
