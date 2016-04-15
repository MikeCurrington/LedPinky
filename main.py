import xml.etree.ElementTree as ET
import ConfigParser
import threading
import time

import SimpleHTTPServer
import SocketServer
import time
import os
from LedWiz import LedWiz
from LedHttp import LedHttp
from gpio import ArcadeGpio
from GameData import GameData

ledwiz = LedWiz()
ledwiz.Connect()
gpio = ArcadeGpio()

gamedata = GameData( 'ColorsDefault.ini', 'Colors.ini', 'controls.xml' )
gamedata.run()

marqueeBrightness = 100
fanspeed = 0

def MarqueeFlicker( gpio ):
  gpio.marqueeBrightness( marqueeBrightness )
  time.sleep(0.1)
  gpio.marqueeBrightness( 0 )
  time.sleep(0.5)
  gpio.marqueeBrightness( marqueeBrightness )
  time.sleep(0.1)
  gpio.marqueeBrightness( 0 )
  time.sleep(0.25)
  gpio.marqueeBrightness( marqueeBrightness )
  time.sleep(0.1)
  gpio.marqueeBrightness( 0 )
  time.sleep(0.25)
  gpio.marqueeBrightness( marqueeBrightness )
  time.sleep(0.1)
  gpio.marqueeBrightness( marqueeBrightness / 10 )
  time.sleep(0.25)
  gpio.marqueeBrightness( marqueeBrightness )



class LightSequence( threading.Thread ):
  def __init__(self, pins):
    threading.Thread.__init__(self)
    self.pins = pins
    self.running = True
    self.seq = 0
    self.brightnesses = []
    for pin in pins:
      self.brightnesses.append( [pin, 0] )

  def run(self):
    while( self.running ):
      for x in xrange(len(self.brightnesses)):
        dist = x - self.seq
        if dist > self.seq/2:
          dist = dist - self.seq
        elif dist < -self.seq/2:
          dist = dist + self.seq
        if dist < 0:
          dist = -dist 
        b = 63 - 8 * dist
        if b < 0:
          b = 0
        self.brightnesses[x][1] = b
      ledwiz.SetPins( self.brightnesses, True )
      time.sleep( 0.1 )
      self.seq = self.seq + 1
      if self.seq > len(self.brightnesses):
        self.seq = 0
    while self.running == False:
      time.sleep(0.5)

def LoadPinMapping( xmlFilename ):
  pins = ET.parse( xmlFilename )
  pinroot = pins.getroot()

  pinMapping = {}
  usedPins = []

  pincontrollers = pinroot.iter('ledController')
  for pincontroller in pincontrollers:
    
    device = pincontroller.get("type")
    
    for pin in pincontroller:
      label = pin.get('label')
      if label == "":
        continue

      pinnumber = int( pin.get('number') )
      if pinnumber in usedPins:
        raise Exception('pin defined twice')
      usedPins.append( pinnumber )
      if label not in pinMapping:
        pinMapping[label] = { "pins":[] }
      pinMapping[label]["pins"].append( {"type":pin.get('type'), "pin":pinnumber, "device":device} )

      print pin.get('number')
      pin.get('label')
      pin.get('type')

  return pinMapping


def LoadMameOutputsIni( iniFilename ):

  mappings = {}

  ini = ConfigParser.RawConfigParser()
  ini.optionxform = str  # make case sensitive
  ini.read(iniFilename)
  
  if not ini.has_section("default"):
    raise Exception('Need default section in mame outputs ini')
  
  for game in ini.sections():
    print game
    outputs = ini.items(game)
    
    mappings[game] = outputs
    for pin,out in outputs:
      print out

  return mappings








def TranslatePortsAndColorsToPins( portsAndColors ):
  pins = []
  for portAndColor in portsAndColors:
    m = pinMapping[ portAndColor[0] ]['pins']
    if len(m) == 1:
      # assume this is a single color port (or single use)
      print "1"
      pins.append( ( m[0]['pin'], 63 ) )
  return pins

def GetAllPins():
  pins = []
  for pinName,pin in pinMapping.iteritems():
    print pinName, pin
    m = pin['pins']
    if len(m) == 1:
      # assume this is a single color port (or single use)
      pins.append( m[0]['pin'] )
  return pins



pinMapping = LoadPinMapping('LEDBlinkyInputMap.xml')

sequenceThread = LightSequence( GetAllPins() )
sequenceThread.daemon = True
sequenceThread.start()


#portsAndColors = gamedata.FindGamePortsAndColors( "rtype" )
#portSettings = TranslatePortsAndColorsToPins( portsAndColors )
#print portSettings

ledwiz.ClearPins(False)
#ledwiz.SetPins(portSettings)


"""
i=0
while(True):
  time.sleep(1)
  i = i+1

exit(0)
"""

class HttpHandler:
  def __init__(self):
    self.ledhttp = LedHttp(self)

  def StartServer(self):
    self.ledhttp.StartServer()

  def SetGame(self, gamename):
    portsAndColors = gamedata.FindGamePortsAndColors( gamename )
    portSettings = TranslatePortsAndColorsToPins( portsAndColors )
    print portSettings
    sequenceThread.running = False

    ledwiz.ClearPins(False)
    ledwiz.SetPins(portSettings)

  def SetMarqueeBrightness( self, brightness ):
    gpio.marqueeBrightness( brightness )
    marqueeBrightness = brightness

  def SetFanSpeed( self, speed ):
    gpio.fanSpeed( speed )
    fanspeed = speed

  def SetSleep( self, sleep ):
    if sleep==True:
      ledwiz.ClearPins(True)
      gpio.marqueeBrightness(0)
      gpio.fanSpeed(0)
    else:
      ledwiz.ClearPins(False)
      MarqueeFlicker(gpio)
      ledwiz.SetAllPins( [129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129], True )

  def SetDemo( self ):
    ledwiz.SetAllPins( [129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129], True )
    sequenceThread.running = True

ledhttp = HttpHandler()
ledhttp.StartServer()


mameOutputsFilename = '/tmp/sdlmame_out'
os.mkfifo(mameOutputsFilename)

mameOutputsFile = open(mameOutputsFilename, "r")
for nextfetch in mameOutputsFilename:
    print nextfetch






