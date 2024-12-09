import  sqlite3

from PyQt6 import QtWidgets
from tercih_penceresi import TercihPenceresi
from kayıt_penceresi import KayıtPenceresi



class Anapencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.baglanti_olustur()
        self.init_ui()


    def baglanti_olustur(self):
        self.baglanti=sqlite3.connect("supermarket.db")
        self.cursor=self.baglanti.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS kullanıcılar (ad TEXT,soyad TEXT,email TEXT,kullanıcı_adı TEXT PRIMARY KEY,parola TEXT)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS urunler(urun_kodu TEXT PRIMARY KEY,urun_adi  TEXT,urun_fiyati REAL)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS kullanıcı_borc(isim TEXT,borc_tutari REAL)")


        self.baglanti.commit()

    def init_ui(self):
        self.kullanici_adi_label=QtWidgets.QLabel("Kullanıcı Adı:",self)
        self.kullanici_adi=QtWidgets.QLineEdit(self)

        self.parola_label=QtWidgets.QLabel("Şifre",self)
        self.parola=QtWidgets.QLineEdit(self)
        self.parola.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.giris=QtWidgets.QPushButton("Giriş Yap",self)
        self.uye_ol=QtWidgets.QPushButton("Üye ol",self)

        self.yazi_alani=QtWidgets.QLabel("",self)

        grid=QtWidgets.QGridLayout(self)
        grid.addWidget(self.kullanici_adi_label,0,0)
        grid.addWidget(self.kullanici_adi,0,1)
        grid.addWidget(self.parola_label,1,0)
        grid.addWidget(self.parola,1,1)
        grid.addWidget(self.yazi_alani,2,0,1,2)
        grid.addWidget(self.giris,3,0,1,2)
        grid.addWidget(self.uye_ol,4,0,1,2)

        self.setLayout(grid)
        self.setWindowTitle("Kullanıcı Girişi")

        self.giris.clicked.connect(self.login)
        self.uye_ol.clicked.connect(self.sign_up)


        self.resize(400,200)
        self.show()

    def login(self):
        adi = self.kullanici_adi.text()
        parola = self.parola.text()

        if not adi or not parola:
            QtWidgets.QMessageBox.warning(self, "Hata", "Kullanıcı adı ya da şifre boş bırakılamaz")
            return

        try:
            self.cursor.execute("SELECT * FROM kullanıcılar WHERE kullanıcı_adı=? AND parola=?", (adi, parola))
            data = self.cursor.fetchall()

            if len(data) == 0:
                self.yazi_alani.setText("Böyle bir kullanıcı kaydı bulunamadı")
            else:
                self.yazi_alani.setText(f"Hoşgeldiniz {adi}")
                self.close()
                self.tercih_penceresi = TercihPenceresi(self.baglanti)
                self.tercih_penceresi.show()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {str(e)}")

    def sign_up(self):
        self.kayıt_penceresi=KayıtPenceresi(self.baglanti)
        self.kayıt_penceresi.show()



