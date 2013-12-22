
import glob
g = glob.glob("script/*.py")
scripts = []
for file in g:
    scripts.append(file[7:-3])
print(scripts)
