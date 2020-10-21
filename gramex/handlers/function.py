from gramex.transforms import build_transform, handler
from .functionhandler import FunctionHandler


class Function(FunctionHandler):
    '''
    Renders the output of a function when the URL is called via GET or POST. It
    accepts these parameters when initialized:

    :arg string function: a string that resolves into any Python function or
        method (e.g. ``str.lower``). By default, it is called as
        ``function(handler)`` where handler is this RequestHandler, but you can
        override ``args`` and ``kwargs`` below to replace it with other
        parameters. The result is rendered as-is (and hence must be a string, or
        a Future that resolves to a string.) You can also yield one or more
        results. These are written immediately, in order.
    :arg list args: positional arguments to be passed to the function.
    :arg dict kwargs: keyword arguments to be passed to the function.
    :arg dict headers: HTTP headers to set on the response.
    :arg list methods: List of HTTP methods to allow. Defaults to
        `['GET', 'POST']`.
    :arg string redirect: URL to redirect to when the result is done. Used to
        trigger calculations without displaying any output.
    '''
    @classmethod
    def setup(cls, headers={}, methods=['GET', 'POST'], **kwargs):
        super(Function, cls).setup(headers, methods, **kwargs)
        # kwargs['function'] = f'handler({kwargs["function"]})'
        """
        kwargs:
            function: math.ceil
        kwargs:
            function: handler(math.ceil)
        """
        trx = build_transform(kwargs, vars={'handler': None},
                              filename='url: %s' % cls.name)
        cls.info['function'] = handler(trx)
