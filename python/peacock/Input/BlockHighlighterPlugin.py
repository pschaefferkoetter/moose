#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html

from PyQt5 import QtCore, QtWidgets
import chigger
import peacock
from peacock.ExodusViewer.plugins.ExodusPlugin import ExodusPlugin
from MeshBlockSelectorWidget import MeshBlockSelectorWidget

class BlockHighlighterPlugin(QtWidgets.QGroupBox, ExodusPlugin):
    """
    Widget for controlling the visible blocks/nodesets/sidesets of the mesh.
    Mirrored off of peaocock.Exodus.plugins.BlockPlugin
    """

    #: pyqtSignal: Emitted when window needs to change
    windowRequiresUpdate = QtCore.pyqtSignal()
    highlight = QtCore.pyqtSignal(object, object, object)

    def __init__(self, **kwargs):
        super(BlockHighlighterPlugin, self).__init__(**kwargs)

        self.setMainLayoutName('RightLayout')
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.MainLayout = QtWidgets.QHBoxLayout(self)
        self.MainLayout.setSpacing(10)
        self.setEnabled(False)

        # Block, nodeset, and sideset selector widgets
        self.BlockSelector = MeshBlockSelectorWidget(chigger.exodus.ExodusReader.BLOCK, 'Blocks:')
        self.SidesetSelector = MeshBlockSelectorWidget(chigger.exodus.ExodusReader.SIDESET, 'Boundaries:')
        self.NodesetSelector = MeshBlockSelectorWidget(chigger.exodus.ExodusReader.NODESET, 'Nodesets:')

        self.MainLayout.addWidget(self.BlockSelector)
        self.MainLayout.addWidget(self.SidesetSelector)
        self.MainLayout.addWidget(self.NodesetSelector)

        self.setup()

    def onWindowReader(self, reader):
        """
        Update boundary/nodeset visibility when window is updated.
        """
        self.blockSignals(True)
        self.BlockSelector.updateBlocks(reader)
        self.SidesetSelector.updateBlocks(reader)
        self.NodesetSelector.updateBlocks(reader)
        self.blockSignals(False)

    def onWindowResult(self, result):
        """
        Enable/disable the nodeset/sidest selection based on variable type.
        """
        varinfo = result[0].getCurrentVariableInformation()
        if varinfo:
            if varinfo.object_type == chigger.exodus.ExodusReader.ELEMENTAL:
                self.SidesetSelector.setEnabled(False)
                self.NodesetSelector.setEnabled(False)
            else:
                self.SidesetSelector.setEnabled(True)
                self.NodesetSelector.setEnabled(True)

    def _setupBlockSelector(self, qobject):
        qobject.selectionChanged.connect(self._callbackBlockSelector)

    def _callbackBlockSelector(self):
        block = self.BlockSelector.getBlocks()
        self.SidesetSelector.reset()
        self.NodesetSelector.reset()
        self.highlight.emit(block, None, None)

    def _setupSidesetSelector(self, qobject):
        qobject.selectionChanged.connect(self._callbackSidesetSelector)

    def _callbackSidesetSelector(self):
        sideset = self.SidesetSelector.getBlocks()
        self.BlockSelector.reset()
        self.NodesetSelector.reset()
        self.highlight.emit(None, sideset, None)

    def _setupNodesetSelector(self, qobject):
        qobject.selectionChanged.connect(self._callbackNodesetSelector)

    def _callbackNodesetSelector(self):
        nodeset = self.NodesetSelector.getBlocks()
        self.BlockSelector.reset()
        self.SidesetSelector.reset()
        self.highlight.emit(None, None, nodeset)
