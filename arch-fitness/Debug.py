
import traceback
import logging
import sys

def test(main, level=logging.INFO):
    logging.basicConfig(stream = sys.stderr, filename = "Debug.log",
                    level = level,
format = "%(asctime)s | %(levelname)8s |:  %(message)s")
    logging.info("starting tests")
    try:
        main()
    except:
        logging.critical(traceback.format_exc())
