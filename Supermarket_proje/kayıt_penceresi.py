
from PyQt6 import  QtWidgets

import sqlite3


class KayıtPenceresi(QtWidgets.QWidget):
    def __init__(self,baglanti):
        super().__init__()
        self.baglanti=baglanti
        self.cursor=self.baglanti.cursor()
        self.init_ui()


    def init_ui(self):

        self.ad_label=QtWidgets.QLabel("Adınız:",self)
        self.ad=QtWidgets.QLineEdit(self)

        self.soyad_label=QtWidgets.QLabel("Soyadınız:",self)
        self.soyad=QtWidgets.QLineEdit(self)

        self.email_label=QtWidgets.QLabel("Email:",self)
        self.email=QtWidgets.QLineEdit(self)

        self.kullanici_adi_label=QtWidgets.QLabel("Kullanıcı Adınız:",self)
        self.kullanici_adi=QtWidgets.QLineEdit(self)

        self.parola_label=QtWidgets.QLabel("Şifreniz:",self)
        self.parola=QtWidgets.QLineEdit(self)
        self.parola.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.kayit_buton=QtWidgets.QPushButton("Kaydet",self)

        self.kayit_buton.clicked.connect(self.kaydet)



        layout=QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.ad_label)
        layout.addWidget(self.ad)

        layout.addWidget(self.soyad_label)
        layout.addWidget(self.soyad)

        layout.addWidget(self.email_label)
        layout.addWidget(self.email)

        layout.addWidget(self.kullanici_adi_label)
        layout.addWidget(self.kullanici_adi)

        layout.addWidget(self.parola_label)
        layout.addWidget(self.parola)

        layout.addWidget(self.kayit_buton)

        self.setWindowTitle("Kullanıcı Bilgileri")
        self.resize(400,200)


    def kaydet(self):
        ad=self.ad.text()
        soyad=self.ad.text()
        email=self.email.text()
        kullanici_adi=self.kullanici_adi.text()
        parola=self.parola.text()


        if ad==""or soyad==""or email==""or kullanici_adi==""or parola=="":
            QtWidgets.QMessageBox.warning(self,"Eksik Bilgi !","Tüm alanları doldurunuz")
            return

        try:
            self.cursor.execute("""
               
             INSERT INTO kullanıcılar(ad,soyad,email,kullanıcı_adı,parola)
             VALUES(?,?,?,?,?)
             
            
            """,(ad,soyad,email,kullanici_adi,parola))

            self.baglanti.commit()
            QtWidgets.QMessageBox.information(self,"Başarılı","Kullanıcı Kaydedildi")

        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.warning(self,"Hata","Bu kullanıcı adı zaten alınmış")

        except Exception as e:
            QtWidgets.QMessageBox.warning(self,"Hata",f"Bir hata oluştu {str(e)}")





