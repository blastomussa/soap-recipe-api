
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from internal.connectionString import CONNECTION_STRING
from pymongo import MongoClient

TEST_ADMIN = {
    '_id': 0,
    'username': 'johndoe',
    'full_name': 'John Doe',
    'email': 'johndoe@example.com',
    'disabled': False,
    'admin': True,
    'hashed_password': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW' #secret
}

def create_admin():
    mongo_client = MongoClient(CONNECTION_STRING)
    mongo_client.api.Users.insert_one(TEST_ADMIN)
    print('Test admin created')


def delete_admin():
    mongo_client = MongoClient(CONNECTION_STRING)
    mongo_client.api.Users.delete_one({'_id': 0})
    print('Test admin Deleted')


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    create_admin()
    


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
    delete_admin()
    