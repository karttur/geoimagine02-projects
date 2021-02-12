"""
Created 22 Jan 2021
Last updated 12 Feb 2021

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