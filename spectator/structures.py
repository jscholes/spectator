# spectator
# Copyright (C) 2016 James Scholes
# This project is free software, licensed under the terms of the GNU General Public License (version 3 or later).
# See the file LICENSE for more details.

from collections import defaultdict


class PropertyNotObservedError(Exception):
    def __init__(self, object, property, callback, *args, **kwargs):
        self.object = object
        self.property = property
        self.callback = callback
        super().__init__(*args, **kwargs)

    def __str__(self):
        return 'Property {0} on object {1} not bound to callback {2}'.format(self.property, self.object, self.callback)


class ObservableObject:
    _observed_properties = defaultdict(lambda: set())

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in self._observed_properties:
            self.update_property_observers(name, value)

    def __delattr__(self, name):
        super().__delattr__(name)
        self._observed_properties.pop(name, None)

    def observe_property(self, property, callback):
        self._observed_properties[property].add(callback)
        callback(getattr(self, property))

    def remove_observation(self, property, callback):
        try:
            self._observed_properties[property].remove(callback)
        except KeyError:
            raise PropertyNotObservedError(self, property, callback)

    def update_property_observers(self, property, value):
        for callback in self._observed_properties[property]:
            callback(value)

