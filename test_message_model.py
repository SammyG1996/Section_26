"""Message tests"""

import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows, Likes


# Before the app is imported we set an enviroment variable to use a different database for the tests.

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


from app import app

# Next we create the tables. We will only have to do this once for all the tests and we'll clear the data afterward

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.user_id = 94566
        user = User.signup("testing", "testing@test.com", "password", None)
        user.id = self.user_id
        db.session.commit()

        self.user = User.query.get(self.user_id)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        """Does basic model work?"""
        
        message = Message(
            text="This is a test",
            user_id=self.user_id
        )

        db.session.add(message)
        db.session.commit()

        # User should have 1 message
        self.assertEqual(len(self.user.messages), 1)
        self.assertEqual(self.user.messages[0].text, "This is a test")

    def test_message_likes(self):
        message1 = Message(
            text="a warble",
            user_id=self.user_id
        )

        message2 = Message(
            text="a very interesting warble",
            user_id=self.user_id 
        )

        user = User.signup("yetanothertest", "t@email.com", "password", None)
        user_id = 888
        user.id = user_id
        db.session.add_all([message1, message2, user])
        db.session.commit()

        user.likes.append(message1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == user_id).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, message1.id)


        