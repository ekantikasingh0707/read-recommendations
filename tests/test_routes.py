"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import db, init_db, Recommendation
from tests.factories import RecommendationsFactory
from service.common import status  # HTTP Status Codes

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/recommendations"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)


    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        self.client = app.test_client()
        db.session.query(Recommendation).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
    
    def _create_recommendation(self, count):
        """Factory method to create recommendations in bulk"""
        recommendations = []
        for _ in range(count):
            test_recommendation = RecommendationsFactory()
            response = self.client.post(BASE_URL, json=test_recommendation.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test recommendation"
            )
            new_recommendation = response.get_json()
            test_recommendation.id = new_recommendation["id"]
            recommendations.append(test_recommendation)
        return recommendations

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
    def test_create_recommendation(self):
        """It should Create a new Recommendation"""
        test_recommendation = RecommendationsFactory()
        logging.debug("Test Recommendation: %s", test_recommendation.serialize())
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_recommendation = response.get_json()
        self.assertEqual(new_recommendation["id"], test_recommendation.id)
        self.assertEqual(new_recommendation["name"], test_recommendation.name)
        self.assertEqual(new_recommendation["recmmendationId"], test_recommendation.recmmendationId)
        self.assertEqual(new_recommendation["recmmendationName"], test_recommendation.recmmendationName)
        self.assertEqual(new_recommendation["type"], test_recommendation.type)
        self.assertEqual(new_recommendation["number_of_likes"], test_recommendation.number_of_likes)

        # Check that the location header was correct
        """response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_recommendation = response.get_json()
        self.assertEqual(new_recommendation["id"], test_recommendation.id)
        self.assertEqual(new_recommendation["name"], test_recommendation.name)
        self.assertEqual(new_recommendation["recommendId"], test_recommendation.recommendId)
        self.assertEqual(new_recommendation["recommendedName"], test_recommendation.recommendedName)
        self.assertEqual(new_recommendation["numberOfLikes"], test_recommendation.numberOfLikes)
        self.assertEqual(new_recommendation["recommendationType"], test_recommendation.recommendationType)"""

