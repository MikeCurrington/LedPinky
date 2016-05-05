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
from SequenceFlicker import SequenceFlicker
from SequenceLightSingle import SequenceLightSingle
from SequenceFadeUp import SequenceFadeUp

pinMapping = PinMap('LEDBlinkyInputMap.xml')

ledwiz = LedWiz( )
ledwiz.Connect()
gpio = ArcadeGpio( pinMapping.GetAllPinsOfDevice('GPIO') )

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





sequenceDemo = SequenceLightSingle( pinMapping.GetAllPinsOfType('S') )
marqueeOn = SequenceFlicker( pinMapping.GetAllPinsOfType('M') )
sequenceGame = SequenceFadeUp( pinMapping.GetAllPinsOfType('S') )

sequencer = Sequencer( devices )
sequencer.Add( sequenceDemo )
sequencer.Add( marqueeOn )
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

    sequencer.Remove( sequenceDemo )
    sequenceGame.SetOnPins(portSettings)
    sequencer.Add( sequenceGame )
    
  def SetMarqueeBrightness( self, brightness ):
    gpio.marqueeBrightness( brightness )
    marqueeBrightness = brightness

  def SetFanSpeed( self, speed ):
    gpio.fanSpeed( speed )
    fanspeed = speed

  def SetSleep( self, sleep ):
    if sleep==True:
      sequencer.Remove( sequenceDemo )
      sequencer.Remove( marqueeOn )
      sequencer.Remove( sequenceGame )
      gpio.fanSpeed(0)
    else:
      sequencer.Add( sequenceDemo )
      sequencer.Add( marqueeOn )

  def SetDemo( self ):
    sequencer.Remove( sequenceGame )
    sequencer.Add( sequenceDemo )


ledhttp = HttpHandler()
ledhttp.StartServer()

mameOutputsFilename = '/tmp/sdlmame_out'
os.mkfifo(mameOutputsFilename)

mameOutputsFile = open(mameOutputsFilename, "r")
for nextfetch in mameOutputsFilename:
    print nextfetch


