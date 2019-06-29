import time
import base64
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

ACCOUNT = input('请输入您的账号:')
PASSOWRD = input('请输入您的密码:')
url = 'https://passport.bilibili.com/login'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 15)
browser.get(url)
browser.maximize_window()
username = wait.until(EC.element_to_be_clickable((By.ID, 'login-username')))
password = wait.until(EC.element_to_be_clickable((By.ID, 'login-passwd')))
submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-login')))
time.sleep(1)
username.send_keys(ACCOUNT)
time.sleep(1)
password.send_keys(PASSOWRD)
time.sleep(1)
submit.click()
time.sleep(3)

bgImg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas.geetest_canvas_bg")))
JSscript = "return document.getElementsByClassName('geetest_canvas_bg geetest_absolute')[0].toDataURL('image/png')"
bgImgDataBase64 = browser.execute_script(JSscript)
print(bgImgDataBase64)
bgImgDataBase64 = bgImgDataBase64.split('base64,')[-1]
bgImgData = base64.b64decode(bgImgDataBase64)
with open("D:\\PythonWorkspace\\PythonFile\\bilibili\\bgImg.png", "wb") as file:
    file.write(bgImgData)

bgImg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas.geetest_canvas_fullbg")))
JSscript = "return document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0].toDataURL('image/png')"
fullbgDataBase64 = browser.execute_script(JSscript)
fullbgDataBase64 = fullbgDataBase64.split('base64,')[-1]
fullbgData = base64.b64decode(fullbgDataBase64)
with open("D:\\PythonWorkspace\\PythonFile\\bilibili\\fullbg.png", "wb") as file:
    file.write(fullbgData)

bgImg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas.geetest_canvas_slice")))
JSscript = "return document.getElementsByClassName('geetest_canvas_slice geetest_absolute')[0].toDataURL('image/png')"
sliderDataBase64 = browser.execute_script(JSscript)
sliderDataBase64 = fullbgDataBase64.split('base64,')[-1]
sliderData = base64.b64decode(sliderDataBase64)
with open("D:\\PythonWorkspace\\PythonFile\\bilibili\\slider.png", "wb") as file:
    file.write(sliderData)

fullbg = Image.open("D:\\PythonWorkspace\\PythonFile\\bilibili\\fullbg.png")
bgImg = Image.open("D:\\PythonWorkspace\\PythonFile\\bilibili\\bgImg.png")
fullbg = np.asarray(fullbg)
bgImg = np.asarray(bgImg)

fullbg = fullbg[:, :, :-1]
bgImg = bgImg[:, :, :-1]

# img = Image.fromarray((fullbg-bgImg).astype('uint8')).convert('RGB')
# img.show()

def get_path(distance):
    result = []
    current = 0
    mid = distance * 4 / 5
    t = 0.4
    v = 0
    while current < (distance - 9):
        if current < mid:
            a = 1
        else:
            a = -2
        v0 = v
        v = v0 + a * t
        s = v0 * t + 0.5 * a * t * t
        current += s
        result.append(round(s))
    result[-1] = distance - 9 - sum(result[:-1])
    return result


def getDistance(fullbg, bgImg):
    m = fullbg - bgImg
    x = 0
    front = 260
    below = 0
    t = 0
    for i in range(len(m)):
        for j in range(len(m[0, :, :])):
            for k in range(len(m[0, 0, :])):
                if m[i, j, k] > 30 and m[i, j, k] < 220:
                    if j < front:
                        front, below = j, i
                        break
                    break
            if j > front:
                t += 1
                if t == 38:
                    return front, below
                break
    return x, i

xOffset, yOffset = getDistance(fullbg, bgImg)
print(xOffset, yOffset)
sliderBlock = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='geetest_slider_button']")))
sliderWidth = sliderBlock.size['width']

sliderPath = get_path(xOffset)
print("Path sum:", sum(sliderPath))
print(sliderPath)
sliderPath.reverse()
print(sliderPath)

action = ActionChains(browser)
action.click_and_hold(sliderBlock).perform()

for x in sliderPath:
    action.move_by_offset(xoffset=x, yoffset=0)
time.sleep(1)
action.release(sliderBlock).perform()

personBlock = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li[report-id='playpage_account'] > a > .i-face > .face")))

# action.reset_actions()
action.move_to_element(personBlock).perform()

nick_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".header-uname > b")))

print(nick_name.text)
