"""
This module provides an abstraction for working with XModuleDescriptors
that are stored in a database an accessible using their Location as an identifier
"""

import re
from .exceptions import InvalidLocationError

URL_RE = re.compile("""
    (?P<tag>[^:]+)://
    (?P<org>[^/]+)/
    (?P<course>[^/]+)/
    (?P<category>[^/]+)/
    (?P<name>[^/]+)
    (/(?P<revision>[^/]+))?
    """, re.VERBOSE)


class Location(object):
    '''
    Encodes a location.

    Locations representations of URLs of the
    form {tag}://{org}/{course}/{category}/{name}[/{revision}]

    However, they can also be represented a dictionaries (specifying each component),
    tuples or list (specified in order), or as strings of the url
    '''
    def __init__(self, location):
        """
        Create a new location that is a clone of the specifed one.

        location - Can be any of the following types:
            string: should be of the form {tag}://{org}/{course}/{category}/{name}[/{revision}]
            list: should be of the form [tag, org, course, category, name, revision]
            dict: should be of the form {
                'tag': tag,
                'org': org,
                'course': course,
                'category': category,
                'name': name,
                'revision': revision,
            }
            Location: another Location object

        In both the dict and list forms, the revision is optional, and can be ommitted.

        None of the components of a location may contain the '/' character

        Components may be set to None, which may be interpreted by some contexts to mean
        wildcard selection
        """
        self.update(location)

    def update(self, location):
        """
        Update this instance with data from another Location object.

        location: can take the same forms as specified by `__init__`
        """
        self.tag = self.org = self.course = self.category = self.name = self.revision = None

        if isinstance(location, basestring):
            match = URL_RE.match(location)
            if match is None:
                raise InvalidLocationError(location)
            else:
                self.update(match.groupdict())
        elif isinstance(location, list):
            if len(location) not in (5, 6):
                raise InvalidLocationError(location)

            (self.tag, self.org, self.course, self.category, self.name) = location[0:5]
            self.revision = location[5] if len(location) == 6 else None
        elif isinstance(location, dict):
            try:
                self.tag = location['tag']
                self.org = location['org']
                self.course = location['course']
                self.category = location['category']
                self.name = location['name']
            except KeyError:
                raise InvalidLocationError(location)
            self.revision = location.get('revision')
        elif isinstance(location, Location):
            self.update(location.list())
        else:
            raise InvalidLocationError(location)

        for val in self.list():
            if val is not None and '/' in val:
                raise InvalidLocationError(location)

    def __str__(self):
        return self.url()

    def url(self):
        """
        Return a string containing the URL for this location
        """
        url = "{tag}://{org}/{course}/{category}/{name}".format(**self.dict())
        if self.revision:
            url += "/" + self.revision
        return url

    def list(self):
        """
        Return a list representing this location
        """
        return [self.tag, self.org, self.course, self.category, self.name, self.revision]

    def dict(self):
        """
        Return a dictionary representing this location
        """
        return {'tag': self.tag,
                'org': self.org,
                'course': self.course,
                'category': self.category,
                'name': self.name,
                'revision': self.revision}


class ModuleStore(object):
    """
    An abstract interface for a database backend that stores XModuleDescriptor instances
    """
    def get_item(self, location):
        """
        Returns an XModuleDescriptor instance for the item at location.
        If location.revision is None, returns the item with the most
        recent revision

        If any segment of the location is None except revision, raises
            keystore.exceptions.InsufficientSpecificationError
        If no object is found at that location, raises keystore.exceptions.ItemNotFoundError

        location: Something that can be passed to Location
        """
        raise NotImplementedError

    # TODO (cpennington): Replace with clone_item
    def create_item(self, location, editor):
        raise NotImplementedError

    def update_item(self, location, data):
        """
        Set the data in the item specified by the location to
        data

        location: Something that can be passed to Location
        data: A nested dictionary of problem data
        """
        raise NotImplementedError

    def update_children(self, location, children):
        """
        Set the children for the item specified by the location to
        data

        location: Something that can be passed to Location
        children: A list of child item identifiers
        """
        raise NotImplementedError