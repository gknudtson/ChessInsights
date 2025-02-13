# import os
# import tempfile
#
# import pytest
#
# from chess_insights import create_app
#
#
# @pytest.fixture
# def app():
#     app = create_app()
#     app.config.update({
#         "TESTING": True,
#     })
#
#     yield app
#
#
# @pytest.fixture()
# def client(app):
#     return app.test_client()
#
#
# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()
#
#
# def test_start(client):
#     rv = client.get('/game/start')
#     assert b'18446462598732906495' in rv.data
#
#
# def test_moves(client):
#     client.get('/game/start')
#     rv = client.get('/game/moves?color=white&square=1')
#     assert b'329728' in rv.data
