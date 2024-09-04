import schedule
import subprocess
import time
import httpx


def cec(cmd: str):
    subprocess.run(["echo", cmd, "|", "cec-client", "-s", "-d", "1"])


def display():
    httpx.post("http://localhost:9222/json/protocol/Page.reload", json={})
    cec("on 0")
    cec("as")


def standby():
    cec("standby 0")


for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
    getattr(schedule.every(), day).at("07:15").do(display)
    getattr(schedule.every(), day).at("09:15").do(standby)

while 1:
    n = schedule.idle_seconds()
    if n is None:
        # no more jobs
        break
    elif n > 0:
        # sleep exactly the right amount of time
        print("Sleeping", n, "seconds")
        time.sleep(n)
    schedule.run_pending()
