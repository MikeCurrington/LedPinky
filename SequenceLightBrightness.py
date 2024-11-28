import time
from SequenceBase import SequenceBase


class SequenceLightBrightness( SequenceBase ):
  def __init__(self, pins):
    super(SequenceLightBrightness, self).__init__(pins)
    print("SequenceLightBrightness pins %d" % len(pins))
    self.brightness = 0.0
    self.brightnesses = []
    for pin in pins:
      self.brightnesses.append( [pin[0], pin[1], self.brightness] )

  def Restart(self):
    print("SequenceLightBrightness Restart\n")
    pass

  def ProcessNext(self):
    print("seq ", self.brightnesses)
    return 100.0  #delay

  def ProcessShutdown(self):
    # put everything back to how it was
    for i in xrange(len(self.brightnesses)):
      self.brightnesses[i][2] = 0.0
    print("SequenceLightBrightness ProcessShutdown\n")

  def GetPinsChanged(self):
    return self.brightnesses

  def SetBrightness(self, brightness):
    for i in xrange(len(self.brightnesses)):
      self.brightnesses[i][2] = brightness

