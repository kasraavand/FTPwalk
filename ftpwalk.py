import os


class ftp_walker(object):
    def __init__(self, connection, root):
        self.connection = connection
        self.root = root

    def listdir(self, _path):
        file_list, dirs, nondirs = [], [], []
        try:
            self.connection.cwd(_path)
        except Exception as exp:
            print("the current path is : ", self.connection.pwd(), exp.__str__(), _path)
            return [], []
        else:
            self.connection.retrlines('LIST', lambda x: file_list.append(x.split()))
            for info in file_list:
                ls_type, name = info[0], info[-1]
                if ls_type.startswith('d'):
                    dirs.append(name)
                else:
                    nondirs.append(name)
            return dirs, nondirs

    def Walk(self, top, path=''):
        dirs, nondirs = self.listdir(top)
        yield (path or top), dirs, nondirs
        path = top
        for name in dirs:
            path = os.path.join(path, name)
            for x in self.Walk(name, path):
                yield x
            self.connection.cwd('..')
            path = os.path.dirname(path)
