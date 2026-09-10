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
import concurrent.futures

# Import Modul Suara & COM API
try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import win32com.client
    import pythoncom
except ImportError:
    pass

# Kode Warna Tema
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
    print(f"{BG_HITAM}{EMAS}         LOKAL AI - ULTIMATE TRADING AGENT          {RESET}")
    print(f"{BG_HITAM}{EMAS}===================================================={RESET}")
    print(f"{PUTIH} Status Waktu : {EMAS}{waktu_sekarang}{RESET}")
    print(f"{PUTIH} Mode Master: Local App Finder + Precise Google Fallback{RESET}")
    print(f"{BG_HITAM}{EMAS}----------------------------------------------------{RESET}\n")

def kunci_fokus_ai_lokal():
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
    ps_copy = f"""
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.Clipboard]::SetImage([System.Drawing.Image]::FromFile('{path_gambar}'))
    """
    subprocess.run(["powershell", "-Command", ps_copy], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def deteksi_platform_key(teks):
    p = teks.lower()
    if any(k in p for k in ["youtube", "yutub", "yt"]): return "youtube"
    elif any(k in p for k in ["instagram", "ig"]): return "instagram"
    elif any(k in p for k in ["fb", "facebook"]): return "facebook"
    elif any(k in p for k in ["gemini"]): return "gemini"
    elif any(k in p for k in ["whatsapp", "wa", "whatap"]): return "whatsapp"
    elif any(k in p for k in ["github"]): return "github"
    elif any(k in p for k in ["google"]): return "google"
    return None

def dengarkan_suara():
    if sr is None:
        print(f"\n\033[91m[ERROR] Modul Suara belum terinstal.\033[0m")
        print(f"{PUTIH}Buka terminal baru dan ketik: {EMAS}pip install SpeechRecognition PyAudio{RESET}\n")
        return "matikan mode suara"
        
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"\n{EMAS}[🎤 LOKAL AI MENDENGARKAN...] Silakan bicara (Katakan 'Matikan mode suara' untuk keluar){RESET}")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=15)
            teks = recognizer.recognize_google(audio, language="id-ID")
            print(f"{ABU}[TERDENGAR]: {teks}{RESET}")
            return teks
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            print(f"{ABU}[INFO] Suara kurang jelas, AI menunggu...{RESET}")
        except sr.RequestError as e:
            print(f"\033[91m[ERROR] Gangguan koneksi layanan Google Voice: {e}\033[0m")
    return ""

def cari_file_100_persen(keyword):
    print(f"\n{EMAS}[INFO] Memindai PARALEL (Super Cepat) disk Internal, Eksternal & HP untuk: '{keyword}'...{RESET}")
    
    keyword_lower = keyword.lower().strip()
    keyword_parts = keyword_lower.split()
    hasil_mentah = []
    
    target_direktori = []
    for huruf_drive in range(ord('A'), ord('Z') + 1):
        drive = chr(huruf_drive) + ":\\"
        if os.path.exists(drive):
            target_direktori.append(drive)

    def scan_fisik(direktori):
        lokal_hasil = []
        try:
            for root, dirs, files in os.walk(direktori):
                root_lower = root.lower()
                if any(x in root_lower for x in ["windows\\system32", "windows\\winsxs", "$recycle.bin", "appdata\\local\\temp", "node_modules", "appdata\\roaming"]):
                    continue
                    
                for dirname in dirs:
                    dirname_lower = dirname.lower()
                    if keyword_lower in dirname_lower or all(part in dirname_lower for part in keyword_parts):
                        lokal_hasil.append((dirname + " (Folder)", os.path.join(root, dirname)))
                        
                for file in files:
                    file_lower = file.lower()
                    if file_lower.endswith(('.xml', '.txt', '.log', '.dll', '.ini', '.rne', '.dds', '.py', '.manifest', '.cjs', '.mjs', '.ts')):
                        continue
                    if keyword_lower in file_lower or all(part in file_lower for part in keyword_parts):
                        lokal_hasil.append((file, os.path.join(root, file)))
        except Exception:
            pass
        return lokal_hasil

    def scan_mtp():
        lokal_hasil = []
        try:
            pythoncom.CoInitialize() 
            shell = win32com.client.Dispatch("Shell.Application")
            this_pc = shell.NameSpace(17)
            
            def walk_mtp(folder_obj, current_path, depth=0):
                if depth > 5: return
                try:
                    items = folder_obj.Items()
                except Exception:
                    return
                    
                for item in items:
                    try:
                        name = item.Name
                        name_lower = name.lower()
                        is_match = keyword_lower in name_lower or all(part in name_lower for part in keyword_parts)
                        
                        if item.IsFolder:
                            if is_match:
                                lokal_hasil.append((name + " (MTP Folder)", current_path + "\\" + name))
                            if name_lower not in ["android", "data", "obb", "cache", ".thumbnails", ".trashed", "miui", "system"]:
                                walk_mtp(item.GetFolder, current_path + "\\" + name, depth + 1)
                        else:
                            if is_match:
                                lokal_hasil.append((name + " (MTP File)", current_path + "\\" + name))
                    except Exception:
                        continue
                        
            for item in this_pc.Items():
                path = item.Path
                if not path.endswith(":\\") and item.IsFolder:
                    if item.Name not in ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos", "Network"]:
                        walk_mtp(item.GetFolder, item.Name)
        except Exception:
            pass
        finally:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass
        return lokal_hasil

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_mtp = executor.submit(scan_mtp)
        futures_fisik = [executor.submit(scan_fisik, drive) for drive in target_direktori]
        
        hasil_mentah.extend(future_mtp.result())
        for future in concurrent.futures.as_completed(futures_fisik):
            hasil_mentah.extend(future.result())

    hasil_unik = []
    seen = set()
    for nama, path in hasil_mentah:
        if path not in seen:
            seen.add(path)
            hasil_unik.append((nama, path))
            
    hasil_unik.sort(key=lambda x: (
        0 if "MTP" in x[0] else (1 if not x[1].upper().startswith("C:\\") else 2),
        0 if "folder" in x[0].lower() else 1,
        len(x[0])
    ))
    
    return hasil_unik[:20]

def cari_software_100_persen(nama_app):
    """Pencarian Akurat Software Terinstal di Laptop (.exe / .lnk)"""
    lokasi_pencarian = [
        os.path.join(os.environ['USERPROFILE'], "Desktop"),
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
        os.path.join(os.environ['APPDATA'], r"Microsoft\Windows\Start Menu\Programs"),
        os.path.join(os.environ['LOCALAPPDATA'], r"Programs"),
        r"C:\Program Files",
        r"C:\Program Files (x86)"
    ]
    
    keyword_target = nama_app.lower().strip()
    daftar_exe = {}
    
    for direktori in lokasi_pencarian:
        if not os.path.exists(direktori):
            continue
        try:
            for root, dirs, files in os.walk(direktori):
                for file in files:
                    if file.lower().endswith(('.exe', '.lnk', '.url')):
                        nama_bersih = os.path.splitext(file)[0].lower()
                        path_lengkap = os.path.join(root, file)
                        daftar_exe[nama_bersih] = path_lengkap
        except Exception:
            continue

    keys = list(daftar_exe.keys())
    
    # 1. Cek kecocokan persis
    if keyword_target in keys:
        return daftar_exe[keyword_target]
        
    # 2. Cek kecocokan parsial yang spesifik (menghindari false positive)
    for nama_file, path_file in daftar_exe.items():
        if keyword_target == nama_file or (len(keyword_target) > 3 and keyword_target in nama_file):
            return path_file
            
    # 3. Gunakan pencocokan terdekat (fuzzy match dengan ambang batas ketat)
    cocok = get_close_matches(keyword_target, keys, n=1, cutoff=0.6)
    if cocok:
        return daftar_exe[cocok[0]]
        
    return None

def eksekusi_shortcut_windows(perintah_lower):
    p = perintah_lower.replace("tekan", "").replace("shortcut", "").replace("tombol", "").strip()
    print(f"{ABU}[INFO] Mengeksekusi shortcut Windows: {perintah_lower}...{RESET}")
    
    if "windows + r" in p or "win + r" in p: pyautogui.hotkey('win', 'r')
    elif "windows + x" in p or "win + x" in p: pyautogui.hotkey('win', 'x')
    elif "windows + d" in p or "win + d" in p: pyautogui.hotkey('win', 'd')
    elif "windows + e" in p or "win + e" in p: pyautogui.hotkey('win', 'e')
    elif "windows + i" in p or "win + i" in p: pyautogui.hotkey('win', 'i')
    elif "windows + s" in p or "win + s" in p: pyautogui.hotkey('win', 's')
    elif "windows + tab" in p or "win + tab" in p: pyautogui.hotkey('win', 'tab')
    elif "alt + tab" in p: pyautogui.hotkey('alt', 'tab')
    elif "ctrl + shift + esc" in p: pyautogui.hotkey('ctrl', 'shift', 'esc')
    elif "ctrl + c" in p: pyautogui.hotkey('ctrl', 'c')
    elif "ctrl + v" in p: pyautogui.hotkey('ctrl', 'v')
    elif "enter" in p: pyautogui.press('enter')
    elif "spasi" in p or "space" in p: pyautogui.press('space')
    elif "tab" in p: pyautogui.press('tab')
    elif "esc" in p: pyautogui.press('esc')
    elif p in ["windows", "win"]: pyautogui.press('win')
    else:
        parts = [x.strip() for x in p.split("+")]
        if len(parts) > 1: pyautogui.hotkey(*parts)
        else: pyautogui.press(parts[0])
    print(f"{EMAS}[OK] Shortcut berhasil dijalankan!{RESET}\n")

def cari_tradingview_mendalam():
    kemungkinan_path = [
        os.path.expanduser(r"~\AppData\Local\Programs\TradingView\TradingView.exe"),
        r"C:\Program Files\TradingView\TradingView.exe",
        r"C:\Program Files (x86)\TradingView\TradingView.exe",
        os.path.expanduser(r"~\Desktop\TradingView.lnk"),
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\TradingView.lnk"
    ]
    for path in kemungkinan_path:
        if os.path.exists(path): return path
    return None

def terjemahkan_aplikasi(perintah):
    p_lower = perintah.lower()
    kata_bersih = p_lower.replace("buka", "").replace("jalankan", "").replace("tolong", "").replace("coba", "").strip()

    if "folder" in p_lower or "drive" in p_lower or "file" in p_lower or "direktori" in p_lower:
        if "c" in p_lower: return "system", "folder c", "explorer C:\\"
        elif "d" in p_lower: return "system", "folder d", "explorer D:\\"
        else: return "system", "explorer", "explorer"

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
        if k in p_lower: return "system", k, v

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
        if k == kata_bersih: return "system", k, kamus_sistem[k]

    keys_sys = list(kamus_sistem.keys())
    cocok_sys = get_close_matches(kata_bersih, keys_sys, n=1, cutoff=0.7)
    if cocok_sys:
        kunci = cocok_sys[0]
        return "system", kunci, kamus_sistem[kunci]

    kata_list = kata_bersih.split()
    for kunci_web, url_web in situs_populer.items():
        if kunci_web in kata_list: return "web", kunci_web, url_web

    # 1. Cari dulu software terinstal di laptop secara akurat
    print(f"{ABU}[INFO] Memindai software terinstal di laptop untuk: '{kata_bersih}'...{RESET}")
    path_ditemukan = cari_software_100_persen(kata_bersih)
    if path_ditemukan: 
        return "installed_app", kata_bersih, path_ditemukan

    # 2. Jika BENAR-BENAR TIDAK ADA di laptop, lakukan Google Fallback (buka Google & tampilkan ke jendela Windows)
    print(f"{ABU}[INFO] Software tidak ditemukan terinstal di laptop. Mencari ke Google Search...{RESET}")
    url_google = f"https://www.google.com/search?q={urllib.parse.quote(kata_bersih)}"
    return "google_fallback", kata_bersih, url_google

def main():
    banner()
    tab_mapping = {} 
    counter_tab = 1
    mode_suara_aktif = False
    
    while True:
        try:
            if mode_suara_aktif:
                perintah = dengarkan_suara()
                if not perintah: continue
                p_lower = perintah.lower()
                
                kata_pemutus = ["matikan mode suara", "stop suara", "kembali ke teks", "stop", "matikan suara"]
                if any(k in p_lower for k in kata_pemutus):
                    mode_suara_aktif = False
                    print(f"{EMAS}[INFO] Mode Suara dimatikan. Kembali ke mode teks keyboard.{RESET}\n")
                    continue
            else:
                prompt_waktu = datetime.now().strftime("[%H:%M]")
                perintah = input(f"{ABU}{prompt_waktu}{EMAS} LOKAL AI > {PUTIH}").strip()
                if not perintah: continue
                p_lower = perintah.lower()
                
                if p_lower in ["mode suara", "aktifkan mode suara", "voice mode"]:
                    mode_suara_aktif = True
                    continue
            
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
            is_perintah_cari_file = p_lower.startswith("cari file ") or p_lower.startswith("buka file ") or "cari file" in p_lower
            is_perintah_buka = "buka" in p_lower or "jalankan" in p_lower
            
            daftar_hotkey_murni = ["win + r", "win + x", "win + d", "win + e", "win + i", "win + s", "win + tab", "alt + tab", "ctrl + shift + esc", "ctrl + c", "ctrl + v", "enter", "spasi", "space", "tab", "esc", "win", "windows"]
            is_perintah_hotkey = p_lower.startswith("tekan ") or p_lower in daftar_hotkey_murni

            is_perintah_ketik = p_lower.startswith("ketik ") or p_lower.startswith("tulis ")
            is_perintah_layar = "lihat layar" in p_lower or "screenshot" in p_lower or "tangkap layar" in p_lower
            is_perintah_hapus = "hapus" in p_lower and ("rekaman" in p_lower or "screenshot" in p_lower or "layar" in p_lower or "foto" in p_lower)
            
            # Deteksi perintah navigasi kembali ke tab yang sudah dibuka
            is_perintah_navigasi = any(k in p_lower for k in ["kembali ke", "pindah ke", "ke tab"]) or (plat_key and ("kembali" in p_lower or "pindah" in p_lower))

            # 1. PENCARIAN FILE LINTAS MULTI-DISK & MTP HP
            if is_perintah_cari_file:
                keyword = p_lower.replace("cari file", "").replace("buka file", "").replace("tolong", "").replace("coba", "").strip()
                if not keyword:
                    print(f"\033[91m[INFO] Mohon masukkan nama file yang ingin dicari.\033[0m\n")
                    continue
                
                hasil = cari_file_100_persen(keyword)
                
                if hasil:
                    print(f"\n{EMAS}================ HASIL PENCARIAN MULTI-DISK ================{RESET}")
                    for idx, (nama_file, path_file) in enumerate(hasil, 1):
                        print(f"{PUTIH}{idx}. {EMAS}{nama_file}{RESET}")
                        print(f"   {ABU}Lokasi: {path_file}{RESET}")
                    print(f"{EMAS}============================================================{RESET}")
                    
                    if mode_suara_aktif:
                        print(f"{PUTIH}Mode Suara: Mengeksekusi pilihan pertama secara otomatis...{RESET}")
                        pilihan_idx = 0
                    else:
                        pilihan = input(f"\n{PUTIH}Masukkan {EMAS}nomor pilihan{PUTIH} untuk membuka (ENTER untuk batal): ").strip()
                        if not pilihan.isdigit(): continue
                        pilihan_idx = int(pilihan) - 1

                    if 0 <= pilihan_idx < len(hasil):
                        nama_terpilih, path_terpilih = hasil[pilihan_idx]
                        
                        if "MTP" in nama_terpilih:
                            print(f"{ABU}[INFO] Membuka langsung folder HP (MTP) yang dituju...{RESET}")
                            try:
                                pythoncom.CoInitialize()
                                shell = win32com.client.Dispatch("Shell.Application")
                                this_pc = shell.NameSpace(17) 
                                
                                parts = path_terpilih.split("\\")
                                current_ns = None
                                
                                for item in this_pc.Items():
                                    if item.Name.lower() == parts[0].lower():
                                        current_ns = item.GetFolder
                                        break
                                        
                                if current_ns:
                                    for part in parts[1:-1] if "MTP File" in nama_terpilih else parts[1:]:
                                        found = False
                                        for subitem in current_ns.Items():
                                            if subitem.Name.lower() == part.lower():
                                                current_ns = subitem.GetFolder
                                                found = True
                                                break
                                        if not found: break
                                            
                                if current_ns:
                                    shell.Explore(current_ns.Self)
                                    print(f"{EMAS}[OK] Jendela File Explorer berhasil dibuka di dalam folder HP!{RESET}\n")
                                else:
                                    clsid_this_pc = "::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"
                                    os.system(f'explorer.exe "{clsid_this_pc}"')
                            except Exception as e:
                                print(f"\033[91m[ERROR] Gagal membuka path MTP langsung: {e}{RESET}\n")
                        else:
                            try:
                                subprocess.run(f'explorer.exe /select, "{path_terpilih}"')
                                print(f"{EMAS}[OK] Jendela File Explorer berhasil ditampilkan dan item disorot!{RESET}\n")
                            except Exception:
                                os.startfile(os.path.dirname(path_terpilih))
                                print(f"{EMAS}[OK] Folder lokasi berhasil dibuka!{RESET}\n")
                    else:
                        print(f"\033[91m[INFO] Nomor pilihan tidak valid.{RESET}\n")
                else:
                    print(f"\033[91m[INFO] Maaf, item dengan kata '{keyword}' tidak ditemukan.{RESET}\n")
                kunci_fokus_ai_lokal()
                continue

            # 2. TRADINGVIEW & GEMINI AUTOMATION
            elif is_perintah_tv:
                print(f"{ABU}[INFO] Membuka aplikasi TradingView Desktop Windows...{RESET}")
                path_tv = cari_tradingview_mendalam()
                
                if path_tv:
                    os.startfile(path_tv)
                    time.sleep(6)
                else:
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

                pyautogui.press('esc')
                time.sleep(1.0)

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                nama_file_ss_tv = f"tradingview_chart_live_{timestamp}.png"
                path_ss_tv = os.path.join(os.getcwd(), nama_file_ss_tv)
                pyautogui.screenshot().save(path_ss_tv)
                print(f"{EMAS}[OK] Tangkapan layar chart berhasil disimpan: {nama_file_ss_tv}{RESET}")

                salin_gambar_ke_clipboard(path_ss_tv)
                os.system("start https://gemini.google.com")
                time.sleep(7)

                ps_gemini_focus = """
                Add-Type -AssemblyName Microsoft.VisualBasic
                [Microsoft.VisualBasic.Interaction]::AppActivate('Gemini')
                Start-Sleep -Milliseconds 1000
                """
                subprocess.run(["powershell", "-Command", ps_gemini_focus], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(1.0)
                
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(2.5)
                
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

            # 3. HAPUS SCREENSHOT
            elif is_perintah_hapus:
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
                    print(f"\033[91m[INFO] Tidak ada file chart yang ditemukan untuk dihapus.{RESET}")
                kunci_fokus_ai_lokal()
                print()

            # 4. TANGKAP LAYAR MANUAL
            elif is_perintah_layar:
                nama_file_ss = f"tradingview_manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                pyautogui.screenshot().save(os.path.join(os.getcwd(), nama_file_ss))
                print(f"{EMAS}[OK] Tangkapan layar berhasil disimpan sebagai '{nama_file_ss}'.")
                kunci_fokus_ai_lokal()
                print()

            # 5. KETIK OTOMATIS
            elif is_perintah_ketik:
                teks_ketik = perintah.replace("ketik ", "", 1).replace("tulis ", "", 1).strip()
                pyautogui.write(teks_ketik, interval=0.05)
                print(f"{EMAS}[OK] Selesai mengetik.")
                kunci_fokus_ai_lokal()
                print()

            # 6. SHORTCUT WINDOWS
            elif is_perintah_hotkey:
                eksekusi_shortcut_windows(p_lower)
                kunci_fokus_ai_lokal()
                print()

            # 7. NAVIGASI KEMBALI KE TAB BROWSER
            elif is_perintah_navigasi and plat_key and plat_key in tab_mapping:
                nomor_tab = tab_mapping[plat_key]
                print(f"{ABU}[INFO] Memfokuskan browser & berpindah ke Tab ke-{nomor_tab} [{plat_key}]...{RESET}")
                try:
                    ps_activate = """
                    Add-Type -AssemblyName Microsoft.VisualBasic
                    try { [Microsoft.VisualBasic.Interaction]::AppActivate("Google Chrome") } catch {}
                    try { [Microsoft.VisualBasic.Interaction]::AppActivate("Microsoft Edge") } catch {}
                    """
                    subprocess.run(["powershell", "-Command", ps_activate], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(0.15)
                    if nomor_tab < 10:
                        pyautogui.hotkey('ctrl', str(nomor_tab))
                    else:
                        pyautogui.hotkey('ctrl', '9')
                except Exception:
                    pass

                print(f"{EMAS}[OK] Berhasil beralih ke tab {plat_key}.")
                kunci_fokus_ai_lokal()
                print()

            # 8. BUKA WEB & APLIKASI LAPTOP (DENGAN GOOGLE FALLBACK JIKA TIDAK ADA)
            elif is_perintah_buka:
                tipe, nama_key, target_url = terjemahkan_aplikasi(perintah)
                
                if tipe == "system":
                    print(f"{ABU}[INFO] Membuka sistem Windows: {nama_key}...")
                    os.system(target_url)
                elif tipe == "installed_app":
                    print(f"{ABU}[INFO] Membuka aplikasi terinstal di laptop: {nama_key}...")
                    os.system(f'start "" "{target_url}"')
                elif tipe == "web":
                    plat_kunci = deteksi_platform_key(perintah)
                    if plat_kunci and plat_kunci in tab_mapping:
                        nomor_ada = tab_mapping[plat_kunci]
                        print(f"{ABU}[INFO] Situs {nama_key} sudah ada di Tab ke-{nomor_ada}. Beralih ke tab tersebut...")
                        try:
                            ps_activate = """
                            Add-Type -AssemblyName Microsoft.VisualBasic
                            try { [Microsoft.VisualBasic.Interaction]::AppActivate("Google Chrome") } catch {}
                            try { [Microsoft.VisualBasic.Interaction]::AppActivate("Microsoft Edge") } catch {}
                            """
                            subprocess.run(["powershell", "-Command", ps_activate], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            time.sleep(0.15)
                            if nomor_ada < 10:
                                pyautogui.hotkey('ctrl', str(nomor_ada))
                            else:
                                pyautogui.hotkey('ctrl', '9')
                        except Exception:
                            pass
                    else:
                        if plat_kunci:
                            tab_mapping[plat_kunci] = counter_tab
                            print(f"{ABU}[INFO] Membuka situs {nama_key} di Tab ke-{counter_tab} (Total Tab: {counter_tab})...")
                            counter_tab += 1
                        else:
                            print(f"{ABU}[INFO] Membuka situs {nama_key}...")
                        os.system(f"start {target_url}")
                elif tipe == "google_fallback":
                    os.system(f"start {target_url}")
                    print(f"{EMAS}[OK] Hasil pencarian Google Search berhasil dibuka & ditampilkan di jendela browser Windows.{RESET}\n")
                else:
                    bebas = p_lower.replace("buka", "").replace("jalankan", "").strip()
                    print(f"{ABU}[INFO] Membuka: {bebas}...")
                    os.system(f"start {bebas}")
                
                kunci_fokus_ai_lokal()
                print(f"{EMAS}[OK] Selesai. Fokus dikunci kembali di LOKAL AI.\n")

            # 9. PENCARIAN GOOGLE UMUM
            else:
                query_teks = p_lower.replace("cari", "").strip()
                print(f"{ABU}[INFO] Memproses pencarian web umum: {query_teks}...")
                url = f"https://www.google.com/search?q={urllib.parse.quote(query_teks)}"
                os.system(f"start {url}")
                print(f"{EMAS}[OK] Selesai di tab browser baru.")
                kunci_fokus_ai_lokal()
                print()
                
        except Exception as e:
            print(f"\n\033[91m[ERROR] Terjadi kesalahan: {e}{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"\n[CRITICAL ERROR]: {err}")
    
    input("\nProgram berhenti. Tekan ENTER untuk keluar...")