"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from .common import status  # HTTP Status Codes
from service.models import Recommendation

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Recommendations REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )

######################################################################
# CREATE A RECOMMENDATION
######################################################################
@app.route("/recommendations", methods=["POST"])
def create_recommendations():
    """
    Creates a Recommendation
    This endpoint will create a Recommendation based the data in the body that is posted
    """
    app.logger.info("Request to create a recommendation")
    check_content_type("application/json")
    recommendation = Recommendation()
    recommendation.deserialize(request.get_json())
    recommendation.create()
    message = recommendation.serialize()
    # location_url = url_for("get_recommendation", recommendation_id=recommendation.id, _external=True)

    app.logger.info("Recommendation with ID [%s] created.", recommendation.id)
    return jsonify(message), status.HTTP_201_CREATED #, {"Location": location_url}



######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Recommendation.init_db(app)

def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
    
    
    #------------------------------------------------------------------
    # READ A RECOMMENDATION
    #------------------------------------------------------------------
    @api.doc('get_recommendations')
    @api.response(404, 'Recommendation not found')
    @api.marshal_with(recommendation_model)
    def getRecName(self, name):
        """
        Read a Recommendation
        This will return a Recommendation based on it's name.
        """
        app.logger.info("Request to Read a recommendation with name [%s]", name)
        recommendation = Recommendation.find(name)
        rec_name = recommendation.recommendationName
        if not recommendation:
            api.abort(status.HTTP_404_NOT_FOUND, "Recommendation with name '{}' was not found.".format(name))
        return rec_name, status.HTTP_200_OK
