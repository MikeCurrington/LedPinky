import wiringpi
import math

RANGE = 100
fRANGE = float(RANGE)

MARQUEEPIN = 1
FANPIN = 2

class ArcadeGpio:

  def __init__(self):
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(MARQUEEPIN,1)
    wiringpi.softPwmCreate(MARQUEEPIN, 0, RANGE) # set pin 0 to be software pwm and a range of 10 values

  def brightnesToLedPwm(self, brightness):
    if brightness <= 0:
      return 0
    elif brightness >= RANGE:
      return RANGE
    else:
      return int( math.ceil ( fRANGE * math.log(brightness,fRANGE) ) )

  def marqueeBrightness(self, brightness):
    pwm = self.brightnesToLedPwm( brightness )
    wiringpi.softPwmWrite(MARQUEEPIN, pwm)




  def SetAllPins( self, pins, send=True ):
    i = 0
    for pin in pins:
      if self.brightnesses[i] != pin:
        self.brightnesses[i] = pin
        self.brightnessChanged = True
      i = i+1
    for ii in xrange(i,self.brightnesses.length):
      if self.brightnesses[ii] != 0:
        self.brightnesses[ii] = 0
        self.brightnessChanged = True
    if send:
      self.SendUpdates( self )

  def ClearPins( self, send=True ):
    for i in xrange(self.brightnesses.length):
      if self.brightnesses[i] != 0:
        self.brightnesses[i] = 0
        self.brightnessChanged = True
    if send:
      self.SendUpdates()

  def SetPins( self, pinNumberBrightnessPairs, send=True ):
    for pin in pinNumberBrightnessPairs:
      if self.brightnesses[pin[0]] != pin[1]:
        self.brightnessChanged = True
        self.brightnesses[pin[0]] = pin[1]
      if pin[1] > 0:
        self.wantedOnOff |= (1<<pin[0])
      else:
        self.wantedOnOff &= ~(1<<pin[0])
    if send:
      self.SendUpdates()



if __name__ == '__main__':
  test = ArcadeGpio()
  test.marqueeBrightness(10)
  while(True):
    pass


