# -*- coding: utf-8 -*-

import collections
import json
from enum import Enum

from TM1py.Objects.TM1Object import TM1Object


class Element(TM1Object):
    """ Abstraction of TM1 Element

    """
    ELEMENT_ATTRIBUTES_PREFIX = "}ElementAttributes_"

    class Types(Enum):
        NUMERIC = 1
        STRING = 2
        CONSOLIDATED = 3

        def __str__(self):
            return self.name.capitalize()

        @classmethod
        def _missing_(cls, value):
            for member in cls:
                if member.name.lower() == value.replace(" ", "").lower():
                    return member
            # default
            raise ValueError("Invalid element type=" + value)

    def __init__(self, name, element_type, attributes=None, unique_name=None, index=None):
        self._name = name
        self._unique_name = unique_name
        self._index = index
        self._element_type = None
        self.element_type = element_type
        self._attributes = attributes

    @staticmethod
    def from_dict(element_as_dict):
        return Element(name=element_as_dict['Name'],
                       unique_name=element_as_dict['UniqueName'],
                       index=element_as_dict['Index'],
                       element_type=element_as_dict['Type'],
                       attributes=element_as_dict['Attributes'])

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def unique_name(self):
        return self._unique_name

    @property
    def index(self):
        return self._index

    @property
    def element_attributes(self):
        return self._attributes

    @property
    def element_type(self):
        return self._element_type

    @element_type.setter
    def element_type(self, value):
        self._element_type = Element.Types(value)

    @property
    def body(self):
        return json.dumps(self._construct_body())

    @property
    def body_as_dict(self):
        return self._construct_body()

    def _construct_body(self):
        body_as_dict = collections.OrderedDict()
        body_as_dict['Name'] = self._name
        body_as_dict['Type'] = str(self._element_type)
        return body_as_dict
