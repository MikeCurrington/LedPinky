import xml.etree.ElementTree as ET
import ConfigParser

import SimpleHTTPServer
import SocketServer
import os
from LedWiz import LedWiz
from LedHttp import LedHttp
from gpio import ArcadeGpio
from GameData import GameData
from PinMap import PinMap
from DeviceManager import DeviceManager
from Sequencer import Sequencer
from SequenceLightChase import SequenceLightChase

ledwiz = LedWiz()
ledwiz.Connect()
gpio = ArcadeGpio()

devices = DeviceManager()
devices.Add( "LEDWIZ", ledwiz )
devices.Add( "GPIO", gpio )
devices.ClearPins()

gamedata = GameData( 'ColorsDefault.ini', 'Colors.ini', 'controls.xml' )
gamedata.run()

marqueeBrightness = 100
fanspeed = 0


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





pinMapping = PinMap('LEDBlinkyInputMap.xml')

sequenceDemo = SequenceLightChase( pinMapping.GetAllPinsOfType('S') )

sequencer = Sequencer( devices )
sequencer.Add( sequenceDemo )
sequencer.start()

ledwiz.ClearPins(False)


class HttpHandler:
  def __init__(self):
    self.ledhttp = LedHttp(self)

  def StartServer(self):
    self.ledhttp.StartServer()

  def SetGame(self, gamename):
    portsAndColors = gamedata.FindGamePortsAndColors( gamename )
    portSettings = pinMapping.TranslatePortsAndColorsToPins( portsAndColors )
    print portSettings
    sequenceThread.running = False

    devices.ClearPins(False)
    devices.SetPins(portSettings)
    
    #ledwiz.ClearPins(False)
    #ledwiz.SetPins(portSettings)

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
    sequenceThread.running = True


ledhttp = HttpHandler()
ledhttp.StartServer()

mameOutputsFilename = '/tmp/sdlmame_out'
os.mkfifo(mameOutputsFilename)

mameOutputsFile = open(mameOutputsFilename, "r")
for nextfetch in mameOutputsFilename:
    print nextfetch


