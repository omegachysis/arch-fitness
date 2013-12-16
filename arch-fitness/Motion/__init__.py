
from . import In
from . import Action

def looped(action, times):
    action.loop = times
    return action
