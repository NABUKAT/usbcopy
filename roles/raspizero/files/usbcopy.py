# -*- coding: utf-8 -*-
from logging import getLogger, INFO, FileHandler
import pyudev
import subprocess
import time

# ログ設定
logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(FileHandler("/home/pi/USBCopy/usbcopy.log"))

# オンボードLED設定
com = "echo none > /sys/class/leds/led0/trigger"
subprocess.run(com, shell=True)
led_on = "echo 1 > /sys/class/leds/led0/brightness"
led_off = "echo 0 > /sys/class/leds/led0/brightness"

# 準備完了(緑LEDを5回点滅)
for i in range(5):
    subprocess.run(led_on, shell=True)
    time.sleep(0.5)
    subprocess.run(led_off, shell=True)
    time.sleep(0.5)

# メイン処理
def main():
    global logger
    # モニター開始
    con = pyudev.Context()
    mon = pyudev.Monitor.from_netlink(con)
    mon.filter_by(subsystem='block')
    mon.start()

    # コピー元USBポート(2,3)
    from_path = "none"

    # コピー先USBポート(4,5)
    to_path = "none"

    for dev in iter(mon.poll, None):
        devinfo = dev.get("DEVLINKS")
        # USBメモリ挿入時の処理
        if dev.action == "add" and "part1" in devinfo:
            if "usb_p2" in devinfo:
                logger.info("USBポート2にUSBメモリが挿入されました。")
                from_path = "/misc/p2/"
                usbcopy(from_path, to_path)
            elif "usb_p3" in devinfo:
                logger.info("USBポート3にUSBメモリが挿入されました。")
                from_path = "/misc/p3/"
                usbcopy(from_path, to_path)
            elif "usb_p4" in devinfo:
                logger.info("USBポート4にUSBメモリが挿入されました。")
                to_path = "/misc/p4/"
                usbcopy(from_path, to_path)
            elif "usb_p5" in devinfo:
                logger.info("USBポート5にUSBメモリが挿入されました。")
                to_path = "/misc/p5/"
                usbcopy(from_path, to_path)
        # USBメモリ抜去時の処理
        elif dev.action == "remove" and "part1" in devinfo:
            if "usb_p2" in devinfo or "usb_p3" in devinfo:
                logger.info("コピー元のUSBメモリが抜去されました。")
                # マウント解除
                subprocess.run("umount " + from_path, shell=True)
                from_path = "none"
            elif "usb_p4" in devinfo or "usb_p5" in devinfo:
                logger.info("コピー先のUSBメモリが抜去されました。")
                # マウント解除
                subprocess.run("umount " + to_path, shell=True)
                to_path = "none"

# コピー処理
def usbcopy(from_path, to_path):
    global logger,led_on,led_off
    # USBメモリの状態が整っていなければ何もしない
    if from_path == "none" or to_path == "none":
        return

    # コピー開始サイン(緑LEDを5回点滅し点灯)
    for i in range(5):
        subprocess.run(led_on, shell=True)
        time.sleep(0.5)
        subprocess.run(led_off, shell=True)
        time.sleep(0.5)
    subprocess.run(led_on, shell=True)

    # コピー開始
    logger.info("コピーを開始します。")
    com = "rsync -r --no-owner --no-group --delete " + from_path + " " + to_path
    res = subprocess.run(com, shell=True)
    if res.returncode != 0:
        logger.error(res)
        logger.info("完了しました。")
    else:
        logger.info("完了しました。")
    
    # コピー終了サイン(緑LEDを5回点滅し消灯)
    subprocess.run(led_off, shell=True)
    time.sleep(0.5)
    for i in range(5):
        subprocess.run(led_on, shell=True)
        time.sleep(0.5)
        subprocess.run(led_off, shell=True)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
