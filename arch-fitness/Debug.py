
import traceback

def test(main):
    try:
        main()
    except:
        print (traceback.format_exc())
        input ()
