import os

# TEST UPDATE
def chType(obj):
    """
        Aggressive  checking !
    """
    if os.path.isfile(obj):
        return True
    elif os.path.isdir(obj):
        return False
    else:
        try:
            try:
                File = open(obj)
                File.close()
                return True

            except PermissionError and OSError:
                return False
        except FileNotFoundError:
            return False


class MFolders(object):

    def __init__(self):
        xRun = os.popen("echo %username%").read().split("\n")
        self.Name = xRun[0]
        self.lisOfFiles = []
        self.li = []
        self.TREE = []
        self.SMapping_f = 0
        self.SMapping_d = 0
        self.SSyncs = None

    def __GetFolder(self, Folder):
        self.li = []
        self.lisOfFiles = []
        for folder in os.walk(Folder):
            self.li = []
            self.SMapping_d += 1
            for _file in os.listdir(folder[0]):
                self.SMapping_f += 1
                fPath = fr"{folder[0]}\{_file}"
                self.li.append({"name": _file,
                                "size": os.path.getsize(fPath),
                                "time_ch": os.path.getctime(fPath),
                                "time_cr": os.path.getmtime(fPath),
                                "type": chType(fPath),
                                "sub": fPath[fPath.rfind(os.path.basename(Folder))+len(os.path.basename(Folder))+1:]})

            self.lisOfFiles.append({"folder": folder[0], "files": self.li})

        return self.lisOfFiles

    def GetFolders(self, *folders):
        """
            Folders { tuple, list }
        """

        self.TREE = []
        for folder in folders:
            self.TREE.append(MFolders.__GetFolder(self, folder))

        return self.TREE


class SyncFolders(MFolders):

    def __init__(self, obj=None):
        MFolders.__init__(self)
        self.liFilesMain = []
        self.slash = "\\"
        self.OBJ = obj

    def Sync(self, folder, RSL=True):
        """
            RSL => Index OF -R_oot- folder in List Of parameter `folder`;
                   Index OF -S_ub Folder- [..];
                   Index OF -(for) L_oop- [..]
        """
        if RSL:
            indexR = 0
            indexS = 1
            indexL = 1

        else:
            indexR = 1
            indexS = 0
            indexL = 0

        Root = folder[indexR]
        FolderTS = folder[indexS][0]['folder']
        for __ in folder[indexL]:

            for _ in Root:

                for create in _['files']:

                    c_s = create['sub']
                    Path = rf"{FolderTS}\{c_s}"
                    if not create['type']:
                        if not os.path.exists(Path):
                            os.mkdir(Path)

                    else:
                        if os.path.exists(Path) and create['type']:
                            if not create['size'] == os.path.getsize(Path):
                                os.system(rf"del {Path}")

                        if not os.path.exists(Path):
                            os.system(f"copy \"{_['folder']}\\{create['name']}\""
                                      f" \"{FolderTS}\\{c_s[:c_s.rfind(self.slash) + 1]}\"")
            break  # important


if __name__ == "__main__":
    s = SyncFolders()
    s.Sync(s.GetFolders(fr"c:\Users\{s.Name}\Desktop\OK",
                        fr"c:\Users\{s.Name}\Desktop\Main"), RSL=True)

