import sqlite3

from PyQt6 import QtWidgets


class UrunSatisislemi(QtWidgets.QWidget):
    def __init__(self,baglanti):
        super().__init__()
        self.baglanti = baglanti
        self.cursor = self.baglanti.cursor()
        self.init_ui()
        self.toplam_fiyat = 0.0
    def init_ui(self):

        self.urun_kodu_label=QtWidgets.QLabel("Ürün Kodunu :")
        self.urun_kodu=QtWidgets.QLineEdit(self)

        self.ekle_buton = QtWidgets.QPushButton("Ekle", self)
        self.hesapla_buton = QtWidgets.QPushButton("Toplam Fiyat Hesapla", self)

        self.tablo=QtWidgets.QTableWidget()
        self.tablo.setColumnCount(4)

        self.tablo.setHorizontalHeaderLabels(["Ürün Kodu","Ürün Adı","Ürün Fiyat","Sil"])
        self.toplam_tutar_label = QtWidgets.QLabel("Toplam Tutar: 0.0")


        self.ekle_buton.clicked.connect(self.urun_ekle)
        self.hesapla_buton.clicked.connect(self.fiyat_hesapla)


        layout=QtWidgets.QVBoxLayout(self)


        layout.addWidget(self.urun_kodu_label)
        layout.addWidget(self.urun_kodu)
        layout.addWidget(self.ekle_buton)

        layout.addWidget(self.hesapla_buton)
        layout.addWidget(self.tablo)
        layout.addWidget(self.toplam_tutar_label)



        self.setWindowTitle("Ürün Satış Ekranı")
        self.resize(400,300)

    def urun_ekle(self):
        urun_kodu=self.urun_kodu.text().strip()

        if  not urun_kodu:
            QtWidgets.QMessageBox.warning(self, "Hata", "Ürün Kodu boş bırakılamaz")
            return

        self.cursor.execute("SELECT *FROM urunler WHERE urun_kodu=?",(urun_kodu,))
        urun=self.cursor.fetchone()

        if urun:
            row_count = self.tablo.rowCount()
            self.tablo.insertRow(row_count)


            self.tablo.setItem(row_count,0,QtWidgets.QTableWidgetItem(urun[0]))
            self.tablo.setItem(row_count,1,QtWidgets.QTableWidgetItem(urun[1]))
            self.tablo.setItem(row_count,2,QtWidgets.QTableWidgetItem(str(urun[2])))

            sil_buton = QtWidgets.QPushButton("Sil")
            sil_buton.setProperty("row", row_count)
            sil_buton.clicked.connect(self.satir_sil)
            self.tablo.setCellWidget(row_count, 3, sil_buton)

            self.toplam_fiyat+=float(urun[2])
            self.toplam_tutar_label.setText(f"Toplam tutar:{self.toplam_fiyat:.2f}")

            self.urun_kodu.clear()

        else:
            QtWidgets.QMessageBox.warning(self,"Sonuç Bulunamadı","Bu ürün koduna ait bilgi yok")

    def fiyat_hesapla(self):
        QtWidgets.QMessageBox.information(self, "Toplam Fiyat", f"Toplam Fiyat: {self.toplam_fiyat:.2f}")

    def satir_sil(self):

        sil_buton = self.sender()
        if sil_buton:

            row = sil_buton.property("row")


            fiyat_item = self.tablo.item(row, 2)
            if fiyat_item:
                fiyat = float(fiyat_item.text())
                self.toplam_fiyat -= fiyat
                self.toplam_tutar_label.setText(f"Toplam Tutar: {self.toplam_fiyat:.2f}")


            self.tablo.removeRow(row)