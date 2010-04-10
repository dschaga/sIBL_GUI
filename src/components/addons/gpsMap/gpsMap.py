#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2010 - Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	gpsMap.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		GPS Map Component Module.
***
***	Others :
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import ui.widgets.messageBox as messageBox
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Map( QWebView ):
	'''
	This Class Is The QWebView Class.
	'''

	@core.executionTrace
	def __init__( self, parent = None ):
		'''
		This Method Initializes The Class.
		
		@param parent: Widget Parent. ( QObject )
		'''

		QWebView.__init__( self, parent )

	@core.executionTrace
	def addMarker( self, coordinates, title, content ):
		'''
		This Method Adds A Marker To The Map.
		
		@param coordinates: Marker Coordinates. ( Tuple )
		@param title: Marker Title. ( String )
		@param content: Marker Popup Window Content. ( String )
		'''

		self.page().mainFrame().evaluateJavaScript( "addMarker( new google.maps.LatLng({0},{1}),\"{2}\",\"{3}\")".format( coordinates[0], coordinates[1], title, content ) )

	@core.executionTrace
	def removeMarkers( self ):
		'''
		This Method Removes The Map Markers.
		'''

		self.page().mainFrame().evaluateJavaScript( "removeMarkers()" )

	@core.executionTrace
	def setCenter( self ):
		'''
		This Method Center The Map.
		'''

		self.page().mainFrame().evaluateJavaScript( "setCenter()" )

	@core.executionTrace
	def setMapType( self, mapTypeId ):
		'''
		This Method Sets The Map Type.
		'''

		self.page().mainFrame().evaluateJavaScript( "setMapType(\"{0}\")".format( mapTypeId ) )

	@core.executionTrace
	def setZoom( self, type ):
		'''
		This Method Sets The Map Zoom.
		'''

		self.page().mainFrame().evaluateJavaScript( "setZoom(\"{0}\")".format( type ) )

class GpsMap( UiComponent ):
	'''
	This Class Is The GpsMap Class.
	'''

	@core.executionTrace
	def __init__( self, name = None, uiFile = None ):
		'''
		This Method Initializes The Class.
		
		@param name: Component Name. ( String )
		@param uiFile: Ui File. ( String )
		'''

		LOGGER.debug( "> Initializing '{0}()' Class.".format( self.__class__.__name__ ) )

		UiComponent.__init__( self, name = name, uiFile = uiFile )

		# --- Setting Class Attributes. ---
		self.deactivatable = True

		self._uiPath = "ui/Gps_Map.ui"
		self._uiResources = "resources"
		self._uiZoomInIcon = "Zoom_In.png"
		self._uiZoomOutIcon = "Zoom_Out.png"
		self._gpsMapHtmlFile = "Google_Maps.html"
		self._gpsMapBaseSize = QSize( 160, 100 )
		self._dockArea = 2

		self._container = None

		self._coreDatabaseBrowser = None

		self._map = None
		self._mapTypeIds = ( ( "Roadmap", "MapTypeId.ROADMAP" ), ( "Satellite", "MapTypeId.SATELLITE" ), ( "Hybrid", "MapTypeId.HYBRID" ), ( "Terrain", "MapTypeId.TERRAIN" ) )

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	@core.executionTrace
	def uiPath( self ):
		'''
		This Method Is The Property For The _uiPath Attribute.

		@return: self._uiPath. ( String )
		'''

		return self._uiPath

	@uiPath.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self, value ):
		'''
		This Method Is The Setter Method For The _uiPath Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiPath" ) )

	@uiPath.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiPath( self ):
		'''
		This Method Is The Deleter Method For The _uiPath Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiPath" ) )

	@property
	@core.executionTrace
	def uiResources( self ):
		'''
		This Method Is The Property For The _uiResources Attribute.

		@return: self._uiResources. ( String )
		'''

		return self._uiResources

	@uiResources.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self, value ):
		'''
		This Method Is The Setter Method For The _uiResources Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiResources" ) )

	@uiResources.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiResources( self ):
		'''
		This Method Is The Deleter Method For The _uiResources Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiResources" ) )

	@property
	@core.executionTrace
	def uiZoomInIcon( self ):
		'''
		This Method Is The Property For The _uiZoomInIcon Attribute.

		@return: self._uiZoomInIcon. ( String )
		'''

		return self._uiZoomInIcon

	@uiZoomInIcon.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiZoomInIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiZoomInIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiZoomInIcon" ) )

	@uiZoomInIcon.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiZoomInIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiZoomInIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiZoomInIcon" ) )

	@property
	@core.executionTrace
	def uiZoomOutIcon( self ):
		'''
		This Method Is The Property For The _uiZoomOutIcon Attribute.

		@return: self._uiZoomOutIcon. ( String )
		'''

		return self._uiZoomOutIcon

	@uiZoomOutIcon.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiZoomOutIcon( self, value ):
		'''
		This Method Is The Setter Method For The _uiZoomOutIcon Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "uiZoomOutIcon" ) )

	@uiZoomOutIcon.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def uiZoomOutIcon( self ):
		'''
		This Method Is The Deleter Method For The _uiZoomOutIcon Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "uiZoomOutIcon" ) )

	@property
	@core.executionTrace
	def gpsMapHtmlFile( self ):
		'''
		This Method Is The Property For The _gpsMapHtmlFile Attribute.

		@return: self._gpsMapHtmlFile. ( String )
		'''

		return self._gpsMapHtmlFile

	@gpsMapHtmlFile.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def gpsMapHtmlFile( self, value ):
		'''
		This Method Is The Setter Method For The _gpsMapHtmlFile Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "gpsMapHtmlFile" ) )

	@gpsMapHtmlFile.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def gpsMapHtmlFile( self ):
		'''
		This Method Is The Deleter Method For The _gpsMapHtmlFile Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "gpsMapHtmlFile" ) )

	@property
	@core.executionTrace
	def gpsMapBaseSize( self ):
		'''
		This Method Is The Property For The _gpsMapBaseSize Attribute.

		@return: self._gpsMapBaseSize. ( QSize() )
		'''

		return self._gpsMapBaseSize

	@gpsMapBaseSize.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def gpsMapBaseSize( self, value ):
		'''
		This Method Is The Setter Method For The _gpsMapBaseSize Attribute.

		@param value: Attribute Value. ( QSize() )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "gpsMapBaseSize" ) )

	@gpsMapBaseSize.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def gpsMapBaseSize( self ):
		'''
		This Method Is The Deleter Method For The _gpsMapBaseSize Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "gpsMapBaseSize" ) )

	@property
	@core.executionTrace
	def dockArea( self ):
		'''
		This Method Is The Property For The _dockArea Attribute.

		@return: self._dockArea. ( Integer )
		'''

		return self._dockArea

	@dockArea.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dockArea( self, value ):
		'''
		This Method Is The Setter Method For The _dockArea Attribute.

		@param value: Attribute Value. ( Integer )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "dockArea" ) )

	@dockArea.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def dockArea( self ):
		'''
		This Method Is The Deleter Method For The _dockArea Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "dockArea" ) )

	@property
	@core.executionTrace
	def container( self ):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self, value ):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "container" ) )

	@container.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def container( self ):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "container" ) )

	@property
	@core.executionTrace
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Property For The _coreDatabaseBrowser Attribute.

		@return: self._coreDatabaseBrowser. ( Object )
		'''

		return self._coreDatabaseBrowser

	@coreDatabaseBrowser.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self, value ):
		'''
		This Method Is The Setter Method For The _coreDatabaseBrowser Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreDatabaseBrowser" ) )

	@coreDatabaseBrowser.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreDatabaseBrowser( self ):
		'''
		This Method Is The Deleter Method For The _coreDatabaseBrowser Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreDatabaseBrowser" ) )

	@property
	@core.executionTrace
	def map( self ):
		'''
		This Method Is The Property For The _map Attribute.

		@return: self._map. ( QObject )
		'''

		return self._map

	@map.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def map( self, value ):
		'''
		This Method Is The Setter Method For The _map Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "map" ) )

	@map.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def map( self ):
		'''
		This Method Is The Deleter Method For The _map Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "map" ) )

	@property
	@core.executionTrace
	def mapTypeIds( self ):
		'''
		This Method Is The Property For The _mapTypeIds Attribute.

		@return: self._mapTypeIds. ( Tuple )
		'''

		return self._mapTypeIds

	@mapTypeIds.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def mapTypeIds( self, value ):
		'''
		This Method Is The Setter Method For The _mapTypeIds Attribute.

		@param value: Attribute Value. ( Tuple )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "mapTypeIds" ) )

	@mapTypeIds.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def mapTypeIds( self ):
		'''
		This Method Is The Deleter Method For The _mapTypeIds Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "mapTypeIds" ) )

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def activate( self, container ):
		'''
		This Method Activates The Component.
		
		@param container: Container To Attach The Component To. ( QObject )
		'''

		LOGGER.debug( "> Activating '{0}' Component.".format( self.__class__.__name__ ) )

		self.uiFile = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiPath )
		self._uiResources = os.path.join( os.path.dirname( core.getModule( self ).__file__ ), self._uiResources )

		self._container = container

		self._container.setsCentricLayoutComponents.append( self.name )

		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface

		self._activate()

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug( "> Deactivating '{0}' Component.".format( self.__class__.__name__ ) )

		self._container.setsCentricLayoutComponents.remove( self.name )

		self.uiFile = None
		self._uiResources = os.path.basename( self._uiResources )
		self._container = None

		self._coreDatabaseBrowser = None

		self._deactivate()

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		self.ui.Zoom_In_pushButton.setIcon( QIcon( os.path.join( self._uiResources, self._uiZoomInIcon ) ) )
		self.ui.Zoom_Out_pushButton.setIcon( QIcon( os.path.join( self._uiResources, self._uiZoomOutIcon ) ) )

		self.ui.Map_Type_comboBox.addItems( [mapType[0] for mapType in self._mapTypeIds] )

		self._map = Map()
		self._map.setMinimumSize( self._gpsMapBaseSize )
		self._map.load( QUrl( "file://{0}".format( os.path.join( self._uiResources, self._gpsMapHtmlFile ) ) ) )

		self.ui.Map_groupBox_gridLayout.addWidget( self._map )

		# Signals / Slots.
		self._coreDatabaseBrowser.ui.Database_Browser_listWidget.connect( self._coreDatabaseBrowser.ui.Database_Browser_listWidget, SIGNAL( "itemSelectionChanged()" ), self.coreDatabaseBrowser_Database_Browser_listWidget_OnItemSelectionChanged )
		self._map.connect( self._map, SIGNAL( "loadFinished( bool )" ), self.map_OnLoadFinished )
		self.ui.Map_Type_comboBox.connect( self.ui.Map_Type_comboBox, SIGNAL( "activated( int )" ), self.Map_Type_comboBox_OnActivated )
		self.ui.Zoom_In_pushButton.connect( self.ui.Zoom_In_pushButton, SIGNAL( "clicked()" ), self.Zoom_In_pushButton_OnClicked )
		self.ui.Zoom_Out_pushButton.connect( self.ui.Zoom_Out_pushButton, SIGNAL( "clicked()" ), self.Zoom_Out_pushButton_OnClicked )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		# Signals / Slots.
		self._coreDatabaseBrowser.ui.Database_Browser_listWidget.disconnect( self._coreDatabaseBrowser.ui.Database_Browser_listWidget, SIGNAL( "itemSelectionChanged()" ), self.coreDatabaseBrowser_Database_Browser_listWidget_OnItemSelectionChanged )
		self._map.disconnect( self._map, SIGNAL( "loadFinished( bool )" ), self.map_OnLoadFinished )
		self.ui.Map_Type_comboBox.disconnect( self.ui.Map_Type_comboBox, SIGNAL( "activated( int )" ), self.Map_Type_comboBox_OnActivated )
		self.ui.Zoom_In_pushButton.disconnect( self.ui.Zoom_In_pushButton, SIGNAL( "clicked()" ), self.Zoom_In_pushButton_OnClicked )
		self.ui.Zoom_Out_pushButton.disconnect( self.ui.Zoom_Out_pushButton, SIGNAL( "clicked()" ), self.Zoom_Out_pushButton_OnClicked )

	@core.executionTrace
	def addWidget( self ):
		'''
		This Method Adds The Component Widget To The Container.
		'''

		LOGGER.debug( "> Adding '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._container.addDockWidget( Qt.DockWidgetArea( self._dockArea ), self.ui )

	@core.executionTrace
	def removeWidget( self ):
		'''
		This Method Removes The Component Widget From The Container.
		'''

		LOGGER.debug( "> Removing '{0}' Component Widget.".format( self.__class__.__name__ ) )

		self._container.removeDockWidget( self.ui )
		self.ui.setParent( None )

	@core.executionTrace
	def coreDatabaseBrowser_Database_Browser_listWidget_OnItemSelectionChanged( self ):
		'''
		This Method Sets Is Triggered When coreDatabaseBrowser_Database_Browser_listWidget Selection Has Changed.
		'''

		self.setMarkers()

	@core.executionTrace
	def map_OnLoadFinished( self, state ):
		'''
		This Method Is Triggered When The GPS Map Finishes Loading.
		
		@param state: Loading State. ( Boolean )
		'''

		self.setMarkers()

	@core.executionTrace
	def Map_Type_comboBox_OnActivated( self, index ):
		'''
		This Method Is Triggered When Map_Type_comboBox Index Changes.
		
		@param index: ComboBox Activated Item Index. ( Integer )
		'''

		self._map.setMapType( self._mapTypeIds[index][1] )

	@core.executionTrace
	def setMarkers( self ):
		'''
		This Method Triggers The GPS Map Markers.
		'''

		self._map.removeMarkers()

		selectedSets = self._coreDatabaseBrowser.ui.Database_Browser_listWidget.selectedItems()
		for set in selectedSets :
			if set._datas.latitude and set._datas.longitude :
				shotDateString = "<b>Shot Date : </b>{0}".format( self._coreDatabaseBrowser.getFormatedShotDate( set._datas.date, set._datas.time ) )
				content = "<p><b>{0}</b></p><p><b>Author : </b>{1}<br><b>Location : </b>{2}<br>{3}<br><b>Comment : </b>{4}<br><b>Url : </b><a href={5}>{5}</a></p>".format( set._datas.title, set._datas.author, set._datas.location, shotDateString, set._datas.comment, set._datas.link )
				self._map.addMarker( ( set._datas.latitude, set._datas.longitude ), set._datas.title, content )
		self._map.setCenter()

	@core.executionTrace
	def Zoom_In_pushButton_OnClicked( self ):
		'''
		This Method Is Triggered When Zoom_In_pushButton Is Clicked.
		'''

		self._map.setZoom( "In" )

	@core.executionTrace
	def Zoom_Out_pushButton_OnClicked( self ):
		'''
		This Method Is Triggered When Zoom_Out_pushButton Is Clicked.
		'''

		self._map.setZoom( "Out" )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************