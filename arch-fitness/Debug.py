
import traceback
import logging

def test(main):
    logging.basicConfig(filename = "Engine.log", level = logging.DEBUG,
format = "%(asctime)s | %(levelname)8s |:  %(message)s")
    logging.info("starting tests")
    try:
        main()
    except:
        logging.critical(traceback.format_exc())
