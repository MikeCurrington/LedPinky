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
from SequenceFadeUp import SequenceFadeUp
from SequenceFlicker import SequenceFlicker
from SequenceGroup import SequenceGroup
from SequenceLightChase import SequenceLightChase
from SequenceLightSingle import SequenceLightSingle
from SequenceLightBrightness import SequenceLightBrightness

#make sure we are running from the same folder as this python file is in!
from os.path import abspath, dirname
os.chdir(dirname(abspath(__file__)))


pinMapping = PinMap('PinMap.xml')

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



sequenceLeftDemoCircle = SequenceLightSingle( pinMapping.GetAllPinsOfGroupInOrder('LEFTSTICK')[::-1] )
sequenceLeftDemoCircle.SetDelay(0.2)
sequenceRightDemoCircle = SequenceLightSingle( pinMapping.GetAllPinsOfGroupInOrder('RIGHTSTICK') )
sequenceLeftDemoCircle.SetDelay(0.1)
sequenceDemo = SequenceGroup()
sequenceDemo.Add(sequenceLeftDemoCircle)
sequenceDemo.Add(sequenceRightDemoCircle)
sequenceDemo.SetDelay(0.1)

sequencePulseCoin = SequenceLightBrightness( pinMapping.GetAllPinsOfGroup('COIN') )
sequencePulseCoin.SetBrightness( -1 )
sequenceEmstation = SequenceLightBrightness( pinMapping.GetAllPinsOfGroup('EMSTATION') )
sequenceEmstation.SetBrightness( -1 )

marqueeOn = SequenceFlicker( pinMapping.GetAllPinsOfGroup('MARQUEE') )
marqueeFade = SequenceFadeUp( pinMapping.GetAllPinsOfGroup('MARQUEE') )
marqueeFade.SetTarget(1.0)
sequenceGame = SequenceFadeUp( pinMapping.GetAllPinsOfGroup('PANEL') )
sequenceGame.SetTarget(1.0)
sequenceFan = SequenceFadeUp( pinMapping.GetAllPinsOfGroup('FAN') )

sequencer = Sequencer( devices )
#sequencer.Add( sequenceDemo )
#sequencer.Add( sequencePulseCoin )
sequencer.Add( sequenceEmstation )
#sequencer.Add( marqueeFade )
#sequencer.Add( marqueeOn )
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
    print(portSettings)

    sequencer.Remove( sequenceEmstation )
    sequenceGame.SetOnPins(portSettings)
    sequencer.Add( sequenceGame )
    
  def SetMarqueeBrightness( self, brightness ):
    #gpio.marqueeBrightness( brightness )
    #marqueeBrightness = brightness
    sequencer.Remove( marqueeOn )
    sequencer.Remove( marqueeFade )
    marqueeFade.SetTarget( float(brightness)/100.0 )
    sequencer.Add( marqueeFade ) # this will put the fade to the head of the list - overriding the marqueeOn sequence

  def SetFanSpeed( self, speed ):
    sequencer.Remove( sequenceFan )
    sequenceFan.SetTarget( float(speed)/100.0 )
    sequencer.Add( sequenceFan )

  def SetSleep( self, sleep ):
    sequencer.Remove( sequenceFan )
    if sleep==True:
      sequencer.Remove( sequenceEmstation )
      sequencer.Remove( marqueeOn )
      sequencer.Remove( sequenceGame )
      marqueeFade.SetTarget( 0.0 )
      sequenceFan.SetTarget( 0.0 )
      #gpio.fanSpeed(0)
    else:
      sequencer.Add( sequenceEmstation )
      sequencer.Add( marqueeOn )
      marqueeFade.SetTarget( 1.0 )
      sequenceFan.SetTarget( 1.0 )
    sequencer.Add( sequenceFan )
    sequencer.Add( marqueeFade )

  def SetDemo( self ):
    sequencer.Remove( sequenceGame )
    sequencer.Add( sequenceEmstation )


ledhttp = HttpHandler()
ledhttp.StartServer()

mameOutputsFilename = '/tmp/sdlmame_out'
os.mkfifo(mameOutputsFilename)

mameOutputsFile = open(mameOutputsFilename, "r")
for nextfetch in mameOutputsFilename:
    print nextfetch


