import importlib
import os
import sys


class Register:
    """Module register"""

    def __init__(self, registry_name):
        self._dict = {}
        self._name = registry_name

    def __setitem__(self, key, value):
        if not callable(value):
            raise Exception("Value of a Registry must be a callable.")
        if key is None:
            key = value.__name__
        if key in self._dict:
            print("Key %s already in registry %s." % (key, self._name))
        self._dict[key] = value

    def register(self, param):
        """Decorator to register a function or class."""

        def decorator(key, value):
            self[key] = value
            return value

        if callable(param):
            # @reg.register
            return decorator(None, param)
        # @reg.register('alias')
        return lambda x: decorator(param, x)

    def __getitem__(self, key):
        try:
            return self._dict[key]
        except Exception as e:
            print(f"module {key} not found: {e}")
            raise e

    def __contains__(self, key):
        return key in self._dict

    def keys(self):
        """key"""
        return self._dict.keys()


class registers():  # pylint: disable=invalid-name, too-few-public-methods
    """All module registers."""

    def __init__(self):
        raise RuntimeError("Registries is not intended to be instantiated")

    Ops = Register('ops')
