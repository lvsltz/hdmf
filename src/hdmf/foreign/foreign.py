import requests

from ..container import Container


class ForeignField(object):
    '''
    An object for resolving data stored in a foreign location i.e. across the web
    '''


    @docval({'name': 'uri', 'type': str, 'help': 'the URI for retreiving the foreign field'},
            {'name': 'namespace', 'type': str, 'help': 'the namespace of data_type'},
            {'name': 'parent', 'type': Container, 'help': 'the UUID object ID of the parent of the foreign object'},
            {'name': 'path', 'type': str, 'help': 'the path of the foreign field, relative to the parent'},
            {'name': 'checksum', 'type': str, 'help': 'the MD5 checksum for the data'},
            {'name': 'manager', 'type', BuildManager, 'the BuildManager used to read this field'},
            {'name': 'data_type', 'type': str, 'help': 'the data_type of the foreign object', 'default': None},
            {'name': 'object_id', 'type': str, 'help': 'the UUID object ID of the foreign object', 'default': True})
    def __init__(self, **kwargs):
        self.__uri = kwargs['uri']
        self.__namespace = kwargs['namespace']
        self.__parent = kwargs['parent']
        self.__path = kwargs['path']
        self.__checksum = kwargs['checksum']
        self.__data_type = kwargs['data_type']
        self.__object_id = kwargs['object_id']

    @property
    def uri(self):
        '''the URI for retreiving the foreign field'''
        return self.__uri

    @property
    def namespace(self):
        '''the namespace of data_type'''
        return self.__namespace

    @property
    def parent(self):
        '''the UUID object ID of the parent of the foreign object'''
        return self.__parent

    @property
    def path(self):
        '''the path of the foreign field, relative to the parent'''
        return self.__path

    @property
    def checksum(self):
        '''the MD5 checksum for the data'''
        return self.__checksum

    @property
    def data_type(self):
        '''the data_type of the foreign object'''
        return self.__data_type

    @property
    def object_id(self):
        '''the UUID object ID of the foreign object'''
        return self.__object_id

    @docval({'name': 'cache', 'type': bool, 'help': 'whether or not to cache result after resolving', 'default': True},
            {'name': 'swap', 'type': bool, 'help': 'whether or not to swap in the returned value to the parent Container', 'default': True},
            returns='the value that was retrieved'})
    def resolve(self):
        '''
        Retrieve the foreign value.

        if *swap* is *True*, the returned value is swapped in place of this object on the Container holding this object

        For example, the following would happen:

        >>> if isinstance(container.foo, ForeignField):
                print('foo is foreign')
        foo is foreign
        >>> container.foo.resolve()
        >>> if not isinstance(container.foo, ForeignField):
                print('foo is no longer foreign')
        foo is no longer foreign
        '''

        json = requests.get(self.uri).json()
        # do something to get a builder
        builder = None

        self.parent.fields[self.path] = self.__manager.resolve(self.parent, self)
