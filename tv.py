import schedule
import subprocess
import time
import reload


def cec(cmd: str):
    print("Sending", cmd)
    bash_command = f'echo "{cmd}" | cec-client -s -d 1'
    subprocess.run(bash_command, shell=True)


def display():
    reload.run_reload()
    cec("on 0")
    cec("as")


def standby():
    cec("standby 0")


for day in ["tuesday", "thursday"]:
    getattr(schedule.every(), day).at("07:15").do(display)
    getattr(schedule.every(), day).at("09:15").do(standby)

if __name__ == "__main__":
    while 1:
        n = schedule.idle_seconds()
        if n is None:
            print("No more jobs, exiting")
            break
        elif n > 0:
            # sleep exactly the right amount of time
            print("Sleeping", n, "seconds")
            time.sleep(n)
        schedule.run_pending()
