import wiringpi

class ArcadeGpio:

  def __init__(self):
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(0,1)
    wiringpi.softPwmCreate(0, 0, 100) # set pin 0 to be software pwm and a range of 10 values


  def marqueeBrightness(self, speed):
    speed = min(max(speed, 0), 100)
    wiringpi.softPwmWrite(0, speed)

if __name__ == '__main__':
  test = ArcadeGpio()
  test.marqueeBrightness(50)
  while(True):
    pass
