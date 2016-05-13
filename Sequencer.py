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
    self.waitingToRemove = []   # sequences we will be removing on the next time around (give them chance to shutdown)
    self.waitingToAdd = []      # sequences will be added next time around (done after a potential shutdown)

  def Add( self, sequence ):
    if sequence not in self.waitingToAdd:
      self.waitingToAdd.append( sequence )

  def Remove( self, sequence ):
    if sequence in self.waitingToAdd:
      self.waitingToAdd.remove( sequence )
    if sequence not in self.waitingToRemove:
      self.waitingToRemove.append( sequence )
    

  def run(self):
    timeUntilNext = 0.0
    sequenceNextEventTimes = {}

    while( self.quit == False ):
      while( self.running ):

        #process everything that wants to shut down
        for sequence in self.waitingToRemove:
          if sequence in self.sequences:
            self.sequences.remove( sequence )
            del sequenceNextEventTimes[sequence]
          
            sequence.ProcessShutdown()
            pinsChanged = sequence.GetPinsChanged()
            if len(pinsChanged) > 0:
              # we could collect all the pins before setting but for now lets set seperately for each sequence and let them fight!
              self.devices.SetPins( pinsChanged, True )
        self.waitingToRemove = []

        #process everything that wants to be added
        for sequence in self.waitingToAdd:
          sequence.Restart()
          if sequence in sequenceNextEventTimes:
            del sequenceNextEventTimes[sequence]
          if sequence not in self.sequences:
            self.sequences.append( sequence )
        self.waitingToAdd = []


        currentTime = time.time()
        shortestWaitTime = 0.5  # check back at least every half second (saves us having to interrupt the wait when we add a new sequence) !
        for sequence in self.sequences:
            if sequence not in sequenceNextEventTimes:
              sequenceNextEventTimes[sequence] = currentTime
            #print "sequenceNextEventTimes[sequence] <= currentTime ", sequenceNextEventTimes[sequence], currentTime
            if sequenceNextEventTimes[sequence] <= currentTime:
              timeUntilNext = sequence.ProcessNext( )
              sequenceNextEventTimes[sequence] += timeUntilNext
              waitTime = sequenceNextEventTimes[sequence] - currentTime
              #print "waittime ", waitTime
              if waitTime < shortestWaitTime:
                shortestWaitTime = waitTime
              pinsChanged = sequence.GetPinsChanged()
            if len(pinsChanged) > 0:
              # we could collect all the pins before setting but for now lets set seperately for each sequence and let them fight!
              #print "setchanged ", pinsChanged
              self.devices.SetPins( pinsChanged, True )


        #print "sleep ", shortestWaitTime
        if shortestWaitTime > 0.0:
          time.sleep( shortestWaitTime )
       
      while self.running == False:
        time.sleep(0.5)

