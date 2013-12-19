
import glob
g = glob.glob("scripts/*.py")
scripts = []
for file in g:
    scripts.append(file[8:-3])
print(scripts)
