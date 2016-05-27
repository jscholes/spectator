# spectator
Simple observable data structures for Python, to facilitate databinding and other patterns.

## Example
Currently only one class, spectator.structures.ObservableObject, is included.  This is a standard Python object offering one-way, callback-based data binding to single properties.

Have a look at the basic sample below.  There's also an [example](https://github.com/jscholes/spectator/blob/master/examples/gui_observer.py) of using ObservableObject in a wxPython-based GUI.

    >>> from spectator.structures import ObservableObject

First, create a subclass of ObservableObject for our model.

    >>> class NetworkConnection(ObservableObject):
    ...     STATUS_CONNECTED = 1
    ...     STATUS_DISCONNECTED = 2
    ...
    ...     def __init__(self):
    ...         self.current_status = self.STATUS_DISCONNECTED
    ...
    ...     def connect(self):
    ...         self.current_status = self.STATUS_CONNECTED
    ...
    ...     def disconnect(self):
    ...         self.current_status = self.STATUS_DISCONNECTED
    ...     # ... rest of model code here ...

Next, create a callback.  In this simple example, the callback simply prints an appropriate message based on the status of the network connection, but this could easily be used to change a network indicator on a GUI to red or green, play an alert, send a text message, etc.

    >>> def status_callback(status):
    ...     if status == NetworkConnection.STATUS_CONNECTED:
    ...         print('Network connection established')
    ...     else:
    ...         print('Network connection lost')

Now, join the dots!  Create a model instance and bind our callback to its current_status property.  The callback is called immediately so we can react to the object's state at the time of binding.

    >>> conn = NetworkConnection()
    >>> conn.observe_property('current_status', status_callback)
    Network connection lost

Tell the model to do something, and the callback is called without any extra intervention on our part.

    >>> conn.connect()
    Network connection established
    >>> conn.disconnect()
    Network connection lost

Remove the binding, modify the object's properties and then reestablish it later.

    >>> conn.remove_observation('current_status', status_callback)
    >>> conn.connect()
    >>> conn.observe_property('current_status', status_callback)
    Network connection established
    >>> conn.remove_observation('current_status', status_callback)

## TODO
Add classes providing data added/updated/removed callbacks for list, dictionary and other sequence types.
