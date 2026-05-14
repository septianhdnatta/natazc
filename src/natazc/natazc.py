"""
GLITXH-VIP GENERATOR V2.5 ULTRA
Credits : glitxh (tele : @glitxh4ff)
saluran : https://whatsapp.com/channel/0029VbCM9ME17EmxSJP3ox3j
NOTED : JANGAN DI HAPUS ANGGEP AJA CREDITS!
"""

import os, sys, subprocess, hashlib, hmac, zlib, json, urllib.request, urllib.error

DEVICE_CHECK_URL = "https://raw.githubusercontent.com/septianhdnatta/idd/refs/heads/main/device.json"

def _get_device_fingerprint():
    fp = []
    
    try:
        import subprocess
        serial = subprocess.check_output(['getprop', 'ro.serialno'], text=True).strip()
        if not serial or serial == 'unknown':
            serial = os.environ.get('ANDROID_SERIAL', '')
        fp.append(serial)
    except:
        fp.append('')
    
    try:
        model = platform.machine()
        fp.append(model)
    except:
        fp.append('')
    
    try:
        brand = platform.system()
        fp.append(brand)
    except:
        fp.append('')
    
    try:
        with open('/system/build.prop', 'r') as f:
            for line in f:
                if 'ro.build.fingerprint' in line:
                    fp.append(line.split('=')[1].strip())
                    break
    except:
        fp.append('')
    
    try:
        import subprocess
        man = subprocess.check_output(['getprop', 'ro.product.manufacturer'], text=True).strip()
        fp.append(man)
    except:
        fp.append('')
    
    try:
        hw = platform.processor()
        fp.append(hw)
    except:
        fp.append('')
    
    try:
        tz = time.tzname[0] if time.tzname else ''
        fp.append(tz)
    except:
        fp.append('')
    
    try:
        uid = str(os.getuid())
        fp.append(uid)
    except:
        fp.append('')
    
    raw = '|'.join(fp).encode()
    
    h1 = hashlib.sha3_512(raw).digest()
    h2 = hashlib.blake2b(h1).digest()
    final = hashlib.sha256(h1 + h2).hexdigest()
    
    return '-'.join([final[i:i+4] for i in range(0, 32, 4)]).upper()

_DEVICE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.deviceid')
_XOR_KEY = bytes([0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10, 0x12, 0x34, 0x56, 0x78, 0x9a, 0xbc, 0xde, 0xf0])

def _xor_encrypt(data):
    return bytes([data[i] ^ _XOR_KEY[i % len(_XOR_KEY)] for i in range(len(data))])

def _save_device_id(fingerprint, use_count=0):
    data = {
        'fp': fingerprint,
        'use': use_count,
        'ts': int(time.time())
    }
    json_str = json.dumps(data)
    compressed = zlib.compress(json_str.encode())
    encrypted = _xor_encrypt(compressed)
    import base64
    encoded = base64.b64encode(encrypted).decode()
    sig = hmac.new(_XOR_KEY, encrypted, hashlib.blake2b).hexdigest()
    with open(_DEVICE_FILE, 'w') as f:
        f.write(encoded + '|' + sig)

def _load_device_id():
    if not os.path.exists(_DEVICE_FILE):
        return None
    try:
        import base64
        with open(_DEVICE_FILE, 'r') as f:
            content = f.read().strip()
        if '|' not in content:
            return None
        encoded, sig = content.split('|')
        encrypted = base64.b64decode(encoded.encode())
        expected = hmac.new(_XOR_KEY, encrypted, hashlib.blake2b).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        decrypted = _xor_encrypt(encrypted)
        decompressed = zlib.decompress(decrypted)
        data = json.loads(decompressed.decode())
        return data
    except:
        return None

def _verify_online():
    try:
        fp = _get_device_fingerprint()
        
        print(f"\nHello user. We will check your device ID status! Please wait a moment...")
        
        req = urllib.request.Request(DEVICE_CHECK_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode()
            data = json.loads(content)
        
        if isinstance(data, list):
            allowed_devices = [str(device).strip() for device in data if device]
        else:
            print(f"Format JSON salah! Diharapkan array, mendapat {type(data)}")
            return False
        
        if fp in allowed_devices:
            return True
        else:
            print("\nHello user. Welcome to the glitxh script. We believe you haven't verified your device ID. Please contact the admin and send your device ID to them.")
            print(f"Device ID: {fp}")
            print("Send it to Telegram at t.me/natazaxz to use the script.")
            return False
            
    except urllib.error.URLError as e:
        print("\nGAGAL KONEKSI KE SERVER")
        print(f"Error: {str(e)}")
        print("Pastikan koneksi internet Anda aktif.")
        return False
    except json.JSONDecodeError as e:
        print("\nERROR FORMAT JSON")
        print(f"Format JSON tidak valid: {str(e)}")
        return False
    except Exception as e:
        print("\nVERIFIKASI GAGAL")
        print(f"Error: {str(e)}")
        return False

def _run_protection():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if not _verify_online():
        print("\n")
        time.sleep(3)
        sys.exit(1)
    
    fingerprint = _get_device_fingerprint()
    stored = _load_device_id()
    if stored is None:
        _save_device_id(fingerprint, 1)
    
    print("\nWelcome back sir!..\n")
    time.sleep(1)

_run_protection()

# ============================================================
# LANJUTAN SCRIPT ASLI
# ============================================================

def _pip(p, m=None):
    try: __import__(m or p.replace("-","_"))
    except ImportError:
        subprocess.check_call([sys.executable,"-m","pip","install",p,"-q"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

for _p,_m in [("colorama",None),("requests",None),("pycryptodome","Crypto"),
               ("urllib3",None),("cfonts",None)]:
    _pip(_p,_m)

import time, threading, socket, re, json, hmac, hashlib
import string, random, codecs, base64
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import requests, urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from colorama import Fore, Style, init
from cfonts import render

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN
M=Fore.MAGENTA; LG=Fore.LIGHTGREEN_EX; W=Fore.RESET; B=Style.BRIGHT

# ══════════════════════════════════════════════════════════════════
#  UTILS
# ══════════════════════════════════════════════════════════════════
def fmt(sec):
    sec=max(0,int(sec)); d,sec=divmod(sec,86400); h,sec=divmod(sec,3600); m,s=divmod(sec,60)
    p=[]
    if d: p.append(f"{d}hari")
    if h: p.append(f"{h}jam")
    if m: p.append(f"{m}menit")
    if s or not p: p.append(f"{s}detik")
    return " ".join(p)

VALID={"ME","IND","ID","VN","TH","BD","PK","TW","EU","CIS","NA","SAC","BR","SG"}
LANG={"ME":"ar","IND":"hi","ID":"id","VN":"vi","TH":"th","BD":"bn",
      "PK":"ur","TW":"zh","EU":"en","CIS":"ru","NA":"en","SAC":"es","BR":"pt","SG":"en"}
TIER_E={"NORMAL":"🍀","LOW":"😬","MEDIUM":"🤩","HIGH":"☠️","LEGEND":"❤️‍🔥"}
TIER_C={"LEGEND":R+B,"HIGH":M+B,"MEDIUM":C+B,"LOW":Y,"NORMAL":G}

# ══════════════════════════════════════════════════════════════════
#  CRYPTO
# ══════════════════════════════════════════════════════════════════
_AK=bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
_AI=bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
KEY=bytes.fromhex("32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533")

def aes_bytes(h): return AES.new(_AK,AES.MODE_CBC,_AI).encrypt(pad(bytes.fromhex(h),16))
def aes_hex(h): return aes_bytes(h).hex()

def ev(n):
    r=[]
    while True:
        b=n&0x7F; n>>=7
        if n: b|=0x80
        r.append(b)
        if not n: break
    return bytes(r)

def pb(fields):
    o=bytearray()
    for f,v in fields.items():
        if isinstance(v,dict): p=pb(v); o+=ev((f<<3)|2)+ev(len(p))+p
        elif isinstance(v,int): o+=ev((f<<3)|0)+ev(v)
        else: p=v.encode() if isinstance(v,str) else v; o+=ev((f<<3)|2)+ev(len(p))+p
    return bytes(o)

def enc_oid(s):
    k=[0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,
       0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
    return {"open_id":s,"field_14":"".join(chr(ord(c)^k[i%32]) for i,c in enumerate(s))}

def ue(s): return "".join(c if 32<=ord(c)<=126 else f"\\u{ord(c):04x}" for c in s)

def decode_resp(text):
    for pfx in("eyJhbGciOiJIUzI1NiIsInN2ciI6IjEiLCJ0eXAiOiJKV1QifQ","eyJ"):
        i=text.find(pfx)
        if i<0: continue
        t=text[i:]; d1=t.find("."); d2=t.find(".",d1+1) if d1>=0 else -1
        if d2<0: continue
        try:
            p=t[d1+1:d2]; p+="="*((4-len(p)%4)%4)
            d=json.loads(base64.urlsafe_b64decode(p))
            for k in("account_id","external_id","user_id","uid"):
                if d.get(k): return str(d[k])
        except: pass
    return "N/A"

# ══════════════════════════════════════════════════════════════════
#  TOR
# ══════════════════════════════════════════════════════════════════
_TOR_PROC=None; _TOR_READY=False; _TOR_REN=False; _TOR_LK=threading.Lock()

def _tor_setup():
    global _TOR_PROC,_TOR_READY
    for p in['/data/data/com.termux/files/usr/etc/resolv.conf','/etc/resolv.conf']:
        try:
            os.makedirs(os.path.dirname(p),exist_ok=True)
            open(p,'w').write("nameserver 1.1.1.1\nnameserver 1.0.0.1\noptions rotate timeout:1 attempts:1\n")
            break
        except: pass
    try: subprocess.run(['pkill','-9','tor'],capture_output=True); time.sleep(1)
    except: pass
    rc=("SocksPort 127.0.0.1:9050\nControlPort 127.0.0.1:9051\nCookieAuthentication 0\n"
        "MaxCircuitDirtiness 8\nUseEntryGuards 0\nNumEntryGuards 8\nSafeLogging 0\n"
        "Log notice stdout\nClientUseIPv4 1\nCircuitBuildTimeout 8\nMaxOnionsPending 2048\n")
    tp='/tmp/torrc'
    for p in['/data/data/com.termux/files/usr/etc/tor/torrc','/tmp/torrc']:
        try: os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(rc); tp=p; break
        except: pass
    _TOR_PROC=subprocess.Popen(['tor','-f',tp],stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,start_new_session=True)
    for _ in range(25):
        time.sleep(1)
        if subprocess.run(['pgrep','-x','tor'],capture_output=True).returncode==0:
            _TOR_READY=True; break

def _tor_renew():
    global _TOR_REN
    with _TOR_LK:
        if _TOR_REN: return
        _TOR_REN=True
    try:
        s=socket.socket(); s.settimeout(4); s.connect(('127.0.0.1',9051))
        s.sendall(b'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\nQUIT\r\n'); s.recv(256); s.close()
        time.sleep(1)
    except: pass
    finally: _TOR_REN=False

threading.Thread(target=_tor_setup,daemon=True).start()
time.sleep(5)

# ══════════════════════════════════════════════════════════════════
#  PROXY + CONNECTION REUSE (thread-local persistent session)
# ══════════════════════════════════════════════════════════════════
WS=[
    "http://gajuiica:wo29gu5sa2sh@31.59.20.176:6754/",
    "http://gajuiica:wo29gu5sa2sh@92.113.242.158:6742/",
    "http://gajuiica:wo29gu5sa2sh@198.23.239.134:6540/",
    "http://gajuiica:wo29gu5sa2sh@45.38.107.97:6014/",
    "http://gajuiica:wo29gu5sa2sh@107.172.163.27:6543/",
    "http://gajuiica:wo29gu5sa2sh@216.10.27.159:6837/",
    "http://gajuiica:wo29gu5sa2sh@142.111.67.146:5611/",
    "http://gajuiica:wo29gu5sa2sh@191.96.254.138:6185/",
    "http://gajuiica:wo29gu5sa2sh@31.58.9.4:6077/",
    "http://gajuiica:wo29gu5sa2sh@23.229.19.94:8689/",
    "http://cidyiiul:0x1sq2qkuk6a@31.59.20.176:6754/",
    "http://cidyiiul:0x1sq2qkuk6a@92.113.242.158:6742/",
    "http://cidyiiul:0x1sq2qkuk6a@198.23.239.134:6540/",
    "http://cidyiiul:0x1sq2qkuk6a@45.38.107.97:6014/",
    "http://cidyiiul:0x1sq2qkuk6a@107.172.163.27:6543/",
    "http://cidyiiul:0x1sq2qkuk6a@216.10.27.159:6837/",
    "http://cidyiiul:0x1sq2qkuk6a@142.111.67.146:5611/",
    "http://cidyiiul:0x1sq2qkuk6a@191.96.254.138:6185/",
    "http://cidyiiul:0x1sq2qkuk6a@31.58.9.4:6077/",
    "http://cidyiiul:0x1sq2qkuk6a@23.229.19.94:8689/",
    "http://ffrevdai:kapukxzd8av3@31.59.20.176:6754/",
    "http://ffrevdai:kapukxzd8av3@92.113.242.158:6742/",
    "http://ffrevdai:kapukxzd8av3@198.23.239.134:6540/",
    "http://ffrevdai:kapukxzd8av3@45.38.107.97:6014/",
    "http://ffrevdai:kapukxzd8av3@107.172.163.27:6543/",
    "http://ffrevdai:kapukxzd8av3@216.10.27.159:6837/",
    "http://ffrevdai:kapukxzd8av3@142.111.67.146:5611/",
    "http://ffrevdai:kapukxzd8av3@191.96.254.138:6185/",
    "http://ffrevdai:kapukxzd8av3@31.58.9.4:6077/",
    "http://ffrevdai:kapukxzd8av3@23.229.19.94:8689/",
    "http://nfjndowc:vuc84qb19nsg@31.59.20.176:6754/",
    "http://nfjndowc:vuc84qb19nsg@92.113.242.158:6742/",
    "http://nfjndowc:vuc84qb19nsg@198.23.239.134:6540/",
    "http://nfjndowc:vuc84qb19nsg@45.38.107.97:6014/",
    "http://nfjndowc:vuc84qb19nsg@107.172.163.27:6543/",
    "http://nfjndowc:vuc84qb19nsg@216.10.27.159:6837/",
    "http://nfjndowc:vuc84qb19nsg@142.111.67.146:5611/",
    "http://nfjndowc:vuc84qb19nsg@191.96.254.138:6185/",
    "http://nfjndowc:vuc84qb19nsg@31.58.9.4:6077/",
    "http://nfjndowc:vuc84qb19nsg@23.229.19.94:8689/",
]
_N_WS=len(WS); _pidx=0; _plock=threading.Lock()
_utor=False; _tts=time.time(); _local=threading.local()

def _sess():
    global _utor,_tts,_pidx
    now=time.time()
    if now-_tts>=5:
        _utor=not _utor; _tts=now
        if _utor: threading.Thread(target=_tor_renew,daemon=True).start()
    if not hasattr(_local,'n'): _local.n=0; _local.s=None
    _local.n+=1
    if _local.s is None or _local.n%50==0:
        s=requests.Session(); s.verify=False
        a=requests.adapters.HTTPAdapter(pool_connections=20,pool_maxsize=50,max_retries=0)
        s.mount('http://',a); s.mount('https://',a)
        if _utor and _TOR_READY:
            s.proxies={'http':'socks5h://127.0.0.1:9050','https':'socks5h://127.0.0.1:9050'}
        else:
            with _plock: p=WS[_pidx%_N_WS]; _pidx+=1
            s.proxies={'http':p,'https':p}
        _local.s=s
    return _local.s

# ══════════════════════════════════════════════════════════════════
#  UA
# ══════════════════════════════════════════════════════════════════
UA=["GarenaMSDK/4.0.39(SM-A325M;Android 13;en;HK;)",
    "GarenaMSDK/4.0.39(Poco F3;Android 12;en;SG;)",
    "GarenaMSDK/4.0.39(Redmi Note 10;Android 11;en;ID;)",
    "GarenaMSDK/4.0.39(Samsung A52;Android 12;en;MY;)",
    "GarenaMSDK/4.0.39(Oppo Reno5;Android 11;en;PH;)",
    "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
    "GarenaMSDK/4.0.39(CPH2359;Android 12;en;US;)",
    "GarenaMSDK/4.0.39(NE2213;Android 13;en;EU;)",
    "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
    "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)"]
_ui=0; _ul=threading.Lock()
def _ua():
    global _ui
    with _ul: u=UA[_ui%len(UA)]; _ui+=1; return u

def _nm(): return 'N4taza'+''.join(random.choices(string.ascii_uppercase+string.digits,k=6))
def _pw(): return "N4TAZA-"+''.join(random.choices(string.ascii_uppercase+string.digits,k=9))+"-VVIP"

# ══════════════════════════════════════════════════════════════════
#  STORAGE + WRITE BUFFER
# ══════════════════════════════════════════════════════════════════
BASE="GLITXH-VIP"; _tfd={}; _fl=threading.Lock()
_wbuf=[]; _wblk=threading.Lock(); _WBSZ=15

def _tfiles(r):
    ru=r.upper(); rd=os.path.join(BASE,ru)
    for d in[rd,f"{rd}/LEGENDA",f"{rd}/High",f"{rd}/Medium",f"{rd}/Low",f"{rd}/Normal"]:
        os.makedirs(d,exist_ok=True)
    return{t:os.path.join(rd,s,f"Account-{ru}.json")
           for t,s in[("LEGEND","LEGENDA"),("HIGH","High"),("MEDIUM","Medium"),
                       ("LOW","Low"),("NORMAL","Normal")]}

def tf(r):
    if r not in _tfd: _tfd[r]=_tfiles(r)
    return _tfd[r]

def _flush(buf):
    by={}
    for e,t,r in buf:
        fp=tf(r).get(t)
        if fp: by.setdefault(fp,[]).append(e)
    with _fl:
        for fp,es in by.items():
            try:
                d=json.load(open(fp,encoding='utf-8')) if os.path.exists(fp) else []
                if not isinstance(d,list): d=[d]
                d.extend(es)
                json.dump(d,open(fp,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
            except: pass

def save(e,t,r):
    with _wblk:
        _wbuf.append((e,t,r))
        if len(_wbuf)>=_WBSZ:
            buf=_wbuf.copy(); _wbuf.clear()
            threading.Thread(target=_flush,args=(buf,),daemon=True).start()

def _flush_all():
    with _wblk:
        if _wbuf: buf=_wbuf.copy(); _wbuf.clear(); _flush(buf)

# ══════════════════════════════════════════════════════════════════
#  TIER
# ══════════════════════════════════════════════════════════════════
def tier(aid):
    if not aid or aid=="N/A": return "NORMAL"
    s=0
    if len(aid)>=6:
        rem=aid[3:]
        if len(set(aid))==1: s+=30
        elif len(set(rem))==1: s+=25
        elif aid[:3] in{"154","155","156","157","158","159"} and len(set(rem))==1: s+=28
    for pat,pts in[(r'(\d)\1{5,}',10),(r'(\d)\1{4,}',8),(r'(\d)\1{3,}',6),(r'(\d)\1{2,}',3)]:
        if re.search(pat,aid): s+=pts; break
    if re.search(r'(12345|23456|34567|45678|56789|98765|87654|76543|65432|54321)',aid): s+=7
    elif re.search(r'(1234|2345|3456|4567|5678|6789|9876|8765|7654|6543|5432|4321)',aid): s+=4
    if len(aid)>=6 and aid==aid[::-1]: s+=8
    elif len(aid)>=4 and aid[:2]==aid[-1:-3:-1]: s+=4
    if len(aid)>=6 and len(set(aid[::2]))==1 and len(set(aid[1::2]))==1: s+=6
    for sn in['888','999','666','777','000','123','321','111','222','333','444','555']:
        if sn in aid: s+=2
    if len(aid)<=8: s+=5
    elif len(aid)<=9: s+=3
    if s>=20: return "LEGEND"
    if s>=12: return "HIGH"
    if s>=6: return "MEDIUM"
    if s>=2: return "LOW"
    return "NORMAL"

# ══════════════════════════════════════════════════════════════════
#  BOOST
# ══════════════════════════════════════════════════════════════════
_boost_on=False; _boost_end=0.0; _boost_tgt=None; _boost_desc=""
_boost_lk=threading.Lock()

def _find_target(aid):
    try: cur=int(aid)
    except: return None
    s=str(cur); pre=s[:2]; sl=len(s)-2; best=None
    for rlen in range(9,4,-1):
        for d in '9876543210':
            suf=d*rlen
            if rlen<sl:
                for f in '9876543210':
                    full=f*(sl-rlen)+suf
                    if len(full)!=sl: continue
                    tgt=int(pre+full); gap=tgt-cur
                    if 0<gap<=800000:
                        sc=rlen*10+(800000-gap)//100000
                        if not best or sc>best[3]: best=(tgt,gap,f"{pre}{full}({rlen}x{d})",sc)
            else:
                full=suf[:sl]; tgt=int(pre+full); gap=tgt-cur
                if 0<gap<=800000:
                    sc=rlen*10+(800000-gap)//100000
                    if not best or sc>best[3]: best=(tgt,gap,f"{pre}{full}({rlen}x{d})",sc)
    for st in range(10):
        for dr in(1,-1):
            seq=''.join(str((st+i*dr)%10) for i in range(sl))
            try:
                tgt=int(pre+seq); gap=tgt-cur
                if 0<gap<=400000:
                    sc=50+(400000-gap)//50000
                    if not best or sc>best[3]: best=(tgt,gap,f"{pre}{seq}(seq)",sc)
            except: pass
    return best

def _check_boost(aid):
    global _boost_on,_boost_end,_boost_tgt,_boost_desc
    r=_find_target(aid)
    if not r: return
    tgt,gap,desc,score=r
    trigger=(gap<=50000) or (gap<=300000 and score>=75) or (gap<=800000 and score>=90)
    if not trigger: return
    with _boost_lk:
        if _boost_on and _boost_tgt==tgt: return
        _boost_on=True; _boost_end=time.time()+60
        _boost_tgt=tgt; _boost_desc=desc
    with _plock:
        sys.stdout.write("\r"+" "*120+"\r")
        print(f"\n{R}{B}[ ! ] BOOST x2! Mengejar {desc} | Gap:{gap:,} | 1 menit..{W}\n")

def _boosting():
    global _boost_on
    if not _boost_on: return False
    if time.time()>_boost_end:
        with _boost_lk: _boost_on=False; _boost_tgt=None
        return False
    return True

# ══════════════════════════════════════════════════════════════════
#  STATE
# ══════════════════════════════════════════════════════════════════
_cnt=0; _cnt_lk=threading.Lock()
_ts={"NORMAL":0,"LOW":0,"MEDIUM":0,"HIGH":0,"LEGEND":0}; _tslk=threading.Lock()
_stuck_t=time.time(); _stuck_lk=threading.Lock(); _stuck_on=True
_t0=time.time(); _p100t=time.time(); _p100c=0
_total=0; _nw=20

# ── Speed stabilizer state ─────────────────────────────────────────
_spd_window=[]; _spd_lock=threading.Lock()
_baseline_spd=0; _stab_on=False

def _stuck_reset():
    with _stuck_lk: globals()['_stuck_t']=time.time()

def _stuck_loop():
    while _stuck_on:
        time.sleep(5)
        with _stuck_lk: idle=time.time()-_stuck_t
        if _total>0 and _cnt>=_total: break
        if idle>=25:
            threading.Thread(target=_tor_renew,daemon=True).start()
            _stuck_reset()

threading.Thread(target=_stuck_loop,daemon=True).start()

# ══════════════════════════════════════════════════════════════════
#  SPEED STABILIZER
# ══════════════════════════════════════════════════════════════════
_stab_extras=[]
_stab_ex_lock=threading.Lock()
_stab_exec=None
_stab_region=""

def _record_speed(cur_cnt):
    global _baseline_spd,_spd_window
    with _spd_lock:
        _spd_window.append((time.time(), cur_cnt))
        cutoff=time.time()-60
        _spd_window=[x for x in _spd_window if x[0]>=cutoff]

def _current_speed():
    with _spd_lock:
        if len(_spd_window)<2: return 0
        dt=_spd_window[-1][0]-_spd_window[0][0]
        dc=_spd_window[-1][1]-_spd_window[0][1]
        return dc/dt if dt>0 else 0

def _stabilizer(region):
    global _baseline_spd,_stab_on,_stab_extras,_stab_exec
    time.sleep(60)
    with _spd_lock:
        if _spd_window:
            dt=_spd_window[-1][0]-_spd_window[0][0]
            dc=_spd_window[-1][1]-_spd_window[0][1]
            _baseline_spd=dc/dt if dt>0 else 0

    while _stuck_on:
        time.sleep(30)
        if not _stuck_on: break
        spd=_current_speed()
        if _baseline_spd>0 and spd>0:
            ratio=spd/_baseline_spd
            if ratio<0.5 and not _stab_on:
                _stab_on=True
                threading.Thread(target=_tor_renew,daemon=True).start()
                with _plock:
                    sys.stdout.write("\r"+" "*120+"\r")
                    print(f"\n{Y}{B}[ ⚠ ] Speed drop! {spd:.1f}/s (baseline:{_baseline_spd:.1f}/s) → stabilizing..{W}\n")
                if _stab_exec:
                    with _stab_ex_lock:
                        for _ in range(_nw):
                            try:
                                f=_stab_exec.submit(worker,region)
                                _stab_extras.append(f)
                            except: pass
            elif ratio>=0.7 and _stab_on:
                _stab_on=False
                with _plock:
                    sys.stdout.write("\r"+" "*120+"\r")
                    print(f"\n{G}{B}[ ✓ ] Speed stable! {spd:.1f}/s{W}\n")
                with _stab_ex_lock:
                    _stab_extras=[f for f in _stab_extras if not f.done()]

# ══════════════════════════════════════════════════════════════════
#  LIVE DASHBOARD
# ══════════════════════════════════════════════════════════════════
_DASH_ON=False

def _dashboard():
    frames=["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]; fi=0
    while _DASH_ON:
        with _cnt_lk: cur=_cnt
        with _tslk: ts2=dict(_ts)
        now=time.time(); el=now-_t0
        spd=_current_speed()
        if spd==0 and el>0: spd=cur/el
        eta=((_total-cur)/spd) if spd>0 and _total>0 else 0
        tot_s=f"/{_total}" if _total>0 else "/∞"
        pct=min(int(cur/_total*25),25) if _total>0 else 0
        bar=f"{G}{'█'*pct}{'░'*(25-pct)}{W}" if _total>0 else f"{C}{'~'*25}{W}"
        boost_s=f" {R}{B}[BOOST x2]{W}" if _boosting() else ""
        stab_s=f" {Y}[STAB]{W}" if _stab_on else ""
        fr=frames[fi%len(frames)]; fi+=1
        line=(f"\r{C}{fr}{W} {cur}{tot_s} {bar} {Y}{spd:.1f}/s{W}"
              f" {fmt(el)} ETA:{fmt(eta)}"
              f" {G}🍀{ts2['NORMAL']}{W}{Y}😬{ts2['LOW']}{W}"
              f"{C}🤩{ts2['MEDIUM']}{W}{M}☠️{ts2['HIGH']}{W}"
              f"{R}❤️‍🔥{ts2['LEGEND']}{W}{boost_s}{stab_s}   ")
        with _plock:
            sys.stdout.write(line); sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r"+" "*140+"\r"); sys.stdout.flush()

# ══════════════════════════════════════════════════════════════════
#  BATCH REGISTER
# ══════════════════════════════════════════════════════════════════
_BATCH=5
_RU="https://100067.connect.garena.com/api/v2/oauth/guest:register"
_TU="https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
_AT=b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390'
_OI=b'1d8ec0240ede109973f3321b9354b44d'
_LP=(b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28'
     b' (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05'
     b'r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640'
     b'\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f'
     b'\xa2\x01\x0e105.235.139.91\xaa\x01\x02')
_LP2=(b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d'
      b'\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA'
      b'\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390'
      b'\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI'
      b'\xca\x03 7428b253defc164018c604a1ebbfebdf'
      b'\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07'
      b'\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02'
      b'\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm'
      b'\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9'
      b'|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk'
      b'\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692'
      b'\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android'
      b'\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3pt'
      b'NrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2'
      b'\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014'
      b'\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5')

def _reg_one(pw):
    bj=json.dumps({"app_id":100067,"client_type":2,"password":pw,"source":2},separators=(",",":"))
    sig=hmac.new(KEY,bj.encode(),hashlib.sha256).hexdigest()
    h={"User-Agent":_ua(),"Authorization":f"Signature {sig}",
       "Content-Type":"application/json; charset=utf-8","Accept":"application/json",
       "Connection":"Keep-Alive","Host":"100067.connect.garena.com"}
    for _ in range(4):
        try:
            r=_sess().post(_RU,headers=h,data=bj,timeout=10)
            if r.status_code in(403,429): continue
            b=r.json(); d=b.get("data",b)
            uid=d.get("uid") or b.get("uid")
            if uid: return uid
        except: pass
    return None

def _batch_reg(n):
    pws=[_pw() for _ in range(n)]
    results=[None]*n
    def _do(i): results[i]=_reg_one(pws[i])
    ths=[threading.Thread(target=_do,args=(i,)) for i in range(n)]
    for t in ths: t.start()
    for t in ths: t.join()
    return [(uid,pw) for uid,pw in zip(results,pws) if uid]

def _tok(uid,pw):
    bj=json.dumps({"client_id":100067,"client_secret":KEY.decode("ascii"),"client_type":2,
                   "password":pw,"response_type":"token","uid":uid},separators=(",",":"))
    sig=hmac.new(KEY,bj.encode(),hashlib.sha256).hexdigest()
    h={"User-Agent":_ua(),"Authorization":f"Signature {sig}",
       "Content-Type":"application/json; charset=utf-8","Accept":"application/json",
       "Connection":"Keep-Alive","Host":"100067.connect.garena.com"}
    for _ in range(3):
        try:
            r=_sess().post(_TU,headers=h,data=bj,timeout=10)
            if r.status_code in(403,429): continue
            b=r.json(); d=b.get("data",b)
            if "open_id" in d:
                oi=d["open_id"]; at=d["access_token"]
                res=enc_oid(oi)
                fld=codecs.decode(ue(res["field_14"]),"unicode_escape").encode("latin1")
                return oi,at,fld
        except: pass
    return None,None,None

def _mreg(at,oi,fld,region):
    nm=_nm(); lang=LANG.get(region,"en")
    url,host=(("https://loginbp.common.ggbluefox.com/MajorRegister","loginbp.common.ggbluefox.com")
              if region in("ME","TH") else
              ("https://loginbp.ggblueshark.com/MajorRegister","loginbp.ggblueshark.com"))
    pl=pb({1:nm,2:at,3:oi,5:102000007,6:4,7:1,13:1,14:fld,15:lang,16:1,17:1})
    try:
        _sess().post(url,headers={"Accept-Encoding":"gzip","Authorization":"Bearer",
            "Connection":"Keep-Alive","Content-Type":"application/x-www-form-urlencoded",
            "Expect":"100-continue","Host":host,"ReleaseVersion":"OB53",
            "User-Agent":_ua(),"X-GA":"v1 1","X-Unity-Version":"2018.4."},
            data=aes_bytes(pl.hex()),verify=False,timeout=10)
    except: pass
    return nm

def _mlogin(at,oi,region):
    lang=LANG.get(region,"en")
    url,host=(("https://loginbp.common.ggbluefox.com/MajorLogin","loginbp.common.ggbluefox.com")
              if region in("ME","TH") else
              ("https://loginbp.ggblueshark.com/MajorLogin","loginbp.ggblueshark.com"))
    raw=_LP+lang.encode()+_LP2
    raw=raw.replace(_AT,at.encode()).replace(_OI,oi.encode())
    fp=bytes.fromhex(aes_hex(raw.hex()))
    h={"Accept-Encoding":"gzip","Authorization":"Bearer","Connection":"Keep-Alive",
       "Content-Type":"application/x-www-form-urlencoded","Expect":"100-continue",
       "Host":host,"ReleaseVersion":"OB53","User-Agent":_ua(),
       "X-GA":"v1 1","X-Unity-Version":"2018.4.11f1"}
    for _ in range(5):
        try:
            r=_sess().post(url,headers=h,data=fp,verify=False,timeout=12)
            if r.status_code==200 and len(r.text)>10:
                aid=decode_resp(r.text)
                if aid!="N/A": return aid
        except: pass
    return "N/A"

def _bind(at,region):
    rk="RU" if region=="CIS" else region
    url=("https://loginbp.common.ggbluefox.com/ChooseRegion" if region in("ME","TH")
         else "https://loginbp.ggblueshark.com/ChooseRegion")
    pl=bytes.fromhex(aes_hex(pb({1:rk}).hex()))
    try:
        _sess().post(url,data=pl,headers={"User-Agent":_ua(),"Connection":"Keep-Alive",
            "Accept-Encoding":"gzip","Content-Type":"application/x-www-form-urlencoded",
            "Expect":"100-continue","Authorization":f"Bearer {at}",
            "X-Unity-Version":"2018.4.11f1","X-GA":"v1 1","ReleaseVersion":"OB53"},
            verify=False,timeout=8)
    except: pass

def _process_one(uid,pw,region):
    oi,at,fld=_tok(uid,pw)
    if not oi: return None
    nm=_mreg(at,oi,fld,region)
    aid=_mlogin(at,oi,region)
    if aid=="N/A": return None
    if region!="BR": threading.Thread(target=_bind,args=(at,region),daemon=True).start()
    return{"uid":uid,"pw":pw,"name":nm,"aid":aid}

# ══════════════════════════════════════════════════════════════════
#  OUTPUT
# ══════════════════════════════════════════════════════════════════
def out(res,region):
    global _cnt,_p100t,_p100c
    uid=res["uid"]; pw=res["pw"]; nm=res["name"]; aid=res["aid"]
    t=tier(aid); te=TIER_E[t]; tc=TIER_C[t]; ts=datetime.now().strftime('%H:%M:%S')
    with _tslk: _ts[t]+=1
    with _cnt_lk: _cnt+=1; cur=_cnt
    _stuck_reset()
    _record_speed(cur)
    save({"uid":uid,"password":pw,"account_id":aid,"name":nm,"region":region,
          "tier":t,"created_at":datetime.now().strftime('%Y-%m-%d %H:%M:%S')},t,region)
    _check_boost(aid)
    tot_s=f"/{_total}" if _total>0 else ""
    with _plock:
        sys.stdout.write("\r"+" "*140+"\r")
        print(f"[{ts}] {tc}{B}[{cur}{tot_s}] {te} ID:{aid}{W} | {uid} | {pw}")
        if cur%100==0:
            now=time.time(); el=now-_t0; spd=_current_speed()
            if spd==0 and el>0: spd=cur/el
            el100=now-_p100t if _p100c>0 else el
            with _tslk: ts2=dict(_ts)
            stab_warn=f" {Y}[SPEED LOW!]{W}" if _stab_on else ""
            print(f"\n{C}{B}▶ {cur}{tot_s} | +100:{fmt(el100)} | {spd:.2f}/s{stab_warn}{W}")
            print(f"  {G}🍀:{ts2['NORMAL']}{W} {Y}😬:{ts2['LOW']}{W} "
                  f"{C}🤩:{ts2['MEDIUM']}{W} {M}☠️:{ts2['HIGH']}{W} "
                  f"{R}❤️‍🔥:{ts2['LEGEND']}{W}\n")
            _p100t=now; _p100c=cur

# ══════════════════════════════════════════════════════════════════
#  WORKER
# ══════════════════════════════════════════════════════════════════
def worker(region):
    while True:
        with _cnt_lk:
            if _total>0 and _cnt>=_total: return

        batch=_batch_reg(_BATCH)
        if not batch: continue

        for uid,pw in batch:
            with _cnt_lk:
                if _total>0 and _cnt>=_total: return
            try:
                res=_process_one(uid,pw,region)
            except:
                res=None
            if not res: continue
            with _cnt_lk:
                if _total>0 and _cnt>=_total: return
            out(res,region)

# ══════════════════════════════════════════════════════════════════
#  BOOST INJECTOR
# ══════════════════════════════════════════════════════════════════
def _boost_inj(ex,region):
    extras=[]
    while _stuck_on or (_total>0 and _cnt<_total):
        time.sleep(0.3)
        if _boosting():
            alive=[f for f in extras if not f.done()]
            need=_nw-len(alive)
            for _ in range(max(0,need)):
                try: extras.append(ex.submit(worker,region))
                except: pass
        else:
            extras=[f for f in extras if not f.done()]

# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════
def main():
    global _nw, _total, _cnt, _stuck_on, _boost_on, _DASH_ON, _t0, _p100t, _p100c, _baseline_spd, _stab_on, _spd_window, _stab_extras, _stab_exec, _stab_region
    
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print(f"{render('x6ataza',colors=['white','red'],align='center')}\n")

        while True:
            region=input(f" {B}{R}[+]{W} Region ({'/'.join(sorted(VALID))}) >>> ").upper().strip()
            if region in VALID: break
            print(f"{R}[ ! ] Region tidak valid.{W}")

        while True:
            try:
                j=input(f" {B}{R}[+]{W} Jumlah ID (0=∞) >>> ").strip()
                if j.isdigit() and int(j)>=0: _total=int(j); break
            except: pass

        try:
            wk=input(f" {B}{R}[+]{W} Workers [{_nw}] (max 999) >>> ").strip()
            if wk.isdigit():
                wki=int(wk)
                if wki>=1000:
                    print(f"\n{R}{B}anda gila{W}\n"); sys.exit(0)
                elif wki>0: _nw=wki
        except: pass

        # reset
        _cnt=0
        _stuck_on=True
        _boost_on=False
        _DASH_ON=True
        _t0=time.time()
        _p100t=time.time()
        _p100c=0
        _baseline_spd=0
        _stab_on=False
        _spd_window=[]
        _stab_extras=[]
        
        for k in _ts: _ts[k]=0
        tf(region)

        print(f"\n {C}Region:{W} {region}  |  "
              f"{C}Target:{W} {'∞' if _total==0 else _total}  |  "
              f"{C}Workers:{W} {_nw} (boost:{_nw*2})  |  "
              f"{C}Batch:{W} {_BATCH}/worker\n")

        # Dashboard thread
        dash=threading.Thread(target=_dashboard,daemon=True); dash.start()

        try:
            with ThreadPoolExecutor(max_workers=_nw*2+10) as ex:
                _stab_exec=ex
                _stab_region=region
                futures=[ex.submit(worker,region) for _ in range(_nw)]
                # Boost injector
                threading.Thread(target=_boost_inj,args=(ex,region),daemon=True).start()
                # Speed stabilizer
                threading.Thread(target=_stabilizer,args=(region,),daemon=True).start()
                for f in futures: f.result()
        except KeyboardInterrupt:
            with _plock: print(f"\n{Y}[ ! ] Dihentikan.{W}")

        _stuck_on=False
        _DASH_ON=False
        dash.join(timeout=1)
        _flush_all()

        el=time.time()-_t0; spd=_cnt/el if el>0 else 0
        print(f"\n{LG}{B}✓ {_cnt}{'/' + str(_total) if _total else ''} akun selesai{W}")
        print(f"{C}{B}⏱ {fmt(el)} | {spd:.2f} akun/detik{W}")
        print(f"{LG}{B}📁 {BASE}/{region}/{W}")
        print(f"\n{C}Final:{W} {G}🍀{_ts['NORMAL']}{W} {Y}😬{_ts['LOW']}{W} "
              f"{C}🤩{_ts['MEDIUM']}{W} {M}☠️{_ts['HIGH']}{W} {R}❤️‍🔥{_ts['LEGEND']}{W}")

        try: input(f"\n{W} tekan enter untuk generate ulang.. ")
        except(KeyboardInterrupt,EOFError):
            if _TOR_PROC:
                try: _TOR_PROC.terminate()
                except: pass
            break

if __name__ == "__main__":
    main()
