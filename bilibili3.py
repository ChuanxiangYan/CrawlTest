import time
import base64
import numpy as np
import math
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException

usern = 'username'
passwd = 'password'
url = 'https://passport.bilibili.com/login'
# browser = webdriver.Chrome(executable_path='F://BaiduNetdiskDownload//chromedriver.exe')
options = webdriver.ChromeOptions()
# 设置为开发者模式，避免被识别
options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 15)
browser.get(url)
# browser.find_element_by_xpath("//input[@id='login-username']").send_keys(username)
# browser.find_element_by_xpath("//input[@id='login-passwd']").send_keys(passwd)
# browser.find_element_by_xpath("//a[@class='btn btn-login']").click()
username = wait.until(EC.element_to_be_clickable((By.ID, 'login-username')))
password = wait.until(EC.element_to_be_clickable((By.ID, 'login-passwd')))
submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-login')))
# submit = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-login')))
time.sleep(1)
username.send_keys(usern)
time.sleep(1)
password.send_keys(passwd)
time.sleep(1)
submit.click()
time.sleep(2)

# WAIT = WebDriverWait(browser, 15)
# sreach_window=browser.current_window_handle  # 此行代码用来定位当前页面

# 获取base64编码的图片，将图片保存至本地
# bgImg = browser.find_element_by_xpath("//canvas[@class='geetest_canvas_bg geetest_absolute']")
bgImg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas.geetest_canvas_bg")))
JSscript = "return document.getElementsByClassName('geetest_canvas_bg geetest_absolute')[0].toDataURL('image/png')"
bgImgDataBase64 = browser.execute_script(JSscript)
print(bgImgDataBase64)
bgImgDataBase64 = bgImgDataBase64.split('base64,')[-1]
bgImgData = base64.b64decode(bgImgDataBase64)
print(bgImgData)
with open("D:\\PythonWorkspace\\PythonFile\\bilibili\\bgImg.png", "wb") as file:
    file.write(bgImgData)

# fullbg = browser.find_element_by_xpath("//canvas[@class='geetest_canvas_fullbg geetest_fade geetest_absolute']")
bgImg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas.geetest_canvas_fullbg")))
JSscript = "return document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0].toDataURL('image/png')"
fullbgDataBase64 = browser.execute_script(JSscript)
fullbgDataBase64 = fullbgDataBase64.split('base64,')[-1]
fullbgData = base64.b64decode(fullbgDataBase64)
with open("D:\\PythonWorkspace\\PythonFile\\bilibili\\fullbg.png", "wb") as file:
    file.write(fullbgData)

# slider = browser.find_element_by_xpath("//canvas[@class='geetest_canvas_slice geetest_absolute']")
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
# print(bgImg)
# print(fullbg)

fullbg = fullbg[:, :, :-1]
bgImg = bgImg[:, :, :-1]
# img = Image.fromarray((fullbg-bgImg).astype('uint8')).convert('RGB')
# img.show()

# def rgb2hsv(r, g, b):
#     r, g, b = r/255.0, g/255.0, b/255.0
#     mx = max(r, g, b)
#     mn = min(r, g, b)
#     df = mx-mn
#     if mx == mn:
#         h = 0
#     elif mx == r:
#         h = (60 * ((g-b)/df) + 360) % 360
#     elif mx == g:
#         h = (60 * ((b-r)/df) + 120) % 360
#     elif mx == b:
#         h = (60 * ((r-g)/df) + 240) % 360
#     if mx == 0:
#         s = 0
#     else:
#         s = df/mx
#     v = mx
#     return h, s, v
#
#
# def rgb_to_hsv(image):
#     for i in range(len(image)):
#         for j in range(len(image[0, :, :])):
#             a = image[i, j, 0]
#             b = image[i, j, 1]
#             c = image[i, j, 2]
#             # image[i, j, 0], image[i, j, 1], image[i, j, 2] = rgb2hsv(a, b, c)
#             print(rgb2hsv(a, b, c))
#             return


# fullbg.flags.writeable = True
# rgb_to_hsv(fullbg)
# img = Image.fromarray(fullbg).convert('HSV')
# img.show()

def get_path(distance):
    result = []
    current = 0
    mid = distance * 4 / 5
    t = 0.5
    v = 0
    while current < (distance - 12):
        if current < mid:
            a = 1
        else:
            a = -4
        v0 = v
        v = v0 + a * t
        s = v0 * t + 0.5 * a * t * t
        current += s
        # if current > distance - 8:
        #     s = distance - 8 - current - s
        result.append(round(s))
        # result.append(s)
    return result
#
#
def getDistance(fullbg, bgImg):
    m = fullbg - bgImg
    x = 0
    # print("len(m):", len(m))
    # print("len(m[0, :, :]):", len(m[0, :, :]))
    # print("len(m[0, 0, :]):", len(m[0, 0, :]))
    for i in range(len(m)):
        for j in range(len(m[0, :, :])):
            for k in range(len(m[0, 0, :])):
                if m[i, j, k] > 30 and m[i, j, k] < 220:
                    x += 3
                    break
            if x > 15 * 3:
                a = j - 15
                return j, i
        x = 0
    return x, i
#
xOffset, yOffset = getDistance(fullbg, bgImg)
xOffset = xOffset - 15
print(xOffset, yOffset)

sliderBlock = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='geetest_slider_button']")))
sliderWidth = sliderBlock.size['width']

sliderPath = get_path(xOffset)
print(sum(sliderPath))
print(sliderPath)
# sliderPath.reverse()
# print(sliderPath)

action = ActionChains(browser)
action.click_and_hold(sliderBlock).perform()

for x in sliderPath:
    action.move_by_offset(xoffset=x, yoffset=0)
time.sleep(2)
action.release(sliderBlock).perform()
