import subprocess
import sys
import os
import re
import requests
import asyncio
from datetime import datetime
import urllib3
import warnings

# ====================== OTOMATİK PİP KURULUM ======================
def pip_kur(paket):
    try:
        __import__(paket.replace("-", "_"))
        print(f"{paket} HAZIR")
    except ImportError:
        print(f"{paket} KURULUYOR... (20-60 sn)")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", paket,
                "--no-cache-dir", "--disable-pip-version-check"
            ])
            print(f"{paket} KURULDU!")
        except Exception as e:
            print(f"{paket} kurulamadı: {e}")
            input("Devam etmek için ENTER...")
            sys.exit(1)

print("Gerekli paketler kontrol ediliyor...")
pip_kur("requests")
pip_kur("urllib3")
pip_kur("python-telegram-bot")

from telegram import Bot
from telegram.error import TelegramError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')

# ====================== TELEGRAM AYARLARI ======================
TOKEN = "8435669727:AAGoKJa1kwcS4RYExyGyZbTMUCGnVzy95kM"
CHAT_ID = "-1003373413736"

async def telegram_gonder(dosya_yolu):
    bot = Bot(token=TOKEN)
    try:
        with open(dosya_yolu, "rb") as f:
            await bot.send_document(
                chat_id=CHAT_ID,
                document=f,
                filename=f"StarLIVE_Karma_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.m3u",
                caption=f"StarLIVE KARMA M3U\n"
                        f"Kategoriler: StarLIVE • SporCafe • AndroIPTV • TRGoals\n"
                        f"Toplam Kanal: {toplam_kanal}\n"
                        f"Güncellendi: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                        f"@mutluapk"
            )
        print(f"\nTELEGRAM'A GÖNDERİLDİ → {dosya_yolu}")
    except Exception as e:
        print(f"Telegram hatası: {e}")

# ====================== M3U İÇERİK ======================
m3u_content = ["#EXTM3U"]
toplam_kanal = 0

# ====================== 1. STARLIVE (SELÇUK + BİRAZCIKSPOR) ======================
def starlive_ekle():
    global toplam_kanal
    print("\nSTARLIVE KAYNAKLARI TOPLANIYOR...")
    
    # --- Selcuksports ---
    url = "https://seep.eu.org/https://www.selcuksportshd.is/"
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    try:
        html = session.get(url, timeout=20, verify=False).text
        active = re.search(r'href=["\'](https?://[^"\']*selcuksportshd[^"\']+)["\']', html)
        if active:
            domain_html = session.get(active.group(1), timeout=20, verify=False).text
            player = re.findall(r'data-url="(https?://[^"]+id=[^"]+)"', domain_html)
            if player:
                for p in player:
                    h = session.get(p, timeout=20, verify=False).text
                    base = re.search(r'this\.baseStreamUrl\s*=\s*[\'"](https://[^\'"]+)[\'"]', h)
                    if base:
                        channels = [
                            "selcukobs1","selcukbeinsports1","selcukbeinsports2","selcukbeinsports3",
                            "selcukbeinsports4","selcukbeinsports5","selcukbeinsportsmax1","selcukbeinsportsmax2",
                            "selcukssport","selcukssport2","selcuksmartspor","selcuksmartspor2",
                            "selcuktivibuspor1","selcuktivibuspor2","selcuktivibuspor3","selcuktivibuspor4",
                            "sssplus1","sssplus2","selcuktabiispor1","selcuktabiispor2",
                            "selcuktabiispor3","selcuktabiispor4","selcuktabiispor5",
                        ]
                        for cid in channels:
                            name = re.sub(r'^selcuk', '', cid, flags=re.I).upper() + " FHD"
                            url_stream = f"{base.group(1)}{cid}/playlist.m3u8"
                            m3u_content.append(f'#EXTINF:-1 tvg-logo="https://r.resimlink.com/vOdqogntYsW.jpg" group-title="StarLIVE - Selcuk",{name}')
                            m3u_content.append(f'#EXTVLCOPT:http-referrer={active.group(1)}')
                            m3u_content.append(url_stream)
                            m3u_content.append("")
                            toplam_kanal += 1
                            print(f"  {name}")
                        break
    except: pass

    # --- Birazcikspor ---
    domain = None
    for i in range(42, 200):
        u = f"https://birazcikspor{i}.xyz/"
        try:
            if requests.head(u, timeout=5).status_code == 200:
                domain = u; break
        except: pass
    if domain:
        try:
            html = requests.get(domain, timeout=10).text
            fid = re.search(r'src="event\.html\?id=([^"]+)"', html)
            if fid:
                event = requests.get(f"{domain}event.html?id={fid.group(1)}", timeout=10).text
                base = re.search(r'var\s+baseurls\s*=\s*\[\s*"([^"]+)"', event)
                if base:
                    channels = [
                        ["TRT 1 HD", "androstreamlivetrt1"], ["Bİ SPOR HD", "androstreamlivebikanal"],
                        ["SIFIR SPOR HD", "androstreamlivesifir"], ["TRT SPOR HD", "androstreamlivetrts"],
                        ["HT SPOR 1 HD", "androstreamlivebs1"], ["TV 8 HD", "androstreamlivetv8"],
                        ["TV 8'5 HD", "androstreamlivetv85"], ["CBC SPOR HD", "androstreamlivecbcs"],
                        ["BEIN SPORTS 1 HD", "androstreamlivebs1"], ["BEIN SPORTS 2 HD", "androstreamlivebs2"],
                        ["BEIN SPORTS 3 HD", "androstreamlivebs3"], ["BEIN SPORTS 4 HD", "androstreamlivebs4"],
                        ["BEIN SPORTS 5 HD", "androstreamlivebs5"], ["BEIN SPORTS MAX 1 HD", "androstreamlivebsm1"],
                        ["BEIN SPORTS MAX 2 HD", "androstreamlivebsm2"], ["S SPORT 1 HD", "androstreamlivess1"],
                        ["S SPORT 2 HD", "androstreamlivess2"], ["TIVIBU SPORT HD", "androstreamlivets"],
                        ["TIVIBU SPORT 1 HD", "androstreamlivets1"], ["TIVIBU SPORT 2 HD", "androstreamlivets2"],
                        ["TIVIBU SPORT 3 HD", "androstreamlivets3"], ["TIVIBU SPORT 4 HD", "androstreamlivets4"],
                        ["SMART SPORT 1 HD", "androstreamlivesm1"], ["SMART SPORT 2 HD", "androstreamlivesm2"],
                        ["EURO SPORT 1 HD", "androstreamlivees1"], ["EURO SPORT 2 HD", "androstreamlivees2"],
                        ["SPORTS TV HD", "androstreamlivesptstv"], ["TABII HD", "androstreamlivetb"],
                        ["TABII 1 HD", "androstreamlivetb1"], ["TABII 2 HD", "androstreamlivetb2"],
                        ["TABII 3 HD", "androstreamlivetb3"], ["TABII 4 HD", "androstreamlivetb4"],
                        ["TABII 5 HD", "androstreamlivetb5"], ["TABII 6 HD", "androstreamlivetb6"],
                        ["TABII 7 HD", "androstreamlivetb7"], ["TABII 8 HD", "androstreamlivetb8"],
                        ["EXXEN HD", "androstreamliveexn"], ["EXXEN 1 HD", "androstreamliveexn1"],
                    ]
                    for name, cid in channels:
                        url = f"{base.group(1)}{cid}.m3u8"
                        try:
                            if requests.head(url, timeout=5).status_code == 200:
                                m3u_content.append(f'#EXTINF:-1 tvg-logo="https://r.resimlink.com/vOdqogntYsW.jpg" group-title="StarLIVE - Birazcik",{name}')
                                m3u_content.append(url)
                                m3u_content.append("")
                                toplam_kanal += 1
                                print(f"  {name}")
                        except: pass
        except: pass

# ====================== 2. SPORCAFE ======================
def sporcafe_ekle():
    global toplam_kanal
    print("\nSPORCAFE KAYNAKLARI TOPLANIYOR...")
    url = "https://www.sporcafe-782a1a67028f.xyz/"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if r.status_code == 200 and "uxsyplayer" in r.text:
            domain = re.search(r'https?://(main\.uxsyplayer[^"\']+)', r.text)
            if domain:
                domain = "https://" + domain.group(1)
                ids = [
                    "sbeinsports-1","sbeinsports-2","sbeinsports-3","sbeinsports-4","sbeinsports-5",
                    "sbeinsportsmax-1","sbeinsportsmax-2","sssport","sssport2","ssmartspor",
                    "ssmartspor2","stivibuspor-1","stivibuspor-2","stivibuspor-3","stivibuspor-4",
                    "sbeinsportshaber","saspor","seurosport1","seurosport2","sf1","stabiispor","sssportplus1"
                ]
                names = {
                    "sbeinsports-1": "beIN SPORTS 1 HD", "sbeinsports-2": "beIN SPORTS 2 HD",
                    "sbeinsports-3": "beIN SPORTS 3 HD", "sbeinsports-4": "beIN SPORTS 4 HD",
                    "sbeinsports-5": "beIN SPORTS 5 HD", "sbeinsportsmax-1": "beIN MAX 1",
                    "sbeinsportsmax-2": "beIN MAX 2", "sssport": "S SPORT", "sssport2": "S SPORT 2",
                    "ssmartspor": "SMART SPOR", "ssmartspor2": "SMART SPOR 2", "stivibuspor-1": "TIVIBU 1",
                    "stivibuspor-2": "TIVIBU 2", "stivibuspor-3": "TIVIBU 3", "stivibuspor-4": "TIVIBU 4",
                    "sbeinsportshaber": "beIN HABER", "saspor": "A SPOR", "seurosport1": "EUROSPORT 1",
                    "seurosport2": "EUROSPORT 2", "sf1": "F1 TV", "stabiispor": "TABİİ SPOR", "sssportplus1": "S SPORT PLUS"
                }
                for cid in ids:
                    try:
                        rr = requests.get(f"{domain}/index.php?id={cid}", headers={"Referer": url}, timeout=8)
                        if rr.status_code == 200:
                            base = re.search(r'this\.adsBaseUrl\s*=\s*[\'"]([^\'"]+)', rr.text)
                            if base:
                                url_stream = f"{base.group(1)}{cid}/playlist.m3u8"
                                name = names.get(cid, cid.upper())
                                m3u_content.append(f'#EXTINF:-1 group-title="SporCafe HD",{name}')
                                m3u_content.append(f'#EXTVLCOPT:http-referrer={url}')
                                m3u_content.append(url_stream)
                                m3u_content.append("")
                                toplam_kanal += 1
                                print(f"  {name}")
                    except: pass
    except: pass

# ====================== 3. ANDROIPTV (BİRAZCIKSPOR) ======================
def androiptv_ekle():
    global toplam_kanal
    print("\nANDROIPTV KAYNAKLARI TOPLANIYOR...")
    channels = [
        ("beIN Sport 1 HD","androstreamlivebs1"), ("beIN Sport 2 HD","androstreamlivebs2"),
        ("beIN Sport 3 HD","androstreamlivebs3"), ("beIN Sport 4 HD","androstreamlivebs4"),
        ("beIN Sport 5 HD","androstreamlivebs5"), ("beIN Sport Max 1 HD","androstreamlivebsm1"),
        ("beIN Sport Max 2 HD","androstreamlivebsm2"), ("S Sport 1 HD","androstreamlivess1"),
        ("S Sport 2 HD","androstreamlivess2"), ("Tivibu Sport HD","androstreamlivets"),
        ("Tivibu Sport 1 HD","androstreamlivets1"), ("Tivibu Sport 2 HD","androstreamlivets2"),
        ("Tivibu Sport 3 HD","androstreamlivets3"), ("Tivibu Sport 4 HD","androstreamlivets4"),
        ("Smart Sport 1 HD","androstreamlivesm1"), ("Smart Sport 2 HD","androstreamlivesm2"),
        ("Euro Sport 1 HD","androstreamlivees1"), ("Euro Sport 2 HD","androstreamlivees2"),
        ("Tabii HD","androstreamlivetb"), ("Tabii 1 HD","androstreamlivetb1"),
        ("Tabii 2 HD","androstreamlivetb2"), ("Tabii 3 HD","androstreamlivetb3"),
        ("Tabii 4 HD","androstreamlivetb4"), ("Tabii 5 HD","androstreamlivetb5"),
        ("Tabii 6 HD","androstreamlivetb6"), ("Tabii 7 HD","androstreamlivetb7"),
        ("Tabii 8 HD","androstreamlivetb8"), ("Exxen HD","androstreamliveexn"),
        ("Exxen 1 HD","androstreamliveexn1"), ("Exxen 2 HD","androstreamliveexn2"),
        ("Exxen 3 HD","androstreamliveexn3"), ("Exxen 4 HD","androstreamliveexn4"),
        ("Exxen 5 HD","androstreamliveexn5"), ("Exxen 6 HD","androstreamliveexn6"),
        ("Exxen 7 HD","androstreamliveexn7"), ("Exxen 8 HD","androstreamliveexn8"),
    ]
    domain = None
    for i in range(25, 100):
        u = f"https://birazcikspor{i}.xyz/"
        try:
            if requests.head(u, timeout=5).status_code == 200:
                domain = u; break
        except: pass
    if domain:
        try:
            html = requests.get(domain, timeout=10).text
            fid = re.search(r'src="event\.html\?id=([^"]+)"', html)
            if fid:
                event = requests.get(f"{domain}event.html?id={fid.group(1)}", timeout=10).text
                base = re.search(r'var\s+baseurls\s*=\s*\[\s*"([^"]+)"', event)
                if base:
                    for name, cid in channels:
                        url = f"{base.group(1)}{cid}.m3u8"
                        try:
                            if requests.head(url, timeout=5).status_code == 200:
                                m3u_content.append(f'#EXTINF:-1 tvg-logo="https://i.hizliresim.com/8xzjgqv.jpg" group-title="AndroIPTV",TR:{name}')
                                m3u_content.append(url)
                                m3u_content.append("")
                                toplam_kanal += 1
                                print(f"  TR:{name}")
                        except: pass
        except: pass

# ====================== 4. TRGOALS ======================
def trgoals_ekle():
    global toplam_kanal
    print("\nTRGOALS KAYNAKLARI TOPLANIYOR...")
    channel_ids = {
        "yayinzirve":"beIN Sports 1 ☪️","yayininat":"beIN Sports 1 ⭐","yayin1":"beIN Sports 1 ♾️",
        "yayinb2":"beIN Sports 2","yayinb3":"beIN Sports 3","yayinb4":"beIN Sports 4",
        "yayinb5":"beIN Sports 5","yayinbm1":"beIN Sports 1 Max","yayinbm2":"beIN Sports 2 Max",
        "yayinss":"Saran Sports 1","yayinss2":"Saran Sports 2","yayint1":"Tivibu Sports 1",
        "yayint2":"Tivibu Sports 2","yayint3":"Tivibu Sports 3","yayint4":"Tivibu Sports 4",
        "yayinsmarts":"Smart Sports","yayinsms2":"Smart Sports 2","yayintrtspor":"TRT Spor",
        "yayintrtspor2":"TRT Spor 2","yayinas":"A Spor","yayinatv":"ATV","yayintv8":"TV8",
        "yayintv85":"TV8.5","yayinnbatv":"NBA TV","yayinex1":"Tâbii 1","yayinex2":"Tâbii 2",
        "yayinex3":"Tâbii 3","yayinex4":"Tâbii 4","yayinex5":"Tâbii 5","yayinex6":"Tâbii 6",
        "yayinex7":"Tâbii 7","yayinex8":"Tâbii 8"
    }
    domain = "https://trgoals1459.xyz"
    try:
        if requests.head(domain, timeout=5).status_code == 200:
            PROXY = "http://proxylendim101010.mywire.org/proxy.php?url="
            for cid, name in channel_ids.items():
                try:
                    r = requests.get(f"{domain}/channel.html?id={cid}", timeout=8)
                    if r.status_code == 200:
                        base = re.search(r'const baseurl = "(.*?)"', r.text)
                        if base:
                            url = f"{PROXY}{base.group(1)}{cid}.m3u8"
                            m3u_content.append(f'#EXTINF:-1 tvg-logo="https://i.hizliresim.com/ska5t9e.jpg" group-title="TRGoals",{name}')
                            m3u_content.append(url)
                            m3u_content.append("")
                            toplam_kanal += 1
                            print(f"  {name}")
                except: pass
    except: pass

# ====================== ANA ÇALIŞTIRMA ======================
async def main():
    global toplam_kanal
    print(f"\nSTARLIVE KARMA M3U OLUŞTURULUYOR → {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
    
    starlive_ekle()
    sporcafe_ekle()
    androiptv_ekle()
    trgoals_ekle()

    dosya_yolu = "/storage/emulated/0/A-PY/StarLIVE_Karma.m3u"
    os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)
    
    with open(dosya_yolu, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_content))
    
    print(f"\nM3U OLUŞTURULDU → {dosya_yolu}")
    print(f"TOPLAM KANAL: {toplam_kanal}")

    await telegram_gonder(dosya_yolu)

    print(f"\nTAMAM! @mutluapk")
    input("Çıkmak için ENTER...")

if __name__ == "__main__":
    asyncio.run(main())