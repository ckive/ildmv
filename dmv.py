import yagmail
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import logging

logger = logging.getLogger('dmv_logs')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('scrapes.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)

driver = webdriver.Chrome()
driver.get(
    'https://ilsosappt.cxmflow.com/Appointment/Index/dbe30824-497b-4325-8c5f-68b146a5e898'
)
#click "In Car Driving Test"
# icdt = driver.find_element_by_class_name("DataControlBtn")
icdt = driver.find_element(by=By.CLASS_NAME, value="DataControlBtn")

icdt.click()
#click "Advance In-Car Appointments"
driver.get(
    'https://ilsosappt.cxmflow.com/Appointment/Index/dbe30824-497b-4325-8c5f-68b146a5e898'
)
aica = driver.find_element(by=By.CLASS_NAME, value="DataControlBtn")
aica.click()

#check all shown locations
driver.get(
    'https://ilsosappt.cxmflow.com/Appointment/Index/dbe30824-497b-4325-8c5f-68b146a5e898'
)
locations = driver.find_elements(by=By.CLASS_NAME, value="center-textDiv")

found = []

for location in locations:
    loc = location.text.split('\n')[0]
    if loc in config['dmv_sites']:
        found.append(loc)

logger.debug('Desired DMV locations not found')

# Send mail!
if found:
    try:
        logger.debug('Appointments found at: {}, sending email'.format(found))
        receiver = config['receiver']
        body = "DMV opened up at {}: 'https://ilsosappt.cxmflow.com/Appointment/Index/dbe30824-497b-4325-8c5f-68b146a5e898'".format(
            found)

        yag = yagmail.SMTP(user=config['user'], password=config['pass'])
        #oauth2_file="~/Desktop/projects/dmv/oauth2_creds.json")
        yag.send(
            to=receiver,
            subject="DMV Appointment Found",
            contents=body,
        )
    except Exception as e:
        logger.error('Email sending failed')