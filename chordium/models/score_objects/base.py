class Base(object):
    def __repl__(self):
        raise NotImplementedError

    def _show_progress(self):
        raise NotImplementedError

    def __eq__(self, other):
        return self.__class__ == other.__class__