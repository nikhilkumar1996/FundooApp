import json
from main import app


def test_get_user_route():
    client = app.test_client()
    url = '/get_all_users'

    response = client.get(url)
    res = json.loads(response.data).get('message')
    assert type(res[3]) is dict
    assert res[3]['Email'] == "kumar@gmail.com"
    assert res[3]['Password'] == "kumar123"
    assert response.status_code == 200
    assert type(res) is list


def test_register_user():
    client = app.test_client()
    url = '/register'

    user_data = {
        "Email": "nikhilkumar1097@gmail.com",
        "Name": "Nikhil",
        "PhoneNo": "7898675234",
        "Password": "nikhil123"

    }
    resource = client.post(url, data=json.dumps(user_data))
    assert resource.status_code == 409



