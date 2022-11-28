# -*- coding: utf-8 -*-
"""
/***************************************************************************
 descriptoolsQgis
                                 A QGIS plugin
 Plugin for terrain descriptor calculation
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-09-12
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Fabiane Dorleles and José Souza
        email                : joseboing@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog 
from qgis.core import QgsProject, Qgis
from osgeo import gdal, osr
from osgeo.gdalconst import *
import numpy

import descriptools.topoindexes as topoindexes
import descriptools.downslope as downslope
import descriptools.slope as slope
import descriptools.flowhand as flowhand
import descriptools.gfi as gfi

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .descriptools_qgis_dialog import descriptoolsQgisDialog
import os.path


class descriptoolsQgis:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'descriptoolsQgis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Descriptools for QGIS')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('descriptoolsQgis', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/descriptools_qgis/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Calculate descriptors'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&Descriptools for QGIS'),
                action)
            self.iface.removeToolBarIcon(action)

    def select_output_file(self):
        filepath = QFileDialog.getExistingDirectory(
            self.dlg, "Select output path ","")
        self.dlg.lineEdit.setText(filepath)

    def export_descriptor(self, descriptor, path, cols, rows, geotransform, projection, nodata):
        print("Creating file at: ", path)
        raster = gdal.GetDriverByName('GTiff').Create(path, cols, rows, 1, gdal.GDT_Float32)
        out_band = raster.GetRasterBand(1)
        out_band.WriteArray(descriptor, 0, 0)
        out_band.FlushCache()
        out_band.SetNoDataValue(nodata) #nodata
        raster.SetGeoTransform(geotransform)
        raster.SetProjection(projection)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = descriptoolsQgisDialog()
            self.dlg.pushButton.clicked.connect(self.select_output_file)

        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()

        # Clear the contents of the comboBox from previous runs
        self.dlg.comboBoxDem.clear()
        self.dlg.comboBoxFdr.clear()
        self.dlg.comboBoxFac.clear()
        
        # Populate the comboBox with names of all the loaded layers
        self.dlg.comboBoxDem.addItems([layer.name() for layer in layers])
        self.dlg.comboBoxFdr.addItems([layer.name() for layer in layers])
        self.dlg.comboBoxFac.addItems([layer.name() for layer in layers])

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            print("Retrieving data")
            selectedDemLayerIndex = self.dlg.comboBoxDem.currentIndex()
            selectedDemLayer = layers[selectedDemLayerIndex].layer()

            selectedFdrLayerIndex = self.dlg.comboBoxFdr.currentIndex()
            selectedFdrLayer = layers[selectedFdrLayerIndex].layer()

            selectedFacLayerIndex = self.dlg.comboBoxFac.currentIndex()
            selectedFacLayer = layers[selectedFacLayerIndex].layer()
            
            # Open input data in GDAL
            ds_dem = gdal.Open(selectedDemLayer.source(), GA_ReadOnly)
            ds_fdr = gdal.Open(selectedFdrLayer.source(), GA_ReadOnly)
            ds_fac = gdal.Open(selectedFacLayer.source(), GA_ReadOnly)

            # Get matrix from input
            DEM = ds_dem.GetRasterBand(1).ReadAsArray()
            FDR = ds_fdr.GetRasterBand(1).ReadAsArray()
            FAC = ds_fac.GetRasterBand(1).ReadAsArray()

            # Get width and height from reference raster
            cols = ds_dem.RasterXSize# number of columns
            rows = ds_dem.RasterYSize# number of rows

            # Get Geotransform from reference raster
            geotransform = ds_dem.GetGeoTransform()#georeference functions
            originX = geotransform[0]#top left x
            originY = geotransform[3]#top left y
            cellsize = geotransform[5]#pixel resolution

            # Get Projection from reference raster
            projection = ds_dem.GetProjection()

            print("Done with import")


            # Get output path folder
            output_path = self.dlg.lineEdit.text()


            ## Prepare auxiliary data

            # Get pixel value, if checkmark was selected use custom value, otherwise get from reference raster
            if self.dlg.checkBoxPixelSize.isChecked():
                # Custom value
                px = self.dlg.doubleSpinBoxPixel.value()
            else:
                # Check in case pixel size is negative
                px = cellsize * -1 if cellsize <0 else cellsize
            
            # Get user river innitiation threshold from spinbox
            river_threshold = self.dlg.doubleSpinBox.value()
            # Create river matrix as int8
            river = numpy.where(FAC>=(river_threshold*1000*1000/(90*90)), 1, 0).astype('int8') #20km²

            #Generate array of boolean to check with descriptors to calculate
            list_to_calculate = [
                self.dlg.checkBoxSlope.isChecked(),
                self.dlg.checkBoxDownslope.isChecked(),
                self.dlg.checkBoxTI.isChecked(),
                self.dlg.checkBoxMTI.isChecked(),
                self.dlg.checkBoxHDistance.isChecked(),
                self.dlg.checkBoxHAND.isChecked(),
                self.dlg.checkBoxGFI.isChecked(),
                self.dlg.checkBoxLFI.isChecked()
            ]

            print("river_threshold", river_threshold)
            print("px", px)
            print("fac>value", (river_threshold*1000*1000/(px*px)))
            print("outpath",output_path)

            print("Starting calculations")

            for item in range(0,8,1):
                descriptor = []
                file = ''
                # Skip if false
                if list_to_calculate[item] == False:
                    continue
                if item == 0:
                    descriptor = slope.slope_sequential_jit(DEM, px)
                    file = 'slope'
                elif item == 1:
                    descriptor = downslope.downslope_sequential_jit(DEM, FDR, px, self.dlg.doubleSpinBox_2.value())
                    file = 'downslope'
                elif item == 2:
                    descriptor = topoindexes.topographic_index_sequential_jit(FAC,slope.slope_sequential_jit(DEM, px),px)
                    file = 'topographic_index'
                elif item == 3:
                    # n = 0.13, 0.08 and 0.05 for 90, 30 and 12.5m
                    descriptor = topoindexes.modified_topographic_index_sequential_jit(FAC,slope.slope_sequential_jit(DEM, px),px, self.dlg.doubleSpinBox_3.value())
                    file = 'modified_topographic_index'
                elif item > 3:
                    flow, indices = flowhand.fdist_indexes_sequential_jit(FDR,river,px)
                    if item == 4:
                        descriptor = flow
                        file = 'horizontal_distance'
                    else:
                        hand = flowhand.hand_calculator(DEM,indices)
                        if item == 5:
                            descriptor = hand
                            file = 'hand'
                        else:
                            # b = 0.1 and n = 0.4
                            if item == 6:
                                descriptor = gfi.geomorphic_flood_index_sequential_jit(hand, FAC, indices, self.dlg.doubleSpinBox_5.value(), self.dlg.doubleSpinBox_4.value(), px)
                                file = 'GFI'
                            if item == 7:
                                descriptor = gfi.ln_hl_H_sequential_jit(hand, FAC, self.dlg.doubleSpinBox_5.value(), self.dlg.doubleSpinBox_4.value(), px)
                                file = 'LFI'
                print("Exporting: ", file)
                self.export_descriptor(descriptor, output_path + '/' + file + '.TIF', cols, rows, geotransform, projection, -100)
                print("Done: ", file)
                print("")

            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            # pass
            self.iface.messageBar().pushMessage(
                "Success", "Output file written at ",
                level=Qgis.Success, duration=3)
