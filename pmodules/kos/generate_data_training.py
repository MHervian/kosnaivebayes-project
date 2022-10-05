# Modul untuk menghitung dan generate data training kos
def generate_training(data_kos, conn):
  data_training = {}

  csr = conn.cursor()
  query = """SELECT 
            kelompok.kel_atribut AS kel_atribut,
            kelompok.nama_kelompok AS nama_kelompok,
            kelompok.status_interval AS status_interval,
            atribut_kos.id_atribut AS id_atribut,
            atribut_kos.nilai_atribut AS nilai_atribut,
            atribut_kos.min_range AS min_range,
            atribut_kos.max_range AS max_range 
            FROM kelompok INNER JOIN atribut_kos
              ON kelompok.kel_atribut = atribut_kos.kelompok_atribut"""
  csr.execute(query)
  atribut = csr.fetchall()
  csr.close()

  for k in data_kos.keys():
    attr_name = k
    attr_val = data_kos[k]

    # Melakukan filtering data atribut
    filter = []
    for atr in atribut:
      if atr[1] == attr_name:
        filter.append(atr)

    # Cek apakah atribut ini jenis data range atau bukan
    jenis = filter[0][2]
    if jenis == "ya":
      for fl in filter:
        if attr_val >= fl[5] and attr_val < fl[6]:
          data_training[k] = fl[4]
          break
    else:
      for fl in filter:
        if attr_val == fl[4]:
          data_training[k] = fl[4]
          break

  # Menghasilkan data training
  return data_training