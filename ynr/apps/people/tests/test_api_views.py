from rest_framework.test import APIClient, APIRequestFactory
from django.test import TestCase
from django.utils import timezone
from django.utils.http import urlencode
from candidates.tests.factories import MembershipFactory
from candidates.tests.uk_examples import UK2015ExamplesMixin

from people.models import Person
from people.tests.factories import PersonFactory
from people.api.next.api_views import PersonViewSet


class TestPersonViewSet(UK2015ExamplesMixin, TestCase):
    def setUp(self):
        self.people = PersonFactory.create_batch(size=1001)
        self.timestamp = timezone.now() - timezone.timedelta(hours=1)

    def test_correct_number_of_objects_returned(self):
        """
        Test that only 1000 object in total are returned when the last_updated
        filter is used
        """
        last_updated_querystring = urlencode(
            {"last_updated": self.timestamp.isoformat()}
        )
        test_cases = [
            {"url": "/api/next/people/", "expected": len(self.people)},
            {
                "url": f"/api/next/people/?{last_updated_querystring}",
                "expected": 1000,
            },
        ]
        client = APIClient()
        for case in test_cases:
            url = case["url"]
            expected = case["expected"]
            with self.subTest(msg=f"{url} returns {expected}"):
                response = client.get(url, format="json")
                data = response.json()
                self.assertEqual(data["count"], expected)

    def test_filter_queryset(self):
        """
        Tests two things:
        - A queryset of 1000 objects is returned
        - That ordering by modified is applied
        """
        factory = APIRequestFactory()
        request = factory.get(
            path="/api/next/people/",
            data={"last_updated": self.timestamp.isoformat()},
        )
        request.query_params = request.GET
        view = PersonViewSet(request=request)
        people = Person.objects.all()
        result = view.filter_queryset(queryset=people)

        # update a random person
        person = people.order_by("?").first()
        person.save()

        self.assertEqual(result.count(), 1000)
        # ordering by modified means the person we updated isnt included
        self.assertNotIn(person, result)

    def test_person_with_previous_party_affiliations(self):
        welsh_candidate = PersonFactory.create(id=3009, name="Foo bar")
        welsh_candidacy = MembershipFactory.create(
            person=welsh_candidate,
            post=self.welsh_run_post,
            ballot=self.senedd_ballot,
            party=self.ld_party,
        )
        welsh_candidacy.previous_party_affiliations.add(self.conservative_party)
        response = self.client.get("/api/next/people/3009/")
        data = response.json()
        previous_party_affiliations = data["candidacies"][0][
            "previous_party_affiliations"
        ]
        self.assertEqual(len(previous_party_affiliations), 1)
        self.assertEqual(
            previous_party_affiliations[0]["ec_id"],
            self.conservative_party.ec_id,
        )
