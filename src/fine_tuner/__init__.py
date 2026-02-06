"""
Resume fine tuning application.
"""
from typing import TYPE_CHECKING

from .application import ResumeFineTuner

if TYPE_CHECKING:
    from config import Settings

def Factory(cfg: Settings):
    return ResumeFineTuner(cfg=cfg)

__all__ = [ResumeFineTuner,Factory]
