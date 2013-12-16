
import traceback
import logging
import sys

exec(open("debug.cfg").read())

log = logging.getLogger("R") # "R" stands for 'root'
log.setLevel(level)

console = logging.StreamHandler()
console.setLevel(level)

logfile = logging.FileHandler("debug.log")
logfile.setLevel(level)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)8s | %(name)s |: %(message)s")

console.setFormatter(formatter)
logfile.setFormatter(formatter)

log.addHandler(console)
log.addHandler(logfile)

def test(main):
    log.info("starting tests")
    try:
        main()
    except:
        log.critical(traceback.format_exc())
