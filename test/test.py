import pytest

import app


def test_get_ad():
    data = {"id": "1"}
    res = app.client.post('/get_ad', json=data)
    assert res.status_code == 200
    assert list(res.get_json().keys()) == ["description", "id", "name", "price"]
    assert res.get_json()["id"] == 1


def test_get_ad1():
    data = {"id": "500", "fields": True}
    res = app.client.post('/get_ad', json=data)
    assert res.status_code == 200
    assert list(res.get_json().keys()) == ["description", "id", "main_url", "name", "price",  "url2", "url3"]
    assert res.get_json()["id"] == 1

def test_get_ad_bad_request():
    data = {"id": "500"}
    res = app.client.post('/get_ad', json=data)
    assert res.status_code == 404
    assert res.get_json() == {
        "error": "404 Not Found: Ad not found"
    }
    res = app.client.get('/get_ad')
    assert res.status_code == 404
    assert res.get_json() == {
        "error": "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
    }

def test_get_ads():
    res = app.client.get('/get_ads')
    assert res.status_code == 400

    data = {"page": "1"}
    res = app.client.post('/get_ads', json=data)
    assert res.get_json()[0] == "page 1. Ads from 1 to 10"
    assert len(res.get_json()[1]) <= 10


def test_get_ads_sort_price_asc():
    data = {"page": "1", "sort": "price_asc"}
    res = app.client.post('/get_ads', json=data)
    assert res.get_json()[0] == "page 1. Ads from 1 to 10"
    assert len(res.get_json()[1]) <= 10
    assert res.get_json()[1][1]["price"] <= res.get_json()[1][2]["price"]


def test_get_ads_sort_price_desc():
    data = {"page": "1", "sort": "price_desc"}
    res = app.client.post('/get_ads', json=data)
    assert res.get_json()[0] == "page 1. Ads from 1 to 10"
    assert len(res.get_json()[1]) <= 10
    assert res.get_json()[1][1]["price"] >= res.get_json()[1][2]["price"]


def test_get_ads_bad_request():
    data = {"page": "1", "sort": "asd"}
    res = app.client.post('/get_ads', json=data)
    assert res.status_code == 400
    assert res.get_json() == {
    "error": "400 Bad Request: incorrect sorting values entered or do not enter a value pagination"
}

def test_post_ad_bad_request():
    data = {"name": "kv41egr"}
    res = app.client.post('/add_ad', json=data)
    assert res.status_code == 400
    assert res.get_json() == {
        "error": "400 Bad Request: name or price values is None"
    }
    data = {"price": 5000}
    res = app.client.post('/add_ad', json=data)
    assert res.status_code == 400
    assert res.get_json() == {
        "error": "400 Bad Request: name or price values is None"
    }


def test_post_ad():
    data = {"name": "k1v416egr", "price": "3170", "description": "adsfgads", "main_url": "mail"}
    res = app.client.post('/add_ad', json=data)
    assert res.status_code == 200
    assert len(res.get_json()) == 1
    assert list(res.get_json().keys()) == ["id"]
    app.client.delete(f'/del_ad/{list(res.get_json().values())[0]}')