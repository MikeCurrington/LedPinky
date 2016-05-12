import time
from SequenceBase import SequenceBase


class SequenceFlicker( SequenceBase ):
  def __init__(self, pins):
    super(SequenceFlicker, self).__init__(pins)
    self.seq = 0
    self.brightnesses = []
    for pin in pins:
        self.brightnesses.append( [pin[0], pin[1], 0.0] )
    self.sequence = [ (1.0, 0.1), (0.0, 0.5), (1.0, 0.1), (0.0, 0.25), (1.0, 0.1), (0.0, 0.25), (1.0, 0.1), (0.05, 0.25), (1.0, 0.1), (1.0, 100.0) ]

  def Restart(self):
    self.seq = 0
    for i in xrange(len(self.brightnesses)):
      self.brightnesses[i][2] = 0.0

  def ProcessNext(self):
    b = self.sequence[self.seq][0]
    for i in xrange(len(self.brightnesses)):
      self.brightnesses[i][2] = b

    timeUntilNext = self.sequence[self.seq][1]
    if self.seq < len(self.sequence)-1:
      self.seq = self.seq+1
    return timeUntilNext 

  def ProcessShutdown(self):
    # put everything back to how it was
    for i in xrange(len(self.brightnesses)):
      self.brightnesses[i][2] = 0.0

  def GetPinsChanged(self):
    if self.seq < len(self.sequence):
      return self.brightnesses
    else:
      return []



