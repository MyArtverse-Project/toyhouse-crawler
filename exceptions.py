class NoUsernameError(Exception):
    """
    Throws an error if username was not provided
    """
    pass


class UsernamePrivateError(Exception):
    """
    Throws an error if username provided had their profile private
    """
    pass
