"""
This is the milestones module and supports all the REST actions for the
milestones data
"""

from flask import make_response, abort
from config import db
from models import Development, DevelopmentSchema


def read_all():
    """
    This function responds to a request for /api/milestones
    with the complete lists of milestones

    :return:        json string of list of milestones
    """
    # Create the list of milestones from our data
    milestones = Development.query.order_by(Development.name).all()

    # Serialize the data for the response
    development_schema = DevelopmentSchema(many=True)
    data = development_schema.dump(milestones)
    return data


def read_one(development_id):
    """
    This function responds to a request for /api/milestones/{development_id}
    with one matching development from milestones

    :param development_id:   Id of development to find
    :return:            development matching id
    """
    # Get the development requested
    development = Development.query.filter(Development.development_id == development_id).one_or_none()

    # Did we find a development?
    if development is not None:

        # Serialize the data for the response
        development_schema = DevelopmentSchema()
        data = development_schema.dump(development)
        return data

    # Otherwise, nope, didn't find that development
    else:
        abort(
            404,
            "development not found for Id: {development_id}".format(development_id=development_id),
        )


def create(development):
    """
    This function creates a new development in the milestones structure
    based on the passed in development data

    :param development:  development to create in milestones structure
    :return:        201 on success, 406 on development exists
    """
    name = development.get("name")
    city = development.get("city")
    description = development.get("description")

    existing_development = (
        Development.query.filter(Development.name == name)
        .filter(Development.city == city)
        .filter(Development.description == description)
        .one_or_none()
    )

    # Can we insert this development?
    if existing_development is None:

        # Create a development instance using the schema and the passed in development
        schema = DevelopmentSchema()
        new_development = Development(name=name, city=city, description=description)

        # Add the development to the database
        db.session.add(new_development)
        db.session.commit()

        # Serialize and return the newly created development in the response
        data = schema.dump(new_development)

        return data, 201

    # Otherwise, nope, development exists already
    else:
        abort(
            409,
            "development {name} {city} {description} exists already".format(
                name=name, city=city, description=description
            ),
        )


def update(development_id, development):
    """
    This function updates an existing development in the milestones structure
    Throws an error if a development with the name we want to update to
    already exists in the database.

    :param development_id:   Id of the development to update in the milestones structure
    :param development:      development to update
    :return:            updated development structure
    """
    # Get the development requested from the db into session
    update_development = Development.query.filter(
        Development.development_id == development_id
    ).one_or_none()

    # Try to find an existing development with the same name as the update
    name = development.get("name")
    city = development.get("city")
    description = development.get("description")

    existing_development = (
        Development.query.filter(Development.name == name)
        .filter(Development.city == city)
        .filter(Development.description == description)
        .one_or_none()
    )

    # Are we trying to find a development that does not exist?
    if update_development is None:
        abort(
            404,
            "development not found for Id: {development_id}".format(development_id=development_id),
        )

    # Would our update create a duplicate of another development already existing?
    elif (
        existing_development is not None and existing_development.development_id != development_id
    ):
        abort(
            409,
            "development {name} {city} {description} exists already".format(
                name=name, city=city, description=description
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in development into a db object
        schema = DevelopmentSchema()
        updt_development = Development(name=name, city=city, description=description , development_id=development_id)

        # merge the new object into the old and commit it to the db
        db.session.merge(updt_development)
        db.session.commit()

        # return updated development in the response
        data = schema.dump(update_development)

        return data, 200


def delete(development_id):
    """
    This function deletes a development from the milestones structure

    :param development_id:   Id of the development to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the development requested
    development = Development.query.filter(Development.development_id == development_id).one_or_none()

    # Did we find a development?
    if development is not None:
        db.session.delete(development)
        db.session.commit()
        return make_response(
            "development {development_id} deleted".format(development_id=development_id), 200
        )

    # Otherwise, nope, didn't find that development
    else:
        abort(
            404,
            "development not found for Id: {development_id}".format(development_id=development_id),
        )
