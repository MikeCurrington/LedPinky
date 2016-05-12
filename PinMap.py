import xml.etree.ElementTree as ET
import ConfigParser


class PinMap:

  def __init__( self, xmlFilename ):
    pins = ET.parse( xmlFilename )
    pinroot = pins.getroot()

    self.pinMapping = {}
    usedPins = {} 

    pincontrollers = pinroot.iter('ledController')
    for pincontroller in pincontrollers:
      
      device = pincontroller.get("type")
      if device not in usedPins:
        usedPins[device] = []
      
      for pin in pincontroller:
        label = pin.get('label')
        if label == "":
          continue

        pinnumber = int( pin.get('number') )
        if pinnumber in usedPins[device]:
          raise Exception('pin defined twice')
        usedPins[device].append( pinnumber )
        if label not in self.pinMapping:
          self.pinMapping[label] = { "pins":[] }
        self.pinMapping[label]["pins"].append( {"type":pin.get('type'), "pin":pinnumber, "device":device, "group":pin.get('group')} )

        print "added ", pin.get('label'), " ", pin.get('type')


  def TranslatePortsAndColorsToPins( self, portsAndColors ):
    pins = []
    for portAndColor in portsAndColors:
      m = self.pinMapping[ portAndColor[0] ]['pins']
      if len(m) == 1:
        # assume this is a single color port (or single use)
        pins.append( ( m[0]['device'], m[0]['pin'], 1.0 ) )
      else:
        print "Unsupported multicolor led"
    return pins


  def GetAllPins( self ):
    pins = []
    for pinName,pin in self.pinMapping.iteritems():
      m = pin['pins']
      if len(m) == 1:
        # assume this is a single color port (or single use)
        pins.append( ( m[0]['device'], m[0]['pin'] ) )
    return pins

  def GetAllPinsOfType( self, pintype ):
    pins = []
    for pinName,pin in self.pinMapping.iteritems():
      m = pin['pins']
      if len(m) == 1 and m[0]['type'] == pintype:
        # assume this is a single color port (or single use)
        pins.append( ( m[0]['device'], m[0]['pin'] ) )
    return pins

  def GetAllPinsOfDevice( self, deviceName ):
    pins = []
    for pinName,pin in self.pinMapping.iteritems():
      m = pin['pins']
      if len(m) == 1 and m[0]['device'] == deviceName:
        pins.append( ( m[0]['device'], m[0]['pin'] ) )
    return pins  

  def GetAllPinsOfGroup( self, pingroup ):
    pins = []
    for pinName,pin in self.pinMapping.iteritems():
      m = pin['pins']
      if m[0]['group'] == pingroup:
        # assume this is a single color port (or single use)
        pins.append( ( m[0]['device'], m[0]['pin'] ) )
    return pins

