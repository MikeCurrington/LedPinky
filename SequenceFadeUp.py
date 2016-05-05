import time
from SequenceBase import SequenceBase


class SequenceFadeUp( SequenceBase ):
  def __init__(self, pins):
    super(SequenceFadeUp, self).__init__(pins)
    self.brightness = 0.0
    self.brightnesses = []
    for pin in pins:
        self.brightnesses.append( [pin[0], pin[1], 0.0] )

  def SetOnPins(self, pins ):
    # n^2 search through the pins we control for the pins we are setting brightness on, not ideal but shouldnt be a performace issue for the numbers of pins we are dealing with
    for i in xrange(len(self.brightnesses)):
      knownPin = self.brightnesses[i]
      found = False
      for pinOn in pins:
        if pinOn[0]==knownPin[0] and pinOn[1]==knownPin[1]:
          self.brightnesses[i][2] = pinOn[2]
          found = True
          break
      if not found:
        self.brightnesses[i][2] = 0.0

  def Restart(self):
    self.brightness = 0.0

  def ProcessNext(self):
    self.brightness += 0.1
    if self.brightness > 1.0:
      self.brightness = 1.0
      return 100.0
    else:
      return 0.1

  def ProcessShutdown(self):
    # put everything back to how it was
    for i in xrange(len(self.brightnesses)):
      self.brightnesses[i][2] = 0.0

  def GetPinsChanged(self):
    return self.brightnesses


