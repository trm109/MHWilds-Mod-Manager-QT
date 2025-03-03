import zipfile
import os


class ModManager:
    def __init__(self, gameDir, modsDir):
        self.gameDir = gameDir  # Path to the game directory
        self.modsDir = modsDir  # Path to the mods directory
        self.config = self.modsDir + "/config.json"
        self.mods = self.getMods()

    def getMods(self):  # -> List[Mod]
        # TODO
        # Get all the mods in the mods folder
        mods = []
        for file in os.listdir(os.path.expanduser("~/Documents/MHWildsMods")):
            if file.endswith(".zip"):  # Only support zip files for now
                mods.append(Mod(self.gameDir, file))
        return mods


class Mod:
    def __init__(self, gameDir, path):
        self.path = path
        self.filename = path.split("/")[-1]
        self.modName = (
            ""  # name of the mod, will be overwritten if the mod has a `modinfo.ini`
        )
        self.extension = self.filename.split(".")[-1]  # extension of the mod
        self.files = []
        self.version = ""  # version of the mod
        self.author = ""  # author of the mod
        self.description = ""  # description of the mod
        self.modType = ""  # packaged or unpackaged mod
        self.parseModInfo()
        self.enabled = self.isInstalled(gameDir)

    def parseModInfo(self):
        # TODO
        files = self.getFiles()
        # Check if the mod has a `modinfo.ini` file
        if any([file.endswith("modinfo.ini") for file in files]):
            # This is a packaged mod
            prefix = ""
            # for the */modinfo.ini file, get its folder name
            for file in files:
                if file.endswith("modinfo.ini"):
                    prefix = file.split("/")[0]
                    break

            if prefix == "":
                # This is a bad mod, handle
                print("Bad mod: " + self.filename)
                return
            # Parse the `modinfo.ini` file to get the version, author, and description
            # TODO grab the contents of modinfo.ini and populate self.version, self.author, and self.description

            pass
        # If it does, parse the file to get the version, author, and description
        # If it doesn't, set the version, author, and description to empty strings
        return

    # Get all the VALID files in an archive. Ignore things like Cover.png, and fix bad paths like _CatLib/reframework
    def getFiles(self):  # -> List[File]
        # TODO
        zip = zipfile.ZipFile(
            os.path.expanduser("~/Documents/MHWildsMods/" + self.path), "r"
        )
        # filter out files ending in /
        # files = [ file for file in zip.namelist() if not file.endswith("/")]
        # print(files)
        # for file in zip.namelist():
        #    if file.endswith(".esp") or file.endswith(".esm") or file.endswith(".bsa") or file.endswith(".dll") or file.endswith(".ini"):
        #        files.append(File(self.path, file))
        return files

    # Determine if the mod is already installed
    def isInstalled(self, gameDir):
        for file in self.files:
            if not file.isInstalled(gameDir):
                return False
        return True

    def install(self, gameDir):
        for file in self.files:
            file.install(gameDir)
        return

    def uninstall(self, gameDir):
        for file in self.files:
            file.uninstall(gameDir)
        return


## Function to get a list of mods in the Documents/MHWildsMods folder
## Mods are downloaded from Nexus Mods and placed in this folder
## Only supports zip files for now.
# def getMods():
#    mods = []
#    for file in os.listdir(os.path.expanduser('~/Documents/MHWildsMods')):
#        if file.endswith(".zip"):
#            mods.append(file)
#    print(mods) # Debug
#    return mods
#
## Takes in a list of mods and updates the mod list in the GUI
# def updateModList(parent):
#    mods = getMods()
#
#    parent.modList.clear()
#
#    for mod in mods:
#        modItem = QListWidgetItem()
#        modWidget = ModWidget(mod)
#
#        modItem.setSizeHint(modWidget.sizeHint())
#
#        parent.modList.addItem(modItem)
#        parent.modList.setItemWidget(modItem, modWidget)
#
#    return
## Updates the mod list
## For each mod in the mod list, determines if it has been toggled on or off based on its archive files
# def refresh(parent):
#    updateModList(parent)
#    return
#
# def isModInstalled(filename):
#    # TODO
#    return
#
# def installMod(filename, modDir, gameDir):
#    #if isModInstalled(filename):
#    #    # Mod is already installed, handle
#    #    return
#    zip = zipfile.ZipFile(os.path.expanduser('~/Documents/MHWildsMods/' + filename), 'r')
#    # Print all files in the zip
#    for file in zip.namelist():
#        print(file)
#
#    # Extract the zip to path
#    # TODO
#    return
#
# def uninstallMod(filename, modDir, gameDir):
#    #if not isModInstalled(filename):
#    #    # Mod is not installed, handle
#    #    return
#
#    # TODO
#    return
