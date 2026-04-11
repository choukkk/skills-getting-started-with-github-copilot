def test_root_redirect(client):
    response = client.get("/", allow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == 12


def test_signup_for_activity(client):
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    follow_up = client.get("/activities")
    assert email in follow_up.json()["Chess Club"]["participants"]


def test_duplicate_signup_returns_400(client):
    email = "duplicate@mergington.edu"

    first_response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert first_response.status_code == 200

    duplicate_response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
