import usb.core
import usb.util
import sys

class LedWiz:

  def __init__(self, defaultPins):
    pass

  #input is a 5 byte list
  def  LWZ_SBA (self, input):
     #find device
     dev = usb.core.find(idVendor=0xfafa, idProduct=0x00f0)
     if dev is None:
        raise ValueError('LedWiz device not found')

     #claim device
     if dev.is_kernel_driver_active(0) is True:
        dev.detach_kernel_driver(0)
     usb.util.claim_interface(dev,0)

     #activate device
     if not dev.get_active_configuration():
        dev.set_configuration(1)


  def ConnectLedwiz ( self ) :
     #find device
     dev = usb.core.find(idVendor=0xfafa, idProduct=0x00f0)
     if dev is None:
        raise ValueError('LedWiz device not found')

     #claim device
     if dev.is_kernel_driver_active(0) is True:
        dev.detach_kernel_driver(0)
     usb.util.claim_interface(dev,0)

     #activate device
     if not dev.get_active_configuration():
        dev.set_configuration(1)

     return dev


  def DisconnectLedwiz ( self, dev ) :
     #release device
     usb.util.release_interface(dev,0)


  def SendUpdates( self ) :

     if (self.resync or self.currentOnOff != self.wantedOnOff or self.wantedPulseSpeed != self.currentPulseSpeed) :
        self.currentOnOff = self.wantedOnOff
        self.currentPulseSpeed = self.wantedPulseSpeed
      
        sbaMsg = [64,(self.currentOnOff>>0)&0xff,(self.currentOnOff>>8)&0xff,(self.currentOnOff>>16)&0xff,(self.currentOnOff>>24)&0xff,self.wantedPulseSpeed,0,0]
        print("sbaMsg " + str(sbaMsg))

        #send message to device
        self.device.ctrl_transfer(0x21, 0x09, 0x0200, 0, sbaMsg)
      
        #use like this to turn all lights on
        #LWZ_SBA([255,255,255,255,4])

        #bmRequesttype - 0x21 - HID
        #bmrequest - 0x09 - SET_REPORT
        #wValue - Report Type and Rport ID - 0x02 0x00
        #wIndex - Interface - 0
        #msg - list of values

     if (self.resync or self.brightnessChanged) :
        self.brightnessChanged = False
        for i in range(0, 31, 8):
           msg = []
           for j in range(0,8,1):
             msg.append( self.brightnesses[i+j] )
           print("bright sbaMsg " + str(msg))
           self.device.ctrl_transfer(0x21, 0x09, 0x0200, 0, msg)

     self.resync = False


  def SetAllPins( self, pins, send=True ):
    i = 0
    self.wantedOnOff = 0
    for pin in pins:
      if pin < 0:
        val = 128-int(pin)
      else:
        val = int(49.0*pin)
      if self.brightnesses[i] != val:
        self.brightnesses[i] = val
        self.brightnessChanged = True
      if val == 0:
        self.wantedOnOff |= (1<<i)
      i = i+1
    if send:
      self.SendUpdates()


  def ClearPins( self, send=True ):
    self.wantedOnOff = 0
    if send:
      self.SendUpdates()


  def SetPins( self, pinNumberBrightnessPairs, send=True ):
    for pin in pinNumberBrightnessPairs:
      #print pin
      pinNum = pin[0]-1
      pinBright = int(49.0 * pin[1])
      if pinBright < 0:
        pinBright = 128 - int(pin[1])
      if self.brightnesses[pinNum] != pinBright:
        self.brightnessChanged = True
        self.brightnesses[pinNum] = pinBright
      if pinBright != 0:
        self.wantedOnOff |= (1<<pinNum)
      else:
        self.wantedOnOff &= ~(1<<pinNum)
    if send:
      self.SendUpdates()


  def __init__(self):
     self.currentOnOff = 0
     self.wantedOnOff = 0xffffffff
     self.currentPulseSpeed = 1
     self.wantedPulseSpeed = 3
     self.brightnesses = []
     for i in range(32):
       self.brightnesses.append( 49 )
     self.resync = True
     self.device = None
  
  def Connect(self):
     if self.device != None:
       self.DisconnectLedwiz(self.device)
     try:
       self.device = self.ConnectLedwiz()
     except AttributeError:
       self.device = None
     self.SendUpdates()

  def __del__(self):
     if self.device != None:
       self.DisconnectLedwiz(self.device)

