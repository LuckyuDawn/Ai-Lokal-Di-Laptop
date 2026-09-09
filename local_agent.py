import os
import sys
import subprocess
import time
import winreg
from datetime import datetime
import urllib.parse
from difflib import get_close_matches
import pyautogui
from PIL import Image

# Kode Warna Tema Hitam & Emas (ANSI Escape Codes)
EMAS = "\033[93m"
HITAM = "\033[30m"
ABU = "\033[90m"
PUTIH = "\033[97m"
RESET = "\033[0m"
BG_HITAM = "\033[40m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_time():
    return datetime.now().strftime("%H:%M:%S | %d-%m-%Y")

def banner():
    clear_screen()
    waktu_sekarang = get_current_time()
    print(f"{BG_HITAM}{EMAS}===================================================={RESET}")
    print(f"{BG_HITAM}{EMAS}          LOKAL AI - ULTIMATE TRADING AGENT         {RESET}")
    print(f"{BG_HITAM}{EMAS}===================================================={RESET}")
    print(f"{PUTIH} Status Waktu : {EMAS}{waktu_sekarang}{RESET}")
    print(f"{PUTIH} Mode Master: TV Active Screenshot & New Concise Prompt{RESET}")
    print(f"{BG_HITAM}{EMAS}----------------------------------------------------{RESET}\n")

def kunci_fokus_ai_lokal():
    """Melepaskan tombol nyangkut dan memaksa fokus ketikan kembali ke AI Lokal"""
    try:
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('alt')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('win')
    except Exception:
        pass
        
    time.sleep(0.2)
    ps_focus = "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.Interaction]::AppActivate('AI Lokal')"
    subprocess.Popen(["powershell", "-Command", ps_focus], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def salin_gambar_ke_clipboard(path_gambar):
    """Menyalin file gambar tangkapan layar ke clipboard Windows menggunakan PowerShell"""
    ps_copy = f"""
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::SetImage([System.Drawing.Image]::FromFile('{path_gambar}'))
    """
    subprocess.run(["powershell", "-Command", ps_copy], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def deteksi_platform_key(teks):
    p = teks.lower()
    if any(k in p for k in ["youtube", "yutub", "yt"]):
        return "youtube"
    elif any(k in p for k in ["instagram", "ig"]):
        return "instagram"
    elif any(k in p for k in ["fb", "facebook"]):
        return "facebook"
    elif any(k in p for k in ["gemini"]):
        return "gemini"
    elif any(k in p for k in ["whatsapp", "wa", "whatap"]):
        return "whatsapp"
    elif any(k in p for k in ["google"]):
        return "google"
    return None

def cari_software_100_persen(nama_app):
    lokasi_pencarian = [
        os.path.join(os.environ['USERPROFILE'], "Desktop"),
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
        os.path.join(os.environ['APPDATA'], r"Microsoft\Windows\Start Menu\Programs"),
        os.path.join(os.environ['LOCALAPPDATA'], r"Programs"),
        r"C:\Program Files",
        r"C:\Program Files (x86)"
    ]
    
    daftar_exe = {}
    for direktori in lokasi_pencarian:
        if not os.path.exists(direktori):
            continue
        for root, dirs, files in os.walk(direktori):
            for file in files:
                if file.lower().endswith(('.exe', '.lnk', '.url', '.msc', '.bat')):
                    nama_file = file.lower()
                    if "streaming" in nama_file or "client" in nama_file:
                        continue
                    nama_bersih = os.path.splitext(file)[0].lower()
                    path_lengkap = os.path.join(root, file)
                    daftar_exe[nama_bersih] = path_lengkap

    keys = list(daftar_exe.keys())
    cocok = get_close_matches(nama_app.lower(), keys, n=1, cutoff=0.25)
    if cocok:
        return daftar_exe[cocok[0]]
    return None

def cari_tradingview_mendalam():
    kemungkinan_path = [
        os.path.expanduser(r"~\AppData\Local\Programs\TradingView\TradingView.exe"),
        r"C:\Program Files\TradingView\TradingView.exe",
        r"C:\Program Files (x86)\TradingView\TradingView.exe",
        os.path.expanduser(r"~\Desktop\TradingView.lnk"),
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\TradingView.lnk"
    ]
    for path in kemungkinan_path:
        if os.path.exists(path):
            return path
    return None

def terjemahkan_aplikasi(perintah):
    p_lower = perintah.lower()
    kata_bersih = p_lower.replace("buka", "").replace("jalankan", "").replace("tolong", "").replace("coba", "").strip()

    if "folder" in p_lower or "drive" in p_lower or "file" in p_lower or "direktori" in p_lower:
        if "c" in p_lower:
            return "system", "folder c", "explorer C:\\"
        elif "d" in p_lower:
            return "system", "folder d", "explorer D:\\"
        else:
            return "system", "explorer", "explorer"

    kamus_pengaturan = {
        "pengaturan jam": "start ms-settings:dateandtime",
        "pengaturan waktu": "start ms-settings:dateandtime",
        "jam": "start ms-settings:dateandtime",
        "waktu": "start ms-settings:dateandtime",
        "pengaturan wifi": "start ms-settings:network-wifi",
        "wifi": "start ms-settings:network-wifi",
        "pengaturan bluetooth": "start ms-settings:bluetooth",
        "bluetooth": "start ms-settings:bluetooth",
        "pengaturan display": "start ms-settings:display",
        "pengaturan layar": "start ms-settings:display",
        "pengaturan suara": "start ms-settings:sound",
        "pengaturan update": "start ms-settings:windowsupdate",
        "pengaturan aplikasi": "start ms-settings:appsfeatures",
        "pengaturan": "start ms-settings:",
        "settings": "start ms-settings:"
    }

    for k, v in kamus_pengaturan.items():
        if k in p_lower:
            return "system", k, v

    situs_populer = {
        "youtube": "https://www.youtube.com",
        "yutub": "https://www.youtube.com",
        "yt": "https://www.youtube.com",
        "fb": "https://www.facebook.com",
        "facebook": "https://www.facebook.com",
        "ig": "https://www.instagram.com",
        "instagram": "https://www.instagram.com",
        "wa": "https://web.whatsapp.com",
        "whatsapp": "https://web.whatsapp.com",
        "whatap": "https://web.whatsapp.com",
        "gemini": "https://gemini.google.com",
        "google": "https://www.google.com",
        "github": "https://github.com",
        "chatgpt": "https://chatgpt.com",
        "netflix": "https://www.netflix.com"
    }
    
    kamus_sistem = {
        "kalkulator": "calc",
        "calculator": "calc",
        "catatan": "notepad",
        "notepad": "notepad",
        "paint": "mspaint",
        "kamera": "start microsoft.windows.camera:",
        "camera": "start microsoft.windows.camera:",
        "terminal": "wt",
        "cmd": "cmd",
        "powershell": "powershell"
    }
    
    for k in kamus_sistem:
        if k == kata_bersih:
            return "system", k, kamus_sistem[k]

    keys_sys = list(kamus_sistem.keys())
    cocok_sys = get_close_matches(kata_bersih, keys_sys, n=1, cutoff=0.7)
    if cocok_sys:
        kunci = cocok_sys[0]
        return "system", kunci, kamus_sistem[kunci]

    kata_list = kata_bersih.split()
    for kunci_web, url_web in situs_populer.items():
        if kunci_web in kata_list:
            return "web", kunci_web, url_web

    path_ditemukan = cari_software_100_persen(kata_bersih)
    if path_ditemukan:
        return "installed_app", kata_bersih, path_ditemukan

    return "unknown", kata_bersih, kata_bersih

def main():
    banner()
    tab_mapping = {} 
    counter_tab = 1
    
    while True:
        try:
            prompt_waktu = datetime.now().strftime("[%H:%M]")
            perintah = input(f"{ABU}{prompt_waktu}{EMAS} LOKAL AI > {PUTIH}").strip()
            
            if not perintah:
                continue
                
            p_lower = perintah.lower()
            
            if p_lower in ["keluar", "exit", "quit"]:
                print(f"\n{EMAS}Menutup sesi LOKAL AI. Memori dibersihkan. Sampai jumpa, Bos!{RESET}")
                time.sleep(1)
                break
                
            if "list software" in p_lower or "daftar software" in p_lower:
                print(f"\n{EMAS}[INFO] Memindai dan menampilkan seluruh software terinstal ke layar...{RESET}\n")
                ps_list = """
                $apps = Get-StartApps | Select-Object Name | Sort-Object Name
                $i = 1
                foreach ($app in $apps) {
                    Write-Output "$i. $($app.Name)"
                    $i++
                }
                Write-Output ""
                Write-Output "Total Software Ditemukan: $($apps.Count)"
                """
                subprocess.run(["powershell", "-Command", ps_list])
                kunci_fokus_ai_lokal()
                print()
                continue

            plat_key = deteksi_platform_key(perintah)
            is_perintah_tv = any(kata in p_lower for kata in ["tradingview", "tradingwiew", "tradinview", "tradingviu", "tv", "trader"])
            is_perintah_buka = "buka" in p_lower or "jalankan" in p_lower
            is_perintah_hotkey = "tekan" in p_lower or "windows" in p_lower or "hotkey" in p_lower or "enter" in p_lower or "spasi" in p_lower or "tab" in p_lower or "esc" in p_lower
            is_perintah_ketik = p_lower.startswith("ketik ") or p_lower.startswith("tulis ")
            is_perintah_layar = "lihat layar" in p_lower or "screenshot" in p_lower or "tangkap layar" in p_lower
            is_perintah_hapus = "hapus" in p_lower and ("rekaman" in p_lower or "screenshot" in p_lower or "layar" in p_lower or "foto" in p_lower)
            is_perintah_navigasi = any(k in p_lower for k in ["kembali ke", "pindah ke", "ke tab"])

            # OTOMATISASI TRADINGVIEW & KIRIM KE GEMINI DENGAN PROMPT BARU
            if is_perintah_tv:
                print(f"{ABU}[INFO] Membuka aplikasi TradingView Desktop Windows...{RESET}")
                path_tv = cari_tradingview_mendalam()
                
                if path_tv:
                    os.startfile(path_tv)
                    print(f"{EMAS}[INFO] Menunggu TradingView terbuka sempurna (6 detik)...{RESET}")
                    time.sleep(6)
                else:
                    print(f"{ABU}[INFO] Membuka TradingView melalui protokol sistem Windows...{RESET}")
                    os.system("start tradingview:")
                    time.sleep(6)

                print(f"{ABU}[INFO] Memaksimalkan jendela TradingView Fullscreen...{RESET}")
                ps_max = """
                Add-Type -AssemblyName Microsoft.VisualBasic
                [Microsoft.VisualBasic.Interaction]::AppActivate('TradingView')
                Start-Sleep -Milliseconds 500
                [System.Windows.Forms.SendKeys]::SendWait('%{SPACE}')
                Start-Sleep -Milliseconds 300
                [System.Windows.Forms.SendKeys]::SendWait('x')
                """
                subprocess.run(["powershell", "-Command", ps_max], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(1.5)

                print(f"{ABU}[INFO] Membersihkan layar dari popup (Menekan Esc)...{RESET}")
                pyautogui.press('esc')
                time.sleep(1.0)

                print(f"{ABU}[INFO] Mengambil tangkapan layar langsung dari chart aktif...{RESET}")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                nama_file_ss_tv = f"tradingview_chart_live_{timestamp}.png"
                path_ss_tv = os.path.join(os.getcwd(), nama_file_ss_tv)
                
                screenshot_tv = pyautogui.screenshot()
                screenshot_tv.save(path_ss_tv)
                print(f"{EMAS}[OK] Tangkapan layar chart berhasil disimpan: {nama_file_ss_tv}{RESET}")

                print(f"{EMAS}[INFO] Menyalin gambar ke Clipboard & Membuka Gemini AI...{RESET}")
                salin_gambar_ke_clipboard(path_ss_tv)
                os.system("start https://gemini.google.com")
                print(f"{EMAS}[INFO] Menunggu Gemini terbuka dan siap (7 detik)...{RESET}")
                time.sleep(7)

                print(f"{ABU}[INFO] Mengaktifkan jendela browser Gemini dan menempelkan gambar (Ctrl+V)...{RESET}")
                ps_gemini_focus = """
                Add-Type -AssemblyName Microsoft.VisualBasic
                [Microsoft.VisualBasic.Interaction]::AppActivate('Gemini')
                Start-Sleep -Milliseconds 1000
                """
                subprocess.run(["powershell", "-Command", ps_gemini_focus], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(1.0)
                
                pyautogui.hotkey('ctrl', 'v')
                print(f"{EMAS}[OK] Gambar chart berhasil di-paste ke kolom chat Gemini!{RESET}")
                time.sleep(2.5)
                
                print(f"{ABU}[INFO] Memasukkan teks prompt baru ke Gemini...")
                
                # PROMPT BARU SESUAI PERMINTAAN
                prompt_advanced = (
                    "ADVANCED TRADING CHART ANALYST\n\n"
                    "Bertindaklah sebagai AI analis trading profesional. Analisis tangkapan layar chart yang diberikan secara visual dan objektif.\n\n"
                    "BERIKAN JAWABAN DENGAN FORMAT PERSIS SEPERTI INI:\n\n"
                    "DECISION: BUY / SELL / WAIT\n"
                    "OPEN POSISI (ENTRY): [Tentukan harga entry yang valid]\n"
                    "TAKE PROFIT (TP): [Tentukan harga TP, wajib minimal 10 pips dari entry jika ada sinyal]\n"
                    "STOP LOSS (SL): [Tentukan harga SL, wajib maksimal 10 pips dari entry jika ada sinyal]\n"
                    "ALASAN SINGKAT: [Gunakan Fibonacci, RSI, dan Bollinger Bands sebagai dasar analisis dalam 1-2 kalimat saja]\n\n"
                    "ATURAN: Jangan memaksakan entry jika struktur market tidak jelas atau ragu, putuskan WAIT."
                )

                ps_prompt = f"""
                Add-Type -AssemblyName System.Windows.Forms
                [System.Windows.Forms.Clipboard]::SetText('{prompt_advanced}')
                """
                subprocess.run(["powershell", "-Command", ps_prompt], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1.0)
                pyautogui.press('enter')
                
                print(f"{EMAS}[OK] Prompt baru berhasil dikirim ke Gemini AI! Selesai.{RESET}")

                kunci_fokus_ai_lokal()
                print(f"{EMAS}[OK] Fokus dikembalikan mutlak ke LOKAL AI!\n")

            elif is_perintah_hapus:
                print(f"{ABU}[INFO] Menghapus file tangkapan layar chart...{RESET}")
                dihapus = False
                for f in os.listdir(os.getcwd()):
                    if f.startswith("tradingview_chart_live_") and f.endswith(".png"):
                        try:
                            os.remove(os.path.join(os.getcwd(), f))
                            print(f"{EMAS}[OK] Berhasil menghapus file chart: {f}{RESET}")
                            dihapus = True
                        except Exception:
                            pass
                if not dihapus:
                    print(f"\033[91m[INFO] Tidak ada file chart yang ditemukan untuk dihapus.\033[0m")
                kunci_fokus_ai_lokal()
                print()

            elif is_perintah_layar:
                print(f"{ABU}[INFO] Mengambil tangkapan layar manual...{RESET}")
                nama_file_ss = f"tradingview_manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                path_ss = os.path.join(os.getcwd(), nama_file_ss)
                pyautogui.screenshot().save(path_ss)
                print(f"{EMAS}[OK] Tangkapan layar berhasil disimpan sebagai '{nama_file_ss}'.")
                kunci_fokus_ai_lokal()
                print()

            elif is_perintah_ketik:
                teks_ketik = perintah.replace("ketik ", "", 1).replace("tulis ", "", 1).strip()
                print(f"{ABU}[INFO] Mengetikkan teks secara otomatis: '{teks_ketik}'...{RESET}")
                pyautogui.write(teks_ketik, interval=0.05)
                print(f"{EMAS}[OK] Selesai mengetik.")
                kunci_fokus_ai_lokal()
                print()

            elif is_perintah_hotkey:
                print(f"{ABU}[INFO] Mengeksekusi perintah keyboard sistem...")
                if "windows + r" in p_lower or "win + r" in p_lower:
                    pyautogui.hotkey('win', 'r')
                elif "windows" in p_lower or "win" in p_lower:
                    pyautogui.press('win')
                elif "enter" in p_lower:
                    pyautogui.press('enter')
                elif "spasi" in p_lower or "space" in p_lower:
                    pyautogui.press('space')
                elif "tab" in p_lower:
                    pyautogui.press('tab')
                elif "esc" in p_lower:
                    pyautogui.press('esc')
                else:
                    target_tombol = p_lower.replace("tekan", "").replace("tombol", "").strip()
                    pyautogui.press(target_tombol)
                print(f"{EMAS}[OK] Perintah keyboard berhasil dieksekusi.")
                kunci_fokus_ai_lokal()
                print()

            elif is_perintah_buka:
                tipe, nama_key, target_url = terjemahkan_aplikasi(perintah)
                
                if tipe == "system":
                    print(f"{ABU}[INFO] Membuka sistem Windows: {nama_key}...")
                    os.system(target_url)
                elif tipe == "installed_app":
                    print(f"{ABU}[INFO] Mengakses software terinstal: {nama_key}...")
                    os.system(f'start "" "{target_url}"')
                elif tipe == "web":
                    plat_kunci = deteksi_platform_key(perintah)
                    if plat_kunci and plat_kunci in tab_mapping:
                        nomor_ada = tab_mapping[plat_kunci]
                        print(f"{ABU}[INFO] Situs {nama_key} sudah ada di Tab ke-{nomor_ada}. Beralih ke tab tersebut...")
                        key_send = f"^{nomor_ada}" if nomor_ada < 9 else "^9"
                        ps_script = f"$wshell = New-Object -ComObject WScript.Shell; $wshell.SendKeys('{key_send}')"
                        subprocess.Popen(["powershell", "-Command", ps_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        if plat_kunci:
                            tab_mapping[plat_kunci] = counter_tab
                            print(f"{ABU}[INFO] Membuka situs {nama_key} di Tab ke-{counter_tab}...")
                            counter_tab += 1
                        else:
                            print(f"{ABU}[INFO] Membuka situs {nama_key}...")
                        os.system(f"start {target_url}")
                else:
                    bebas = p_lower.replace("buka", "").replace("jalankan", "").strip()
                    print(f"{ABU}[INFO] Membuka: {bebas}...")
                    os.system(f"start {bebas}")
                
                kunci_fokus_ai_lokal()
                print(f"{EMAS}[OK] Selesai. Fokus dikunci kembali di LOKAL AI.\n")

            elif is_perintah_navigasi and plat_key and plat_key in tab_mapping:
                nomor_tab = tab_mapping[plat_key]
                query = p_lower
                for kata in ["kembali ke", "pindah ke", "ke tab", "ke yt", "ke youtube", "buka tab", "di youtube", "di yutub", "di yt", "di tab yt", "di instagram", "di ig", "di fb", "kembali", "pindah", "cari", "tlg", "tolong", "coba", "video"]:
                    query = query.replace(kata, "")
                query = query.strip()

                print(f"{ABU}[INFO] Melompat ke Tab ke-{nomor_tab} [{plat_key}] & mencari: '{query}'...")
                key_send = f"^{nomor_tab}" if nomor_tab < 9 else "^9"
                ps_script = f"""
                $wshell = New-Object -ComObject WScript.Shell
                $wshell.SendKeys('{key_send}')
                Start-Sleep -Milliseconds 150
                if ('{query}' -ne '') {{
                    $wshell.SendKeys('/')
                    Start-Sleep -Milliseconds 150
                    $wshell.SendKeys('{query}')
                    Start-Sleep -Milliseconds 150
                    $wshell.SendKeys('{{ENTER}}')
                }}
                """
                subprocess.Popen(["powershell", "-Command", ps_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{EMAS}[OK] Berhasil kembali ke tab {plat_key}.")
                kunci_fokus_ai_lokal()
                print()

            else:
                query_teks = p_lower.replace("cari", "").strip()
                print(f"{ABU}[INFO] Memproses pencarian web umum: {query_teks}...")
                url = f"https://www.google.com/search?q={urllib.parse.quote(query_teks)}"
                os.system(f"start {url}")
                print(f"{EMAS}[OK] Selesai di tab browser baru.")
                kunci_fokus_ai_lokal()
                print()
                
        except Exception as e:
            print(f"\n\033[91m[ERROR] Terjadi kesalahan: {e}{RESET}")

if __name__ == "__main__":
    main()