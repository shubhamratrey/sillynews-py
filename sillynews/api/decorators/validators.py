import constants


def allowed_methods(function):
    def wrap(response, *args, **kwargs):
        request_method = response.request.method
        _allowed_methods = getattr(response, 'allowed_methods', [])
        _allowed_methods = [_allowed_method.upper() for _allowed_method in _allowed_methods]
        if _allowed_methods and request_method not in _allowed_methods:
            response.set_unsupported_method(
                'Only %s %s supported.' % (" ".join(_allowed_methods), "is" if len(_allowed_methods) <= 1 else "are"),
                constants.INVALID_RESOURCE.REQUEST_METHOD)
            return {}
        return function(response, *args, **kwargs)

    return wrap
