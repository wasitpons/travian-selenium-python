import Service.auth as auth
import Service.receive as receive
import Service.util as util
import Service.training as training
import time
import random

browser = auth.login()
while(True):
  # death = browser.find_elements_by_class_name('dead')
  # if(len(death) != 0):
  #   receive.autoReceiveHero(browser)

  # util.goToBuildingId(browser, '30')
  
  # training.autoTrainingTroop(browser)

  
  sleepTime = random.randint(120,300)

  print('## Wait ' + str(sleepTime/60) + ' minute ##')
  time.sleep(sleepTime)