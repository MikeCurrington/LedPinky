
class SequenceBase( threading.Thread ):
  def __init__(self, pins):
    self.pins = pins
    self.running = True
    self.quit = False
    self.daemon = True

  def Tick(self, timeElapsed):
    return []

