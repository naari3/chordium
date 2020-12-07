class Base(object):
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._show_progress()}>"

    def _show_progress(self):
        raise NotImplementedError

    def __eq__(self, other):
        return self.__class__ == other.__class__