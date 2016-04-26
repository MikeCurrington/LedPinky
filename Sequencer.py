import time
import threading
from DeviceManager import DeviceManager



class Sequencer( threading.Thread ):
  def __init__(self, devices):
    threading.Thread.__init__(self)
    self.running = True
    self.quit = False
    self.daemon = True
    self.devices = devices
    self.sequences = []

  def Add( self, sequence ):
    self.sequences.append( sequence )

  def run(self):
    timeUntilNext = 0.0
    sequenceNextEventTimes = {}

    while( self.quit == False ):
      timeOfNextEvent = time.clock()
      while( self.running ):

        currentTime = time.clock()
        shortestWaitTime = 0.5  # check back at least every half second (saves us having to interrupt the wait when we add a new sequence) !
        for sequence in self.sequences:
          if sequence not in sequenceNextEventTimes:
            sequenceNextEventTimes[sequence] = currentTime
          if sequenceNextEventTimes[sequence] <= currentTime:
            timeUntilNext = sequence.ProcessNext( )
            sequenceNextEventTimes[sequence] += timeUntilNext
            waitTime = sequenceNextEventTimes[sequence] - currentTime
            if waitTime < shortestWaitTime:
              shortestWaitTime = waitTime
            pinsChanged = sequence.GetPinsChanged()
            if len(pinsChanged) > 0:
              # we could collect all the pins before setting but for now lets set seperately for each sequence and let them fight!
              self.devices.SetPins( pinsChanged, True )

        if shortestWaitTime > 0.0:
          time.sleep( shortestWaitTime )
        
      while self.running == False:
        time.sleep(0.5)

