import Service.util as util
import Service.auth as auth
from selenium.webdriver.common.keys import Keys
import time

class village:
  def __init__(self, browser):
    if browser is None:
      self.browser = auth.login(True)
    self.browser = browser
  
  def goToDorf1(self, villageId):
    config = util.readConfig()
    self.browser.get(
        config["SERVER"] +
        '/dorf1.php?newdid=' +
        str(villageId)
      )
    util.waitUntil(self.browser, 5, 'contentContainer')

  def submitNewVillage(self):
    try:
      self.browser.find_element_by_name('s1').click()
    except:
      print("<< Error >> something went wrong in submitNewVillage")
  
  def goToFoundNewVillage(self, villageId, newVillageId):
    config = util.readConfig()
    self.browser.get(
      config["SERVER"] +
      "/a2b.php?newdid=" + str(villageId) +
      "&id=" + str(newVillageId) +
      "&s=1"
    )
    util.waitUntil(self.browser, 5, 'troopstipo')

  def isSettlerInVillage(self):
    try:
      village = self.browser.find_elements_by_xpath("//td[text()='Settler']")
      if len(village) > 0:
        return True
      return False
    except:
      return False

  def celebrate(self):
    config = util.readConfig()
    villagesId = config["VILLAGESID"]
    while True:
      if(self.isCelebrate()):
        for villageId in villagesId:
          self.browser.get(
            config["SERVER"] + "/build.php" +
            "?newdid=" + str(villageId) +
            "&id=21&type=2"
          )
          util.waitUntil(self.browser, 5, 'build_logo')
          time.sleep(1)
          try:
            celebrateStatusContainer = self.browser.find_element_by_xpath("//div[@class='villageListBarBox']/div[@class='bar']")
            celebrateStatus = str(celebrateStatusContainer.get_attribute('style')).split(':')[1]
            print("<< Celebrate >> Progress: " + str(celebrateStatus))
            time.sleep(1)
          except:
            print("Error")
      else:
        break

  def isCelebrate(self):
    try:
      villageSlot = self.browser.find_element_by_xpath("//div[contains(@class, 'boxTitleAdditional')]").text
      currentVillageAmount = str(villageSlot).split("/")[0]
      maxVillageAmount = str(villageSlot).split("/")[1]
      return int(currentVillageAmount) == int(maxVillageAmount)
    except:
      print("<< Error >> something went wrong in isNewVillage")

  def getVillageIdWithSettler(self):
    villagesId = util.readConfigWithKey("VILLAGESID")
    for villageId in villagesId:
      self.goToDorf1(villageId)
      if(self.isSettlerInVillage()):
        return villageId
    return None

  def isSubmitTroop(self, villageId):
    try:
      settlerMaximum = self.browser.find_element_by_xpath("//a[contains(@onclick, 'document.snd.t60.value')]").text
      settlerInput = self.browser.find_element_by_name('t60')
      settlerInput.send_keys(settlerMaximum)
      settlerInput.send_keys(Keys.ENTER)
      time.sleep(1)
      return True
    except:
      print("<< Not found >> Can not create settler in village: " + str(villageId))
      return False

  def createSettler(self):
    villagesId = util.readConfigWithKey("VILLAGESID")
    for villageId in villagesId:
      util.goToVillageBuiding(self.browser, villageId, '32')
      util.waitUntil(self.browser, 5, 'build_logo')
      time.sleep(1)
      if(self.isSubmitTroop(villageId)):
        return villageId
    self.create()

  def isSuccessCreateNewVillage(self):
    try:
      self.browser.find_element_by_class_name('error')
      return False
    except:
      return True
    
  def createNewVillage(self, villageId, newVillageId):
    self.goToFoundNewVillage(villageId, newVillageId)
    self.submitNewVillage()

  def waitForCreateNewVillage(self):
    try:
      coolDownTime = self.browser.find_element_by_id('timer5').text
      coolDownTimeInMinute = str(coolDownTime).split(":")[1]
      coolDownTimeInSecond = str(coolDownTime).split(":")[2]

      print(
        "<< Create new village >>" + " Duration: " + 
        coolDownTimeInMinute + " minute " +
        coolDownTimeInSecond + " second"
      )
      time.sleep((int(coolDownTimeInMinute) * 60) + int(coolDownTimeInSecond) + 0.5)
    except:
      print("<< Error >> something went wrong in waitForCreateNewVillage")

  def findNewVillage(self, villageId):
    print("<< Find New Village >> Finding ...")
    newVillageId = int(villageId)
    while True:
      self.createNewVillage(villageId, newVillageId + 1)
      if(self.isSuccessCreateNewVillage()):
        self.waitForCreateNewVillage()
        newVillageId = newVillageId + 1
        break
      print("<Finding ..> VillageId: " + str(newVillageId + 1) + "is not village")

      self.createNewVillage(villageId, newVillageId + 200)
      if(self.isSuccessCreateNewVillage()):
        self.waitForCreateNewVillage()
        newVillageId = newVillageId + 200
        break
      print("<Finding ..> VillageId: " + str(newVillageId + 200) + "is not village")
      newVillageId += 1

    return newVillageId

  def create(self):
    config = util.readConfig()
    villagesId = config["VILLAGESID"]

    villageId = self.getVillageIdWithSettler()
    if villageId is None:
      villageId = self.createSettler()
    
    newVillageId = self.findNewVillage(villageId) 
    villagesId.append(newVillageId)
    config["VILLAGESID"] = villagesId
    util.writeConfig(config)
    print("<< Create Village >> New village id: " + str(newVillageId))
    self.sendResourceToVillageId(newVillageId)
    time.sleep(1)

  def inputCoordinate(self, villageId):
    time.sleep(1)
    x = self.browser.find_element_by_xpath("//a[contains(@href, '" + str(villageId) + "')]//span[@class='coordinateX']").text
    y = self.browser.find_element_by_xpath("//a[contains(@href, '" + str(villageId) + "')]//span[@class='coordinateY']").text

    inputX = self.browser.find_element_by_xpath("//input[@name='x']")
    inputY = self.browser.find_element_by_xpath("//input[@name='y']")

    inputX.send_keys(str(x).split('(')[1])
    inputY.send_keys(str(y).split(')')[0])
    time.sleep(1)
    inputY.send_keys(Keys.ENTER)
    time.sleep(1)

  def inputResource(self):
    try:
      resourceMaximum = self.browser.find_elements_by_xpath("//input[contains(@name, 'r')]")
      for index in range(0,len(resourceMaximum)):
        resourceMaximum[index].send_keys(7500000)
        time.sleep(1)

    except Exception as e:
      print(e)

  def submitResource(self, capitalId, villageId):
    duration = self.browser.find_element_by_xpath("//tr[th/text() = 'Duration:']/td").text
    coolDownTimeInMinute = str(duration).split(":")[1]
    coolDownTimeInSecond = str(duration).split(":")[2]

    print("<< Send Resource >> Duration " + str(duration))
    self.browser.find_element_by_xpath("//button[@id='btn_ok']").send_keys(Keys.ENTER)

    time.sleep((int(coolDownTimeInMinute) * 60) + int(coolDownTimeInSecond) + 0.5)
    print("<< Send Resource >> From village " + str(capitalId) + " to " + str(villageId) + " successful.")

  def sendResourceToVillageId(self, villageId):
    config = util.readConfig()
    capitalId = config["VILLAGESID"][0]
    util.goToVillageBuiding(self.browser, capitalId, '36')
    util.waitUntil(self.browser, 5, 'build_logo')
    self.inputResource()
    self.inputCoordinate(villageId)
    self.submitResource(capitalId, villageId)

  
  