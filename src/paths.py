import os


def get_project_root() -> str:
    """ Returns the root of a project """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
