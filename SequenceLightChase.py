import time
from SequenceBase import SequenceBase


class SequenceLightChase( SequenceBase ):
  def __init__(self, pins):
    super(SequenceLightChase, self).__init__(pins)
    self.seq = 0
    self.brightnesses = []
    for pin in pins:
      self.brightnesses.append( [pin[0], pin[1], 0] )

  def ProcessNext(self):
    for x in xrange(len(self.brightnesses)):
      dist = x - self.seq
      if dist > self.seq/2:
        dist = dist - self.seq
      elif dist < -self.seq/2:
        dist = dist + self.seq
      if dist < 0:
        dist = -dist
      b = 63 - 8 * dist
      if b < 0:
        b = 0
      self.brightnesses[x][2] = b
    self.seq = self.seq + 1
    if self.seq > len(self.brightnesses):
      self.seq = 0
    return 0.1

  def GetPinsChanged(self):
    return self.brightnesses

