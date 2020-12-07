from .base import Base


class Tie(Base):
    def _show_progress(self):
        return "="
