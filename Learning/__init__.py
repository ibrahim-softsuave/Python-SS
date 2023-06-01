from .celery import app as celery_app

__all__ = ['celery_app']

excluded_endpoints = [
    '/api/v1/register',
    '/api/v1/login'
]