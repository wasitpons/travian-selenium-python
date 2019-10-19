from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Service.util import waitUntil, readConfig

def login(isHeadless):
  config = readConfig()
  print('## Connect to ' + config['SERVER'] + ' ##')
  options = Options()
  options.headless = isHeadless
  options.add_argument('disable-dev-shm-usage')
  browser = webdriver.Chrome(executable_path='Lib/chromedriver', chrome_options=options)
  browser.get(config['SERVER'])

  usernameInput = browser.find_element_by_name('user')
  passwordInput = browser.find_element_by_name('pw')

  usernameInput.send_keys(config['USERNAME'])
  passwordInput.send_keys(config['PASSWORD'])

  submitButton = browser.find_element_by_name('s2')
  print('## Login... ##')
  submitButton.click()
  waitUntil(browser, 5, 'villageBuildings')
  print(' ## Login Successfully ##')
  return browser
