import time
from SequenceBase import SequenceBase


class SequenceFlicker( SequenceBase ):
  def __init__(self, pins):
    super(SequenceFlicker, self).__init__(pins)
    self.seq = -1
    self.brightnesses = []
    for pin in pins:
        self.brightnesses.append( [pin[0], pin[1], 0] )
    self.sequence = [ (1.0, 0.1), (0.0, 0.5), (1.0, 0.1), (0.0, 0.25), (1.0, 0.1), (0.0, 0.25), (1.0, 0.1), (0.2, 0.25), (1.0, 100.0) ]

  def ProcessNext(self):
    if self.seq < len(self.sequence)-1:
      self.seq = self.seq+1
    return self.sequence[self.seq][1]

  def GetPinsChanged(self):
    if self.seq < 0:
      return []

    b = self.sequence[self.seq][0]
    for i in xrange(len(self.brightnesses)):
      self.brightnesses[i][2] = b
    return self.brightnesses



