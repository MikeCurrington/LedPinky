
class SequenceBase(object):
  def __init__(self, pins):
    self.pins = pins
    self.running = True
    self.quit = False
    self.daemon = True

  def ProcessNext(self):
    return 1.0

  def GetPinsChanged(self):
    return []
