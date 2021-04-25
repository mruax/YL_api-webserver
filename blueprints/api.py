# Flask functions import:
from urllib import request

from flask_restful import reqparse, abort, Api, Resource, marshal
from flask import Blueprint, render_template, jsonify

# Database functions import:
from data import Company, Type, User
from data.db_session import create_session
from data.items import Item

# Datetime import:
from datetime import date

# This blueprint describes api functions:
api_blueprint = Blueprint(
    'api_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')

# Request parser for 'POST' request:
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('amount', required=True)
parser.add_argument('company', required=True)
parser.add_argument('date', required=True)
parser.add_argument('description', required=True)
parser.add_argument('type', required=True)
parser.add_argument('creator', required=True)


def abort_if_item_not_found(item_id):
    """
    This function check item by id

    :param item_id: Requested item id
    :type item_id: int
    :return: abort(404) if not found
    """
    db_sess = create_session()  # Create database session
    # item = db_sess.query(Item).get(item_id)  # Get item from database by id
    item = db_sess.query(Item).filter(Item.id == item_id).first()
    db_sess.close()  # Shut down database session
    if not item:
        abort(404, message=f"Item {item_id} not found")
        return False


class ItemResource(Resource):
    def get(self, item_id):
        if not abort_if_item_not_found(item_id):
            db_sess = create_session()  # Create database session
            item = db_sess.query(Item).get(item_id)  # Get item from database by id
            db_sess.close()  # Shut down database session
            return jsonify({'item': item.to_dict(only=('name', 'amount', 'company', 'date', 'description', 'type', 'creator'))})


    def delete(self, item_id):
        if not abort_if_item_not_found(item_id):
            db_sess = create_session()  # Create database session
            item = db_sess.query(Item).get(item_id)
            db_sess.delete(item)
            db_sess.commit()
            db_sess.close()  # Shut down database session
            return jsonify({'success': 'OK'})


    def put(self, item_id):
        if not abort_if_item_not_found(item_id):
            db_sess = create_session()  # Create database session
            item = db_sess.query(Item).filter(
                    Item.id == item_id).first()  # Get item from database by id
            args = parser.parse_args()
            obj = db_sess.query(Item).order_by(
                Item.id.desc()).first()
            company = db_sess.query(Company).filter(
                    Company.name == item.company).first()
            item_type = db_sess.query(Type).filter(
                    Type.name == item.type).first()
            creator = db_sess.query(User).filter(
                    User.login == item.creator).first()
            if item.name.isalpha() and item.amount.isdigit() and \
                    company and not item.description.isdigit() and \
                    item_type and creator:
                item.name = args['name'],
                item.amount = args['amount'],
                item.company = args['company'],
                item.date = date(*list(map(int, args['date'].split('-')))),
                item.description = args['description'],
                item.type = args['type'],
                item.creator = args['creator']
                # setattr(item, "id", obj.id)
                # setattr(item, "name", args['name'])
                # setattr(item, "amount", args['amount'])
                # setattr(item, "company", args['company'])
                # # setattr(item, "date", date(*list(map(int, args['date'].split('-')))))
                # setattr(item, "date", args['date'])
                # setattr(item, "type", args['type'])
                # setattr(item, "creator", args['creator'])
            db_sess.commit()
            db_sess.close()  # Shut down database session
            return jsonify({'success': 'OK'})



class ItemsListResource(Resource):
    def get(self):
        db_sess = create_session()  # Create database session
        items = db_sess.query(Item).all()
        db_sess.close()  # Shut down database session
        return jsonify({'items': [item.to_dict(
            only=('name', 'amount', 'company', 'date', 'description', 'type',
                  'creator')) for item in items]})

    def post(self):
        args = parser.parse_args()
        db_sess = create_session()  # Create database session
        try:
            item = Item(
                name=args['name'],
                amount=args['amount'],
                company=args['company'],
                date=date(*list(map(int, args['date'].split('-')))),
                description=args['description'],
                type = args['type'],
                creator = args['creator']
            )
            company = db_sess.query(Company).filter(Company.name == item.company).first()
            item_type = db_sess.query(Type).filter(Type.name == item.type).first()
            creator = db_sess.query(User).filter(User.login == item.creator).first()
            if item.name.isalpha() and item.amount.isdigit() and company and \
                    not item.description.isdigit() and \
                    item_type and creator:
                db_sess.add(item)
                db_sess.commit()
                db_sess.close()  # Shut down database session
                return jsonify({'success': 'OK'})
        except Exception:
            db_sess.close()  # Shut down database session
            return jsonify({'failure': 'Bad request'})
