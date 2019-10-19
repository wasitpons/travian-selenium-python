import Service.auth as auth
import Service.util as util
import time

SERVER = util.readConfigWithKey("SERVER")

class city:
  def __init__(self, browser):
    if browser is None:
      self.browser = auth.login(False)
    self.browser = browser

  def isBroken(self, villageId):
    self.browser.get(SERVER + "/dorf2.php?newdid=" + str(villageId))
    util.waitUntil(self.browser, 5, 'village2')
    time.sleep(2)
    try:
      city = self.browser.find_elements_by_xpath("//div[contains(@class, 'max')]")
      print("<< Building Dorf2 >> VillageId: " + str(villageId) + " city: " + str(len(city)))
      if(len(city) >= 18):
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
    if(self.isMaxLevel()):
      coolDownTimeInSecond = self.getUnitCoolDownInSecond()
      util.getUpgradeButton(self.browser).click()
      time.sleep(coolDownTimeInSecond)
    else:
      print("Upgrade again ...")
      self.upgradeUnit()

  def upgradeToMaxLevel(self, villageId, positionId):
    while(True):
      try:
        util.goToVillageBuiding(self.browser, villageId, positionId)
        util.waitUntil(self.browser, 5, 'build_logo')
        time.sleep(0.5)
        self.upgradeUnit()
      except:
        buildingName = self.browser.find_element_by_class_name('titleInHeader')
        print('<< Build City >> ' + str(buildingName.text) + ' reach to max level. ####')
        break

  def createUnit(self, villageId, buildingId, positionId):
    session = util.getBuildingSession(self.browser)
    self.browser.get(
      SERVER + "/dorf2.php" +
      "?newdid=" + str(villageId) +
      "&а=" + str(buildingId) +
      "&id=" + str(positionId) +
      "&c=" + str(session)
    )
    time.sleep(1)
  
  def build(self):
    time.sleep(1)
    config = util.readConfig()
    cities = util.readCity()
    buildingList = util.readBuilding()
    villages = config["VILLAGESID"]
    for villageId in villages:
      if(self.isBroken(villageId)):
        for city in cities["cities"]:
          positionId = city["id"]
          buildName = city["building"]
          buildingId = util.getKeyByValue(buildingList, buildName)
          self.createUnit(villageId, buildingId, positionId)
          self.upgradeToMaxLevel(villageId, positionId)