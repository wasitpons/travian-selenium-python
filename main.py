import Service.auth as auth
from Service.hero import hero
from Service.farm import farm
from Service.city import city
from Service.village import village
import Service.util as util
import time

isHeadLess = True
browser = auth.login(isHeadLess)

Hero = hero(browser)
Farm = farm(browser)
City = city(browser)
Village = village(browser)

while(True):
  try:
    if(Hero.isDead()):
      Hero.receive()
    
    Farm.build()
    City.build()

    if(Village.isCelebrate()):
      Village.celebrate()

    Village.create()

  except Exception as e:
    print(e)
    browser.close()
