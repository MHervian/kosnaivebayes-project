# -----------------------------------------------------------------------------------
# File ini adalah program utama dari Naive Bayes
# 
# (C) 2021, Sleman, Yogyakarta
# -----------------------------------------------------------------------------------
import string
from unittest import result
from flask import Flask, render_template, redirect, request, session
from flask.helpers import url_for
from flask_session import Session
from pmodules.mysqlconn.connection import mysql_conn
from pmodules.kos.generate_data_training import generate_training
# from pmodules.naive_bayes.metode import generate_recomendation
import json

# Buat Flask Application
app = Flask(__name__)
app.secret_key = "belajarkosnaivebayes!!!"

# --------------------------
# Routes untuk bagian Admin
# --------------------------
# ========= LOGIN SYSTEM ==================
# Halaman login (Sebagai halaman login Admin)
@app.route("/admin")
def login_admin():
  if "username" in session:
    return redirect(url_for("dashboard"))

  msg = request.args.get("msg")
  
  return render_template("admin/index.html", message = msg)

# Proses login
@app.route("/admin/login", methods=["POST"])
def proses_login():
  # Baca data login
  username = request.form["username"]
  password = request.form["password"]

  conn = mysql_conn()

  csr = conn.cursor()
  query = f"SELECT * FROM pengguna WHERE username = '{username}' AND pass = '{password}'"
  csr.execute(query)
  result = csr.fetchall()
  csr.close()
  conn.close()
  
  if len(result) == 1:
    session["username"] = username
    return redirect(url_for("dashboard"))
  else:
    pesan = "login failed"
    return redirect(url_for("login_admin", msg = pesan))

# Logout
@app.route("/admin/logout")
def proses_logout():
  session.pop("username", None)
  pesan = "user logout"
  return redirect(url_for("login_admin", msg = pesan))
# ============ / END LOGIN SYSTEM =================

# ============ DASHBOARD ========================
# Halaman dashboard sebagai halaman utama admin
@app.route("/admin/dashboard")
def dashboard():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  conn = mysql_conn()
  csr = conn.cursor()
  # Kueri data kos
  query = "SELECT * FROM kos LIMIT 5"
  csr.execute(query)
  kos = csr.fetchall()

  # Kueri data atribut
  query = "SELECT * FROM kelompok"
  csr.execute(query)
  atribut = csr.fetchall()

  # Kueri data training
  query = """SELECT 
              kos.id_kos AS id_kos,
              kos.nama AS nama,
              data_training.label_jarak AS jarak,
              data_training.label_luas AS luas,
              data_training.label_fasilitas AS fasilitas,
              data_training.label_area AS area,
              data_training.label_harga AS harga 
            FROM data_training 
            INNER JOIN kos ON kos.id_kos = data_training.id_kos LIMIT 5"""
  csr.execute(query)
  training = csr.fetchall()
  
  current_user = session["username"]
  return render_template(
                      "admin/dashboard.html",
                      user=current_user,
                      kos=kos,
                      atribut=atribut,
                      training=training)
# ============ / DASHBOARD =========================

# ============ KOS ==============================
# Halaman data kos
@app.route("/admin/kos")
def kos():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))

  msg = ""
  if request.args.get("msg") != "":
    msg = request.args.get("msg")
  
  conn = mysql_conn()
  csr = conn.cursor()
  query = "SELECT * FROM kos"
  csr.execute(query)
  result = csr.fetchall()
  csr.close()
  conn.close()

  return render_template("admin/kos.html", list_kos=result, message = msg)

# Halaman form input kos
@app.route("/admin/kos/input")
def input_kos():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  return render_template("admin/forms/kos/input_kos.html")

# Proses menyimpan data kos dan membuat data training
@app.route("/admin/kos/create", methods=["POST"])
def create_kos_process():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))

  # Membaca data kos yang diinput
  nama_kos = request.form["nama_kos"]
  jarak = int(request.form["jarak"])
  panjang = float(request.form["panjang"])
  lebar = float(request.form["lebar"])
  fasilitas = request.form["fasilitas"]
  area = request.form["area"]
  harga = int(request.form["harga"])
  rating = float(request.form["rating"])
  alamat = request.form["alamat"]
  kontak = request.form["kontak"]
  
  ukuran = panjang * lebar
  fas_arr = fasilitas.split(",")
  area_arr = area.split(",")

  # Hitung jumlah data fasilitas
  if len(fas_arr) > 5:
    fas_count = 5
  else:
    fas_count = len(fas_arr)

  # Hitung jumlah data area
  if len(area_arr) > 10:
    area_count = 10
  else:
    area_count = len(area_arr)
  
  data_kos = {
    "jarak": jarak,
    "ukuran": ukuran,
    "fasilitas": fas_count,
    "area": area_count,
    "harga": harga
  }

  conn = mysql_conn()

  # Melakukan eksekusi simpan data kos di basis data
  csr = conn.cursor()
  query = f"""INSERT INTO 
              kos(jarak, panjang, lebar, fasilitas, area, harga, alamat, kontak, nama, rating) 
             VALUES
              ({jarak}, {panjang}, {lebar}, '{fasilitas}', '{area}', {harga}, '{alamat}', '{kontak}', '{nama_kos}', '{rating}')"""
  csr.execute(query)
  conn.commit()
  id_kos = csr.lastrowid

  # Membangun nilai atribut data training pada data kos
  data_training = generate_training(data_kos, conn)
  jarak = data_training["jarak"]
  ukuran = data_training["ukuran"]
  fasilitas = data_training["fasilitas"]
  area = data_training["area"]
  harga = data_training["harga"]

  # Melakukan eksekusi simpan data training
  query = f"""INSERT INTO 
              data_training(id_kos, label_jarak, label_luas, label_fasilitas, label_area, label_harga) 
             VALUES({id_kos}, {jarak}, {ukuran}, {fasilitas}, {area}, {harga})"""
  csr.execute(query)
  conn.commit()

  csr.close()
  conn.close()

  pesan = "kos created"
  return redirect(url_for("kos", msg = pesan))

@app.route("/admin/kos/detail", methods=["GET"])
def detail_kos():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("kos", msg = pesan))
  
  id_kos = request.args.get("id")

  conn = mysql_conn()
  csr = conn.cursor()
  query = f"""SELECT 
                kos.id_kos AS id_kos, kos.jarak AS jarak, kos.panjang AS panjang,
                kos.lebar AS lebar, kos.fasilitas AS fasilitas, kos.area AS area,
                kos.harga AS harga, kos.alamat AS alamat, kos.kontak AS kontak,
                kos.nama AS nama, kos.rating AS rating, data_training.id_label AS id_label, data_training.label_jarak AS lj,
                data_training.label_luas AS ll, data_training.label_fasilitas AS lf, data_training.label_area AS la,
                data_training.label_harga AS lh
              FROM kos INNER JOIN data_training ON data_training.id_kos = kos.id_kos 
              WHERE kos.id_kos = {id_kos}
                """
  csr.execute(query)
  result = csr.fetchone()
  data = {
    "id_kos": result[0],
    "jarak": result[1],
    "panjang": result[2],
    "lebar": result[3],
    "fasilitas": result[4],
    "area": result[5],
    "harga": result[6],
    "alamat": result[7],
    "kontak": result[8],
    "nama": result[9],
    "rating": result[10],
    "id_label": result[11],
    "l_jarak": result[12],
    "l_luas": result[13],
    "l_fasilitas": result[14],
    "l_area": result[15],
    "l_harga": result[16]
  }

  return render_template("admin/detail_kos.html", kos=data)

# Halaman form edit data kos
@app.route("/admin/kos/edit", methods=["GET"])
def edit_kos():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  id_kos = request.args.get("id")

  conn = mysql_conn()
  csr = conn.cursor()
  query = f"SELECT * FROM kos WHERE id_kos = {id_kos}"
  csr.execute(query)
  result = csr.fetchone()

  return render_template("admin/forms/kos/edit_kos.html", kos=result)

# Update data kos
@app.route("/admin/kos/update", methods=["POST"])
def update_kos_process():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  # Membaca data kos yang diinput
  id_kos = request.form["id_kos"]
  nama_kos = request.form["nama_kos"]
  jarak = int(request.form["jarak"])
  panjang = float(request.form["panjang"])
  lebar = float(request.form["lebar"])
  fasilitas = request.form["fasilitas"]
  area = request.form["area"]
  harga = int(request.form["harga"])
  rating = float(request.form["rating"])
  alamat = request.form["alamat"]
  kontak = request.form["kontak"]
  
  ukuran = panjang * lebar
  fas_arr = fasilitas.split(",")
  area_arr = area.split(",")

  # Hitung jumlah data fasilitas
  if len(fas_arr) > 5:
    fas_count = 5
  else:
    fas_count = len(fas_arr)

  # Hitung jumlah data area
  if len(area_arr) > 10:
    area_count = 10
  else:
    area_count = len(area_arr)
  
  data_kos = {
    "jarak": jarak,
    "ukuran": ukuran,
    "fasilitas": fas_count,
    "area": area_count,
    "harga": harga
  }

  conn = mysql_conn()

  # Melakukan eksekusi update data kos di basis data
  csr = conn.cursor()
  query = f"""UPDATE kos SET
              jarak = {jarak}, panjang = {panjang}, lebar = {lebar}, fasilitas = '{fasilitas}', 
              area = '{area}', harga = {harga}, alamat = '{alamat}', kontak = '{kontak}', nama = '{nama_kos}', rating = '{rating}' 
              WHERE id_kos = {id_kos}"""
  csr.execute(query)
  conn.commit()

  # Membangun nilai atribut data training pada data kos
  data_training = generate_training(data_kos, conn)
  jarak = data_training["jarak"]
  ukuran = data_training["ukuran"]
  fasilitas = data_training["fasilitas"]
  area = data_training["area"]
  harga = data_training["harga"]

  # Melakukan eksekusi simpan data training
  query = f"""UPDATE data_training SET 
            label_jarak = {jarak}, label_luas = {ukuran}, label_fasilitas = {fasilitas}, label_area = {area}, label_harga = {harga} 
            WHERE id_kos = {id_kos}"""
  csr.execute(query)
  conn.commit()

  csr.close()
  conn.close()
  
  pesan = "kos updated"
  return redirect(url_for("kos", msg = pesan))

@app.route("/admin/kos/delete")
def delete_kos_process():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  id_kos = request.args.get("id")

  conn = mysql_conn()
  csr = conn.cursor()
  # Hapus data training 
  query = f"DELETE FROM data_training WHERE id_kos = {id_kos}"
  csr.execute(query)
  conn.commit()

  # Hapus data kos
  query = f"DELETE FROM kos WHERE id_kos = {id_kos}"
  csr.execute(query)
  conn.commit()

  csr.close()
  conn.close()

  pesan = "kos deleted"
  return redirect(url_for("kos", msg = pesan))
# ============ / KOS ==============================

# ============ ATRIBUT ============================
@app.route("/admin/atribut")
def atribut():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  conn = mysql_conn()
  csr = conn.cursor()
  query = "SELECT * FROM kelompok"
  csr.execute(query)
  result = csr.fetchall()
  csr.close()
  conn.close()

  return render_template("admin/atribut.html", kelompok=result)

@app.route("/admin/atribut/detail")
def detail_atribut():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  id_kelompok = request.args.get("id")
  
  conn = mysql_conn()
  csr = conn.cursor()
  query = f"SELECT * FROM atribut_kos WHERE kelompok_atribut = {id_kelompok} ORDER BY nilai_atribut ASC"
  csr.execute(query)
  result = csr.fetchall()
  query = f"SELECT nama_kelompok, deskripsi FROM kelompok WHERE kel_atribut = {id_kelompok}"
  csr.execute(query)
  detail = csr.fetchall()
  csr.close()
  conn.close()

  return render_template("admin/detail_atribut.html", data=result, detail=detail)
# ============ / ATRIBUT ==========================

# ============= DATA TRAINING =======================
@app.route("/admin/data-training")
def data_training():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  conn = mysql_conn()
  csr = conn.cursor()
  query = """SELECT 
              kos.id_kos AS id_kos,
              kos.nama AS nama,
              data_training.label_jarak AS jarak,
              data_training.label_luas AS luas,
              data_training.label_fasilitas AS fasilitas,
              data_training.label_area AS area,
              data_training.label_harga AS harga 
            FROM data_training 
            INNER JOIN kos ON kos.id_kos = data_training.id_kos"""
  csr.execute(query)
  result = csr.fetchall()
  total = len(result)
  csr.close()
  conn.close()
  
  return render_template("admin/training.html", training=result, total=total)
# =========== / DATA TRAINING =======================

# ============ ADMIN CMS ======================
# Halaman data admin CMS
@app.route("/admin/pengguna")
def pengguna():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))

  msg = ""
  if request.args.get("msg") != "":
    msg = request.args.get("msg")

  # Kueri data admin pengguna aplikasi
  conn = mysql_conn()

  csr = conn.cursor()
  query = "SELECT * FROM pengguna"
  csr.execute(query)
  result = csr.fetchall()
  csr.close()
  conn.close()
  
  return render_template("admin/admin.html", admins=result, message = msg)

# Halaman form input data admin baru
@app.route("/admin/pengguna/input")
def input_admin():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  return render_template("admin/forms/admin/input_admin.html")

# Proses create admin baru
@app.route("/admin/pengguna/create", methods=["POST"])
def create_admin_process():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))

  # Baca data kos dari form input
  username = request.form["username"]
  password = request.form["password"]
  
  conn = mysql_conn()
  csr = conn.cursor()
  query = f"INSERT INTO pengguna(username, pass) VALUES ('{username}','{password}')"
  csr.execute(query)
  conn.commit()
  csr.close()
  conn.close()

  pesan = "admin created"
  return redirect(url_for("pengguna", msg = pesan))

# Halaman form edit data admin
@app.route("/admin/pengguna/edit", methods=["GET"])
def edit_admin():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  id_user = request.args.get("id")
  
  conn = mysql_conn()
  csr = conn.cursor()
  query = f"SELECT * FROM pengguna WHERE id_user={id_user}"
  csr.execute(query)
  result = csr.fetchone()
  csr.close()
  conn.close()
  
  return render_template("admin/forms/admin/edit_admin.html", admin=result)

# Proses update data admin
@app.route("/admin/pengguna/update", methods=["POST"])
def update_admin_process():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  id_user = request.form["id_user"]
  username = request.form["username"]
  password = request.form["password"]

  conn = mysql_conn()
  csr = conn.cursor()
  query = f"UPDATE pengguna SET username = '{username}', pass = '{password}' WHERE id_user = {id_user}"
  csr.execute(query)
  conn.commit()
  csr.close()
  conn.close()

  pesan = "admin updated"
  return redirect(url_for("pengguna", msg = pesan))

@app.route("/admin/pengguna/delete", methods=["GET"])
def delete_admin_process():
  if "username" not in session:
    pesan = "user not login"
    return redirect(url_for("login_admin", msg = pesan))
  
  id_user = request.args.get("id")
  conn = mysql_conn()
  csr = conn.cursor()
  query = f"DELETE FROM pengguna WHERE id_user = {id_user}"
  csr.execute(query)
  conn.commit()
  csr.close()
  conn.close()

  pesan = "admin deleted"
  return redirect(url_for("pengguna", msg = pesan))
# ============ / ADMIN CMS ====================

# --------------------------
# Routes untuk bagian End-User atau pengguna aplikasi
# --------------------------
# ============ HOMEPAGE =======================
@app.route("/")
def homepage():
  return render_template("enduser/index.html")
# ============ / HOMEPAGE =======================

# ============ LIST KOS =======================
@app.route("/kos")
def list_kos():
  conn = mysql_conn()
  csr = conn.cursor()
  query = "SELECT * FROM kos"
  csr.execute(query)
  result = csr.fetchall()

  return render_template("enduser/kos.html", kos = result)

@app.route("/kos/detail")
def detail_kos_enduser():
  id_kos = request.args.get("id")

  conn = mysql_conn()
  csr = conn.cursor()
  query = f"SELECT * FROM kos WHERE id_kos = {id_kos}"
  csr.execute(query)
  result = csr.fetchall()
  
  return render_template("enduser/detail_kos.html", kos = result)
# ============ / LIST KOS =====================

# ============ FORM PILIHAN =======================
@app.route("/form")
def form_pengisian():
  return render_template("enduser/form.html")
# ========== / FORM PILIHAN =======================

# ============ REKOMENDASI ========================
@app.route("/hasil-rekomendasi", methods=["POST"])
def hasil_rekomendasi():
  # Bagian ini untuk deskripsi hasil pilihan dari halaman form
  atr_perjalanan = ["3 - 4 Menit", "5 - 7 Menit", "8 - 10 Menit", "11 - 15 Menit"]
  atr_ukuran = ["6 - 9 Meter Persegi", "10 - 15 Meter Persegi", "16 - 24 Meter Persegi", "25 - 40 Meter Persegi"]
  atr_fasilitas = ["1", "2", "3", "4", "5"]
  atr_area = ["1", "2", "3", "4", "5"]
  atr_harga = ["Rp300.000 - Rp400.000", "Rp410.000 - Rp500.000", "Rp510.000 - Rp600.000", "Rp610.000 - Rp750.000"]

  # 1. Membaca data dari form
  # kelompok = request.form.getlist("kelompok[]")
  jarak = request.form.get("jarak")
  ukuran = request.form.get("ukuran")
  fasilitas = request.form.get("fasilitas")
  area = request.form.get("area")
  harga = request.form.get("harga")

  # arr_atr = ["jarak", "ukuran", "fasilitas", "area", "harga"]
  arr_atr_uji = [jarak, ukuran, fasilitas, area, harga]
  print(arr_atr_uji)

  # 2. Kueri data training dari basis data
  conn = mysql_conn()
  csr = conn.cursor()
  query = f"SELECT * FROM data_training"
  csr.execute(query)
  data_training = csr.fetchall()
  csr.close()
  conn.close()

  # 3. Menghitung nilai Y dari masing2 data training
  nilai_Y = []
  jmlh_data = len(data_training)
  for x in range(jmlh_data):
    nilai_Y.append(round(1 / jmlh_data, 2))

  # 4. Melakukan pencocokan nilai atribut antar data uji
  # dgn data training dan menghitung nilai HMAP masing - masing 
  # data training
  result_HMAP = []
  x = 0
  for training in data_training:
    total_kesamaan = 0
    nilai_HMAP = 0.0
    nilai_X = 0
    kesamaan_atribut = []
    y = 0
    warna = ""

    # Melakukan proses pemisahan dari data training untuk diambil
    # nilai atributnya
    tmp_training = [training[d] for d in range(2,7)]

    # Melakukan pengecekan kecocokan masing - masing atribut
    # uji
    for atribut in tmp_training:
      atribut = int(atribut)
      uji = int(arr_atr_uji[y])
      if uji == atribut:
        kesamaan_atribut.append(1)
        nilai_X *= 1
        total_kesamaan += 1
      else:
        kesamaan_atribut.append(0)
        nilai_X *= 0
      y += 1

    # Menghitung nilai HMAP
    nilai_HMAP = nilai_Y[x] * nilai_X

    # Menentukan kesimpulan dengan warna pada data training
    if total_kesamaan <= 1:
      warna = "style=background-color:#ff8080;"
    elif total_kesamaan == 2:
      warna = "style=background-color:#ffa31a;"
    elif total_kesamaan == 3:
      warna = "style=background-color:#ffe680;"
    elif total_kesamaan == 4:
      warna = "style=background-color:#b3ff66;"
    elif total_kesamaan == 5:
      warna = "style=background-color:#79d279;"
    else:
      warna = "style=background-color:transparent;"

    # Gabungkan semuanya: nilai_y, nilai_atribut, nilai_HMAP, total_kesamaan
    result_HMAP.append([training[1]] + [nilai_Y[x]] + kesamaan_atribut + [nilai_HMAP] + [total_kesamaan] + [warna])
    print("Total Kesamaan: " + str(total_kesamaan))
    print(result_HMAP[x])
    x += 1
  
  # 5. Melakukan pengurutan data training berdasarkan kesamaan atribut terbanyak 
  # ke terkurang secara DESCENDING
  def myFunc(e):
    return e[8]

  result_HMAP.sort(reverse=True, key=myFunc)
  # print(result_HMAP)

  # 6. Kueri data kos dari basis data
  conn = mysql_conn()
  csr = conn.cursor()
  query = f"SELECT * FROM kos"
  csr.execute(query)
  kos = csr.fetchall()
  csr.close()
  conn.close()

  # 7. Mulai membuat data hasil rekomendasi
  rekomendasi = []
  x = 0
  for training in result_HMAP:
    id_kos = int(training[0])
    for k in kos:
      id = int(k[0])
      if id_kos == id:
        rekomendasi.append(list(k) + [training[9]])

  dt_jarak = list(["Kurang dari 7 menit", "Lebih dari sama 7 menit"])
  dt_ukuran = list(["Kurang dari 16 meter persegi", "Lebih dari sama 16 meter persegi"])
  dt_area = list(["Kurang dari 4 tempat umum", "Lebih dari sama 4 tempat umum"])
  dt_harga = list(["Kurang dari Rp.500.000/bln", "Lebih dari sama Rp.500.000/bln"])

  new_form = []
  new_form.append(dt_jarak[int(jarak) - 1])
  new_form.append(dt_ukuran[int(ukuran) - 1])
  new_form.append(int(fasilitas))
  new_form.append(dt_area[int(area) - 1])
  new_form.append(dt_harga[int(harga) - 1])

  # print(rekomendasi)

  dt = []
  dt.append(new_form)
  dt.append(rekomendasi)

  # print("Hasil")
  # print(dt)

  kelompok_jarak = request.form.get("kelompok_jarak")
  kelompok_ukuran = request.form.get("kelompok_ukuran")
  kelompok_fasilitas = request.form.get("kelompok_fasilitas")
  kelompok_area = request.form.get("kelompok_area")
  kelompok_harga = request.form.get("kelompok_harga")

  p = [
    atr_perjalanan[int(kelompok_jarak) - 1],
    atr_ukuran[int(kelompok_ukuran) - 1],
    atr_fasilitas[int(kelompok_fasilitas) - 1],
    atr_area[int(kelompok_area) - 1],
    atr_harga[int(kelompok_harga) - 1]
  ]

  return render_template("enduser/rekomendasi.html", data=dt, pilihan=p)

# ============= / REKOMENDASI =====================

# Jalankan aplikasi
if __name__ == "__main__":
  app.run()