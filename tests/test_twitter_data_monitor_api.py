# import json
# import pytest
# import warnings
# from flask import jsonify
# import os
# import tempfile
# import pytest
# from app import app, db
#
# @pytest.fixture
# def client():
#     db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#     app.config['TESTING'] = True
#     client = app.test_client()
#
#     with app.app_context():
#         db.create_all()
#
#     yield client
#
#     os.close(db_fd)
#     os.unlink(app.config['DATABASE'])
#
# def test_empty_db(client):
#     """Start with a blank database."""
#
#     rv = client.get('/api/actors/silva_marina')
#     assert b'No entries here so far' in rv.data
