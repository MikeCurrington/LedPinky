import threading


class GameData(threading.Thread):

  def __init__( self, defaultColorsIniFilename, gameColorsIniFilename, gameControlsXmlFilename ):
    threading.Thread.__init__(self)
    self.loaded = False
    self.defaultColorsIniFilename = defaultColorsIniFilename
    self.gameColorsIniFilename = gameColorsIniFilename
    self.gameControlsXmlFilename = gameControlsXmlFilename

  def run(self):
    self.gamesColors = LoadGameColorIni(self.gameColorsIniFilename)
    self.defaultColors = LoadGameColorIni(self.defaultColorsIniFilename)
    self.gameControls = LoadControlsXml(self.gameControlsXmlFilename)
    self.mameOutputMappings = LoadMameOutputMapping('ButtonMap.xml')

    self.loaded = True

  def LoadGameColorIni( iniFilename ):
    config = ConfigParser.RawConfigParser()
    config.optionxform = str  # make case sensitive
    config.read(iniFilename)
    colors = {}
    for game in config.sections():
      colors[game] = config.items(game)
    return colors

  def LoadControlsXml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    """
    print(root.tag)
    for child in root:
    #print(child.tag)
    rom = child.get("romname")
    players = child.get("numPlayers")
    
    print( str(rom) + " " + str(players) )
    """


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


  def FindGamePortsAndColors( game ):
    
    if self.loaded==False:
      self.join()
      raise Exception('StillLoading')
    
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
      if color[0] in portMapping:
        ports = portMapping[color[0]]  # we can have multiple led 'ports' mapped to the same mame output (more than one light off a single output)
        for port in ports:
          portsAndColors.append( (port, color[1]) )
              
    print portsAndColors
    return portsAndColors


