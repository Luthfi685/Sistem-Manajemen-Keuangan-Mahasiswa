import csv
from datetime import datetime

FILE = 'keuangan_mahasiswa.csv'


def inisialisasi_file():
    try:
        with open(FILE, mode='x', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Tanggal", "Jenis", "Kategori", "Jumlah", "Keterangan"])
            writer.writeheader()
    except FileExistsError:
        pass  


def catat_transaksi():
    print("\n=== Catat Transaksi ===")
    jenis = input("Jenis (Pemasukan/Pengeluaran): ").strip().capitalize()
    if jenis not in ['Pemasukan', 'Pengeluaran']:
        print(" Jenis tidak valid!")
        return

    kategori = input("Kategori (contoh: Makan, Beasiswa, Transport): ").strip()
    try:
        jumlah = float(input("Jumlah (angka): "))
    except ValueError:
        print(" Jumlah harus berupa angka.")
        return

    keterangan = input("Keterangan tambahan (opsional): ")
    tanggal = datetime.now().strftime("%Y-%m-%d")

    transaksi = {
        "Tanggal": tanggal,
        "Jenis": jenis,
        "Kategori": kategori,
        "Jumlah": jumlah,
        "Keterangan": keterangan
    }

    with open(FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=transaksi.keys())
        writer.writerow(transaksi)

    print(" Transaksi berhasil dicatat.")


def lihat_riwayat():
    print("\n=== Riwayat Transaksi Hari Ini ===")
    hari_ini = datetime.now().strftime("%Y-%m-%d")
    ditemukan = False

    try:
        with open(FILE, mode='r') as file:
            reader = csv.DictReader(file)
            transaksi_list = list(reader)

            for t in transaksi_list:
                if t["Tanggal"] == hari_ini:
                    print(f"[{t['Tanggal']}] {t['Jenis']} - {t['Kategori']} - Rp{t['Jumlah']} ({t['Keterangan']})")
                    ditemukan = True

            if not ditemukan:
                print(" Belum ada transaksi hari ini.")
    except FileNotFoundError:
        print(" File belum tersedia.")


def hitung_saldo():
    print("\n=== Hitung Saldo Akhir ===")
    total_pemasukan = 0
    total_pengeluaran = 0

    try:
        with open(FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                jumlah = float(row["Jumlah"])
                if row["Jenis"] == "Pemasukan":
                    total_pemasukan += jumlah
                elif row["Jenis"] == "Pengeluaran":
                    total_pengeluaran += jumlah
    except FileNotFoundError:
        print(" Tidak ada data transaksi.")
        return

    saldo = total_pemasukan - total_pengeluaran
    print(f" Total Pemasukan   : Rp{total_pemasukan}")
    print(f" Total Pengeluaran : Rp{total_pengeluaran}")
    print(f" Saldo Akhir       : Rp{saldo}")


def menu():
    inisialisasi_file()
    while True:
        print("\n=== MANAJEMEN KEUANGAN MAHASISWA ===")
        print("1. Catat Transaksi")
        print("2. Lihat Riwayat Harian")
        print("3. Hitung Saldo Akhir")
        print("4. Keluar")

        pilihan = input("Pilih menu (1-4): ")
        if pilihan == "1":
            catat_transaksi()
        elif pilihan == "2":
            lihat_riwayat()
        elif pilihan == "3":
            hitung_saldo()
        elif pilihan == "4":
            print("👋 Terima kasih telah menggunakan aplikasi.")
            break
        else:
            print(" Pilihan tidak valid!")


menu()
