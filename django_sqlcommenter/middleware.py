import logging
from contextlib import ExitStack

from django.db import connections

from .query_wrapper import QueryWrapper

logger = logging.getLogger(__name__)


class SqlCommenterWithMetrics:
    """
    Middleware to append a comment to each database query with details about
    the framework and the execution context.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with ExitStack() as stack:
            for db_alias in connections:
                stack.enter_context(connections[db_alias].execute_wrapper(QueryWrapper(request)))
            return self.get_response(request)
