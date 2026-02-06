from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config import Settings


class ResumeFineTuner:
    """
    Main entry point for resume fine tuner application.
    """

    def __init__(self,cfg: Settings):
        self.cfg = cfg
        pass

    def is_ready(self)-> bool:
        """Check if the all dependencies are ready."""
        # TODO: add DataDog metrics posting
        return True