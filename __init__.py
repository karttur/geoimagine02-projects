"""
projects
==========================================

Package belonging to Karttur´s GeoImagine Framework.

Author
------
Thomas Gumbricht (thomas.gumbricht@karttur.com)

"""

from .version import __version__, VERSION, metadataD

from .process_project import SetupProcesses

__all__ = ['SetupProcesses']