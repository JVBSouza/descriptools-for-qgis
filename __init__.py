# -*- coding: utf-8 -*-
"""
/***************************************************************************
 descriptoolsQgis
                                 A QGIS plugin
 Plugin for terrain descriptor calculation
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-09-12
        copyright            : (C) 2022 by Fabiane Dorleles and José Souza
        email                : joseboing@gmail.com
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
    """Load descriptoolsQgis class from file descriptoolsQgis.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .descriptools_qgis import descriptoolsQgis
    return descriptoolsQgis(iface)
