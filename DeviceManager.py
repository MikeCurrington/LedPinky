
class DeviceManager:

  def __init__(self):
    self.devices = {}
  
  def Add( self, deviceName, device ):
    self.devices[deviceName] = device

  def ClearPins(self, apply = True):
    for deviceName, device in self.devices.iteritems():
      device.ClearPins( apply )

  def SetPins(self, devicesPortsSettings, apply = True):
    devices = {}
    for pin in devicesPortsSettings:
      if pin[0] in devices:
        devices[pin[0]].add( ( pin[1], pin[2] ) )

    for device,portsSettings in devices.iteritems():
      device.SetPins( portsSettings, apply )

