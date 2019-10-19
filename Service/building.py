import Service.util as util
import time

config = util.readConfig()

def isMaxLevel(browser):
  try:
    browser.find_element_by_class_name('clocks').text
    return True
  except:
    return False

def getBuildCoolDown(browser):
  coolDownTime = browser.find_element_by_class_name('clocks').text
  coolDownTimeInMinute = str(coolDownTime).split(":")[1]
  coolDownTimeInSecond = str(coolDownTime).split(":")[2]
  buildingName = browser.find_element_by_class_name('titleInHeader').text
  print(
    "######  "+
    buildingName +
    " time: "
    + coolDownTimeInMinute +
    " minute "
    + coolDownTimeInSecond +
    " second ######"
  )
  return (int(coolDownTimeInMinute) * 60) + int(coolDownTimeInSecond) + 0.5

def buildUnit(browser):
  if(isMaxLevel(browser)):
    coolDownTimeInSecond = getBuildCoolDown(browser)
    util.getUpgradeButton(browser).click()
    time.sleep(coolDownTimeInSecond)
  else:
    raise Exception('Your building reach to max level.')

def upgradeToMaxLevel(browser, villageId, buildingId):
  while(True):
    try:
      util.goToVillageBuiding(browser, villageId, buildingId)
      util.waitUntil(browser, 5, 'build_logo')
      buildUnit(browser)
    except:
      buildingName = browser.find_element_by_class_name('titleInHeader')
      print('### ' + str(buildingName.text) + ' have been upgraded. ####')
      break

def autoBuilding(browser):
  print('sth')

def buildFarm(browser):
  villagesId = config["VILLAGESID"]
  farmersList = util.readFarmer()
  for villageId in villagesId:
    for building in farmersList["farmers"]:
      buildingId = building["id"]
      upgradeToMaxLevel(browser, villageId, buildingId)
  # for today
  browser.quit()

def createNewBuilding(browser, buildingId, positionid):
  browser.get(
    config["SERVER"] +
    'dorf2.php?а=' + str(buildingId) +
    "&id=" + str(positionid) +
    "&c=" + util.getBuildingSession
  )

# def buildCity(browser):
#   villagesId = config["VILLAGESID"]
#   buildingList = util.readBuilding()
#   cityList = util.readCity()
#   for villageId in villagesId:
#     for buildingId in farmersList["farmers"]:
      
#       upgradeToMaxLevel(browser, villageId, buildingId)
