import yagmail
from selenium import webdriver

driver = webdriver.Chrome()
driver.get(
    'https://ilsosappt.cxmflow.com/Appointment/Index/dbe30824-497b-4325-8c5f-68b146a5e898'
)
#click "In Car Driving Test"
icdt = driver.find_element_by_class_name("DataControlBtn")
icdt.click()
#click "Advance In-Car Appointments"
driver.get(
    'https://ilsosappt.cxmflow.com/Appointment/Index/dbe30824-497b-4325-8c5f-68b146a5e898'
)
aica = driver.find_element_by_class_name("DataControlBtn")
aica.click()

#check all shown locations
driver.get(
    'https://ilsosappt.cxmflow.com/Appointment/Index/dbe30824-497b-4325-8c5f-68b146a5e898'
)
locations = driver.find_elements_by_class_name("DataControlBtnUnit")

for location in locations:
    dmv = location.find_elements_by_class_name("center-textDiv")[0]
    if dmv.text.split("\n")[0] == "Chicago West":
        print("FOUND IT!")

# Send mail!
receiver = "danyang2023@u.northwestern.edu"
body = "Chicago North opened up: 'https://ilsosappt.cxmflow.com/Appointment/Index/dbe30824-497b-4325-8c5f-68b146a5e898'"

yag = yagmail.SMTP('ddysideacc@gmail.com',
                   oauth2_file="~/Downloads/oauth2_creds.json")
yag.send(
    to=receiver,
    subject="DMV Appointment Found",
    contents=body,
)