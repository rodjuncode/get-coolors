import sys
import time
import os.path
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

GET_COOLORS_SCRIPT = "[GET-COOLORS.CO]"
PALETTES_FILE = "palettes.txt"

if (len(sys.argv) > 2 or (len(sys.argv) > 1 and not sys.argv[1].isdigit())):
	# validate argument
	print (GET_COOLORS_SCRIPT + " Illegal arguments. Please inform an integer value for minutes interval (or no argument, to run once). Quitting now.")
	sys.exit()
else:
	# saving delay
	delay = 0
	if len(sys.argv) > 1:
		delay = int(sys.argv[1])


# make it headless, so no browser on the screen
print(GET_COOLORS_SCRIPT + " Setting up Chrome.")
o = webdriver.ChromeOptions()
o.add_argument('headless')

# enable browser logging
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'ALL' }

# creates webdriver
driver = webdriver.Chrome(ChromeDriverManager().install(),desired_capabilities=d,chrome_options=o)

keepCooloring = 1
while (keepCooloring):
	# access coolors.co
	print(GET_COOLORS_SCRIPT + " Acessing coolors.co.")
	driver.get('http://coolors.co/generate')

	# get log
	print(GET_COOLORS_SCRIPT + " Grabbing browser log.")
	log = driver.get_log('browser')

	# extract palette
	print(GET_COOLORS_SCRIPT + " Saving palette.")
	palette = log[1]['message'].split("\"")[1].split(" ")

	# save palette on file
	newPalette = ""
	for color in palette[:-1]:
		newPalette = newPalette + "#" + color + ","
	newPalette = newPalette + "#" + palette[-1] + "\n"
	if (os.path.exists(PALETTES_FILE) and os.path.isfile(PALETTES_FILE)):
		with open(PALETTES_FILE) as old: palettes = old.read()
	else:
		palettes = ""
	with open(PALETTES_FILE, 'w+') as new: new.write(newPalette + palettes)

	# wait for a while until next coolor
	if (delay > 0):
		print(GET_COOLORS_SCRIPT + " Sleeping for " + str(delay) + " minutes, until next Coolor.")
		time.sleep(delay*60)
	else:
		keepCooloring = 0

#quit
print(GET_COOLORS_SCRIPT + " Done & Quitting.")
driver.quit() 