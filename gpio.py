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

  def __init__(self, outputPins):
    self.brightnesses = {}
    self.brightnessesChanged = {}
    for pin in outputPins:
      self.brightnesses[pin[1]] = 0

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


  def ClearPins( self, send=True ):
    for pin,oldBright in self.brightnesses.iteritems():
      if self.brightnesses[pin] != 0:
        self.brightnesses[pin] = 0
        self.brightnessesChanged[pin] = pin
    if send:
      self.SendUpdates()

  def SetPins( self, pinNumberBrightnessPairs, send=True ):
    for pin in pinNumberBrightnessPairs:
      if pin[0] in self.brightnesses:   # make sure the pin is allowed to be written to
        print "gpio pin ", pin
        if self.brightnesses[pin[0]] != pin[1]:
          self.brightnessesChanged[pin[0]] = pin[0]
          self.brightnesses[pin[0]] = pin[1]
    if send:
      self.SendUpdates()

  def SendUpdates( self ):
    print "SendUpdates ", self.brightnessesChanged
    for changedPin in self.brightnessesChanged:
      print "gpio write ", changedPin, " ", RANGE * self.brightnesses[changedPin]
      wiringpi.softPwmWrite(changedPin, int( RANGE * self.brightnesses[changedPin] ))
    self.brightnessesChanged = {}

if __name__ == '__main__':
  test = ArcadeGpio()
  test.marqueeBrightness(10)
  while(True):
    pass


