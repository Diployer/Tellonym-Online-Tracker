import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_tellonym_online_status(username):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    driver.get(f'https://tellonym.me/{username}')
    wait = WebDriverWait(driver, 10)
    
    try:
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-radium][style*="background-color: rgb(98, 191, 47)"]')))
        online_status = 'Online'
    except:
        online_status = 'Offline'

    driver.quit()
    return online_status

def track_tellonym_online_status(username):
    online_status_file = 'online_status.txt'
    check_interval = 60  
    last_status = None

    while True:
        online_status = check_tellonym_online_status(username)

        if online_status != last_status:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            with open(online_status_file, 'a') as f:
                f.write(f"{timestamp} - Online Status: {online_status}\n")

            last_status = online_status
        time.sleep(check_interval)




def main():
    username = 'user_name'  
    track_tellonym_online_status(username)

main()



