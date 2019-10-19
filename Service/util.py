from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time
import random
import math

def readJsonFile(path):
  if os.path.exists(path):
    with open(path, 'r') as f:
      return json.loads(f.read())

def writeJsonFile(path, data):
  if os.path.exists(path):
    with open(path, 'w') as f:
      json.dump(data, f)

def readConfig():
  configFile = 'config.json'
  return readJsonFile(configFile)

def readConfigWithKey(key):
  configFile = 'config.json'
  config = readJsonFile(configFile)
  return config[key]
  
def writeConfig(data):
  configFile = 'config.json'
  writeJsonFile(configFile, data)

def readBuilding():
  bulidingFile = 'Travian/buildings.json'
  return readJsonFile(bulidingFile)

def readFarmer():
  farmersFile = 'Travian/farmers.json'
  return readJsonFile(farmersFile)

def readCity():
  citiesFile = 'Travian/cities.json'
  return readJsonFile(citiesFile)

def readTroop():
  troopsFile = 'Travian/troops.json'
  return readJsonFile(troopsFile)

def waitUntil(browser, timeout, expectClassName):
  WebDriverWait(browser, timeout).until(
  EC.presence_of_element_located((By.CLASS_NAME, expectClassName)))

def goToVillage(browser, villageName):
  print('## Current village ' + villageName + ' ##')
  browser.find_element_by_id('vul_' + villageName).click()

def goToBuildingId(browser, id):
  config = readConfig()
  browser.get(config['SERVER'] + '/build.php?id=' + id)
  time.sleep(1)
  waitUntil(browser, 5, 'build_logo')

def goToVillageBuiding(browser, villageId, buildingId):
  config = readConfig()
  browser.get(config['SERVER'] + "/build.php?newdid=" + str(villageId) + "&id=" + str(buildingId))

def getUpgradeButton(browser):
  upgradeButton = browser.find_element_by_xpath("//button[starts-with(@value, 'Upg')]")
  return upgradeButton

def enableSession(browser):
  browser.find_element_by_xpath("//button[@id='buttonBuild']")
  
def getBuildingSession(browser):
  config = readConfig()
  browser.get(config["SERVER"] + "/build.php?id=33")
  upgradeButton = browser.find_elements_by_xpath("//button[contains(@value, 'Upgrade')]")[0]
  onClickAttribute = upgradeButton.get_attribute('onclick')
  session = str(onClickAttribute).split('&c=')[1][0:3]
  return session

def getShortenedInteger(number_to_shorten):
    trailing_zeros = math.floor(math.log10(abs(number_to_shorten)))
    if trailing_zeros < 3:
        # Ignore everything below 1000
        return trailing_zeros
    elif 3 <= trailing_zeros <= 5:
        # Truncate thousands, e.g. 1.3k
        return str(round(number_to_shorten/(10**3), 1)) + 'k'
    elif 6 <= trailing_zeros <= 8:
        # Truncate millions like 3.2M
        return str(round(number_to_shorten/(10**6), 1)) + 'M'
    else:
        raise ValueError('Values larger or equal to a billion not supported')

def sleep():
  sleepTime = random.randint(15,45)
  print('## Wait ' + str(sleepTime/60) + ' minute ##')
  time.sleep(sleepTime)

def getKeyByValue(datas, value):
  for k, v in datas.items():
    if value == v:
      return k
    
    