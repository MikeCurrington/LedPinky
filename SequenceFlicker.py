def MarqueeFlicker( gpio ):
  gpio.marqueeBrightness( marqueeBrightness )
  time.sleep(0.1)
  gpio.marqueeBrightness( 0 )
  time.sleep(0.5)
  gpio.marqueeBrightness( marqueeBrightness )
  time.sleep(0.1)
  gpio.marqueeBrightness( 0 )
  time.sleep(0.25)
  gpio.marqueeBrightness( marqueeBrightness )
  time.sleep(0.1)
  gpio.marqueeBrightness( 0 )
  time.sleep(0.25)
  gpio.marqueeBrightness( marqueeBrightness )
  time.sleep(0.1)
  gpio.marqueeBrightness( marqueeBrightness / 10 )
  time.sleep(0.25)
  gpio.marqueeBrightness( marqueeBrightness )



