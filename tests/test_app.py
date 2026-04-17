from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_list(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    json_payload = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in json_payload
    assert json_payload[expected_activity]["max_participants"] == 12


def test_signup_for_activity_succeeds(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "newstudent@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    activity_name = quote("Astronomy Club", safe="")
    email = "newstudent@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "michael@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_for_activity_succeeds(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "michael@mergington.edu"
    unregister_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(unregister_url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"


def test_unregister_when_not_signed_up_returns_400(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "newstudent@mergington.edu"
    unregister_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(unregister_url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = quote("Astronomy Club", safe="")
    email = "newstudent@mergington.edu"
    unregister_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(unregister_url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
