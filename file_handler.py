import fileinput

def fixTypos(filePath, typo, typoFix):
    with open(filePath, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace(typo, typoFix)
    with open(filePath, 'w') as file:
        file.write(filedata)