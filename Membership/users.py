import json
from random import randint

class membership():
    def __init__(self) -> None:
        self.status = True
        self.users = self.getdata()

#************************************************************************************************************************************************

    def program(self):
        self.menu()
        entry = self.selection()

        if entry == 1:
            self.login()
        if entry == 2:
            self.signin()
        if entry == 3:
            self.forgetpassword()
        if entry == 4:
            self.exit()

#************************************************************************************************************************************************

    def menu(self):
        print("\n1-giriş yap\n2-kayıt ol\n3-şifremi unuttum\n4-çıkış\n")
        
#************************************************************************************************************************************************

    def selection(self):
        while True:
            try:
                selection = int(input("seçimin : "))
                while selection > 4 or selection < 1:
                    print("lütfen 1-4 arası değer gir!")
                    selection = int(input("seçimin : "))
                break
            except:
                print("lütfen sayı gir!")

        return selection

#************************************************************************************************************************************************

    def getdata(self):
        try:
            with open("users.json","r") as file:
                users = json.load(file)
        except FileNotFoundError:
            with open("users.json","w") as file:
                file.write("{}")
            
            with open("users.json","r") as file:
                users = json.load(file)
        
        return users

#************************************************************************************************************************************************

    def login(self):
        print("\n*** giriş ekranı ***")

        username = input("kullanıcı adı gir : ")
        userpassword = input("şifre gir : ")

        
        status = self.checkit(username,userpassword)

        if status:
            self.loginsuccessful()
        else:
            self.loginfailed("bilgiler yanlış!")

#************************************************************************************************************************************************

    def signin(self):
        print("\n*** kayıt ekranı ***")

        username = input("kullanıcı adı gir : ")
        while True:
            userpassword = input("şifre gir : ")
            repeatuserpassword = input("şifreyi tekrar gir : ")
            
            if userpassword == repeatuserpassword:
                break
            else:
                print("şifreler eşleşmiyor tekrar gir!")

        usermail = input("e-posta adresini gir : ")

        status = self.isitregistered(username,usermail)

        if status:
            print("bu kullanıcı adı veya e-posta sistemde kayıtlıdır")
        else:
            activationcode = self.sendactivationcode()
        
        activationstatus = self.activationcheck(activationcode)

        if activationstatus:
            self.save(username,userpassword,usermail)
        else:
            print("aktivasyon geçersiz!")

#************************************************************************************************************************************************

    def forgetpassword(self):
        print("\n*** şifremi unuttum ekranı ***")
        mail = input("e-posta adresini gir : ")

        if self.havemail(mail):
            with open("activation.txt","w") as file:
                activation = str(randint(1000,9999))
                file.write(activation)

            activationcode = input("şifrenizi değiştirmek için gönderdiğimiz aktivasyon kodunu gir : ")

            if activationcode == activation:
                while True:
                    newpassword = input("yeni şifreni gir : ")
                    repeatnewpassword = input("yeni şifreni tekrar gir : ")

                    if newpassword == repeatnewpassword:
                        break
                    else:
                        print("girdiğiniz şifreler uyuşmuyor tekrar deneyin")

            self.users = self.getdata()

            for user in self.users["users"]:
                if user["usermail"] == mail:
                    user["userpassword"] = str(newpassword)
            with open("users.json","w") as file:
                json.dump(self.users,file)
                print("şifre başarıyla değiştirildi")
        else:
            print("böyle bir mail sistemde kayıtlı değil")
     
#************************************************************************************************************************************************

    def exit(self):
        print("program durduruldu")
        self.status = False
        
#************************************************************************************************************************************************

    def checkit(self,username,userpassword):
        self.users = self.getdata()
        
        for user in self.users["users"]:
            if user["username"] == username and user["userpassword"] == userpassword and user["timeout"] == "0" and user["activation"] == "Y":
                return True
            else:
                return False

#************************************************************************************************************************************************

    def loginsuccessful(self):
        print("hoş geldiniz!")
        self.status = False

#************************************************************************************************************************************************

    def loginfailed(self,reason):
        print(reason)

#************************************************************************************************************************************************

    def isitregistered(self,username,usermail):
        self.users = self.getdata()

        try:
            for user in self.users["users"]:
                if user["username"] == username and user["usermail"] == usermail:
                    return True
        except KeyError:
            return False

        return False 

#************************************************************************************************************************************************

    def sendactivationcode(self):
        with open("activation.txt","w") as file:
            activation = str(randint(1000,9999))
            file.write(activation)
        return activation

#************************************************************************************************************************************************

    def activationcheck(self,activationcode):
        getactivationcode = input("aktivasyon kodunuzu girin : ")

        if getactivationcode == activationcode:
            return True
        else:
            False

#************************************************************************************************************************************************

    def save(self,username,userpassword,usermail):
        self.users = self.getdata()

        try:
            self.users["users"].append({"username" : username,"userpassword" : userpassword,"usermail" : usermail,"activation" : "Y","timeout" : "0"})
        except KeyError:
            self.users["users"] = []
            self.users["users"].append({"username" : username,"userpassword" : userpassword,"usermail" : usermail,"activation" : "Y","timeout" : "0"})

        with open("users.json","w") as file:
            json.dump(self.users,file)
            print("kayıt başarıyla oluşturuldu")

#************************************************************************************************************************************************

    def havemail(self,usermail):
        self.users = self.getdata()

        for user in self.users["users"]:
            if user["usermail"] == usermail:
                return True
        return False

#************************************************************************************************************************************************

newregister = membership()

while newregister.status:
    newregister.program()