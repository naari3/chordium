from .base import Base


class BarLine(Base):
    def __repr__(self):
        return "<BarLine>"

    def _show_progress(self):
        return "|"