import Service.auth as auth
import Service.util as util
import time

SERVER = util.readConfigWithKey("SERVER")

class farm:
  def __init__(self, browser):
    if browser is None:
      self.browser = auth.login()
    self.browser = browser

  def isBroken(self, villageId):
    self.browser.get(SERVER + "/dorf1.php?newdid=" + str(villageId))
    util.waitUntil(self.browser, 5, 'village1')
    time.sleep(1)
    try:
      farm = self.browser.find_elements_by_xpath("//div[contains(@class, 'max')]")
      print("<< Dorf1 Building >> VillageId: " + str(villageId) + " farm: " + str(len(farm)))
      if(len(farm) >= 18):
        return False
      return True
    except:
      return True

  def isMaxLevel(self):
    try:
      self.browser.find_elements_by_xpath("//span[contains(text(), 'maximum')]")
      return True
    except:
      return False

  def getUnitCoolDownInSecond(self):
    maxLevel = self.browser.find_elements_by_xpath("//span[contains(text(), 'maximum')]")
    if(len(maxLevel) > 0):
      raise Exception('Your building reach to max level.')
  
    coolDownContainer = self.browser.find_elements_by_class_name('clocks')
    if(len(coolDownContainer) == 0):
      self.browser.refresh()
      print("Refresh ...")
      time.sleep(2)
      print(self.browser.current_url)
      return self.getUnitCoolDownInSecond()

    coolDownTime = self.browser.find_element_by_class_name('clocks').text
    coolDownTimeInMinute = str(coolDownTime).split(":")[1]
    coolDownTimeInSecond = str(coolDownTime).split(":")[2]
    buildingName = self.browser.find_element_by_class_name('titleInHeader').text
    print(
      "<< Buiding City >>  "+
      buildingName +
      " time: "
      + coolDownTimeInMinute +
      " minute "
      + coolDownTimeInSecond +
      " second"
    )
    return (int(coolDownTimeInMinute) * 60) + int(coolDownTimeInSecond) + 0.5

  def upgradeUnit(self):
    time.sleep(2)
    if(self.isMaxLevel()):
      coolDownTimeInSecond = self.getUnitCoolDownInSecond()
      util.getUpgradeButton(self.browser).click()
      time.sleep(coolDownTimeInSecond)
    else:
      raise Exception('Your building reach to max level.')

  def upgradeToMaxLevel(self, villageId, buildingId):
    while(True):
      try:
        util.goToVillageBuiding(self.browser, villageId, buildingId)
        util.waitUntil(self.browser, 5, 'build_logo')
        self.upgradeUnit()
      except:
        buildingName = self.browser.find_element_by_class_name('titleInHeader')
        print('<< Build >> ' + str(buildingName.text) + ' reach to max level. ####')
        break

  def createNewBuilding(self, buildingId, positionid):
    self.browser.get(
      SERVER +
      'dorf2.php?а=' + str(buildingId) +
      "&id=" + str(positionid) +
      "&c=" + util.getBuildingSession
    )

  def build(self):
    time.sleep(1)
    villagesId = util.readConfigWithKey("VILLAGESID")
    farmersList = util.readFarmer()
    for villageId in villagesId:
      print("<< Move Dorf 1 >> Go to village Id " + str(villageId))
      if(self.isBroken(villageId)):
        for building in farmersList["farmers"]:
          buildingId = building["id"]
          self.upgradeToMaxLevel(villageId, buildingId)