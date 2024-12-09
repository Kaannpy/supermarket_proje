from PyQt6 import QtWidgets

from urunler_penceresi import UrunEklemePenceresi, UrunSorgulamaPenceresi,UrunSilmePenceresi
from borclar_penceresi import BorcEklemePenceresi,BorcSorgulamaPenceresi,BorcSilmePenceresi
from urun_satis_penceresi import UrunSatisislemi


class TercihPenceresi(QtWidgets.QWidget):
    def __init__(self,baglanti):
        super().__init__()
        self.baglanti=baglanti
        self.init_ui()



    def init_ui(self):

        urun_grup_box=QtWidgets.QGroupBox("Ürün ve Satış İşlemleri")

        urun_layout=QtWidgets.QVBoxLayout()
        self.urun_ekle_btn = QtWidgets.QPushButton("Ürün Ekle",self)
        self.urun_sorgula_btn = QtWidgets.QPushButton("Ürün Sorgula",self)
        self.urun_silme_btn = QtWidgets.QPushButton("Ürün Silme",self)
        self.satis_islemi_btn = QtWidgets.QPushButton("Satış İşlemleri",self)

        urun_layout.addWidget(self.urun_ekle_btn)
        urun_layout.addWidget(self.urun_sorgula_btn)
        urun_layout.addWidget(self.urun_silme_btn)
        urun_layout.addWidget(self.satis_islemi_btn)


        urun_grup_box.setLayout(urun_layout)

        borc_grup_box=QtWidgets.QGroupBox("Borç İşlemleri")
        borc_layout = QtWidgets.QVBoxLayout()

        self.borc_ekle_btn = QtWidgets.QPushButton("Borç Ekle",self)
        self.borc_sorgula_btn = QtWidgets.QPushButton("Borç Sorgula",self)
        self.borc_sil_btn=QtWidgets.QPushButton("Borç Sil",self)

        borc_layout.addWidget(self.borc_ekle_btn)
        borc_layout.addWidget(self.borc_sorgula_btn)
        borc_layout.addWidget(self.borc_sil_btn)





        borc_grup_box.setLayout(borc_layout)






        self.cikis_btn = QtWidgets.QPushButton("Çıkış", self)


        main_layout=QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(urun_grup_box)
        main_layout.addWidget(borc_grup_box)
        main_layout.addWidget(self.cikis_btn)

        self.setLayout(main_layout)
        self.resize(500,300)



        self.urun_ekle_btn.clicked.connect(self.urun_ekle)
        self.urun_sorgula_btn.clicked.connect(self.urun_sorgula)
        self.urun_silme_btn.clicked.connect(self.urun_silme)
        self.satis_islemi_btn.clicked.connect(self.satis_islemi)
        self.borc_ekle_btn.clicked.connect(self.borc_ekle)
        self.borc_sorgula_btn.clicked.connect(self.borc_sorgula)
        self.borc_sil_btn.clicked.connect(self.borc_silme)
        self.cikis_btn.clicked.connect(self.cikis_yap)

        self.setWindowTitle("Tercih Ekranı")
        self.resize(400,200)


    def urun_ekle(self):
        self.urun_ekleme_penceresi=UrunEklemePenceresi(self.baglanti)
        self.urun_ekleme_penceresi.show()

    def urun_sorgula(self):
        self.urun_sorgulama_penceresi=UrunSorgulamaPenceresi(self.baglanti)
        self.urun_sorgulama_penceresi.show()

    def urun_silme(self):
        self.urun_silme_penceresi=UrunSilmePenceresi(self.baglanti)
        self.urun_silme_penceresi.show()

    def borc_ekle(self):
        self.borc_ekleme_penceresi=BorcEklemePenceresi(self.baglanti)
        self.borc_ekleme_penceresi.show()

    def borc_sorgula(self):
        self.borc_sorgulama_penceresi=BorcSorgulamaPenceresi(self.baglanti)
        self.borc_sorgulama_penceresi.show()

    def borc_silme(self):
        self.borc_silme_penceresi=BorcSilmePenceresi(self.baglanti)
        self.borc_silme_penceresi.show()
    def satis_islemi(self):
        self.urun_satis_penceresi=UrunSatisislemi(self.baglanti)
        self.urun_satis_penceresi.show()
    def cikis_yap(self):
        self.close()


