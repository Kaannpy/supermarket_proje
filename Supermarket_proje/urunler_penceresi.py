from PyQt6 import QtWidgets
import sqlite3



class UrunEklemePenceresi(QtWidgets.QWidget):
    def __init__(self, baglanti):
        super().__init__()
        self.baglanti = baglanti
        self.cursor = self.baglanti.cursor()
        self.init_ui()

    def init_ui(self):
        self.urun_kodu_label = QtWidgets.QLabel("Ürün Kodu:", self)
        self.urun_kodu = QtWidgets.QLineEdit(self)

        self.urun_adi_label = QtWidgets.QLabel("Ürün Adı:", self)
        self.urun_adi = QtWidgets.QLineEdit(self)

        self.urun_fiyati_label = QtWidgets.QLabel("Ürün Fiyatı:", self)
        self.urun_fiyati = QtWidgets.QLineEdit(self)

        self.kaydet_buton = QtWidgets.QPushButton("Kaydet", self)

        self.kaydet_buton.clicked.connect(self.urun_ekle)

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.urun_kodu_label)
        layout.addWidget(self.urun_kodu)

        layout.addWidget(self.urun_adi_label)
        layout.addWidget(self.urun_adi)

        layout.addWidget(self.urun_fiyati_label)
        layout.addWidget(self.urun_fiyati)

        layout.addWidget(self.kaydet_buton)

        self.setWindowTitle("Ürün Ekleme Penceresi")
        self.resize(400, 200)

    def urun_ekle(self):
        urun_kodu = self.urun_kodu.text()
        urun_adi = self.urun_adi.text()
        urun_fiyati = self.urun_fiyati.text()

        if urun_kodu == "" or urun_adi == "" or urun_fiyati == "":
            QtWidgets.QMessageBox.warning(self, "Eksik Bilgi", "Tüm alanları doldurunuz!")
            return

        try:
            self.cursor.execute(
                "INSERT INTO urunler(urun_kodu, urun_adi, urun_fiyati) VALUES(?, ?, ?)",
                (urun_kodu, urun_adi, float(urun_fiyati))
            )

            self.baglanti.commit()

            QtWidgets.QMessageBox.information(self, "Başarılı", "Ürün Eklendi!")

        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Hata", "Bu ürün zaten mevcut")


class UrunSorgulamaPenceresi(QtWidgets.QWidget):
    def __init__(self, baglanti):
        super().__init__()
        self.baglanti = baglanti
        self.cursor = self.baglanti.cursor()

        self.init_ui()

    def init_ui(self):
        self.urunkodu_ara = QtWidgets.QLineEdit(self)
        self.urunkodu_ara.setPlaceholderText("Ürün Kodunu giriniz")

        self.ara_buton = QtWidgets.QPushButton("Ürün Ara", self)

        self.listele_buton = QtWidgets.QPushButton("Ürünleri Listele", self)

        self.tablo = QtWidgets.QTableWidget(self)
        self.tablo.setColumnCount(3)
        self.tablo.setHorizontalHeaderLabels(["Ürün Kodu", "Ürün Adı", "Ürün Fiyatı"])

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.urunkodu_ara)
        layout.addWidget(self.ara_buton)
        layout.addWidget(self.listele_buton)
        layout.addWidget(self.tablo)

        self.setWindowTitle("Ürün Sorgulama")
        self.resize(400, 200)

        self.ara_buton.clicked.connect(self.urun_ara)
        self.listele_buton.clicked.connect(self.urunleri_listele)

    def urun_ara(self):
        urun_kodu = self.urunkodu_ara.text()

        if not urun_kodu:
            QtWidgets.QMessageBox.warning(self, "Eksik Bilgi", "Ürün Kodunu Giriniz")
            return

        self.cursor.execute("SELECT * FROM urunler WHERE urun_kodu=?", (urun_kodu,))
        urun = self.cursor.fetchone()

        if urun:
            self.tablo.setRowCount(1)
            self.tablo.setItem(0, 0, QtWidgets.QTableWidgetItem(str(urun[0])))
            self.tablo.setItem(0, 1, QtWidgets.QTableWidgetItem(urun[1]))
            self.tablo.setItem(0, 2, QtWidgets.QTableWidgetItem(str(urun[2])))
        else:
            QtWidgets.QMessageBox.warning(self, "Sonuç Bulunamadı", "Böyle bir ürün kodu yok!")

    def urunleri_listele(self):
        self.cursor.execute("SELECT * FROM urunler")
        urunler = self.cursor.fetchall()

        self.tablo.setRowCount(0)

        if urunler:
            self.tablo.setRowCount(len(urunler))

            for satir_sayisi, urun in enumerate(urunler):
                self.tablo.setItem(satir_sayisi, 0, QtWidgets.QTableWidgetItem(str(urun[0])))
                self.tablo.setItem(satir_sayisi, 1, QtWidgets.QTableWidgetItem(urun[1]))
                self.tablo.setItem(satir_sayisi, 2, QtWidgets.QTableWidgetItem(str(urun[2])))

        else:
            QtWidgets.QMessageBox.warning(self, "Sonuç bulunamadı", "Hiç ürün bulunmadı")


class UrunSilmePenceresi(QtWidgets.QWidget):
    def __init__(self, baglanti):
        super().__init__()
        self.baglanti = baglanti
        self.cursor = self.baglanti.cursor()
        self.init_ui()

    def init_ui(self):

        self.urun_kodu_label=QtWidgets.QLabel("Ürün kodu:",self)
        self.urun_kodu=QtWidgets.QLineEdit(self)

        self.sil_buton=QtWidgets.QPushButton("Sil",self)

        self.sil_buton.clicked.connect(self.urun_silme)


        layout=QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.urun_kodu_label)
        layout.addWidget(self.urun_kodu)

        layout.addWidget(self.sil_buton)

        self.setWindowTitle("Ürün Silme Ekranı")
        self.resize(400,200)

    def urun_silme(self):

        urun_kodu=self.urun_kodu.text()


        if not urun_kodu:
            QtWidgets.QMessageBox.warning(self,"Eksik Bilgi","Tüm alanları doldurunuz")
            return

        try:

            self.cursor.execute("SELECT *FROM urunler WHERE urun_kodu=?",(urun_kodu,))
            urun=self.cursor.fetchone()

            if urun is None:
                QtWidgets.QMessageBox.warning(self,"Hata","Böyle bir ürün kodu yok")

            else:
                self.cursor.execute("DELETE  FROM urunler WHERE urun_kodu=?",(urun_kodu,))
                self.baglanti.commit()
                QtWidgets.QMessageBox.information(self,"Başarılı","Ürün Başarıyla Silindi")

        except Exception as e :
                QtWidgets.QMessageBox.warning(self,"Hata",f"Bir hata oluştu:{str(e)}")














