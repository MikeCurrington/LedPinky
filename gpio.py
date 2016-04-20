import wiringpi
import math

RANGE = 100
fRANGE = float(RANGE)

MARQUEEPIN =0 
FANPIN = 1 
USE_HARD_PWM = True
HARD_PWM_DIV = 192 # divisor of 19.2Mhz base freq
HARD_PWM_RANGE = 1024

class ArcadeGpio:

  def __init__(self):
    self.brightnesses = []
    self.brightnessChanged = False
    self.currentOnOff = 0
    self.wantedOnOff = 0

    wiringpi.wiringPiSetup()

    wiringpi.pinMode(MARQUEEPIN,1)
    wiringpi.softPwmCreate(MARQUEEPIN, 0, RANGE) # set pin 0 to be software pwm and a range of 100 values

    if USE_HARD_PWM:
      wiringpi.pwmSetMode(wiringpi.PWM_MODE_MS)
      wiringpi.pwmSetRange(HARD_PWM_RANGE)
      wiringpi.pwmSetClock(HARD_PWM_DIV) # freq = 19Mhz / range / clock = 9600?
    if USE_HARD_PWM:
      wiringpi.pinMode(FANPIN,wiringpi.PWM_OUTPUT)
    else:
      wiringpi.pinMode(FANPIN,1)
      wiringpi.softPwmCreate(FANPIN, 0, RANGE)

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

  def fanSpeed(self, speed):
    if speed >= RANGE:
      pwm = RANGE
    elif speed < 0:
      pwm = 0
    else:
      pwm = speed
    #wiringpi.softPwmWrite(FANPIN, pwm)
    wiringpi.pwmWrite(FANPIN, pwm*HARD_PWM_RANGE/RANGE)


  def SetAllPins( self, pins, send=True ):
    i = 0
    for pin in pins:
      if self.brightnesses[i] != pin:
        self.brightnesses[i] = pin
        self.brightnessChanged = True
      i = i+1
    for ii in xrange(i,len(self.brightnesses)):
      if self.brightnesses[ii] != 0:
        self.brightnesses[ii] = 0
        self.brightnessChanged = True
    if send:
      self.SendUpdates( self )

  def ClearPins( self, send=True ):
    for i in xrange(len(self.brightnesses)):
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

  def SendUpdates( self ):
    if self.brightnessChanged:
      self.brightnessChanged = False
    if self.wantedOnOff != self.currentOnOff:
      self.currentOnOff = self.wantedOnOff


if __name__ == '__main__':
  test = ArcadeGpio()
  test.marqueeBrightness(10)
  while(True):
    pass


