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
***	loaderScript.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***		Loader Script Component Module.
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
import platform
import re
import socket
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import dbUtilities.types
import foundations.core as core
import foundations.exceptions
import foundations.parser
import ui.widgets.messageBox as messageBox
from foundations.parser import Parser
from foundations.io import File
from globals.constants import Constants
from manager.uiComponent import UiComponent

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class LoaderScript( UiComponent ):
	'''
	This Class Is The LoaderScript Class.
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

		self._uiPath = "ui/Loader_Script.ui"
		self._dockArea = 2

		self._container = None

		self._coreDatabaseBrowser = None
		self._coreTemplatesOutliner = None

		self._ioDirectory = "loaderScripts/"

		self._bindingIdentifierPattern = "@[a-zA-Z0-9_]*"
		self._templateScriptSection = "Script"
		self._templateIblAttributesSection = "sIBL File Attributes"
		self._templateRemoteConnectionSection = "Remote Connection"

		self._win32ExecutionMethod = "ExecuteSIBLLoaderScript"

		self._overrideKeys = {}

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
	def coreTemplatesOutliner( self ):
		'''
		This Method Is The Property For The _coreTemplatesOutliner Attribute.

		@return: self._coreTemplatesOutliner. ( Object )
		'''

		return self._coreTemplatesOutliner

	@coreTemplatesOutliner.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreTemplatesOutliner( self, value ):
		'''
		This Method Is The Setter Method For The _coreTemplatesOutliner Attribute.

		@param value: Attribute Value. ( Object )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "coreTemplatesOutliner" ) )

	@coreTemplatesOutliner.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def coreTemplatesOutliner( self ):
		'''
		This Method Is The Deleter Method For The _coreTemplatesOutliner Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "coreTemplatesOutliner" ) )

	@property
	@core.executionTrace
	def ioDirectory( self ):
		'''
		This Method Is The Property For The _ioDirectory Attribute.

		@return: self._ioDirectory. ( String )
		'''

		return self._ioDirectory

	@ioDirectory.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ioDirectory( self, value ):
		'''
		This Method Is The Setter Method For The _ioDirectory Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "ioDirectory" ) )

	@ioDirectory.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def ioDirectory( self ):
		'''
		This Method Is The Deleter Method For The _ioDirectory Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "ioDirectory" ) )

	@property
	@core.executionTrace
	def bindingIdentifierPattern( self ):
		'''
		This Method Is The Property For The _bindingIdentifierPattern Attribute.

		@return: self._bindingIdentifierPattern. ( String )
		'''

		return self._bindingIdentifierPattern

	@bindingIdentifierPattern.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def bindingIdentifierPattern( self, value ):
		'''
		This Method Is The Setter Method For The _bindingIdentifierPattern Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "bindingIdentifierPattern" ) )

	@bindingIdentifierPattern.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def bindingIdentifierPattern( self ):
		'''
		This Method Is The Deleter Method For The _bindingIdentifierPattern Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "bindingIdentifierPattern" ) )

	@property
	@core.executionTrace
	def templateScriptSection( self ):
		'''
		This Method Is The Property For The _templateScriptSection Attribute.

		@return: self._templateScriptSection. ( String )
		'''

		return self._templateScriptSection

	@templateScriptSection.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateScriptSection( self, value ):
		'''
		This Method Is The Setter Method For The _templateScriptSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "templateScriptSection" ) )

	@templateScriptSection.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateScriptSection( self ):
		'''
		This Method Is The Deleter Method For The _templateScriptSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "templateScriptSection" ) )

	@property
	@core.executionTrace
	def templateIblAttributesSection( self ):
		'''
		This Method Is The Property For The _templateIblAttributesSection Attribute.

		@return: self._templateIblAttributesSection. ( String )
		'''

		return self._templateIblAttributesSection

	@templateIblAttributesSection.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateIblAttributesSection( self, value ):
		'''
		This Method Is The Setter Method For The _templateIblAttributesSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "templateIblAttributesSection" ) )

	@templateIblAttributesSection.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateIblAttributesSection( self ):
		'''
		This Method Is The Deleter Method For The _templateIblAttributesSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "templateIblAttributesSection" ) )

	@property
	@core.executionTrace
	def templateRemoteConnectionSection( self ):
		'''
		This Method Is The Property For The _templateRemoteConnectionSection Attribute.

		@return: self._templateRemoteConnectionSection. ( String )
		'''

		return self._templateRemoteConnectionSection

	@templateRemoteConnectionSection.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateRemoteConnectionSection( self, value ):
		'''
		This Method Is The Setter Method For The _templateRemoteConnectionSection Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Read Only !".format( "templateRemoteConnectionSection" ) )

	@templateRemoteConnectionSection.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def templateRemoteConnectionSection( self ):
		'''
		This Method Is The Deleter Method For The _templateRemoteConnectionSection Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "templateRemoteConnectionSection" ) )

	@property
	@core.executionTrace
	def overrideKeys( self ):
		'''
		This Method Is The Property For The _overrideKeys Attribute.

		@return: self._overrideKeys. ( Dictionary )
		'''

		return self._overrideKeys

	@overrideKeys.setter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def overrideKeys( self, value ):
		'''
		This Method Is The Setter Method For The _overrideKeys Attribute.

		@param value: Attribute Value. ( Dictionary )
		'''

		if value :
			assert type( value ) is dict, "'{0}' Attribute : '{1}' Type Is Not 'dict' !".format( "sections", value )
		self._overrideKeys = value

	@overrideKeys.deleter
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.ProgrammingError )
	def overrideKeys( self ):
		'''
		This Method Is The Deleter Method For The _overrideKeys Attribute.
		'''

		raise foundations.exceptions.ProgrammingError( "'{0}' Attribute Is Not Deletable !".format( "overrideKeys" ) )

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
		self._coreTemplatesOutliner = self._container.componentsManager.components["core.templatesOutliner"].interface

		self._ioDirectory = os.path.join( self._container.userApplicationDirectory, Constants.ioDirectory, self._ioDirectory )
		not os.path.exists( self._ioDirectory ) and os.makedirs( self._ioDirectory )

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
		self._coreTemplatesOutliner = None

		self._ioDirectory = os.path.basename( os.path.abspath( self._ioDirectory ) )

		self._deactivate()

	@core.executionTrace
	def initializeUi( self ):
		'''
		This Method Initializes The Component Ui.
		'''

		LOGGER.debug( "> Initializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		self.ui.Remote_Connection_groupBox.hide()

		# Signals / Slots.
		self.ui.Output_Loader_Script_pushButton.connect( self.ui.Output_Loader_Script_pushButton, SIGNAL( "clicked()" ), self.Output_Loader_Script_pushButton_OnClicked )
		self.ui.Send_To_Software_pushButton.connect( self.ui.Send_To_Software_pushButton, SIGNAL( "clicked()" ), self.Send_To_Software_pushButton_OnClicked )
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget.connect( self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget, SIGNAL( "itemSelectionChanged()" ), self.coreTemplatesOutlinerUi_Templates_Outliner_treeWidget_OnItemSelectionChanged )

	@core.executionTrace
	def uninitializeUi( self ):
		'''
		This Method Uninitializes The Component Ui.
		'''

		LOGGER.debug( "> Uninitializing '{0}' Component Ui.".format( self.__class__.__name__ ) )

		# Signals / Slots.
		self.ui.Output_Loader_Script_pushButton.disconnect( self.ui.Output_Loader_Script_pushButton, SIGNAL( "clicked()" ), self.Output_Loader_Script_pushButton_OnClicked )
		self.ui.Send_To_Software_pushButton.disconnect( self.ui.Send_To_Software_pushButton, SIGNAL( "clicked()" ), self.Send_To_Software_pushButton_OnClicked )
		self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget.disconnect( self._coreTemplatesOutliner.ui.Templates_Outliner_treeWidget, SIGNAL( "itemSelectionChanged()" ), self.coreTemplatesOutlinerUi_Templates_Outliner_treeWidget_OnItemSelectionChanged )

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
	def Output_Loader_Script_pushButton_OnClicked( self ):
		'''
		This Method Is Triggered When Output_Loader_Script_pushButton Is Clicked.
		'''

		self.outputLoadertScript()

	@core.executionTrace
	def coreTemplatesOutlinerUi_Templates_Outliner_treeWidget_OnItemSelectionChanged( self ):
		'''
		This Method Sets Is Triggered When coreTemplatesOutlinerUi_Templates_Outliner_treeWidget Selection Has Changed.
		'''

		template = self._coreTemplatesOutliner.getSelectedTemplate()

		if template :
			templateParser = Parser( template._datas.path )
			templateParser.read() and templateParser.parse( rawSections = ( self._templateScriptSection ) )

			if self._templateRemoteConnectionSection in templateParser.sections :
				self.ui.Remote_Connection_groupBox.show()
				connectionType = foundations.parser.getAttributeCompound( "ConnectionType", templateParser.getValue( "ConnectionType", self._templateRemoteConnectionSection ) )
				if connectionType.value == "Socket" :
					self.ui.Software_Port_spinBox.setValue( int( foundations.parser.getAttributeCompound( "DefaultPort", templateParser.getValue( "DefaultPort", self._templateRemoteConnectionSection ) ).value ) )
					self.ui.Address_lineEdit.setText( QString( foundations.parser.getAttributeCompound( "DefaultAddress", templateParser.getValue( "DefaultAddress", self._templateRemoteConnectionSection ) ).value ) )
					self.ui.Remote_Connection_Options_frame.show()
				elif connectionType.value == "Win32" :
					self.ui.Remote_Connection_Options_frame.hide()
			else :
				self.ui.Remote_Connection_groupBox.hide()
		else :
			self.ui.Remote_Connection_groupBox.hide()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, foundations.exceptions.SocketConnectionError )
	def Send_To_Software_pushButton_OnClicked( self ) :
		'''
		This Method Remotes Connect To Target Software.
		'''

		if self.outputLoadertScript() :
			LOGGER.info( "{0} | Starting Remote Connection !".format( self.__class__.__name__ ) )
			templateParser = Parser( self._coreTemplatesOutliner.getSelectedTemplate()._datas.path )
			templateParser.read() and templateParser.parse( rawSections = ( self._templateScriptSection ) )
			connectionType = foundations.parser.getAttributeCompound( "ConnectionType", templateParser.getValue( "ConnectionType", self._templateRemoteConnectionSection ) )
			if connectionType.value == "Socket" :
				try :
					connection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
					connection.connect( ( str( self.ui.Address_lineEdit.text() ), int( self.ui.Software_Port_spinBox.value() ) ) )
					socketCommand = foundations.parser.getAttributeCompound( "ExecutionCommand", templateParser.getValue( "ExecutionCommand", self._templateRemoteConnectionSection ) ).value.replace( "$loaderScriptPath", os.path.join( self._ioDirectory, self._coreTemplatesOutliner.getSelectedTemplate()._datas.outputScript ) )
					LOGGER.debug( "> Current Socket Command : '%s'.", socketCommand )
					connection.send( socketCommand )
					dataBack = connection.recv( 8192 )
					LOGGER.debug( "> Received Back From Application : '%s'", dataBack )
					connection.close()
					LOGGER.info( "{0} | Ending Remote Connection !".format( self.__class__.__name__ ) )
				except Exception as error:
					messageBox.messageBox( "Error", "Error", "{0} | Remote Connection Error : '{1}' !".format( self.__class__.__name__, error ) )
					raise foundations.exceptions.SocketConnectionError( error )
			elif connectionType.value == "Win32" :
				if platform.system() == "Windows" or platform.system() == "Microsoft":
					try :
						import win32com.client
						connection = win32com.client.Dispatch( foundations.parser.getAttributeCompound( "TargetApplication", templateParser.getValue( "TargetApplication", self._templateRemoteConnectionSection ) ).value )
						connection._FlagAsMethod( self._win32ExecutionMethod )
						connectionCommand = foundations.parser.getAttributeCompound( "ExecutionCommand", templateParser.getValue( "ExecutionCommand", self._templateRemoteConnectionSection ) ).value.replace( "$loaderScriptPath", os.path.join( self._ioDirectory, self._coreTemplatesOutliner.getSelectedTemplate()._datas.outputScript ) )
						LOGGER.debug( "> Current Connection Command : '%s'.", connectionCommand )
						getattr( connection, self._win32ExecutionMethod )( connectionCommand )
					except Exception as error:
						messageBox.messageBox( "Error", "Error", "{0} | Remote Connection On Win32 OLE Server Error: '{1}' !".format( self.__class__.__name__, error ) )
						raise foundations.exceptions.SocketConnectionError( error )

	@core.executionTrace
	def getDefaultOverrideKeys( self ):
		'''
		This Method Gets Default Override Keys.
		'''

		overrideKeys = {}

		selectedSet = self._coreDatabaseBrowser.ui.Database_Browser_listWidget.selectedItems()
		set = selectedSet and selectedSet[0] or None
		overrideKeys["Background|BGfile"] = foundations.parser.getAttributeCompound( "Background|BGfile", set._datas.backgroundImage )
		overrideKeys["Enviroment|EVfile"] = foundations.parser.getAttributeCompound( "Enviroment|EVfile", set._datas.lightingImage )
		overrideKeys["Reflection|REFfile"] = foundations.parser.getAttributeCompound( "Reflection|REFfile", set._datas.reflectionImage )

		return overrideKeys

	@core.executionTrace
	def outputLoadertScript( self ) :
		'''
		This Method Output The Loader Script.
		
		@return: Output Success. ( Boolean )
		'''

		template = self._coreTemplatesOutliner.getSelectedTemplate()

		if not template :
			messageBox.messageBox( "Error", "Error", "{0} | In Order To Output The Loader Script, You Need To Select A Template !".format( self.__class__.__name__ ) )
			return

		if not os.path.exists( template._datas.path ) :
			messageBox.messageBox( "Error", "Error", "{0} | '{1}' Template File Doesn't Exists !".format( self.__class__.__name__, template.name ) )
			return

		selectedSet = self._coreDatabaseBrowser.ui.Database_Browser_listWidget.selectedItems()
		set = selectedSet and selectedSet[0] or None

		if not set :
			messageBox.messageBox( "Error", "Error", "{0} | In Order To Output The Loader Script, You Need To Select A Set !".format( self.__class__.__name__ ) )
			return

		if not os.path.exists( set._datas.path ) :
			messageBox.messageBox( "Error", "Error", "{0} | '{1}' Ibl Set File Doesn't Exists !".format( self.__class__.__name__, set.name ) )
			return

		self._overrideKeys = self.getDefaultOverrideKeys()

		for component in self._container.componentsManager.getComponents() :
			profile = self._container._componentsManager.components[component]
			interface = self._container.componentsManager.getInterface( component )
			if interface.activated and profile.name != self.name :
				hasattr( interface, "getOverrideKeys" ) and interface.getOverrideKeys()

		loaderScript = File( os.path.join( self._ioDirectory, template._datas.outputScript ) )
		loaderScript.content = self.getLoaderScript( template._datas.path, set._datas.path, self._overrideKeys )
		if loaderScript.content and loaderScript.write() :
			messageBox.messageBox( "Information", "Information", "{0} | '{1}' Output Done !".format( self.__class__.__name__, template._datas.outputScript ) )
			return True
		else :
			messageBox.messageBox( "Error", "Error", "{0} | '{1}' Output Failed !".format( self.__class__.__name__, template._datas.outputScript ) )
			return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler( None, False, Exception )
	def getLoaderScript( self, template, iblSet, overrideKeys ):
		'''
		This Method Build A Loader Script.
		
		@param template: Template Path. ( String )
		@param iblSet: iblSet Path. ( String )
		@param overrideKeys: Override Keys. ( Dictionary )
		@return: Loader Script. ( List )
		'''

		templateParser = Parser( template )
		templateParser.read() and templateParser.parse( rawSections = ( self._templateScriptSection ) )
		templateSections = dict.copy( templateParser.sections )

		for attribute, value in dict.copy( templateSections[self._templateIblAttributesSection] ).items():
			templateSections[self._templateIblAttributesSection][foundations.parser.removeNamespace( attribute, rootOnly = True )] = value
			del templateSections[self._templateIblAttributesSection][attribute]

		bindedAttributes = dict( [( attribute, foundations.parser.getAttributeCompound( attribute, value ) ) for section in templateSections.keys() if section not in ( self._templateScriptSection ) for attribute, value in templateSections[section].items() ] )

		iblSetParser = Parser( iblSet )
		iblSetParser.read() and iblSetParser.parse()
		iblSetSections = dict.copy( iblSetParser.sections )

		flattenedIblAttributes = dict( [( attribute, foundations.parser.getAttributeCompound( attribute, value ) ) for section in iblSetSections.keys() for attribute, value in iblSetSections[section].items() ] )

		for attribute in flattenedIblAttributes :
			if attribute in bindedAttributes.keys() :
				bindedAttributes[attribute].value = flattenedIblAttributes[attribute].value

		if "Lights|DynamicLights" in bindedAttributes.keys() :
			dynamicLights = []
			for section in iblSetSections :
				if re.search( "Light[0-9]*", section ) :
					dynamicLights.append( section )
					dynamicLights.append( iblSetParser.getValue( "LIGHTname", section ) )
					lightColorTokens = iblSetParser.getValue( "LIGHTcolor", section ).split( "," )
					for color in lightColorTokens:
						dynamicLights.append( color )
					dynamicLights.append( iblSetParser.getValue( "LIGHTmulti", section ) )
					dynamicLights.append( iblSetParser.getValue( "LIGHTu", section ) )
					dynamicLights.append( iblSetParser.getValue( "LIGHTv", section ) )

					LOGGER.debug( "> Dynamic Lights : '{0}'.".format( ", ".join( dynamicLights ) ) )

			bindedAttributes["Lights|DynamicLights"].value = ",".join( dynamicLights )

		for attribute in overrideKeys :
			if attribute in bindedAttributes.keys() :
				bindedAttributes[attribute].value = overrideKeys[attribute] and overrideKeys[attribute].value or None

		loaderScript = templateParser.sections[self._templateScriptSection][foundations.parser.setNamespace( "Script", templateParser.rawSectionContentIdentifier )]

		bindedLoaderScript = []
		for line in loaderScript :
			bindingParameters = re.findall( "{0}".format( self._bindingIdentifierPattern ), line )
			if bindingParameters:
				for parameter in bindingParameters :
					for attribute in bindedAttributes.values() :
						if parameter == attribute.link :
							line = line.replace( parameter, attribute.value and attribute.value or "-1" )
			bindedLoaderScript.append( line )

		return bindedLoaderScript

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
