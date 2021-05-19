import datetime

from django.conf import global_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import override_settings

from chipy_org.apps.meetings.models import Meeting, Topic

import pytest


User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def with_static_files():
    with override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE):
        yield


@pytest.fixture
def user():
    return User.objects.create(username="chipy")


@pytest.mark.parametrize("url_name", ("future_meetings", "past_meetings", "past_topics"))
def test_simple_read_routes_respond(url_name, client):
    response = client.get(reverse(url_name), follow=True)
    assert response.status_code == 200


def test_topic_read_routes_respond(client):
    topic = Topic.objects.create(title="test topic")
    response = client.get(reverse("past_topic", args=[topic.id]), follow=True)
    assert response.status_code == 200


def test_meeting_read_routes_respond(client):
    meeting = Meeting.objects.create(when=datetime.datetime.now())
    response = client.get(reverse("meeting", args=[meeting.id]), follow=True)
    assert response.status_code == 200

def test_authentication_required_for_proposing_topic(client, user):
    response = client.get(reverse("propose_topic"))
    assert response.status_code == 302

    client.force_login(user)

    response = client.get(reverse("propose_topic"), follow=True)
    assert response.status_code == 200
