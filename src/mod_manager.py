import zipfile
import os


class ModManager:
    def __init__(self, gameDir, modsDir):
        self.gameDir = gameDir  # Path to the game directory
        self.modsDir = modsDir  # Path to the mods directory
        self.config = self.modsDir + "/config.json"
        self.mods = []
        self.getMods()

    def getMods(self):  # -> None
        # TODO
        # Get all the mods in the mods folder
        mods = []
        for file in os.listdir(os.path.expanduser("~/Documents/MHWildsMods")):
            if file.endswith(".zip"):  # Only support zip files for now
                mods.append(Mod(self.gameDir, file))
        for mod in mods:
            print(mod.filename)  # Debug
        self.mods = mods
        return


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

    def parseModInfo(self):  # -> None
        # TODO
        self.files = self.getFiles()
        # Check if the mod has a `modinfo.ini` file
        modType = self.determineModType()
        print(modType)
        match modType:
            case "packaged":
                # reference the modinfo.ini file
                return
            case "top-level-packaged":
                # reference the modinfo.ini file
                return
            case "raw_dll":
                # use the filename as the mod name
                return
            case "native":
                # use the filename as the mod name
                return
            case "unknown":
                # use the filename as the mod name
                return
            case _:
                # error
                raise ValueError("Invalid mod type")

        return

    def determineModType(self):  # -> str
        # TODO
        if self.files == []:
            print("No files found, is this an empty mod?")
            return "null"
        # Types are: packaged, top-level-packaged, raw_dll, native, and unknown
        print("parsing files:")
        # for file in self.files:
        # print(file) # Debug

        # check if the mod has a modinfo.ini file
        if any([file.endswith("modinfo.ini") for file in self.files]):
            print("Found modinfo.ini file")
            # Check if the `modinfo.ini` file is at the top level
            if [file for file in self.files if file.endswith("modinfo.ini")][0].count(
                "/"
            ) == 0:
                print("Top-level modinfo.ini file: top-level-packaged")
                return "top-level-packaged"
            print("No top-level modinfo.ini file: packaged")
            return "packaged"

        # check for dll files that are at top level
        for file in (file for file in self.files if file.endswith(".dll")):
            print("Found DLL file")
            if file.count("/") == 0:
                print("Top-level DLL file: raw_dll")
                return "raw_dll"

        # check for top-level `reframework` folder
        if any([file.startswith("reframework") for file in self.files]):
            print("Found top-level reframework folder: native")
            return "native"

        print("Unknown mod type")
        return "unknown"

    def determineSpecialCase(files):  # -> str
        # For specific mods. Hard-coded support
        # REFramework
        # CatLib
        # MHWilds Overlay
        # reframework d2d
        return ""

    # Get all the VALID files in an archive. Ignore things like Cover.png, and fix bad paths like _CatLib/reframework
    def getFiles(self):  # -> files
        # TODO
        zip = zipfile.ZipFile(
            os.path.expanduser("~/Documents/MHWildsMods/" + self.path), "r"
        )
        # filter out files ending in /
        files = [file for file in zip.namelist() if not file.endswith("/")]
        folders = [file for file in zip.namelist() if file.endswith("/")]
        # print(files)
        # for file in zip.namelist():
        #    if file.endswith(".esp") or file.endswith(".esm") or file.endswith(".bsa") or file.endswith(".dll") or file.endswith(".ini"):
        #        files.append(File(self.path, file))
        print(files)
        print(folders)
        return files

    # Determine if the mod is already installed
    def isInstalled(self, gameDir):
        # for file in self.files:
        # Check if file is symlinked
        print("Mod.isInstalled() called")
        return True

    def install(self, gameDir):
        match self.modType:
            case "packaged":
                # Enter the top level folder (which is typically the name of the mod) and extract files to gameDir/
                return
            case "top-level-packaged":
                # Easy, just extract files to gameDir/
                return
            case "raw_dll":
                # Extract files to gameDir/
                return
            case "native":
                # Extract files to gameDir/
                return
            case "unknown":
                # Extract files to gameDir/
                return
            case _:
                raise ValueError("Invalid mod type")

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
