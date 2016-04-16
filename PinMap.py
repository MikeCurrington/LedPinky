import xml.etree.ElementTree as ET
import ConfigParser


class PinMap:

  def __init__( self, xmlFilename ):
    pins = ET.parse( xmlFilename )
    pinroot = pins.getroot()

    self.pinMapping = {}
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
        if label not in self.pinMapping:
          self.pinMapping[label] = { "pins":[] }
        self.pinMapping[label]["pins"].append( {"type":pin.get('type'), "pin":pinnumber, "device":device} )

        print pin.get('number')
        pin.get('label')
        pin.get('type')


  def TranslatePortsAndColorsToPins( self, portsAndColors ):
    pins = []
    for portAndColor in portsAndColors:
      m = self.pinMapping[ portAndColor[0] ]['pins']
      if len(m) == 1:
        # assume this is a single color port (or single use)
        pins.append( ( m[0]['device'], m[0]['pin'], 63 ) )
      else:
        print "Unsupported multicolor led"
    return pins


  def GetAllPins( self ):
    pins = []
    for pinName,pin in self.pinMapping.iteritems():
      print pinName, pin
    m = pin['pins']
    if len(m) == 1:
      # assume this is a single color port (or single use)
      pins.append( ( m[0]['device'], m[0]['pin'] ) )
    return pins



