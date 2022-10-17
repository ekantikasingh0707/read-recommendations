"""
Models for YourResourceModel

All of the models are stored in this module
"""
from importlib.util import set_loader
import logging
from enum import Enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

class RecommendationType(Enum):
    """Enumeration of valid Recommendation Types"""
    CROSSSELL = 0
    UPSELL = 1
    ACCESSORY = 2

class Recommendation(db.Model):
    """
    Class that represents a Recommendation
    """
    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    recommendationId = db.Column(db.Integer)
    recommendationName = db.Column(db.String(63))
    type = db.Column(
        db.Enum(RecommendationType), nullable=False, server_default=(RecommendationType.UPSELL.name)
    )
    number_of_likes = db.Column(db.Integer)

    def __repr__(self):
        return f"<Recommendation {self.name} id=[{self.id}] RecommendationId=[{self.recommendationId}] RecommendationName=[{self.recommendationName}] RecommendationType=[{self.type}] number_of_likes=[{self.number_of_likes}]>"

    def create(self):
        """
        Creates a Recommendation to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Recommendation to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a YourResourceModel from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a YourResourceModel into a dictionary """
        # return {"id": self.id, "name": self.name}
        return {
            "id": self.id,
            "name": self.name,
            "recommendationId": self.recommendationId,
            "recommendationName": self.recommendationName,
            "type": self.type.name,
            "number_of_likes": self.number_of_likes
        }

    def deserialize(self, data: dict):
        """
        Deserializes a YourResourceModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.number_of_likes = data["number_of_likes"]
            self.recommendationId = data["recommendationId"]
            self.recommendationName = data["recommendationName"]
            self.type = getattr(RecommendationType, data["type"])
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError("Invalid Recommendation: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Recommendation: body of request contained bad or no data " + str(error)
            ) from error
        return self

    @classmethod
    def init_db(cls, app: Flask):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """Returns all of the recommendations in the database"""
        logger.info("Processing all recommendations")
        return cls.query.all()

    @classmethod
    def find(cls, reco_id: int):
        """Finds a recmmendation by it's ID
        :param reco_id: the id of the recmmendation to find
        :type reco_id: int
        :return: an instance with the reco_id, or None if not found
        :rtype: recmmendation
        """
        logger.info("Processing lookup for id %s ...", reco_id)
        return cls.query.get(reco_id)

    @classmethod
    def find_or_404(cls, recommendation_id: int):
        """Finds a recmmendation by it's ID
        :param reco_id: the id of the recmmendation to find
        :type reco_id: int
        :return: an instance with the reco_id, or 404_NOT_FOUND if not found
        :rtype: recmmendation
        """
        logger.info("Processing lookup or 404 for id %s ...", recommendation_id)
        return cls.query.get_or_404(recommendation_id)

    @classmethod
    def find_by_name(cls, name)-> list:
        """Returns all recmmendationModels with the given name

        Args:
            name (string): the name of the recmmendationModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
    
    @classmethod
    def find_by_type(cls, type: RecommendationType = RecommendationType.UPSELL) -> list:
        """Returns all recmmendationModels by their Type
        :param gender: values are ['UPSELL', 'CROSSSELL']
        :type available: enum
        :return: a collection of recommendations that are available
        :rtype: list
        """
        logger.info("Processing type query for %s ...", type.name)
        return cls.query.filter(cls.type == type)