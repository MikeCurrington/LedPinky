import wiringpi
import math

RANGE = 100
fRANGE = float(RANGE)

USE_HARD_PWM = True
HARD_PWM_PIN = 1
HARD_PWM_DIV = 192 # divisor of 19.2Mhz base freq
HARD_PWM_RANGE = 1024

class ArcadeGpio:

  def __init__(self, outputPins):
    self.brightnesses = {}
    self.brightnessesChanged = {}
    for pin in outputPins:
      self.brightnesses[pin[1]] = 0

    wiringpi.wiringPiSetup()

    # set output modes of pins
    for pin in outputPins:
      self.brightnesses[pin[1]] = 0
      if pin[1] != HARD_PWM_PIN or not USE_HARD_PWM:
        # setup as software pwm pin
        wiringpi.pinMode(pin[1], wiringpi.OUTPUT)
        wiringpi.softPwmCreate(pin[1], 0, RANGE)
      else:
        # hardware pwm pin
        wiringpi.pwmSetMode(wiringpi.PWM_MODE_MS)
        wiringpi.pwmSetRange(HARD_PWM_RANGE)
        wiringpi.pwmSetClock(HARD_PWM_DIV) # freq = 19Mhz / range / clock = 9600?
        wiringpi.pinMode(pin[1], wiringpi.PWM_OUTPUT)

  def brightnesToLedPwm(self, brightness):
    if brightness <= 0:
      return 0
    elif brightness >= RANGE:
      return RANGE
    else:
      return int( math.ceil ( fRANGE * math.log(brightness,fRANGE) ) )

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
      if changedPin==HARD_PWM_PIN and USE_HARD_PWM:
        print "gpio write pwm ", changedPin, " ", HARD_PWM_RANGE * self.brightnesses[changedPin]
        wiringpi.pwmWrite(changedPin, int( HARD_PWM_RANGE * self.brightnesses[changedPin] ))
      else:
        print "gpio write ", changedPin, " ", RANGE * self.brightnesses[changedPin]
        wiringpi.softPwmWrite(changedPin, int( RANGE * self.brightnesses[changedPin] ))
    self.brightnessesChanged = {}

if __name__ == '__main__':
  test = ArcadeGpio()


