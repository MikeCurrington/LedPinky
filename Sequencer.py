


class Sequencer( threading.Thread ):
  def __init__(self, pins):
    threading.Thread.__init__(self)
    self.running = True
    self.quit = False
    self.daemon = True

    self.sequences = []


  def Add( self, sequence ):
    self.sequences.append( sequence )


  def run(self):
    timeUntilNext = 0.0
    sequenceNextEventTimes = 0.0

    while( self.quit == False ):
      timeOfNextEvent = time.clock()
      while( self.running ):

        currentTime = time.clock()
        shortestWaitTime = 1.0  # check back in every second (saves us having to interrupt the wait when we add a new sequence) !
        for sequence in self.sequences:
          if sequence not in sequenceNextEventTimes:
            sequenceNextEventTimes[sequence] = currentTime
          if sequenceNextEventTimes[sequence] <= currentTime:
            sequenceNextEventTimes[sequence] += sequence.ProcessNext( )
            waitTime = sequenceNextEventTimes[sequence] - currentTime
            if waitTime < shortestWaitTime:
              shortestWaitTime = waitTime
            pinsChanged = sequence.GetPinsChanged()
            if length(pinsChanged) > 0:
              # we could collect all the pins before setting but for now lets set seperately for each sequence and let them fight!
              devices.SetPins( pinsChanged, True )

        if shortestWaitTime > 0.0:
          time.sleep( shortestWaitTime )
        
        self.seq = self.seq + 1
        if self.seq > len(self.brightnesses):
          self.seq = 0
      while self.running == False:
        time.sleep(0.5)

