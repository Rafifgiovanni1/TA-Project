# Menginstall website

## Instalasi
Sebelum melakukan instalasi pastikan python sudah terinstall dengan versi 3.8 keatas.
Instalasi python dapat dicek menggunakan command berikut:

```bash
python -V
```

contoh output jika python terinstall:
```bash
Python 3.8.10
```

Jika sudah benar maka jalankan program berikut untuk menginstall pipenv:

```bash
pip install pipenv
# atau
pip3 install pipenv
```
*Note: gunakan salah satu command*

Jika pipenv sudah terinstall dengan benar kita lanjut menginstall library untuk website
```bash
pipenv install
```
Setelah instalasi selesai, coba verifikasi versi flask yang terinstall dengan menggunakan command:

```bash
pipenv run flask --version
```
Jika sudah terinstall output nya:
```bash
Python 3.8.10
Flask 2.3.2
Werkzeug 2.3.6
```

## Migrasi database

Buat file `.env` di root folder(di tempat yang sama dengan `wsgi.py`) dan isi file dengan format berikut:
```python
SECRET_KEY = "tjkgd\f<dsojjfsdpdsfldsfsdfds"
ENV  = "development"
DEBUG = "true"
DBASE_NAME = "" #nama database
DBASE_PASSWORD = "" #password database,abaikan jika tidak ada password
DBASE_USERNAME = "" # username database
```

Lalu jalankan command berikut:
```bash
pipenv run migrate

pipenv run upgrade
```

Jika terjadi error seperti `Target database is not up to date.`, coba jalankan command berikut:

```bash
pipenv run_stamp
```

Jika migrasi sudah benar maka website bisa dijalankan menggunakan command:
```bash
pipenv run server
```

Server website berhasil dijalankan jika memiliki output berikut:
```bash
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 439-689-393
```

Lalu buka http://127.0.0.1:8000 di browser

# Menggunakan website

## Membuat akun admin

Sebelum menggunakan website maka akun admin harus dibuat terlebih dahulu.
Akun admin dapat dibuat menggunakan command:

```bash
pipenv run create_admin
```

Kemudian isi data untuk akun admin seperti username,password dan email. Setelah sukses dibuat kita bisa langsung login dengan akun admin

## Halaman admin

Untuk login masukan username dan password sesuai dengan akun yang dibuat.

!["Halaman admin"]({{url_for('static',filename='image/admin_page.png')}})

Halaman utama admin terdapat sebuah form yang berfungsi untuk mengganti data akun seperti password dan email.

## Halaman murid

Klik link murid di sidebar maka akan berpindah ke halaman murid, halaman yang menampilkan data semua murid.

!["Halaman murid"]({{url_for('static',filename='image/student_page.png')}})

Detail murid dapat dilihat jika link kolom nik di klik, dihalaman tesebut admin dapat mengedit data murid ataupun menghapus data murid.

Untuk menambah murid, klik tombol **"Tambah murid baru"**, maka akan dialihkan ke halaman dengan input file.

!["Halaman tambah murid"]({{url_for('static',filename='image/student_add_page.png')}})

Aturan file yang akan di input:

1. Nama file boleh bebas selama berbentuk excel
2. Jika file excel memiliki lebih dari satu sheet maka semua sheet akan digabung menjadi satu
3. Contoh tabel excel yang benar untuk input adalah sebagai berikut:
!["Contoh template"]({{url_for('static',filename='image/student_template.png')}})
*Note: seluruh kolom di gambar wajib ada di file excel*

File excel harus murni tabel tidak boleh ada kop surat pada file, jika ada kolom tambahan maka akan di abaikan oleh program.
Jika data sukses ditambahkan maka data murid akan di input dan otomatis membuat akun untuk murid tersebut. Semua akun murid akan memiliki username nik mereka masing masing dengan password: "password".

## Halaman nilai tugas dan ulangan

Di halaman ini admin bisa melihat dan menginput data nilai dan tugas murid. Secara default nilai dari kelas 1 semester yang ditampilkan tapi admin juga bisa memfilter nilai sesuai kelas, semester dan mata pelajaran.

!["Halaman nilai tugas dan ulangan"]({{url_for('static',filename='image/student_score.png')}})

Di halman tambah nilai murid, terdapat input file yang digunakan untuk menginput file nilai.

!["Halaman tambah nilai tugas dan ulangan"]({{url_for('static',filename='image/student_score_add.png')}})

Input file tersebut memiliki beberapa aturan:

1. File harus memiliki nama yang beformat seperti: nilai_kelas_\[1-6]\(a|b)_(semester1|semester2).xlsx, contoh yang nama file yang benar: nilai_kelas_1a_semester1.xlsx,nilai_kelas_5a_semester2.xlsx, selain format itu file akan ditolak oleh program
2. Masing masing nilai dari mata pelajaran ataupun nilai sikap harus memiliki sheet nya di file excel ini, jika kurang maka akan program akan error
3. Dalam satu sheet mata pelajaran haru ada kolom berikut:
	- nik
	- nama
	- tugas1 - 4(tidak boleh pakai spasi)
	- ujian1 dan ujian2
	untuk nilai sikap sheet nya harus diberi nama: "NILAI SIKAP" dan harus memiliki kolom:
		- nama
		- nik
		- displin
		- percayadiri(tidak boleh spasi)
  Jika tedapat kolom lain selain yang disebutkan maka akan diabaikan oleh program.
4. Contoh format file excel:
	!["Contoh format nilai"]({{url_for('static',filename='image/student_score_template.png')}})

	!["Contoh format nilai"]({{url_for('static',filename='image/student_score_template_attitude.png')}})
5. Jika ada nilai yang di update maka harus di edit terlebih dahulu di excel baru lakukan update ulang file excel yang sama
6. Sama seperti file murid, file nilai tidak boleh ada atribut lain seperti kop surat harus murni tabel nilai


## Halaman absensi murid
Halaman yang menampilkan jumlah absen dari para murid. Secara default halaman ini akan menampilkan data dari kelas 1 semeste 1, tapi admin juga dapat memfilter data nya juga.
!["Halaman absensi murid"]({{url_for('static',filename='image/student_presention.png')}})

Klik tombol "Tambah absen murid" maka akan di alihkan ke halaman untuk menambahkan data absensi murid.
!["Halaman absensi murid"]({{url_for('static',filename='image/student_presention_add.png')}})

Input file tersebut memiliki beberapa aturan:

1. File harus memiliki nama yang beformat seperti: absensi_kelas_\[1-6]\(a|b)_(semester1|semester2).xlsx, contoh yang nama file yang benar: absensi_kelas_1a_semester1.xlsx,absensi_kelas_5a_semester2.xlsx, selain format itu file akan ditolak oleh program
2. Jika ada lebih dari satu sheet maka sheet berikutnya akan diabaikan oleh program(hanya sheet pertama yang akan dibaca)
3. File excel harus memiliki kolom: nik,nama,S,I,A, jika ada yang lebih maka akan diabaikan oleh program
4. Jika ada absen yang di update maka harus di ubah di excel sebelum melaukan update ulang file yang sama
5. File excel harus murni tabel tidak boleh ada atribut lain
6. Contoh format file:
	!["Template absensi murid"]({{url_for('static',filename='image/student_presention_template.png')}})

## Halaman nilai semester murid

Halaman yang berisi data nilai ulangan semester murid, admin juga dapat memfilter data sesuai kelas dan semester.
!["Halaman nilai semester murid"]({{url_for('static',filename='image/student_semester.png')}})

Klik tombol "Tambah nilai semester" maka akan di alihkan ke halaman untuk menambahkan data nilai ulangan semester murid.
!["Halaman tambah nilai semester murid"]({{url_for('static',filename='image/student_semester_add.png')}})

Input file nilai semester memiliki beberapa aturan sebagai berikut:

1. Nama file harus memiliki format sebagai berikut: nilaiSemester_kelas_\[1-6]\(a|b)_(semester1|semester2).xlsx, contoh nya: nilaiSemester_kelas_5a_semester1.xlsx atau nilaiSemester_kelas_6a_semester2.xlsx, selain itu file akan ditolak
2. File excel harus berisi nama,nik dan semua nilai mata pelajaran jika ada yang selain itu maka akan diabaikan oleh program(*Note: disini mata pelajaran agama wajib ditulis pag*)
3. Jika ada lebih dari satu sheet maka sheet berikutnya akan diabaikan oleh program(hanya membaca sheet pertama saja)
4. Jika ada nilai yang ingin di update maka ubah dahulu nilai di excel kemudian lakukan upload ulang file yang sama
5. Data file excel harus murni tabel dan tidak boleh ada atribut lain
6. Contoh format isi file excel nilai semester:
	!["Contoh format file excel nilai ulangan semester"]({{url_for('static',filename='image/student_semester_template.png')}})


