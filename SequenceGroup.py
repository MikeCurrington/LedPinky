import time
from SequenceBase import SequenceBase


class SequenceGroup( SequenceBase ):
  def __init__(self):
    super(SequenceGroup, self).__init__([])
    self.children = []
    self.pinsChanged = []
    self.delay = 0.05

  def Add(self, sequence):
    self.children.append(sequence)

  def Restart(self):
    self.seq = 0
    self.lastSeq = 0
    self.pinsChanged = []
    for child in self.children:
      child.Restart()

  def ProcessNext(self):
    self.pinsChanged = []
    for child in self.children:
      child.ProcessNext()
    for child in self.children:
      for childPins in child.GetPinsChanged():
        self.pinsChanged.append( childPins )
    return self.delay

  def ProcessShutdown(self):
    # put everything back to how it was
    self.pinsChanged = []
    for child in self.children:
      child.ProcessShutdown()
    for child in self.children:
      for childPins in child.GetPinsChanged():
        self.pinsChanged.append( childPins ) 

  def GetPinsChanged(self):
    return self.pinsChanged

  def SetDelay(self, d):
    self.delay = d

