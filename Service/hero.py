from Service.util import readConfig
import time

class hero:
  def __init__(self, browser): 
    self.browser = browser
  def isDead(self):
    death = self.browser.find_elements_by_class_name('dead')
    return len(death) != 0

  def receive(self):
    config = readConfig()
    print('## Receiving ... ##')
    self.browser.get(config['SERVER'] + '/hero_inventory.php?revive=1')
    time.sleep(1)

# def adventure(browser):
  