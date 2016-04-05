import xml.etree.ElementTree as ET
import ConfigParser
import threading


class GameData(threading.Thread):

  def __init__( self, defaultColorsIniFilename, gameColorsIniFilename, gameControlsXmlFilename ):
    threading.Thread.__init__(self)
    self.loaded = False
    self.defaultColorsIniFilename = defaultColorsIniFilename
    self.gameColorsIniFilename = gameColorsIniFilename
    self.gameControlsXmlFilename = gameControlsXmlFilename

  def run(self):
    self.gamesColors = self.LoadGameColorIni(self.gameColorsIniFilename)
    self.defaultColors = self.LoadGameColorIni(self.defaultColorsIniFilename)
    self.gameControls = self.LoadControlsXml(self.gameControlsXmlFilename)
    self.mameOutputMappings = self.LoadMameOutputMapping('ButtonMap.xml')
    self.loaded = True


  def LoadGameColorIni( self, iniFilename ):
    config = ConfigParser.RawConfigParser()
    config.optionxform = str  # make case sensitive
    config.read(iniFilename)
    colors = {}
    for game in config.sections():
      colors[game] = config.items(game)
    return colors


  def LoadControlsXml(self, filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    controls = {}
    for child in root:
      if child.tag=='game':
        rom = child.get("romname")
        print rom
        players = int( child.get("numPlayers") )
        alternating = (1 == int( child.get("alternating") ))
        #print( str(rom) + " " + str(players) )
        controls[rom] = [players, alternating]
    return controls


  def LoadMameOutputMapping( self, xmlFilename ):
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


  def GetPlayerFromControlName( self, buttonid ):
    if buttonid[0] == 'P' and buttonid[1].isdigit():
      print buttonid[1]
      return int( buttonid[1] )
    else:
      return 0

  def FindGamePortsAndColors( self, game ):
    
    if self.loaded==False:
      self.join()
      raise Exception('StillLoading')
   
    maxControllers = 100 
    if game in self.gameControls:
      gameControl = self.gameControls[game]
      print "found controls ",gameControl
      if gameControl[1]==1:
        maxControllers = 1  # alternating
      else:
        maxControllers = gameControl[0]
    
    if game in self.gamesColors:
      colors = self.gamesColors[game]
      print "found colors ",game
    else:
      colors = self.defaultColors['default']
    
    if game in self.mameOutputMappings:
      portMapping = self.mameOutputMappings[game]
    else:
      portMapping = self.mameOutputMappings['default']
    
    portsAndColors = []
    for color in colors:
      if self.GetPlayerFromControlName(color[0]) <= maxControllers and color[0] in portMapping:
        ports = portMapping[color[0]]  # we can have multiple led 'ports' mapped to the same mame output (more than one light off a single output)
        for port in ports:
          portsAndColors.append( (port, color[1]) )

    print colors, portsAndColors
    return portsAndColors


