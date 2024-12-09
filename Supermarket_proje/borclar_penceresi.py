
import sqlite3

from PyQt6 import QtWidgets



class BorcEklemePenceresi(QtWidgets.QWidget):

    def __init__(self,baglanti):
        super().__init__()
        self.baglanti = baglanti
        self.cursor = self.baglanti.cursor()
        self.init_ui()

    def init_ui(self):

        self.isim_label=QtWidgets.QLabel("İsim",self)
        self.isim=QtWidgets.QLineEdit(self)

        self.borc_tutari_label=QtWidgets.QLabel("Borç Tutarı",self)
        self.borc_tutari=QtWidgets.QLineEdit(self)

        self.kaydet_buton=QtWidgets.QPushButton("Kaydet",self)

        self.kaydet_buton.clicked.connect(self.borc_ekle)

        layout=QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.isim_label)
        layout.addWidget(self.isim)
        layout.addWidget(self.borc_tutari_label)
        layout.addWidget(self.borc_tutari)
        layout.addWidget(self.kaydet_buton)

        self.setWindowTitle("Borç Ekleme Penceresi")
        self.resize(400,200)

    def borc_ekle(self):
        isim=self.isim.text().strip()
        borc_tutari=self.borc_tutari.text().strip()


        if isim==""or borc_tutari=="":
            QtWidgets.QMessageBox.warning(self,"Eksik Bilgi","Tüm alanları doldurunuz")
            return


        try:
            borc_tutari=float(borc_tutari)

        except:
            QtWidgets.QMessageBox.warning(self,"Hata","Borç sadece rakam olmalıdır")


        try:
            self.cursor.execute("SELECT borc_tutari FROM kullanıcı_borc WHERE isim=?",(isim,))
            mevcut_borc=self.cursor.fetchone()

            if mevcut_borc:
                yeni_borc=borc_tutari+mevcut_borc[0]

                self.cursor.execute("UPDATE kullanıcı_borc SET borc_tutari=? WHERE isim=?",(yeni_borc,isim))
                QtWidgets.QMessageBox.information(self,"Başarılı","Borç Başarıyla Güncellendi")

            else:
                self.cursor.execute("INSERT INTO kullanıcı_borc(isim,borc_tutari) VALUES(?,?)",(isim,borc_tutari))

            QtWidgets.QMessageBox.information(self,"Başarılı","Borç Eklendi")

            self.baglanti.commit()

            self.isim.clear()
            self.borc_tutari.clear()

        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.warning(self,"Hata","Bu kullanıcı zaten var")

        except Exception as e:
            QtWidgets.QMessageBox.warning(self,"Hata",f"Bir hata oluştu :{str(e)}")


class BorcSorgulamaPenceresi(QtWidgets.QWidget):
    def __init__(self, baglanti):
        super().__init__()
        self.baglanti = baglanti
        self.cursor = self.baglanti.cursor()
        self.init_ui()

    def init_ui(self):

        self.kullanici_ara_label=QtWidgets.QLabel("Adınızı yazınız",self)
        self.kullanici_ara=QtWidgets.QLineEdit(self)

        self.borc_ara=QtWidgets.QPushButton("Borç Sorgula",self)


        self.tablo=QtWidgets.QTableWidget(self)
        self.tablo.setColumnCount(2)
        self.tablo.setHorizontalHeaderLabels(["İsim", "Borç Tutarı"])

        layout=QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.kullanici_ara_label)
        layout.addWidget(self.kullanici_ara)
        layout.addWidget(self.borc_ara)

        layout.addWidget(self.tablo)

        self.borc_ara.clicked.connect(self.borc_sorgulama)

        self.setWindowTitle("Borç Sorgulama Penceresi")
        self.resize(400,200)

    def borc_sorgulama(self):
        kullanici_ara = self.kullanici_ara.text().strip()

        if not kullanici_ara:
            QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen bir isim giriniz!")
            return

        try:

            sorgu = """
                SELECT isim, SUM(borc_tutari) AS toplam_borc FROM kullanıcı_borc 
                WHERE isim LIKE ? 
                GROUP BY isim
                """
            self.cursor.execute(sorgu, (f"%{kullanici_ara}%",))
            sonuc = self.cursor.fetchone()

            self.tablo.setRowCount(0)
            if not sonuc:
                QtWidgets.QMessageBox.information(self, "Sonuç", "Borç bilgisi bulunamadı")
                return

            self.tablo.setRowCount(1)
            self.tablo.setItem(0, 0, QtWidgets.QTableWidgetItem(sonuc[0]))
            self.tablo.setItem(0, 1, QtWidgets.QTableWidgetItem(str(sonuc[1])))

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Hata", f"Bir hata oluştu: {str(e)}")



class BorcSilmePenceresi(QtWidgets.QWidget):
    def __init__(self, baglanti):
        super().__init__()
        self.baglanti = baglanti
        self.cursor = self.baglanti.cursor()
        self.init_ui()

    def init_ui(self):
        self.isim_label=QtWidgets.QLabel("İsim",self)
        self.isim=QtWidgets.QLineEdit(self)

        self.borc_tutari_label=QtWidgets.QLabel("Borç Tutarı",self)
        self.borc_tutari=QtWidgets.QLineEdit(self)

        self.sil_buton=QtWidgets.QPushButton("Sil",self)

        layout=QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.isim_label)
        layout.addWidget(self.isim)

        layout.addWidget(self.borc_tutari_label)
        layout.addWidget(self.borc_tutari)

        layout.addWidget(self.sil_buton)
        self.sil_buton.clicked.connect(self.borc_silme)

        self.setWindowTitle("Borç Silme Penceresi")
        self.resize(400,200)

    def borc_silme(self):
        isim = self.isim.text().strip()
        borc_tutari = self.borc_tutari.text().strip()

        if isim == "" or borc_tutari == "":
            QtWidgets.QMessageBox.warning(self, "Eksik Bilgi", "Tüm alanları doldurunuz")
            return

        try:
            borc_tutari = float(borc_tutari)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Geçersiz Bilgi", "Borç tutarı sadece rakam olmalıdır")
            return

        try:
            self.cursor.execute("SELECT borc_tutari FROM kullanıcı_borc WHERE isim=?", (isim,))
            mevcut_borc = self.cursor.fetchone()

            if mevcut_borc is None:
                QtWidgets.QMessageBox.warning(self, "Hata", "Bu kullanıcı için borç gözükmüyor")
                return

            if borc_tutari > mevcut_borc[0]:
                QtWidgets.QMessageBox.warning(self, "Hata", "Silmek istediğiniz borç tutarı mevcut borçtan büyük!")
                return

            yeni_borc = mevcut_borc[0] - borc_tutari
            self.cursor.execute("UPDATE kullanıcı_borc SET borc_tutari=? WHERE isim=?", (yeni_borc, isim))
            self.baglanti.commit()

            self.isim.clear()
            self.borc_tutari.clear()

            QtWidgets.QMessageBox.information(self, "Başarılı", "Borç başarıyla güncellendi.")

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Hata", f"Bir hata oluştu: {str(e)}")













