try:
    import _winreg as reg
except:
    import winreg as reg

class SoftwareInfo:
    '''
    className:SoftwareInfo
    Description:Return the Installed Software name with version and publisher name 
    '''
    def getVal(self,name,asubkey):
        try:
            return reg.QueryValueEx(asubkey, name)[0]
        except:
            return "undefined"
    def getCheck(self,all_softwares,version,publisher):
        val=0
        for i in all_softwares:
            if(i['version']==version) and (i['publisher']==publisher):
                val=1
        return val
                
    def getReg_keys(self,flag):
        Hkeys=reg.HKEY_LOCAL_MACHINE
        path=r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
        Regkey = reg.ConnectRegistry(None, Hkeys)
        key = reg.OpenKey(Regkey, path,0, reg.KEY_READ | flag)
        key_count = reg.QueryInfoKey(key)[0]
        all_softwares=[]
        for i in range(key_count):
            singsoft={}
            try:
                keyname=reg.EnumKey(key, i)
                asubkey = reg.OpenKey(key, keyname)
                data=["DisplayName","DisplayVersion","Publisher"]
                name=self.getVal(data[0],asubkey)
                version=self.getVal(data[1],asubkey)
                publisher=self.getVal(data[2],asubkey)
                if(name!='undefined' and version!="undefined" and publisher!="undefined"):
                    val=self.getCheck(all_softwares,version,publisher)
                    if val!=1:
                        singsoft['name']=name
                        singsoft['version']=version
                        singsoft['publisher']=publisher
                        all_softwares.append(singsoft)
            except Exception as ex:
                continue
        return all_softwares
    
    def getSoftwareList(self):
        '''
        Get All installed Softwae in th list format with name,version,publisher
        '''
        try:
           return  self.getReg_keys(reg.KEY_WOW64_32KEY)+self.getReg_keys(reg.KEY_WOW64_64KEY)
        except Exception as ex:
            return ex
        
    def GetInstalledBrowsers(self):
        path='SOFTWARE\Clients\StartMenuInternet'
        Hkeys=reg.HKEY_LOCAL_MACHINE
        Regkey = reg.ConnectRegistry(None, Hkeys)
        key = reg.OpenKey(Regkey, path,0, reg.KEY_READ | reg.KEY_WOW64_32KEY)
        key_count = reg.QueryInfoKey(key)[0]
        browser_list=[]
        for i in range(key_count):
            singsoft={}
            try:
                keyname=reg.EnumKey(key, i)
                browser_list.append(keyname)
            except Exception as ex:
                continue
        return browser_list

