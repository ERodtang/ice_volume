import processing
from processing.core.Processing import Processing
import os
from os import path
import qgis
from  qgis.core import *
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry


def ice_thickness_estimator(Root_folder_path, No_ice_raster_path, river_polygon_path):
    '''
    Processes DEM rasters. Clipping them to the extent of river_polygon_path. 
    Then subtracting each of them from No_ice_raster_path. 
    Then computes statistics for the resultant difference rasters.

    Parameters
    ----------
    Root_folder_path : TYPE
        You need to specify the root folder of your project.
    No_ice_raster_path : TYPE
        Specify which DEM (in the DEM folder) that corresponds to the no ice condition (As low discharge as possible).
    river_polygon_path : TYPE
        Specify the name of a shape file that contains a polygon that covers the river, must be in project root directory.
    Returns
    -------
    NULL : TYPE
        DESCRIPTION.

    '''
    root = QgsProject.instance().layerTreeRoot()
    
    DEM_folder_path = Root_folder_path + '/DEM/'                 # The root folder of your project must contain a folder called DEM containing your digital elevation models
    river_polygon = QgsVectorLayer(river_polygon_path, 'river_polygon')
    root.addLayer(river_polygon)
    No_ice_raster_name = os.path.basename(No_ice_raster_path)
    
    #Initialise folder structure
    CLIPPED_DEM_folder_path = Root_folder_path + '/CLIPPED_DEM/'
    if os.path.isdir(CLIPPED_DEM_folder_path) == False: 
        os.mkdir(CLIPPED_DEM_folder_path)
    
    FILLED_DEM_folder_path = Root_folder_path + '/FILLED_DEM/'
    if os.path.isdir(FILLED_DEM_folder_path) == False: 
        os.mkdir(FILLED_DEM_folder_path)
    
    FDIR_folder_path = Root_folder_path + '/FDIR/'
    if os.path.isdir(FDIR_folder_path) == False: 
        os.mkdir(FDIR_folder_path)
    
    WSHED_folder_path = Root_folder_path + '/WSHED/'
    if os.path.isdir(WSHED_folder_path) == False: 
        os.mkdir(WSHED_folder_path)
    
    DIFFERENCE_DEM_folder_path = Root_folder_path + '/DIFFERENCE_DEM/'
    if os.path.isdir(DIFFERENCE_DEM_folder_path) == False:
        os.mkdir(DIFFERENCE_DEM_folder_path)
    
    STATS_folder_path = Root_folder_path + '/STATS/'
    if os.path.isdir(STATS_folder_path) == False:
        os.mkdir(STATS_folder_path)

    PRE_FILLED_DEM_folder_path = Root_folder_path + '/PRE_FILLED_DEM/'
    if os.path.isdir(PRE_FILLED_DEM_folder_path) == False:
        os.mkdir(PRE_FILLED_DEM_folder_path)
    
    FDIR2_folder_path = Root_folder_path + '/FDIR2/'
    if os.path.isdir(FDIR2_folder_path) == False:
        os.mkdir(FDIR2_folder_path)
    
    WSHED2_folder_path = Root_folder_path + '/WSHED2/'
    if os.path.isdir(WSHED2_folder_path) == False:
        os.mkdir(WSHED2_folder_path)

    REVERSED_folder_path = Root_folder_path + '/REVERSED/'
    if os.path.isdir(REVERSED_folder_path) == False:
        os.mkdir(REVERSED_folder_path)
    
    REV_FILL_folder_path = Root_folder_path + '/REV_FILL/'
    if os.path.isdir(REV_FILL_folder_path) == False:
        os.mkdir(REV_FILL_folder_path)
    
    #Initialise QGIS group structure
    if QgsLayerTreeGroup.findGroup(root,'DEM') == NULL:
        QgsLayerTreeGroup.addGroup(root,'DEM')
    
    if QgsLayerTreeGroup.findGroup(root,'CLIPPED_DEM') == NULL:
        QgsLayerTreeGroup.addGroup(root,'CLIPPED_DEM')
    
    if QgsLayerTreeGroup.findGroup(root,'FILLED_DEM') == NULL:
        QgsLayerTreeGroup.addGroup(root,'FILLED_DEM')
    
    if QgsLayerTreeGroup.findGroup(root,'PRE_FILLED_DEM') == NULL:
        QgsLayerTreeGroup.addGroup(root,'PRE_FILLED_DEM')
    
    if QgsLayerTreeGroup.findGroup(root,'FDIR') == NULL:
        QgsLayerTreeGroup.addGroup(root,'FDIR')
    
    if QgsLayerTreeGroup.findGroup(root,'WSHED') == NULL:
        QgsLayerTreeGroup.addGroup(root,'WSHED')
        
    if QgsLayerTreeGroup.findGroup(root,'FDIR2') == NULL:
        QgsLayerTreeGroup.addGroup(root,'FDIR2')
    
    if QgsLayerTreeGroup.findGroup(root,'WSHED') == NULL:
        QgsLayerTreeGroup.addGroup(root,'WSHED')

    if QgsLayerTreeGroup.findGroup(root,'WSHED2') == NULL:
        QgsLayerTreeGroup.addGroup(root,'WSHED2')
    
    if QgsLayerTreeGroup.findGroup(root,'DIFFERENCE_DEM') == NULL:
        QgsLayerTreeGroup.addGroup(root,'DIFFERENCE_DEM')
    
    if QgsLayerTreeGroup.findGroup(root,'STATS') == NULL:
        QgsLayerTreeGroup.addGroup(root,'STATS')

    if QgsLayerTreeGroup.findGroup(root,'REVERSED') == NULL:
        QgsLayerTreeGroup.addGroup(root,'REVERSED')
        
    if QgsLayerTreeGroup.findGroup(root,'REV_FILL') == NULL:
        QgsLayerTreeGroup.addGroup(root,'REV_FILL')
    
    DEM_group = QgsLayerTreeGroup.findGroup(root,'DEM')
    DIFFERENCE_DEM_group = QgsLayerTreeGroup.findGroup(root,'DIFFERENCE_DEM')
    CLIPPED_DEM_group = QgsLayerTreeGroup.findGroup(root,'CLIPPED_DEM')
    FILLED_DEM_group = QgsLayerTreeGroup.findGroup(root,'FILLED_DEM')
    STATS_group = QgsLayerTreeGroup.findGroup(root,'STATS')
    FDIR_group = QgsLayerTreeGroup.findGroup(root,'FDIR')
    WSHED_group = QgsLayerTreeGroup.findGroup(root,'WSHED')
    FDIR2_group = QgsLayerTreeGroup.findGroup(root,'FDIR2')
    WSHED2_group = QgsLayerTreeGroup.findGroup(root,'WSHED2')
    PRE_FILLED_DEM_group = QgsLayerTreeGroup.findGroup(root,'PRE_FILLED_DEM')
    REVERSED_group = QgsLayerTreeGroup.findGroup(root,'REVERSED')
    REV_FILL_group = QgsLayerTreeGroup.findGroup(root,'REV_FILL')
    
    No_ice_FILLED_raster_path = FILLED_DEM_folder_path + No_ice_raster_name
    No_ice_FILLED_raster_path = No_ice_FILLED_raster_path.removesuffix('DEM.tif')+'FILLED_DEM.tif'
    
    #Add all DEM files to Qgis canvas
    for root, dirs, files in os.walk(DEM_folder_path):
        for name in files:
            if name.endswith('.tif') == True:
                DEM_full_path = root + name
                DEM_layer_name = name
                DEM_layer_name = DEM_layer_name.removesuffix('.tif')
                DEM_layer = QgsRasterLayer(DEM_full_path,DEM_layer_name)
                #Only add to canvas if layer doesn't already exist
                if len(QgsProject.instance().mapLayersByName(DEM_layer_name)) == 0:
                    QgsProject.instance().addMapLayer(DEM_layer, False)
                    DEM_group.addLayer(DEM_layer)
                else:
                    print("Tried to add layer " + DEM_layer_name + ", however layer already in canvas. Hence layer not added")
    
    #Clip rasters to river extent
    for layer in DEM_group.findLayers():
        ras = QgsRasterLayer(str(DEM_folder_path)+str(layer.name())+'.tif')
        output_string = str(CLIPPED_DEM_folder_path)+str(layer.name())
        output_string = output_string.removesuffix('DEM')+'CLIPPED_DEM.tif'
        parameters = {'INPUT': ras,
        'MASK': river_polygon,
        'NODATA': -9999,
        'ALPHA_BAND': False,
        'CROP_TO_CUTLINE': True,
        'KEEP_RESOLUTION': True,
        'OPTIONS': None,
        'DATA_TYPE': 0,
        'OUTPUT': output_string}
        processing_results = processing.run('gdal:cliprasterbymasklayer', parameters)
        CLIPPED_layer_name = str(layer.name()).removesuffix('DEM')+'CLIPPED_DEM'
        CLIPPED_layer = QgsRasterLayer(output_string, CLIPPED_layer_name)
        #Only add to canvas if layer doesn't already exist
        if len(QgsProject.instance().mapLayersByName(CLIPPED_layer_name)) == 0:
            QgsProject.instance().addMapLayer(CLIPPED_layer, False)
            CLIPPED_DEM_group.addLayer(CLIPPED_layer)
        else:
            print("Tried to add layer " + CLIPPED_layer_name + ", however layer already in canvas. Hence layer not added")
            
    #Fill sinks - using SAGA wang and liu       
    for layer in CLIPPED_DEM_group.findLayers():
        input_raster = QgsRasterLayer(str(CLIPPED_DEM_folder_path) + str(layer.name())+'.tif')
        if input_raster.isValid() == False:
            raise Exception("input_raster is invalid")
        filled_string = str(PRE_FILLED_DEM_folder_path) + str(layer.name())
        filled_string = filled_string.removesuffix('CLIPPED_DEM')+'PRE_FILLED_DEM.tif'
        
        fdir_string = str(FDIR_folder_path) + str(layer.name())
        fdir_string = fdir_string.removesuffix('CLIPPED_DEM')+'FDIR.tif'
        
        wshed_string = str(WSHED_folder_path) + str(layer.name())
        wshed_string = wshed_string.removesuffix('CLIPPED_DEM')+'WSHED.tif'

        parameters = {'ELEV': input_raster,
        'FILLED': filled_string,
        'FDIR': fdir_string,
        'WSHED': wshed_string,
        'MINSLOPE': 0.1,}
        processing_results = processing.run("saga:fillsinkswangliu", parameters)
        FILLED_layer_name = str(layer.name()).removesuffix('CLIPPED_DEM')+'PRE_FILLED_DEM'
        FILLED_layer = QgsRasterLayer(filled_string, FILLED_layer_name + '.tif')
        if FILLED_layer.isValid() == False:
            raise Exception("FILLED_layer is invalid")
        #Only add to canvas if layer doesn't already exist
        if len(QgsProject.instance().mapLayersByName(FILLED_layer_name)) == 0:
            QgsProject.instance().addMapLayer(FILLED_layer, False)
            PRE_FILLED_DEM_group.addLayer(FILLED_layer)
        else:
            print("Tried to add layer " + FILLED_layer_name + ", however layer already in canvas. Hence layer not added")

        FDIR_layer_name = str(layer.name()).removesuffix('CLIPPED_DEM')+'FDIR'
        FDIR_layer = QgsRasterLayer(filled_string, FDIR_layer_name)
        if len(QgsProject.instance().mapLayersByName(FDIR_layer_name)) == 0:
            QgsProject.instance().addMapLayer(FDIR_layer, False)
            FDIR_group.addLayer(FDIR_layer)
        else:
            print("Tried to add layer " + FDIR_layer_name + ", however layer already in canvas. Hence layer not added") 
       
        WSHED_layer_name = str(layer.name()).removesuffix('CLIPPED_DEM')+'WSHED'
        WSHED_layer = QgsRasterLayer(filled_string, WSHED_layer_name)        
        if len(QgsProject.instance().mapLayersByName(WSHED_layer_name)) == 0:
            QgsProject.instance().addMapLayer(WSHED_layer, False)
            WSHED_group.addLayer(WSHED_layer)
        else:
            print("Tried to add layer " + WSHED_layer_name + ", however layer already in canvas. Hence layer not added")
    
    #Reverse layers
    ras={} #Initialize raster dictionary
    for layer in PRE_FILLED_DEM_group.findLayers():
        entries = []
        lyr1 = QgsRasterLayer(str(PRE_FILLED_DEM_folder_path)+str(layer.name()))
        output = str(REVERSED_folder_path)+str(layer.name())
        output = output.removesuffix('PRE_FILLED_DEM.tif')+'REVERSED.tif'
        ras[(str(layer.name())+'_ras')] = qgis.analysis.QgsRasterCalculatorEntry()
        ras[(str(layer.name())+'_ras')].ref = str(layer.name())+'@1'
        ras[(str(layer.name())+'_ras')].raster = lyr1
        ras[(str(layer.name())+'_ras')].bandNumber = 1
        entries.append(ras[(str(layer.name())+'_ras')])
        computation_str = str(ras[(str(layer.name())+'_ras')].ref + '*-1')
        calc = qgis.analysis.QgsRasterCalculator(computation_str, output, 'GTiff', lyr1.extent(), lyr1.width() ,lyr1.height(),entries)
        calc.processCalculation()
        REVERSED_layer_name = layer.name()
        REVERSED_layer_name = REVERSED_layer_name.removesuffix('PRE_FILLED_DEM.tif')+'REVERSED'
        REVERSED_layer = QgsRasterLayer(output,REVERSED_layer_name)
        #Only add to canvas if layer doesn't already exist
        if len(QgsProject.instance().mapLayersByName(REVERSED_layer_name)) == 0:
            QgsProject.instance().addMapLayer(REVERSED_layer, False)
            REVERSED_group.addLayer(REVERSED_layer)
        else:
            print("Tried to add layer " + REVERSED_layer_name + ", however layer already in canvas. Hence layer not added")

    #Fill sinks, Wang and Liu for reversed rasters
    for layer in REVERSED_group.findLayers():
        input_raster = QgsRasterLayer(str(REVERSED_folder_path) + str(layer.name())+'.tif')
        rev_fill_string = str(REV_FILL_folder_path) + str(layer.name())
        rev_fill_string = rev_fill_string.removesuffix('REVERSED')+'REV_FILL.tif'
        
        fdir2_string = str(FDIR2_folder_path) + str(layer.name())
        fdir2_string = fdir2_string.removesuffix('REVERSED')+'FDIR2.tif'
        
        wshed2_string = str(WSHED2_folder_path) + str(layer.name())
        wshed2_string = wshed2_string.removesuffix('REVERSED')+'WSHED2.tif'

        parameters = {'ELEV': input_raster,
        'FILLED': rev_fill_string,
        'FDIR': fdir2_string,
        'WSHED': wshed2_string,
        'MINSLOPE': 0.1,}
        processing_results = processing.run("saga:fillsinkswangliu", parameters)
        REV_FILL_layer_name = str(layer.name()).removesuffix('REVERSED')+'REV_FILL'
        REV_FILL_layer = QgsRasterLayer(rev_fill_string, REV_FILL_layer_name)
        #Only add to canvas if layer doesn't already exist
        if len(QgsProject.instance().mapLayersByName(REV_FILL_layer_name)) == 0:
            QgsProject.instance().addMapLayer(REV_FILL_layer, False)
            REV_FILL_group.addLayer(REV_FILL_layer)
        else:
            print("Tried to add layer " + REV_FILL_layer_name + ", however layer already in canvas. Hence layer not added")

        FDIR2_layer_name = str(layer.name()).removesuffix('REVERSED')+'FDIR2'
        FDIR2_layer = QgsRasterLayer(filled_string, FDIR2_layer_name)
        if len(QgsProject.instance().mapLayersByName(FDIR2_layer_name)) == 0:
            QgsProject.instance().addMapLayer(FDIR2_layer, False)
            FDIR2_group.addLayer(FDIR2_layer)
        else:
            print("Tried to add layer " + FDIR2_layer_name + ", however layer already in canvas. Hence layer not added") 
       
        WSHED2_layer_name = str(layer.name()).removesuffix('REVERSED')+'WSHED2'
        WSHED2_layer = QgsRasterLayer(filled_string, WSHED2_layer_name)        
        if len(QgsProject.instance().mapLayersByName(WSHED2_layer_name)) == 0:
            QgsProject.instance().addMapLayer(WSHED2_layer, False)
            WSHED2_group.addLayer(WSHED2_layer)
        else:
            print("Tried to add layer " + WSHED2_layer_name + ", however layer already in canvas. Hence layer not added")
    
    #Reverse layers
    ras={} #Initialize raster dictionary
    for layer in REV_FILL_group.findLayers():
        entries = []
        lyr1 = QgsRasterLayer(str(REV_FILL_folder_path)+str(layer.name()) + '.tif')
        if lyr1.isValid() == False:
            raise Exception("lyr1 is invalid")
        output = str(FILLED_DEM_folder_path)+str(layer.name())
        output = output.removesuffix('REV_FILL')+'FILLED_DEM.tif'
        ras[(str(layer.name())+'_ras')] = qgis.analysis.QgsRasterCalculatorEntry()
        ras[(str(layer.name())+'_ras')].ref = str(layer.name())+'@1'
        ras[(str(layer.name())+'_ras')].raster = lyr1
        ras[(str(layer.name())+'_ras')].bandNumber = 1
        entries.append(ras[(str(layer.name())+'_ras')])
        computation_str = str(ras[(str(layer.name())+'_ras')].ref + '*-1')
        calc = qgis.analysis.QgsRasterCalculator(computation_str, output, 'GTiff', lyr1.extent(), lyr1.width() ,lyr1.height(),entries)
        calc.processCalculation()
        FILLED_layer_name = layer.name()
        FILLED_layer_name = FILLED_layer_name.removesuffix('REV_FILL')+'FILLED_DEM.tif'
        FILLED_layer = QgsRasterLayer(output,FILLED_layer_name)
        if FILLED_layer.isValid() == False:
            raise Exception("FILLED_layer is invalid")
        #Only add to canvas if layer doesn't already exist
        if len(QgsProject.instance().mapLayersByName(FILLED_layer_name)) == 0:
            QgsProject.instance().addMapLayer(FILLED_layer, False)
            FILLED_DEM_group.addLayer(FILLED_layer)
        else:
            print("Tried to add layer " + FILLED_layer_name + ", however layer already in canvas. Hence layer not added")
    
    #Subtract rasters from no ice raster
    no_ice_layer = QgsRasterLayer(No_ice_FILLED_raster_path)
    no_ice_ras = qgis.analysis.QgsRasterCalculatorEntry()
    no_ice_ras.ref = 'no_ice_ras@1'
    no_ice_ras.raster = no_ice_layer
    no_ice_ras.bandNumber = 1
    ras={} #Initialize raster dictionary
    for layer in FILLED_DEM_group.findLayers():
        entries = []
        entries.append(no_ice_ras)
        lyr1 = QgsRasterLayer(str(FILLED_DEM_folder_path)+str(layer.name()))
        output = str(DIFFERENCE_DEM_folder_path)+str(layer.name())
        output = output.removesuffix('FILLED_DEM.tif')+'DIFFERENCE_DEM.tif'
        ras[(str(layer.name())+'_ras')] = qgis.analysis.QgsRasterCalculatorEntry()
        ras[(str(layer.name())+'_ras')].ref = str(layer.name())+'@1'
        ras[(str(layer.name())+'_ras')].raster = lyr1
        ras[(str(layer.name())+'_ras')].bandNumber = 1
        entries.append(ras[(str(layer.name())+'_ras')])
        computation_str = str(ras[(str(layer.name())+'_ras')].ref + ' - no_ice_ras@1')
        calc = qgis.analysis.QgsRasterCalculator(computation_str, output, 'GTiff', lyr1.extent(), lyr1.width() ,lyr1.height(),entries)
        calc.processCalculation()
        DIFFERENCE_layer_name = layer.name()
        DIFFERENCE_layer_name = DIFFERENCE_layer_name.removesuffix('FILLED_DEM.tif')+'DIFFERENCE_DEM.tif'
        DIFFERENCE_layer = QgsRasterLayer(output,DIFFERENCE_layer_name)
        #Only add to canvas if layer doesn't already exist
        if len(QgsProject.instance().mapLayersByName(DIFFERENCE_layer_name)) == 0:
            QgsProject.instance().addMapLayer(DIFFERENCE_layer, False)
            DIFFERENCE_DEM_group.addLayer(DIFFERENCE_layer)
        else:
            print("Tried to add layer " + DIFFERENCE_layer_name + ", however layer already in canvas. Hence layer not added")
    
    
    #Calculate raster statistics
    for layer in DIFFERENCE_DEM_group.findLayers():
        current_DEM = DIFFERENCE_DEM_folder_path+layer.name()
        current_OUTPUT = STATS_folder_path + layer.name()
        current_OUTPUT = current_OUTPUT.removesuffix('DIFFERENCE_DEM')+"STATS.shp"
        column_prefix = '_'
        parameters = {'COLUMN_PREFIX' : column_prefix, 
        'INPUT' : river_polygon, 
        'INPUT_RASTER' : current_DEM, 
        'OUTPUT' : current_OUTPUT, 
        'RASTER_BAND' : 1,
        'STATISTICS' : [1,2,3,4,5,6]}
        processing_results = processing.run("native:zonalstatisticsfb", parameters)
        STATS_layer_name = str(layer.name()).removesuffix('DIFFERENCE_DEM')+'STATS'
        STATS_layer = QgsVectorLayer(processing_results['OUTPUT'], STATS_layer_name)
        #Only add to canvas if layer doesn't already exist
        if len(QgsProject.instance().mapLayersByName(STATS_layer_name)) == 0:
            QgsProject.instance().addMapLayer(STATS_layer, False)
            STATS_group.addLayer(STATS_layer)
        else:
            print("Tried to add layer " + STATS_layer_name + ", however layer already in canvas. Hence layer not added")
