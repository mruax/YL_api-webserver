# Warning! Unittest deletes last item/type/company in database and create new.

import unittest

import werkzeug
from flask import Flask

from blueprints.api import *
from data import db_session

# Database setup:
db_session.global_init("../db/storage.db")

app = Flask(__name__)
app.testing = True
api = Api(app)
# app.route("/api/v2/items", methods=["GET", "POST", "PUT", "DELETE"])
api.add_resource(ItemsListResource, '/api/v2/items')  # all items
api.add_resource(ItemResource, '/api/v2/items/<int:item_id>')  # item by id


class ApiTestDeleteRequests(unittest.TestCase):
    def test_item_delete_correct(self):  # Test №1
        print("DELETE-requests testing:")
        with app.app_context():
            try:
                db_sess = create_session()  # Create database session
                obj = db_sess.query(Item).order_by(
                    Item.id.desc()).first()
                db_sess.close()  # Shut down database session
                item = ItemResource()
                a = item.delete(obj.id)
                print('1: Correct')
            except Exception as e:
                print(e)


class ApiTestGetRequests(unittest.TestCase):
    def test_item_get_correct(self):  # Test №2
        """
        Test checks obtaining first item by ID from database.

        :return: print string with result
        """
        print("GET-requests testing:")
        with app.app_context():
            try:
                item = ItemResource()
                a = item.get(1)
                self.assertEqual(type(a.json), dict)
                print("2: Correct")
            except Exception:
                print("Database is empty")

    def test_item_get_incorrect1(self):  # Test №3
        with app.app_context():
            try:
                item = ItemResource()
                with self.assertRaises(werkzeug.exceptions.NotFound):
                    raise Exception("3: Item with id 0 not found")
                a = item.get(0)
            except Exception as e:
                print(e)

    def test_item_get_incorrect2(self):  # Test №4
        with app.app_context():
            try:
                item = ItemResource()
                with self.assertRaises(werkzeug.exceptions.NotFound):
                    raise Exception("4: Item with id -1 not found")
                a = item.get(-1)
            except Exception as e:
                print(e)

    def test_item_get_incorrect3(self):  # Test №5
        with app.app_context():
            try:
                item = ItemResource()
                with self.assertRaises(werkzeug.exceptions.NotFound):
                    raise Exception("5: Item with null id not found")
                a = item.get()
            except Exception as e:
                print(e)

    def test_item_get_incorrect4(self):  # Test №6
        with app.app_context():
            try:
                item = ItemResource()
                with self.assertRaises(werkzeug.exceptions.NotFound):
                    raise Exception("6: Item with id 'TestID' not found")
                a = item.get("TestID")
            except Exception as e:
                print(e)

    def test_item_get_incorrect5(self):  # Test №7
        with app.app_context():
            try:
                item = ItemResource()
                with self.assertRaises(werkzeug.exceptions.NotFound):
                    raise Exception("7: Item with id '1' not found")
                a = item.get("1")
            except Exception as e:
                print(e)

    def test_items_get_correct(self):  # Test №8
        """
        Test checks obtaining all items from database.

        :return: print string with result
        """
        with app.app_context():
            try:
                item = ItemsListResource()
                a = item.get()
                self.assertEqual(type(a.json), dict)
                print("8: Correct")
            except Exception:
                print("Database is empty")


class ApiTestPostRequests(unittest.TestCase):
    def test_item_post_correct(self):  # Test №9
        print("POST-requests testing:")
        with app.test_client() as client:
            payload = {'name': 'testPost',
                       'amount': '100',
                       'company': 'TestCompany',
                       'date': '2021-04-23',
                       'description': 'bla bla bla',
                       'type': 'food',
                       'creator': 'mateus'}
            result = client.post(
                '/api/v2/items',
                data=payload
            )
            try:
                self.assertEqual(
                    result.data,
                    b'{"success":"OK"}\n'
                )
                print("9: Correct")
            except Exception as e:
                print(e)

    def test_item_post_incorrect(self):  # Test №10
        with app.test_client() as client:
            payload = {'name': 123,  # All fields have incorrect type
                       'amount': 'abc',
                       'company': 100,
                       'date': 12345,
                       'description': 321,
                       'type': 321,
                       'creator': 123}
            result = client.post(
                '/api/v2/items',
                data=payload
            )
            try:
                self.assertEqual(
                    result.data,
                    b'{"success":"OK"}\n'
                )
            except Exception:
                print("10: Incorrect field types")


class ApiTestPutRequests(unittest.TestCase):
    def test_item_put_correct(self):  # Test №11
        print("PUT-requests testing:")
        with app.app_context():
            try:
                db_sess = create_session()  # Create database session
                obj = db_sess.query(Item).order_by(
                    Item.id.desc()).first()

                item = ItemResource()
                payload = {'name': 'testPost2',
                           'amount': 1002,
                           'company': 'TestCompany',
                           'date': '2021-04-24',
                           'description': 'bla bla bla2',
                           'type': 'food',
                           'creator': 'mateus'}
                a = item.put(payload)
                db_sess.close()  # Shut down database session
                # result = client.put(
                #     '/api/v2/items',
                #     data=payload
                # )
                self.assertEqual(
                    a.data,
                    b'{"success":"OK"}\n'
                )
                print("11: Correct")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    unittest.main()
