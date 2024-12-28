from flask_sqlalchemy import SQLAlchemy
from app import db

class Pembeli(db.Model):
    id_pembeli = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    alamat = db.Column(db.Text)
    no_telepon = db.Column(db.String(20))
    transaksis = db.relationship('Transaksi', backref='pembeli') # Relasi ke Transaksi

    def to_dict(self):
        return {
            'id_pembeli': self.id_pembeli,
            'nama': self.nama,
            'alamat': self.alamat,
            'no_telepon': self.no_telepon
        }

class Penjual(db.Model):
    id_penjual = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    barangs = db.relationship('Barang', backref='penjual') # Relasi ke Barang
    transaksis = db.relationship('Transaksi', backref='penjual') # Relasi ke Transaksi

    def to_dict(self):
        return {
            'id_penjual': self.id_penjual,
            'nama': self.nama
        }

class Barang(db.Model):
    id_barang = db.Column(db.Integer, primary_key=True)
    id_penjual = db.Column(db.Integer, db.ForeignKey('penjual.id_penjual'), nullable=False)
    id_dbarang = db.Column(db.Integer, db.ForeignKey('dbarang.id_dbarang'), nullable=False)
    nama = db.Column(db.String(255), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    transaksis = db.relationship('Transaksi', backref='barang') # Relasi ke Transaksi

    def to_dict(self):
        return {
            'id_barang': self.id_barang,
            'id_penjual': self.id_penjual,
            'id_dbarang' : self.id_dbarang,
            'nama': self.nama,
            'harga': self.harga
        }
    
class DBarang(db.Model):
    id_dbarang = db.Column(db.Integer, primary_key=True)
    deskripsi = db.Column(db.Text)
    barangs = db.relationship('Barang', backref='dbarang')

    def to_dict(self):
        return {
            'id_dbarang' : self.id_dbarang,
            'deskripsi' : self.deskripsi
        }

class Transaksi(db.Model):
    id_transaksi = db.Column(db.Integer, primary_key=True)
    id_pembeli = db.Column(db.Integer, db.ForeignKey('pembeli.id_pembeli'), nullable=False)
    id_penjual = db.Column(db.Integer, db.ForeignKey('penjual.id_penjual'), nullable=False)
    id_barang = db.Column(db.Integer, db.ForeignKey('barang.id_barang'), nullable=False)
    tanggal_transaksi = db.Column(db.Date)
    total_harga = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id_transaksi': self.id_transaksi,
            'id_pembeli': self.id_pembeli,
            'id_penjual': self.id_penjual,
            'id_barang': self.id_barang,
            'tanggal_transaksi' : str(self.tanggal_transaksi),
            'total_harga' : self.total_harga
        }