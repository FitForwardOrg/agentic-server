"""
Resume fine tuning application.
"""

from typing import TYPE_CHECKING

from .application import ResumeFineTuner

if TYPE_CHECKING:
    from src.config import Settings


def factory(cfg: Settings):
    """Create a new resume fine tuner instance."""
    return ResumeFineTuner(cfg=cfg)


__all__ = [ResumeFineTuner, factory]
