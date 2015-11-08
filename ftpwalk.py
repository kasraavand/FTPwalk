import ftplib
from os import path

class ftp_walker(object):
    def __init__(self):
        self.connection = ftplib.FTP('ftp.xenbase.org')
        self.connection.login()

    def listdir(self,path):
        file_list, dirs, nondirs = [],[],[]
        try:
            self.connection.cwd(path)
        except:
            return [],[]

        self.connection.retrlines('LIST',lambda x:file_list.append(x.split()))
        for info in file_list:
            ls_type,name = info[0],info[-1]
            if ls_type.startswith('d'):
                dirs.append(name)
            else:
                nondirs.append(name)
        return dirs,nondirs

    def Walk(self,top):
        dirs, nondirs = self.listdir(top)
        yield top, dirs, nondirs
        for name in dirs:
            new_path = path.join(top, name)
            for x in self.Walk(new_path):
                yield x
            yield top, dirs, nondirs

if __name__=='__main__':
    FT=ftp_walker()
    for root,dirs,files in FT.Walk('/'):
          print(root,dirs,files)
    
