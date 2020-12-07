from .base import Base


class Same(Base):
    def _show_progress(self):
        return "%"
