
class DeviceManager:

  def __init__(self):
    self.devices = {}
  
  def Add( self, deviceName, device ):
    self.devices[deviceName] = device

  def ClearPins(self, apply = True):
    for deviceName, device in self.devices.iteritems():
      device.ClearPins( apply )

  def SetPins(self, devicesPortsSettings, apply = True):
    devicesOut = {}
    for pin in devicesPortsSettings:
      if pin[0] in self.devices:
        if pin[0] not in devicesOut:
          devicesOut[pin[0]] = []
        devicesOut[pin[0]].append( ( pin[1], pin[2] ) )

    for deviceName,portsSettings in devicesOut.iteritems():
      #print "dev send ", portsSettings
      self.devices[deviceName].SetPins( portsSettings, apply )

