import xml.etree.ElementTree as ET
import ConfigParser

import SimpleHTTPServer
import SocketServer
import time
import os
from LedWiz import LedWiz
from LedHttp import LedHttp
from gpio import ArcadeGpio


ledwiz = LedWiz()
ledwiz.Connect()
gpio = ArcadeGpio()

gpio.marqueeBrightness( 100 )
time.sleep(0.1)
gpio.marqueeBrightness( 0 )
time.sleep(0.5)
gpio.marqueeBrightness( 100 )
time.sleep(0.1)
gpio.marqueeBrightness( 0 )
time.sleep(0.25)
gpio.marqueeBrightness( 100 )
time.sleep(0.1)
gpio.marqueeBrightness( 0 )
time.sleep(0.25)
gpio.marqueeBrightness( 100 )
time.sleep(0.1)
gpio.marqueeBrightness( 10 )
time.sleep(0.25)
gpio.marqueeBrightness( 99 )



def LoadPinMapping( xmlFilename ):
  pins = ET.parse( xmlFilename )
  pinroot = pins.getroot()

  pinMapping = {}
  usedPins = []

  pincontrollers = pinroot.iter('ledController')
  for pincontroller in pincontrollers:
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
      pinMapping[label]["pins"].append( {"type":pin.get('type'), "pin":pinnumber} )

      print pin.get('number')
      pin.get('label')
      pin.get('type')

  return pinMapping

def LoadMameOutputMapping( xmlFilename ):
  mappings = {}

  buttons = ET.parse( xmlFilename )
  buttonroot = buttons.getroot()

  gameButtons = buttonroot.iter('buttons')
  for buttons in gameButtons:
    gamename = buttons.get('game', 'default')
    mapping = {}
    for button in buttons:
      mameName = button.get('mame')
      portName = button.get('port')
      print mameName
      if mameName in mapping:
        mapping[mameName].append( portName )
      else:
        mapping[mameName] = [portName]
    mappings[gamename] = mapping

  return mappings


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


def LoadGameColorIni( iniFilename ):
  config = ConfigParser.RawConfigParser()
  config.optionxform = str  # make case sensitive
  config.read(iniFilename)
  colors = {}
  for game in config.sections():
    colors[game] = config.items(game)
  return colors



pinMapping = LoadPinMapping('LEDBlinkyInputMap.xml')

mameOutputMappings = LoadMameOutputMapping('ButtonMap.xml')

#mameOutputMapping = LoadMameOutputsIni('MameOutputs.ini')




tree = ET.parse('controls.xml')
root = tree.getroot()

"""
print(root.tag)
for child in root:
  #print(child.tag)
  rom = child.get("romname")
  players = child.get("numPlayers")

  print( str(rom) + " " + str(players) )
"""

gamesColors = LoadGameColorIni('Colors.ini')
defaultColors = LoadGameColorIni('ColorsDefault.ini')

def FindGamePortsAndColors( game ):
  if game in gamesColors:
    colors = gamesColors[game]
    print "found colors ",game
  else:
    colors = defaultColors['default']

  if game in mameOutputMappings:
    portMapping = mameOutputMappings[game]
  else:
    portMapping = mameOutputMappings['default']
  
  portsAndColors = [] 
  for color in colors:
    if color[0] in portMapping:
      ports = portMapping[color[0]]  # we can have multiple led 'ports' mapped to the same mame output (more than one light off a single output)
      for port in ports:
        portsAndColors.append( (port, color[1]) )

  print portsAndColors
  return portsAndColors


def TranslatePortsAndColorsToPins( portsAndColors ):
  pins = []
  for portAndColor in portsAndColors:
    m = pinMapping[ portAndColor[0] ]['pins']
    if len(m) == 1:
      # assume this is a single color port (or single use)
      print "1"
      pins.append( ( m[0]['pin'], 63 ) )
  return pins



portsAndColors = FindGamePortsAndColors( "rtype" )
portSettings = TranslatePortsAndColorsToPins( portsAndColors )
print portSettings

ledwiz.ClearPins(False)
ledwiz.SetPins(portSettings)


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
    portsAndColors = FindGamePortsAndColors( gamename )
    portSettings = TranslatePortsAndColorsToPins( portsAndColors )
    print portSettings

    ledwiz.ClearPins(False)
    ledwiz.SetPins(portSettings)


ledhttp = HttpHandler()
ledhttp.StartServer()


mameOutputsFilename = '/tmp/sdlmame_out'
os.mkfifo(mameOutputsFilename)

mameOutputsFile = open(mameOutputsFilename, "r")
for nextfetch in mameOutputsFilename:
    print nextfetch






