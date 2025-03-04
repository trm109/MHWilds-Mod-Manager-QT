import zipfile
import os


class ModManager:
    def __init__(self, gameDir, modsDir):
        self.gameDir = gameDir  # Path to the game directory
        self.modsDir = modsDir  # Path to the mods directory
        self.config = os.path.expanduser(modsDir + "/config.json")
        self.mods = []
        # get all the mods
        self.getMods()
        # Debug
        print("ModManager initialized:")
        print("\tGame Directory: " + self.gameDir)
        print("\tMods Directory: " + self.modsDir)
        print("\tConfig File: " + self.config)
        print("\tMods:")
        for mod in self.mods:
            print("\t\t" + mod.modName)
            print("\t\t\tVersion: " + mod.version)
            print("\t\t\tAuthor: " + mod.author)
            print("\t\t\tDescription: " + mod.description)
            print("\t\t\tMod Type: " + mod.modType)
        return

    def getMods(self):  # -> None
        # Get all the mod archives in the MHWildsMods folder
        mods = []

        # Get all the mod archives in the MHWildsMods folder
        for file in os.listdir(os.path.expanduser("~/Documents/MHWildsMods")):
            if file.endswith(".zip"):  # Only support zip files for now
                # Instantiate a Mod object for each mod
                mods.append(Mod(self, file))

        # Set the mods list
        self.mods = mods
        return


class Mod:
    def __init__(self, parent, archivePath):
        self.parent = parent
        self.archivePath = archivePath
        self.modName = ""
        self.files = []
        self.folders = []
        self.version = ""  # version of the mod
        self.author = ""  # author of the mod
        self.description = ""  # description of the mod
        self.modType = ""  # packaged or unpackaged mod
        # set the mod info
        self.setModInfo()
        # unpack the mod archive based on modType
        self.importMod()
        # check if the mod is enabled
        self.enabled = self.isInstalled()

    def setModInfo(self):  # -> None
        # TODO
        # set self.files
        self.setFiles()
        # set self.modType
        self.setModType()
        # Parse modDir/self.modName/modinfo.ini
        self.parseModInfo()

        return

    def parseModInfo(self):  # -> None
        # TODO
        zip = zipfile.ZipFile(
            os.path.expanduser(self.parent.modsDir + "/" + self.archivePath), "r"
        )
        # check if the mod has a modinfo.ini file
        if not any([file.endswith("modinfo.ini") for file in self.files]):
            self.modName = self.archivePath.split(".")[0]
            self.version = "n/a"
            self.author = "n/a"
            self.description = "n/a"
            return
        # Parse the modinfo.ini file
        for file in self.files:
            if file.endswith("modinfo.ini"):
                with zip.open(file) as f:
                    for line in f:
                        line = line.decode("utf-8").strip()
                        if line.startswith("name="):
                            self.modName = line.split("=")[1]
                        elif line.startswith("version="):
                            self.version = line.split("=")[1]
                        elif line.startswith("author="):
                            self.author = line.split("=")[1]
                        elif line.startswith("description="):
                            self.description = line.split("=")[1]
                return

    def importMod(self):  # -> None
        # TODO
        zip = zipfile.ZipFile(
            os.path.expanduser(self.parent.modsDir + "/" + self.archivePath), "r"
        )
        # Unzip/Untar/Unrar's the folder based on the mod type
        match self.modType:
            case "packaged":
                # Extract the archive to modDir/self.modName, minus the top level archive folder
                # for example; the archive path DynamicCamera/* -> modDir/self.modName/*
                toplevelFolder = [
                    file for file in zip.namelist() if file.count("/") >= 1
                ][0].split("/")[0]
                zip.extractall(os.path.expanduser(self.parent.modsDir + "/imported"))
                # move the folder to modDir/self.modName
                os.rename(
                    os.path.expanduser(
                        self.parent.modsDir + "/imported/" + toplevelFolder
                    ),
                    os.path.expanduser(
                        self.parent.modsDir + "/imported/" + self.modName
                    ),
                )
                return
            case "top-level-packaged":
                # Easy, just extract files to modDir/self.modName
                # for example; the archive path DynamicCamera -> modDir/self.modName
                zip.extractall(
                    os.path.expanduser(
                        self.parent.modsDir + "/imported/" + self.modName
                    )
                )
                return
            case "raw_dll":
                # Extract files to modDir/self.modName
                zip.extractall(
                    os.path.expanduser(
                        self.parent.modsDir + "/imported/" + self.modName
                    )
                )
                # TODO generate a modinfo.ini file
                return
            case "native":
                # Extract files to modDir/self.modName
                zip.extractall(
                    os.path.expanduser(
                        self.parent.modsDir + "/imported/" + self.modName
                    )
                )
                # TODO generate a modinfo.ini file
                return
            case "unknown":
                # Extract files to modDir/self.modName
                zip.extractall(
                    os.path.expanduser(
                        self.parent.modsDir + "/imported/" + self.modName
                    )
                )
                # generate a modinfo.ini file
                return
            case _:
                raise ValueError("Invalid mod type")
        return

    def setModType(self):  # -> None
        # Types are: packaged, top-level-packaged, raw_dll, native, and unknown
        if self.files == []:
            self.modType = "null"
            return

        # check if the mod has a modinfo.ini file
        if any([file.endswith("modinfo.ini") for file in self.files]):
            # Check if the `modinfo.ini` file is at the top level
            if [file for file in self.files if file.endswith("modinfo.ini")][0].count(
                "/"
            ) == 0:
                self.modType = "top-level-packaged"
                return
            else:
                self.modType = "packaged"
                return

        # check for top-level `reframework` folder
        if "reframework/" in self.folders:
            self.modType = "native"
            return

        # check for dll files that are at top level
        # exists(file) where file.endswith(".dll") and file.count("/") == 0
        for file in (file for file in self.files if file.endswith(".dll")):
            if file.count("/") == 0:
                self.modType = "raw_dll"
                return

        self.modType = "unknown"
        return

    def determineSpecialCase(self):  # -> None
        # For specific mods. Hard-coded support
        # REFramework
        # CatLib
        # MHWilds Overlay
        # reframework d2d
        if len(self.files) == 1 and self.files[0] == "reframework-d2d.dll":
            # this is a older version of the reframework-d2d mod, warn user.
            # TODO
            return (
                "ERROR:"
                + "\n"
                + "This is an older version of the REFramework D2D mod. Please download the official version from: https://www.nexusmods.com/monsterhunterrise/mods/134?tab=files"
                + "\n\n"
                + "This older version is NOT supported by MHWilds-Mod-Manager-QT and will not install correctly"
            )
        return

    # Get all the VALID files in an archive. Ignore things like Cover.png, and fix bad paths like _CatLib/reframework
    def setFiles(self):  # -> files
        # TODO
        zip = zipfile.ZipFile(
            os.path.expanduser(self.parent.modsDir + "/" + self.archivePath), "r"
        )
        # filter out files ending in /
        files = [file for file in zip.namelist() if not file.endswith("/")]
        folders = [file for file in zip.namelist() if file.endswith("/")]

        if files == []:
            raise ValueError("No files found in the archive")

        # print("Files:")
        # for file in files:
        #    print("\t" + file)
        # print("Folders:")
        # for folder in folders:
        #    print("\t" + folder)
        # raise ValueError("DEBUG")

        self.files = files
        self.folders = folders
        return

    # Determine if the mod is already installed
    def isInstalled(self):
        print("Checking if mod is installed: " + self.modName)
        # Note:
        # We are assuming that the mod is installed if ALL the files are present
        # If ANY of the files are missing, we will treat the mod as not installed
        # previous, non-symlinked files will be treated as not installed
        for file in self.files:
            if os.path.exists(os.path.expanduser(self.parent.gameDir + "/" + file)):
                # check if its a symlink
                if os.path.islink(os.path.expanduser(self.parent.gameDir + "/" + file)):
                    # treat as installed
                    continue
                else:
                    # treat as not installed, but will replace original file (handled by install())
                    print(
                        "File exists but is not a symlink: "
                        + self.parent.gameDir
                        + "/"
                        + file
                    )
                    print("Therefor, the mod is not installed")
                    return False
            else:
                # treat as not installed
                print("File does not exist: " + self.parent.gameDir + "/" + file)
                print("Therefor, the mod is not installed")
                return False
        print("All files are present, mod is installed")
        return True

    def install(self):
        # TODO ignore certain file types, like `modinfo.ini`, `*.png`
        print("Installing mod: " + self.modName)

        for folder in self.folders:
            if self.modType == "packaged":
                # trim the first folder
                folder = folder.split("/", 1)[1]
                print("Trimmed folder: " + folder)
            # For packaged mods, the top level folder is the mod name, but this is corrected in setModType()
            folderPath = os.path.expanduser(self.parent.gameDir + "/" + folder)
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)
            print("Created folder: " + folderPath)

        for file in self.files:
            if self.modType == "packaged":
                file = file.split("/", 1)[1]
                print("Trimmed file: " + file)
            symlinkFrom = os.path.expanduser(
                self.parent.modsDir + "/imported/" + self.modName + "/" + file
            )
            if os.path.isdir(symlinkFrom):
                # TODO handle this better
                print("ERROR: File is a directory, not a file: " + symlinkFrom)
                continue

            symlinkTo = os.path.expanduser(self.parent.gameDir + "/" + file)
            # Check if file already exists
            if os.path.exists(symlinkTo):
                # check if its a directory
                if os.path.isdir(symlinkTo):
                    # remove the directory
                    print("ERROR: File is a directory, not a file: " + symlinkTo)
                    raise ValueError("File is a directory, not a file: " + symlinkTo)
                # already exists, check if its a symlink
                if os.path.islink(symlinkTo):
                    # remove the symlink
                    os.unlink(symlinkTo)
                    print("Removed existing symlink: " + symlinkTo)
                else:
                    # move the file to a backup location
                    os.rename(symlinkTo, symlinkTo + ".bak")
                    print("Moved existing file to: " + symlinkTo + ".bak")
            ## Checkif file is a symlink (then we know its two mods colliding)
            os.symlink(symlinkFrom, symlinkTo)
            print("Created symlink: " + symlinkFrom + " -> " + symlinkTo)
        print("Finished installing mod: " + self.modName)
        return

    def uninstall(self):
        # TODO Handle .bak files
        print("Uninstalling mod: " + self.modName)
        # Does not touch folders, only symlinked files
        for file in self.files:
            if self.modType == "packaged":
                file = file.split("/", 1)[1]
            symlinkTo = os.path.expanduser(self.parent.gameDir + "/" + file)
            if os.path.islink(symlinkTo):
                os.unlink(symlinkTo)
                # Check for .bak files
                if os.path.exists(symlinkTo + ".bak"):
                    os.rename(symlinkTo + ".bak", symlinkTo)
                    print("Restored backup file: " + symlinkTo)
                print("Removed symlink: " + symlinkTo)
            else:
                print("File is not a symlink: " + symlinkTo)
        print("Finished uninstalling mod: " + self.modName)
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
