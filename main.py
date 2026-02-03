 # ================== DATA AWAL ==================
# Daftar karyawan tetap
KARYAWAN = ["Akmalu", "Khansa", "Hedi", "Hasna", "Mutty"]

# Penyimpanan data absensi (list of dictionaries)
absensi_data = []

# ================== FUNGSI BANTUAN ==================
def validasi_nama(nama):
    """Validasi nama: hanya huruf dan spasi, minimal 2 karakter, tidak kosong"""
    if not nama or len(nama.strip()) < 2:
        return False, "Nama minimal 2 karakter dan tidak boleh kosong!"

    nama_clean = nama.strip()
    for char in nama_clean:
        if not (char.isalpha() or char.isspace()):
            return False, f"Karakter '{char}' tidak diizinkan! Hanya huruf dan spasi."

    return True, nama_clean

def validasi_jam(jam_str):
    try:
        jam_str = jam_str.replace(':', '.')
        parts = jam_str.split('.')
        if len(parts) != 2:
            return None

        jam = int(parts[0])
        menit = int(parts[1])

        if 0 <= jam <= 23 and 0 <= menit <= 59:
            return f"{jam:02d}.{menit:02d}"
        return None
    except:
        return None

def validasi_tanggal(tgl_str):
    try:
        parts = tgl_str.split('-')
        if len(parts) != 3:
            return None

        hari = int(parts[0])
        bulan = int(parts[1])
        tahun = int(parts[2])

        if not (1 <= hari <= 31 and 1 <= bulan <= 12 and 2000 <= tahun <= 2100):
            return None

        # Validasi hari per bulan
        hari_per_bulan = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if hari > hari_per_bulan[bulan - 1]:
            return None

        return f"{hari:02d}-{bulan:02d}-{tahun:04d}"
    except:
        return None

def tentukan_status_otomatis(jam):
    """Tentukan status otomatis: ≤ 08.00 = hadir, > 08.00 = telat"""
    try:
        jam_float = float(jam.replace(':', '.'))
        return "hadir" if jam_float <= 8.00 else "telat"
    except:
        return "telat"

def tampilkan_header():
    print("\n" + "="*65)
    print(" " * 18 + "SISTEM ABSENSI KARYAWAN")
    print("="*65)

def tampilkan_karyawan():
    print("\nDaftar Karyawan:")
    if not KARYAWAN:      #percabangan
        print("  ℹ️  Belum ada data karyawan.")
        return
    for i, nama in enumerate(KARYAWAN, 1):          #perulangan
        print(f"  {i}. {nama:<15}")

# ================== FUNGSI VALIDASI INPUT DENGAN PENGULANGAN ==================
def input_pilihan_karyawan():
    """Input nomor karyawan dengan validasi ulang hingga valid"""
    while True:
        try:
            tampilkan_karyawan()
            if not KARYAWAN:
                print("❌ Tidak ada karyawan terdaftar! Tambahkan karyawan terlebih dahulu.")
                return None

            pilih = int(input(f"\nPilih nomor karyawan (1-{len(KARYAWAN)}): "))   #batas maksimal sesuai jumlah data
            if 1 <= pilih <= len(KARYAWAN):     # memastikan nomor sesuai daftar
                return KARYAWAN[pilih-1]
            else:
                print(f"❌ Input tidak valid! Harap masukkan angka 1 hingga {len(KARYAWAN)}.")
        except ValueError:
            print("❌ Input harus berupa angka!")

def input_kategori_absensi():
    """Pilih kategori absensi: hadir/telat (otomatis), izin, atau sakit"""
    print("\n[+] PILIH STATUS KEHADIRAN")
    print("  1. Hadir / Telat   → Input jam wajib")
    print("  2. Izin            → Tanpa input jam")
    print("  3. Sakit           → Tanpa input jam")
    print("\n  ⚠️  Catatan: Untuk opsi 1, jam ≤ 08.00 = hadir, > 08.00 = telat")

    while True:               # Loop sampai user memasukkan input valid.
        pilih = input("\nPilihan (1-3) [Ketik 'batal' untuk cancel]: ").strip().lower()

        if pilih == 'batal':
            return None

        if pilih in ['1', '2', '3']:
            kategori_map = {
                '1': 'otomatis',  # Akan divalidasi berdasarkan jam
                '2': 'izin',
                '3': 'sakit'
            }
            return kategori_map[pilih]          # Mengembalikan kategori sesuai pilihan user.
        else:
            print("❌ Pilihan tidak valid! Masukkan angka 1, 2, atau 3.")


def input_jam_absen():
    """Input jam dengan validasi ulang hingga format valid (HANYA UNTUK STATUS HADIR/TELAT)"""
    while True:
        jam = input("Jam absen (format HH.MM atau HH:MM, contoh: 08.00): ").strip()
        if jam.lower() == 'batal':
            return None

        jam_valid = validasi_jam(jam)
        if jam_valid:
            return jam_valid
        else:
            print("❌ Format jam tidak valid! Contoh benar: 08.00 atau 08:30")
            print("   Tips: Gunakan titik (.) atau titik dua (:) sebagai pemisah")

def input_tanggal_absen():
    """Input tanggal dengan validasi ulang hingga format valid"""
    while True:
        tanggal = input("Tanggal absen (format DD-MM-YYYY, contoh: 02-02-2026): ").strip()
        if tanggal.lower() == 'batal':
            return None
        tanggal_valid = validasi_tanggal(tanggal)
        if tanggal_valid:
            return tanggal_valid
        else:
            print("❌ Format tanggal tidak valid! Contoh benar: 02-02-2026")
            print("   Pastikan: hari (01-31), bulan (01-12), tahun (2000-2100)")

def input_id_valid(prompt, data_list):
    """Input ID dengan validasi ulang hingga ID ditemukan"""
    while True:
        try:
            id_input = input(prompt).strip()
            if id_input.lower() == 'batal':
                return None
            id_cari = int(id_input)
            for record in data_list:
                if record['id'] == id_cari:
                    return id_cari
            print(f"❌ ID {id_cari} tidak ditemukan! Daftar ID valid: {[r['id'] for r in data_list]}")
        except ValueError:
            print("❌ ID harus berupa angka!")

# ================== CRUD FUNCTIONS DENGAN VALIDASI PENUH ==================
def tambah_karyawan():
    tampilkan_header()
    print("\n[+] MANAJEMEN DATA KARYAWAN")

    print("\n[+] TAMBAH KARYAWAN BARU")
    print("   - Hanya huruf dan spasi")
    print("   - Minimal 2 karakter")
    print("   - Tidak boleh duplikat")
    print("   - Ketik 'batal' untuk membatalkan")

    while True:
        nama_input = input("\nNama karyawan baru: ").strip()

        # Opsi cancel
        if nama_input.lower() == 'batal':
            print("❌ Penambahan karyawan dibatalkan.")
            return

        # Validasi format nama
        valid, hasil = validasi_nama(nama_input)
        if not valid:
            print(f"❌ {hasil}")
            continue

        nama_clean = hasil

        # Cek duplikasi (case-insensitive)
        if any(nama_clean.lower() == nama.lower() for nama in KARYAWAN):
            print(f"❌ Nama '{nama_clean}' sudah terdaftar! Gunakan nama lain.")
            continue

        # Konfirmasi penambahan
        konfirmasi = input(f"Konfirmasi tambah '{nama_clean}'? (y/n): ").strip().lower()
        if konfirmasi == 'y':
            KARYAWAN.append(nama_clean)
            print(f"\n✅ Karyawan '{nama_clean}' berhasil ditambahkan!")
            print(f"   Total karyawan sekarang: {len(KARYAWAN)} orang")
            return
        elif konfirmasi == 'n':
            print("ℹ️ Penambahan dibatalkan.")
            return
        else:
            print("ℹ️ Input tidak valid. Silakan ulangi.")

def create_absensi():
    tampilkan_header()
    print("\n[+] TAMBAH ABSENSI BARU")

    # Harus ada karyawan terdaftar
    if not KARYAWAN:
        print("❌ Tidak ada karyawan terdaftar! Tambahkan karyawan terlebih dahulu.")
        input("\n❚ Tekan Enter untuk kembali ke menu...")
        return

    # LANGKAH 1: Pilih Karyawan
    nama = input_pilihan_karyawan()
    if nama is None:
        print("❌ Proses dibatalkan oleh pengguna.")
        return

    # LANGKAH 2: Pilih Kategori Absensi
    kategori = input_kategori_absensi()
    if kategori is None:
        print("❌ Proses dibatalkan oleh pengguna.")
        return

    # LANGKAH 3: Input Jam (HANYA UNTUK KATEGORI 'otomatis')
    jam_valid = "-"
    if kategori == 'otomatis':
        jam_valid = input_jam_absen()
        if jam_valid is None:
            print("❌ Proses dibatalkan oleh pengguna.")
            return
    # Untuk 'izin'/'sakit': jam langsung diisi "-"

    # LANGKAH 4: Input Tanggal (WAJIB UNTUK SEMUA KATEGORI)
    tanggal_valid = input_tanggal_absen()
    if tanggal_valid is None:
        print("❌ Proses dibatalkan oleh pengguna.")
        return

    # LANGKAH 5: Tentukan Keterangan Akhir
    if kategori == 'otomatis':
        # Status otomatis berdasarkan jam
        keterangan = tentukan_status_otomatis(jam_valid)
        status_display = "TEPAT WAKTU ✅" if keterangan == "hadir" else "TERLAMBAT ⚠️"
        print(f"\nℹ️  Berdasarkan jam {jam_valid}: {status_display}")
    else:
        # Izin atau sakit - status tetap
        keterangan = kategori
        print(f"\nℹ️  Status: {keterangan.upper()} (tanpa input jam)")

    # Simpan data
    record = {
        "id": len(absensi_data) + 1,
        "nama": nama,
        "jam": jam_valid,  # "-" untuk izin/sakit, jam valid untuk hadir/telat
        "keterangan": keterangan,
        "tanggal": tanggal_valid
    }
    absensi_data.append(record)

    # Tampilkan konfirmasi sukses dengan visual yang jelas
    print(f"\n" + "="*65)
    print("✅ ABSENSI BERHASIL DITAMBAHKAN")
    print("="*65)
    print(f"   ID       : {record['id']}")
    print(f"   Nama     : {nama}")
    print(f"   Jam      : {record['jam']}")
    print(f"   Status   : ", end="")

    # Visualisasi status dengan emoji
    icon_map = {'hadir':'✅', 'telat':'⚠️ ', 'izin':'📝', 'sakit':'🤒'}
    icon = icon_map.get(keterangan, '❓')
    status_text = {
        'hadir': 'HADIR (Tepat Waktu)',
        'telat': 'TERLAMBAT',
        'izin': 'IZIN',
        'sakit': 'SAKIT'
    }.get(keterangan, keterangan.upper())

    print(f"{icon} {status_text}")
    print(f"   Tanggal  : {tanggal_valid}")
    print("="*65)

def read_absensi():
    tampilkan_header()
    if not absensi_data:
        print("\nℹ️  Belum ada data absensi.")
        return

    print("\n[+] DATA ABSENSI LENGKAP")
    print(f"\n{'ID':<4} {'NAMA':<15} {'JAM':<8} {'STATUS':<18} {'TANGGAL':<12}")
    print("-" * 70)

    for record in absensi_data:
        icon_map = {'hadir':'✅', 'telat':'⚠️ ', 'izin':'📝', 'sakit':'🤒'}
        icon = icon_map.get(record['keterangan'], '❓')

        # Format status dengan deskripsi lebih jelas
        status_text = {
            'hadir': 'HADIR (Tepat)',
            'telat': 'TERLAMBAT',
            'izin': 'IZIN',
            'sakit': 'SAKIT'
        }.get(record['keterangan'], record['keterangan'].upper())

        jam_tampil = record['jam']  # Sudah "-" untuk izin/sakit
        print(f"{record['id']:<4} {record['nama']:<15} {jam_tampil:<8} "
              f"{icon} {status_text:<15} {record['tanggal']:<12}")

    # Statistik per karyawan
    print("\n[+] REKAP PER KARYAWAN:")
    for nama in KARYAWAN:
        jumlah = sum(1 for r in absensi_data if r['nama'] == nama)
        if jumlah > 0:
            hadir = sum(1 for r in absensi_data if r['nama'] == nama and r['keterangan'] == 'hadir')
            telat = sum(1 for r in absensi_data if r['nama'] == nama and r['keterangan'] == 'telat')
            izin = sum(1 for r in absensi_data if r['nama'] == nama and r['keterangan'] == 'izin')
            sakit = sum(1 for r in absensi_data if r['nama'] == nama and r['keterangan'] == 'sakit')

            print(f"   👤 {nama:<15} : Total {jumlah}x "
                  f"[✅{hadir} ⚠️{telat} 📝{izin} 🤒{sakit}]")

def update_absensi():
    tampilkan_header()
    if not absensi_data:
        print("\nℹ️  Tidak ada data untuk diupdate.")
        return

    read_absensi()
    print("\n[+] UPDATE ABSENSI (Ketik 'batal' untuk membatalkan)")

    # Input ID dengan validasi ulang
    id_update = input_id_valid("\nMasukkan ID absensi yang ingin diupdate: ", absensi_data)
    if id_update is None:
        print("❌ Proses dibatalkan oleh pengguna.")
        return

    # Cari record
    record = next((r for r in absensi_data if r['id'] == id_update), None)
    print(f"\nMengupdate data: {record['nama']} | Jam: {record['jam']} | Status: {record['keterangan'].upper()} | Tanggal: {record['tanggal']}")

    # Update status kehadiran terlebih dahulu
    print("\nPilih status kehadiran baru:")
    print("  1. Hadir / Telat")
    print("  2. Izin")
    print("  3. Sakit")
    print("  4. Pertahankan status saat ini")

    while True:
        pilih_status = input("Pilihan (1-4): ").strip()
        if pilih_status in ['1', '2', '3', '4', '']:
            break
        print("❌ Pilihan tidak valid! Masukkan 1-4.")

    if pilih_status in ['1', '2', '3']:
        status_baru = {'1': 'otomatis', '2': 'izin', '3': 'sakit'}[pilih_status]

        if status_baru == "otomatis":
            # Untuk hadir/telat, minta input jam dan tentukan status akhir
            jam_baru = input_jam_absen()
            if jam_baru is not None:
                record['jam'] = jam_baru
                record['keterangan'] = tentukan_status_otomatis(jam_baru)
                print(f"ℹ️  Status diupdate menjadi: {record['keterangan'].upper()} (berdasarkan jam {jam_baru})")
        else:
            # Untuk sakit/izin, reset jam ke "-"
            record['keterangan'] = status_baru
            record['jam'] = "-"
            print(f"✅ Status diupdate menjadi: {status_baru.upper()} (jam diisi '-')")
    # Jika pilih 4 atau Enter, pertahankan status saat ini

    # Update tanggal (opsional)
    tgl_baru = input(f"\nTanggal baru (Enter untuk pertahankan '{record['tanggal']}'): ").strip()
    if tgl_baru:
        tgl_valid = validasi_tanggal(tgl_baru)
        while tgl_baru and not tgl_valid:
            print("❌ Format tanggal tidak valid!")
            tgl_baru = input(f"Tanggal baru (Enter untuk skip): ").strip()
            if tgl_baru == '':
                break
            tgl_valid = validasi_tanggal(tgl_baru)
        if tgl_valid:
            record['tanggal'] = tgl_valid
            print(f"ℹ️  Tanggal diupdate menjadi: {tgl_valid}")

    print("\n✅ Data berhasil diupdate!")

def delete_absensi():
    tampilkan_header()
    if not absensi_data:
        print("\nℹ️  Tidak ada data untuk dihapus.")
        return

    read_absensi()                  # melihat ID absensi yang tersedia
    print("\n[+] HAPUS ABSENSI (Ketik 'batal' untuk membatalkan)")

    # Input ID dengan validasi ulang
    id_hapus = input_id_valid("\nMasukkan ID absensi yang ingin dihapus: ", absensi_data)
    if id_hapus is None:
        print("❌ Proses dibatalkan oleh pengguna.")
        return

    # Cari dan hapus record
    for i, r in enumerate(absensi_data):
        if r['id'] == id_hapus:
            nama_hapus = r['nama']
            del absensi_data[i]
            break

    # Reset ID agar sequential
    for i, record in enumerate(absensi_data, 1):
        record['id'] = i

    print(f"✅ Absensi {nama_hapus} (ID: {id_hapus}) berhasil dihapus!")

# ================== MAIN PROGRAM DENGAN VALIDASI MENU ==================
def main():
    while True:
        tampilkan_header()
        print("\n[ MENU UTAMA ]")
        print("  1. Tambah Karyawan Baru")
        print("  2. Tambah Absensi")
        print("  3. Lihat Data Absensi")
        print("  4. Update Absensi")
        print("  5. Hapus Absensi")
        print("  6. Keluar")

        pilih = input("\nPilihan Anda (1-6): ").strip()

        if pilih == '1':
            tambah_karyawan()
        elif pilih == '2':
            create_absensi()
        elif pilih == '3':
            read_absensi()
        elif pilih == '4':
            update_absensi()
        elif pilih == '5':
            delete_absensi()
        elif pilih == '6':
            print("\n" + "="*65)
            print("   Terima kasih telah menggunakan Sistem Absensi Karyawan!")
            print("="*65)
            break
        else:
            print("\n❌ Pilihan tidak valid! Harap masukkan angka 1-6.")
            continue

        input("\n❚ Tekan Enter untuk kembali ke menu...")

# ================== JALANKAN PROGRAM ==================
if __name__ == "__main__":
    main()
