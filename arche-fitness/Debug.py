##   Copyright 2013 Matthew A. Robinson
##
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##       http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.

import traceback
import logging
from logging import *
import sys

exec(open("config/debug.cfg").read())

log = logging.getLogger("R") # "R" stands for 'root'
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(levelSystemConsole)

logfile = logging.FileHandler("error.log")
logfile.setLevel(levelLogFile)

formatter = logging.Formatter(
    "%(lineno)4d | %(asctime)s | %(levelname)8s | %(name)s |: %(message)s")

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
