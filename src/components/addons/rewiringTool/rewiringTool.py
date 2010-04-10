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
***	rewiringTool.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Rewiring Tool Addons Component Module.
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

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.parser
import foundations.strings as strings
import ui.widgets.messageBox as messageBox
from foundations.parser import Parser
from globals.constants import Constants
from manager.uiComponent import UiComponent
from ui.widgets.variable_QPushButton import Variable_QPushButton

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class RewiringTool( UiComponent ):
	'''
	This Class Is The RewiringTool Class.
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

		self._uiPath = "ui/Rewiring_Tool.ui"
		self._dockArea = 2

		self._container = None

		self._coreDatabaseBrowser = None

		self._reWireFramesWidgets = None
		self._reWireComboBoxesWidgets = None
		self._reWireLineEditWidgets = None

		self._addonsLoaderScript = None

		self._rewiringParameters = ( ( "Background", "Background|BGfile", "backgroundImage" ),
									( "Lighting", "Enviroment|EVfile", "lightingImage" ),
									( "Reflection", "Reflection|REFfile", "reflectionImage" ),
									( "Custom Image", None, None ) )

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
	def reWireFramesWidgets( self ):
		'''
		This Method Is The Property For The _reWireFramesWidgets Attribute.

		@return: self._reWireFramesWidgets. ( Tuple )
		'''

		return self._reWireFramesWidgets

	@reWireFramesWidgets.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def reWireFramesWidgets( self, value ):
		'''
		This Method Is The Setter Method For The _reWireFramesWidgets Attribute.

		@param value: Attribute Value. ( Tuple )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "reWireFramesWidgets" ) )

	@reWireFramesWidgets.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def reWireFramesWidgets( self ):
		'''
		This Method Is The Deleter Method For The _reWireFramesWidgets Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "reWireFramesWidgets" ) )

	@property
	@core.executionTrace
	def reWireComboBoxesWidgets( self ):
		'''
		This Method Is The Property For The _reWireComboBoxesWidgets Attribute.

		@return: self._reWireComboBoxesWidgets. ( Tuple )
		'''

		return self._reWireComboBoxesWidgets

	@reWireComboBoxesWidgets.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def reWireComboBoxesWidgets( self, value ):
		'''
		This Method Is The Setter Method For The _reWireComboBoxesWidgets Attribute.

		@param value: Attribute Value. ( Tuple )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "reWireComboBoxesWidgets" ) )

	@reWireComboBoxesWidgets.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def reWireComboBoxesWidgets( self ):
		'''
		This Method Is The Deleter Method For The _reWireComboBoxesWidgets Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "reWireComboBoxesWidgets" ) )

	@property
	@core.executionTrace
	def reWireLineEditWidgets( self ):
		'''
		This Method Is The Property For The _reWireLineEditWidgets Attribute.

		@return: self._reWireLineEditWidgets. ( Tuple )
		'''

		return self._reWireLineEditWidgets

	@reWireLineEditWidgets.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def reWireLineEditWidgets( self, value ):
		'''
		This Method Is The Setter Method For The _reWireLineEditWidgets Attribute.

		@param value: Attribute Value. ( Tuple )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "reWireLineEditWidgets" ) )

	@reWireLineEditWidgets.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def reWireLineEditWidgets( self ):
		'''
		This Method Is The Deleter Method For The _reWireLineEditWidgets Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "reWireLineEditWidgets" ) )

	@property
	@core.executionTrace
	def rewiringParameters( self ):
		'''
		This Method Is The Property For The _rewiringParameters Attribute.

		@return: self._rewiringParameters. ( Tuple )
		'''

		return self._rewiringParameters

	@rewiringParameters.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def rewiringParameters( self, value ):
		'''
		This Method Is The Setter Method For The _rewiringParameters Attribute.

		@param value: Attribute Value. ( Tuple )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "rewiringParameters" ) )

	@rewiringParameters.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def rewiringParameters( self ):
		'''
		This Method Is The Deleter Method For The _rewiringParameters Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "rewiringParameters" ) )

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
		self._container = container

		self._container.templatesCentricLayoutComponents.append( self.name )

		self._coreDatabaseBrowser = self._container.componentsManager.components["core.databaseBrowser"].interface
		self._addonsLoaderScript = self._container.componentsManager.components["addons.loaderScript"].interface

		self._activate()

	@core.executionTrace
	def deactivate( self ):
		'''
		This Method Deactivates The Component.
		'''

		LOGGER.debug( "> Deactivating '{0}' Component.".format( self.__class__.__name__ ) )

		self._container.templatesCentricLayoutComponents.remove( self.name )

		self.uiFile = None
		self._container = None

		self._coreDatabaseBrowser = None
		self._addonsLoaderScript = None

		self._deactivate()

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		self._reWireFramesWidgets = ( self.ui.Background_frame, self.ui.Lighting_frame, self.ui.Reflection_frame )
		self._reWireComboBoxesWidgets = ( self.ui.Background_comboBox, self.ui.Lighting_comboBox, self.ui.Reflection_comboBox )
		self._reWireLineEditWidgets = ( self.ui.Background_Path_lineEdit, self.ui.Lighting_Path_lineEdit, self.ui.Reflection_Path_lineEdit )

		for frame in self._reWireFramesWidgets:
			LOGGER.debug( " > Hiding '%s'.", frame )
			frame.hide()

		for index in range( len( self._reWireComboBoxesWidgets ) ):
			self._reWireComboBoxesWidgets[index]._datas = self._rewiringParameters[index][1]
			self._reWireComboBoxesWidgets[index].addItems( [parameter[0] for parameter in self._rewiringParameters] )
			self._reWireComboBoxesWidgets[index].setCurrentIndex( index )

		# Signals / Slots.
		self.ui.Background_comboBox.connect( self.ui.Background_comboBox, SIGNAL( "activated( int )" ), self.setReWireWidgetFramesVisibility )
		self.ui.Lighting_comboBox.connect( self.ui.Lighting_comboBox, SIGNAL( "activated( int )" ), self.setReWireWidgetFramesVisibility )
		self.ui.Reflection_comboBox.connect( self.ui.Reflection_comboBox, SIGNAL( "activated( int )" ), self.setReWireWidgetFramesVisibility )
		self.ui.Background_Path_toolButton.connect( self.ui.Background_Path_toolButton, SIGNAL( "clicked()" ), self.Background_Path_toolButton_OnClicked )
		self.ui.Lighting_Path_toolButton.connect( self.ui.Lighting_Path_toolButton, SIGNAL( "clicked()" ), self.Lighting_Path_toolButton_OnClicked )
		self.ui.Reflection_Path_toolButton.connect( self.ui.Reflection_Path_toolButton, SIGNAL( "clicked()" ), self.Reflection_Path_toolButton_OnClicked )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		self._reWireFramesWidgets = None
		self._reWireComboBoxesWidgets = None
		self._reWireLineEditWidgets = None

		# Signals / Slots.
		self.ui.Background_comboBox.disconnect( self.ui.Background_comboBox, SIGNAL( "activated( int )" ), self.setReWireWidgetFramesVisibility )
		self.ui.Lighting_comboBox.disconnect( self.ui.Lighting_comboBox, SIGNAL( "activated( int )" ), self.setReWireWidgetFramesVisibility )
		self.ui.Reflection_comboBox.disconnect( self.ui.Reflection_comboBox, SIGNAL( "activated( int )" ), self.setReWireWidgetFramesVisibility )
		self.ui.Background_Path_toolButton.disconnect( self.ui.Background_Path_toolButton, SIGNAL( "clicked()" ), self.Background_Path_toolButton_OnClicked )
		self.ui.Lighting_Path_toolButton.disconnect( self.ui.Lighting_Path_toolButton, SIGNAL( "clicked()" ), self.Lighting_Path_toolButton_OnClicked )
		self.ui.Reflection_Path_toolButton.disconnect( self.ui.Reflection_Path_toolButton, SIGNAL( "clicked()" ), self.Reflection_Path_toolButton_OnClicked )

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
	def setReWireWidgetFramesVisibility( self, index ):
		'''
		This Method Shows / Hides ReWire Widget Frames.

		@param index: ComboBox Index. ( Tuple )
		'''

		for index in range( len( self._reWireComboBoxesWidgets ) ):
			if self._reWireComboBoxesWidgets[index].currentText() == "Custom Image" :
				LOGGER.debug( "> Showing ReWire Frame '%s'.", self._reWireFramesWidgets[index] )
				self._reWireFramesWidgets[index].show()
			else:
				LOGGER.debug( "> Hiding ReWire Frame '%s'.", self._reWireFramesWidgets[index] )
				self._reWireFramesWidgets[index].hide()

	@core.executionTrace
	def setReWireCustomPath( self, component ):
		'''
		This Method Sets The ReWire Custom Image Line Edits.

		@param component: Target Component. ( String )
		'''

		customFile = self._container.storeLastBrowsedPath( QFileDialog.getOpenFileName( self, self.tr( "Custom " + component + " File :" ), self._container.lastBrowsedPath ) )
		LOGGER.debug( "> Chosen Custom %s : '%s'.", component, customFile )
		if customFile != "":
			if component == "Background":
				self.ui.Background_Path_lineEdit.setText( QString( customFile ) )
			elif component == "Lighting":
				self.ui.Lighting_Path_lineEdit.setText( QString( customFile ) )
			elif component == "Reflection":
				self.ui.Reflection_Path_lineEdit.setText( QString( customFile ) )

	@core.executionTrace
	def Background_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Background ToolButton Is Clicked.
		'''

		self.setReWireCustomPath( "Background" )

	@core.executionTrace
	def Lighting_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Lighting ToolButton Is Clicked.
		'''

		self.setReWireCustomPath( "Lighting" )

	@core.executionTrace
	def Reflection_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Reflection ToolButton Is Clicked.
		'''

		self.setReWireCustomPath( "Reflection" )

	@core.executionTrace
	def getOverrideKeys( self ):
		'''
		This Method Gets Override Keys.
		'''

		selectedSet = self._coreDatabaseBrowser.ui.Database_Browser_listWidget.selectedItems()
		set = selectedSet and selectedSet[0] or None

		if set :
			if os.path.exists( set._datas.path ) :
				for index, comboBox in enumerate( self._reWireComboBoxesWidgets ):
					parameter = self._rewiringParameters[comboBox.currentIndex()]
					if comboBox.currentText() == "Custom Image" :
						self._addonsLoaderScript.overrideKeys[comboBox._datas] = foundations.parser.getAttributeCompound( parameter[1], self._reWireLineEditWidgets[index].text() )
					else:
						self._addonsLoaderScript.overrideKeys[comboBox._datas] = getattr( set._datas, parameter[2] ) and foundations.parser.getAttributeCompound( parameter[1], getattr( set._datas, parameter[2] ) )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************