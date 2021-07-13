# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IceVolume
                                 A QGIS plugin
 This plugin subtracts riverbed DEM from Ice surface DEM to estimate ice volume
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-07-09
        copyright            : (C) 2021 by Einar Rødtang
        email                : einar.rodtang@protonmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load IceVolume class from file IceVolume.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ice_volume import IceVolume
    return IceVolume(iface)