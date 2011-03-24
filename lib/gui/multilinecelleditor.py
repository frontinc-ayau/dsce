# This file is part of the DomainSharedContactsEditor (DSCE) application.
#
# DSCE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DSCE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DSCE.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (c) 2010 Klaus Melcher (melcher.kla@gmail.com)

# XXX Not ready to use
class MultiLineCellEditor(wx.grid.PyGridCellEditor):
    def __init__(self):
        wx.grid.PyGridCellEditor.__init__(self)
        self.startValue = None
        self.endValue = None

    def Create(self, parent, id, evtHandler):
        self.parent = parent
        self.id = id
        self.evtHandler = evtHandler
        self._edc = ExpandoTextCtrl(parent, size=(200,-1))
        self._edc.SetInsertionPoint(0)
        self.SetControl(self._edc)

        if evtHandler:
            self._edc.PushEventHandler(evtHandler)

        parent.Bind(EVT_ETC_LAYOUT_NEEDED, self.onRefEdit, self._edc)

    def onRefEdit(self):
        log.debug("In onRefEdit()")
        self.Fit()

    def onEnter(self):
        self._edc.WriteText("\n")

    def writeValueToControl(self, value):
        """Used to write the start value to the control.
        """
        if isinstance(value, list):
            for item in value:
                self._edc.WriteText("%s\n" % item)
        else:
            self._edc.WriteText("%s" % value)

    def BeginEdit(self, row, col, grid):
        self.startValue = grid.GetTable().GetValue(row, col)

        self.writeValueToControl(self.startValue)

        grid.Bind(wx.EVT_KEY_DOWN, self.onKeyDown, self._edc) # main purpose to catch ENTER

    def setRowSize(self, grid, row, height):
        grid.SetRowSize(row, height)
        grid.ForceRefresh()
        self._edc.SetMinSize((200,height))
        

    def valueChanged(self):
        """True if startValue and endValue changed, else False.
        """
        self.endValue = self.endValue.replace(',',' ').replace(';',' ')

        if self.endValue.split() == self.startValue:
            return False
        else:
            return True


    def EndEdit(self, row, col, grid):
        changed = False
        self.endValue = self._edc.GetValue()

        if self.valueChanged():
            grid.GetTable().SetValue(row, col, self.endValue)
            changed = True

        self.cleanup()

        return changed
