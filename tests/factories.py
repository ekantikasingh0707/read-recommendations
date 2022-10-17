"""
Test Factory to make fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyChoice
from service.models import Recommendation, RecommendationType


class RecommendationFactory(factory.Factory):
    """Creates fake recommendations that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Recommendation

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    recommendationId = factory.Sequence(lambda n: n)
    recommendationName = factory.Faker("name")
    type = FuzzyChoice(choices=[RecommendationType.UPSELL, RecommendationType.CROSSSELL, RecommendationType.ACCESSORY])
    number_of_likes = factory.Sequence(lambda n:n)
