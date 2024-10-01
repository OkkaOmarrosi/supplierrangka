# Sistem Supply Chain Management (SCM) - Modul Supplier

## Kelompok 2 | Integrasi Aplikasi Korporasi SD-A1
1. MOH. OKKA OAMRROSI IPUTUSARMA (164221105)
2. KYLA BELVA QUEENA (164221015)
3. FRADINKA AMELIA EDYPUTRI (164221045)
4. VERDYAN FARREL BILIARSA (164221076)
5. HAFIZAH MUFIDA NOVRIZAL ENDA (164221071)
6. PUTU ANGGA KURNIAWAN (164221098)

## Deskripsi Proyek
Modul ini merupakan bagian dari Sistem Supply Chain Management (SCM) untuk perusahaan PT. Sepeda Onthel Surabaya. Modul Supplier bertanggung jawab untuk mengelola informasi produk, harga, dan ketersediaan stok dari pemasok, serta berinteraksi dengan modul Retail dan Distributor melalui RESTful API.

## Fitur Utama
1. **Kelola Produk**: Mengelola data produk, termasuk menampilkan, menambah, mengedit, dan menghapus produk yang tersedia.
2. **Kelola Pesanan**: Mendapatkan dan menampilkan pesanan dari Retail, memproses pesanan, dan berkomunikasi dengan Distributor untuk pengiriman.
3. **Integrasi RESTful API**: Modul Supplier menyediakan endpoint API yang dapat diakses oleh modul lain, seperti Retail dan Distributor.

## Alur Kerja Modul Supplier
1. **Retail meminta detail produk**:
   - Retail mengirimkan permintaan untuk mendapatkan daftar produk yang tersedia.
   - Supplier menampilkan daftar produk beserta harga dan ketersediaan stok.
   
   **Endpoint**:
   GET /api/products : *Mendapatkan daftar produk dari pemasok*.
   CONTOH:
```Json
   {
    "berat": "0.50",
    "harga": "450000.00",
    "id_produk": 3,
    "linkgambar": "https://standert.de/cdn/shop/files/Kreissage-RS-Road-Bike-Frameset-Navy_500x500@2x.webp?v=1697787188",
    "nama_produk": "Speed",
    "stock": 49
  }
```

2. **Retail membuat pesanan draft**:
- Retail membuat pesanan draft berdasarkan produk yang dipilih, termasuk informasi produk dan alamat pengiriman.
- Supplier menerima draft pesanan dan mempersiapkan produk yang akan dikirim.

**Endpoint**:
POST /api/orders : *Menambah pesanan pembelian produk dari Retail ke Supplier*. 
CONTOH:
```Json
{
   "namapembeli": "verdyan",
   "order_id": 6,
   "resi": "PKO-3668",
   "total_price": "560000.00",
   "total_weight": "4.00"
}
```

3. **Supplier mengirim pesanan ke Distributor**:
- Supplier mengirim detail pesanan ke Distributor, termasuk informasi produk dan alamat pengiriman dari Retail.
- Distributor memberikan harga ongkos kirim kepada Supplier.

**Endpoint**: 
POST /api/distributors/orders : *Mengirim permintaan pengiriman dari Supplier ke Distributor*.

4. **Supplier mengirim total harga ke Retail**:
- Supplier mengirimkan informasi ongkos kirim dari Distributor dan harga total produk kepada Retail.
- Retail memverifikasi harga produk dan ongkos kirim, kemudian melakukan konfirmasi pesanan.

**Endpoint**:
POST /api/orders/confirm : *Mengirim konfirmasi harga produk dan ongkos kirim dari Supplier ke Retail*.
CONTOH:
```Json
{
   "namapembeli": 'Verdyan',
   "order_id": 6,
   "resi": "PKO-3668",
   "total_price": "5600000.00",
   "total_weight": "4.00"
}
```
5. **Supplier menerima konfirmasi dari Retail**:
- Setelah Retail mengonfirmasi pesanan, Supplier mengirim informasi tersebut ke Distributor untuk memproses pengiriman.

**Endpoint**:  
POST /api/distributors/confirm : *Mengirim konfirmasi pesanan dari Retail ke Distributor untuk memproses pengiriman*. 

6. **Supplier memberikan nomor resi ke Retail**:
- Distributor memberikan nomor resi dan detail pengiriman ke Supplier.
- Supplier mengirimkan nomor resi tersebut ke Retail untuk melacak pesanan.

**Endpoint**:
GET /api/orders/tracking/{order_id} : *Mendapatkan nomor resi dan status pengiriman pesanan*.

7. **Supplier menampilkan daftar pemasok**:
- Supplier menyediakan endpoint untuk mendapatkan data pemasok yang aktif.

**Endpoint**:
```Json
GET /api/suppliers : *Mendapatkan data pemasok*.
{
   {
      "location": "Jakarta",
      "name": "SUP002"
   }
}
```

8. **Retail mengecek harga pengiriman**:
- Retail mengirimkan permintaan untuk mengecek harga pengiriman berdasarkan ID log pengiriman.
- Supplier mengembalikan informasi harga pengiriman dan estimasi lama pengiriman.

**Endpoint**:
POST /api/cek_harga : Memeriksa harga dan estimasi lama pengiriman.
{
   "harga_pengiriman": 4200,
   "id_log": 102,
   "lama_pengiriman": "4 hari"
}

## Teknologi yang Digunakan
- **Backend**: Python, Flask
- **Database**: SQLite (atau MySQL, Firebase, sesuai preferensi)
- **Integrasi API**: RESTful API
- **Frontend**: HTML, CSS, JavaScript

## Struktur Direktori
├── app.py # Main file untuk Flask application 
├── templates/ # Direktori untuk file HTML │ 
├── dashboard.html # Halaman dashboard 
│ ├── products.html # Halaman kelola produk 
│ └── orders.html # Halaman kelola pesanan 
├── static/ # Direktori untuk file CSS, JavaScript 
│ └── style.css # File CSS untuk styling 
├── models.py # Model untuk database (SQLite) 
├── api/ # Direktori untuk API │ 
├── supplier.py # API endpoint untuk modul Supplier 
└── README.md # Dokumentasi proyek


## Cara Menjalankan Proyek
1. Clone repository ini ke lokal:
   ```bash
   git clone <repository_url>
   ```
2. Install dependencies:
pip install -r requirements.txt
3. Jalankan server Flask:
python app.py
4. Akses aplikasi melalui browser:
http://165.22.187.192:8000/


Endpoint API Modul Supplier:
1. GET /api/products - Mendapatkan daftar produk dari Supplier.
2. POST /api/orders - Mengirim pesanan draft dari Retail ke Supplier.
3. POST /api/distributors/orders - Mengirim permintaan pengiriman dari Supplier ke Distributor.
4. POST /api/orders/confirm - Mengirim konfirmasi harga produk dan ongkos kirim dari Supplier ke Retail.
5. GET /api/orders/tracking/{order_id} - Mendapatkan nomor resi dan status pengiriman pesanan.


Struktur Halaman Web
1. Login/Register: Halaman login dan register untuk pengguna Supplier.
2. Dashboard: Tampilan utama yang menampilkan ringkasan data produk dan pesanan.
3. Kelola Produk: Halaman untuk mengelola (tambah, edit, hapus) produk.
4. Kelola Pesanan: Halaman untuk melihat dan memproses pesanan dari Retail.

## Konfirmasi Pesanan:
Retailer akan mengonfirmasi pesanan, yang akan mengirimkan id_log ke endpoint. Endpoint ini akan mengirimkan permintaan ke API distributor untuk memproses pesanan dan mengonfirmasi order.