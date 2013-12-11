#!/usr/bin/env python3

age = 0

def initialProcedure():
    global age
    
    print ("Explain the pushup and good-form " + \
           "pushups and explain the purpose of the pushup")
    
    input()
    
    print ("""Note: please consult a doctor about any medical conditions
before you begin the program.  I am not responsible for any injuries
relating to the program neither are any of the constituent creators
or modifiers of this program responsible for any injuries relating to
the program here-in provided that those who modified this program
and/or redistributed it have included this explicit message without
modification.  By pressing 'continue', you verify that you agree
to these terms; you also verify that you have consulted with a
health practitioner about your health and/or have confirmed
you are physically fit for strenuous exercise.""")
    
    input("Continue...")
    
    print("""To taylor this program more specifically to you and your
relating health, it is required that you provide your age.  You
are *not* required to provide your age to continue with the program, but
we will assume you are under 40 years of age.  Please enter your age
below, if you do not wish to provide it, just press 'skip this step'.""")
    
    age = input("Enter your age (leave blank to 'skip'): ")
    if not age:
        age = 20
    else:
        age = int(age)

    input("End initial procedure...")

def pushupsTest(continuous=True):
    # Ask the user to perform as many pushups as they can in a row,
    # then return the number they have reported.
    pushups = 0
    if continuous:
        print ("""When you are ready to begin, perform a good form pushup
in a way you can press the button on a single rep; the test will begin
on the first press of the mouse button, or any button on the keyboard (excluding 'enter'/'return').
When you cannot perform any more or you break proper form,
press the 'finish' button, or press the enter key on your keyboard.""")
        data = ""
        while data != "finish":
            data = input()
            if data != "finish":
                pushups += 1
                print(pushups)
            else:
                break
    else:
        print ("""When you are ready to begin, start performing pushups.
Continue until you either experience unsafe amounts of pain, wear out
from exhaustion, or are forced to break proper form.""")
        input("'press' I'm done!")
        pushups = int(input("How many pushups did you perform? :: "))

    return pushups

def initialTest():
    print("This test will outline your basic health.")
    print("Perform as many good-form pushups as you can.")

    print("""You can choose to record continuously, where you will
press a button for every pushup you complete, and they will be recorded
in real-time for you, or you can chooose to record manually, where you
complete the number required for the set/test and report your numbers
following.""")
    print("Would you like to use 'continuous' or 'manual' recording?")

    continuous = (input(" :: ") == "continuous")

    input("This can be changed any time in 'settings'")

    score = pushupsTest(continuous)
    rank = 0

    if age < 40:
        if score in range(0, 6):
            rank = 1
        elif score in range(6, 15):
            rank = 2
        elif score in range(15, 30):
            rank = 3
        elif score in range(30, 50):
            rank = 4
        elif score in range(50, 100):
            rank = 5
        elif score in range(100, 150):
            rank = 6
        elif score >= 150:
            rank = 7
        else:
            rank = 8
    elif age in range(40, 56):
        if score in range(0, 6):
            rank = 1
        elif score in range(6, 13):
            rank = 2
        elif score in range(13, 25):
            rank = 3
        elif score in range(25, 45):
            rank = 4
        elif score in range(45, 75):
            rank = 5
        elif score in range(75, 125):
            rank = 6
        elif score >= 125:
            rank = 7
        else:
            rank = 8
    elif age >= 56:
        if score in range(0, 6):
            rank = 1
        elif score in range(6, 11):
            rank = 2
        elif score in range(11, 20):
            rank = 3
        elif score in range(20, 35):
            rank = 4
        elif score in range(35, 65):
            rank = 5
        elif score in range(65, 100):
            rank = 6
        elif score >= 100:
            rank = 7
        else:
            rank = 8

    print ("You were ranked to RANK ", rank)
    input ()
    
    
initialProcedure()
initialTest()
