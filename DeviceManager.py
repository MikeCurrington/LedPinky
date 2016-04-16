
class DeviceManager:

  def __init__(self):
    self.devices = {}
  
  def Add( self, device, name ):
    self.devices[name] = device

  def ClearPins(self):
    for device in self.devices:
      device.ClearPins()

  def SetPins(self, devicesPortsSettings):
    devices = {}
    for pin in devicesPortsSettings:
      if pin[0] in devices:
        devices[pin[0]].add( ( pin[1], pin[2] ) )

    for device,portsSettings in devices.iteritems():
      device.SetPins( portsSettings )

