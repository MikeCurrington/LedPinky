import time
from SequenceBase import SequenceBase


class SequenceLightChase( SequenceBase ):
  def __init__(self, pins):
    super(SequenceLightChase, self).__init__(pins)
    self.seq = -1
    self.brightnesses = []
    for pin in pins:
        self.brightnesses.append( [pin[0], pin[1], 0] )
    self.sequence = [ (1.0, 0.1), (0.0, 0.5), (1.0, 0.1), (0.0, 0.25), (1.0, 0.1), (0.0, 0.25), (1.0, 0.1), (0.2, 0.25), (1.0, 100.0) ]

  def ProcessNext(self):
    if self.seq < len(self.sequence):
      self.seq = self.seq+1
    return self.sequence[self.seq][1]

  def GetPinsChanged(self):
    if self.seq < 0:
      return []

    b = self.sequence[self.seq][0]
    for i in xrange(self.brightnesses):
      self.brightnesses[i][3] = b
    return self.brightnesses



