import Service.util as util
from selenium.webdriver.common.keys import Keys
import time

try:
  config = util.readConfig()
  villages = config['VILLAGES']
  tribu = config['TRIBU']
except:
  print('Training.py can not read json config')

def maximizeTroop(browser, village):
  util.goToVillage(browser, village)
  util.waitUntil(browser, 5, 'build_logo')
  maximumOfTraining = browser.find_elements_by_xpath("//a")[30]
  trainingAmount = maximumOfTraining.text
  return trainingAmount

def submitTroop(browser, trainingAmount, troopName):
  try:
    troops = util.readTroop()
    tribeTroop = troops[tribu]
    trainingInput = browser.find_element_by_name(tribeTroop[troopName])
    trainingInput.send_keys(trainingAmount)
    trainingInput.send_keys(Keys.ENTER)
  except:
    print('Error: Can not train ' + troopName)

def praetorian(browser):
  util.goToBuildingId(browser, '30')
  Praetorian = 0
  for village in villages:
    trainingAmount = maximizeTroop(browser, village)
    submitTroop(browser, trainingAmount, 'Praetorian')
    print('### Praetorian training ' + util.getShortenedInteger(int(trainingAmount)) + ' ##')
    
    Praetorian += int(trainingAmount)
    time.sleep(2)
    util.waitUntil(browser, 5, 'build_logo')

  util.sleep()
  return Praetorian

def imperatoris(browser):
  util.goToBuildingId(browser, '29')
  Imperatoris = 0
  for village in villages:
    trainingAmount = maximizeTroop(browser, village)
    submitTroop(browser, trainingAmount, 'Equites Imperatoris')
    print('### Imperatoris training ' + util.getShortenedInteger(int(trainingAmount)) + ' ##')
    
    Imperatoris += int(trainingAmount)
    time.sleep(2)
    util.waitUntil(browser, 5, 'build_logo')

  util.sleep()
  return Imperatoris