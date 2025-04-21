import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@db:5432/library'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
