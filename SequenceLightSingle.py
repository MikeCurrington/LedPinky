import time
from SequenceBase import SequenceBase


class SequenceLightSingle( SequenceBase ):
  def __init__(self, pins):
    super(SequenceLightSingle, self).__init__(pins)
    print("pins %d" % len(pins))
    self.seq = 0
    self.lastSeq = 0
    self.pinsChanged = []
    self.delay = 0.05

  def Restart(self):
    self.seq = 0
    self.lastSeq = 0
    self.pinsChanged = []

  def ProcessNext(self):
    if len(self.pins)<=0:
      return 10.0
    self.pinsChanged = [ [self.pins[self.lastSeq][0], self.pins[self.lastSeq][1], 0.0 ], [self.pins[self.seq][0], self.pins[self.seq][1], 1.0] ]
    #print "seq ", self.pinsChanged
    self.lastSeq = self.seq
    self.seq = self.seq + 1
    if self.seq >= len(self.pins):
      self.seq = 0
    return self.delay

  def ProcessShutdown(self):
    # put everything back to how it was
    self.pinsChanged = [ [self.pins[self.lastSeq][0], self.pins[self.lastSeq][1], 0.0 ] ]  

  def GetPinsChanged(self):
    return self.pinsChanged

  def SetDelay(self, d):
    self.delay = d

