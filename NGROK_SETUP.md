# Remote Access Setup dengan Ngrok

Panduan ini menjelaskan cara mengakses Streamlit dashboard dari komputer lain menggunakan ngrok.

## Apa itu Ngrok?

Ngrok adalah tool yang membuat tunnel dari internet ke localhost, memungkinkan Anda mengakses aplikasi lokal dari mana saja.

## Setup Ngrok

### 1. Install Ngrok (sudah termasuk di setup_alpine.sh)

Manual install jika belum:
```bash
# Linux x86_64
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
sudo tar xvzf ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin
rm ngrok-v3-stable-linux-amd64.tgz

# Linux ARM64
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz
sudo tar xvzf ngrok-v3-stable-linux-arm64.tgz -C /usr/local/bin
rm ngrok-v3-stable-linux-arm64.tgz
```

### 2. Sign Up dan Dapatkan Authtoken

1. Kunjungi: https://ngrok.com/signup
2. Buat akun gratis (bisa pakai Google/GitHub)
3. Setelah login, copy authtoken dari dashboard
4. Authenticate ngrok:
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
   ```

### 3. Jalankan Aplikasi

**Terminal 1** - Jalankan Streamlit:
```bash
# Activate virtual environment
source venv/bin/activate

# Run Streamlit
streamlit run app.py
```

**Terminal 2** - Jalankan Ngrok:
```bash
ngrok http 8501
```

### 4. Akses dari Komputer Lain

Setelah ngrok berjalan, Anda akan melihat output seperti:
```
ngrok                                                                           

Session Status                online
Account                       your_account (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://xxxx-xx-xx-xxx-xxx.ngrok-free.app -> http://localhost:8501

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy URL** yang ada di baris `Forwarding` (contoh: `https://xxxx-xx-xx-xxx-xxx.ngrok-free.app`)

Buka URL tersebut di browser komputer lain, dan Anda bisa mengakses Streamlit dashboard!

## Ngrok Free Tier Limitations

- Session timeout setelah 2 jam (perlu restart ngrok)
- Random URL setiap kali restart
- Limit koneksi per menit
- Banner "Visit Site" di halaman pertama

## Alternative: Ngrok Background Mode

Untuk menjalankan ngrok di background:
```bash
nohup ngrok http 8501 > ngrok.log 2>&1 &
```

Lihat URL:
```bash
curl http://localhost:4040/api/tunnels | grep public_url
```

Stop ngrok:
```bash
pkill ngrok
```

## Tips

1. **Save URL**: Free tier memberikan random URL, save URL untuk sesi Anda
2. **Security**: Jangan share URL ke public jika ada data sensitif
3. **Performance**: Ngrok menambah latency, normal untuk akses remote
4. **Monitoring**: Akses `http://localhost:4040` untuk monitoring traffic ngrok

## Troubleshooting

**Error: "command not found: ngrok"**
- Jalankan `setup_alpine.sh` lagi atau install manual

**Error: "ERR_NGROK_108"**
- Perlu authenticate dulu: `ngrok config add-authtoken YOUR_TOKEN`

**URL tidak bisa diakses**
- Pastikan Streamlit berjalan di port 8501
- Check firewall tidak block ngrok
- Coba restart ngrok

**Slow performance**
- Normal untuk free tier
- Coba ganti region: `ngrok http 8501 --region=ap` (Asia Pacific)

## Alternative Tanpa Ngrok

Jika di jaringan yang sama (LAN):
```bash
# Jalankan Streamlit accessible dari network
streamlit run app.py --server.address=0.0.0.0 --server.port=8501

# Akses dari komputer lain di LAN yang sama:
http://IP_ADDRESS_SERVER:8501
```

Untuk mendapatkan IP address server:
```bash
ip addr show | grep "inet "
# atau
hostname -I
```
