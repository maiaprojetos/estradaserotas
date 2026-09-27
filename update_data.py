import io, json, re, zipfile
from pathlib import Path
import requests
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
DATA.mkdir(exist_ok=True)
UA={"User-Agent":"MapaRodoviarioBrasilV3/1.0"}

def clean(v):
    if pd.isna(v): return None
    if hasattr(v,"item"):
        try: v=v.item()
        except Exception: pass
    return v

def pick_col(df, names):
    low={str(c).strip().lower():c for c in df.columns}
    for n in names:
        if n in low:return low[n]
    for c in df.columns:
        s=str(c).strip().lower()
        if any(n in s for n in names): return c
    return None

def coords(df):
    lat=pick_col(df,["latitude","lat","lat_decimal","latitude_decimal"])
    lon=pick_col(df,["longitude","lon","lng","long","longitude_decimal"])
    if not lat or not lon:return None,None
    a=pd.to_numeric(df[lat],errors="coerce"); b=pd.to_numeric(df[lon],errors="coerce")
    # Handle common Brazilian decimal-comma strings.
    if a.isna().mean()>0.9:
        a=pd.to_numeric(df[lat].astype(str).str.replace(".","",regex=False).str.replace(",",".",regex=False),errors="coerce")
    if b.isna().mean()>0.9:
        b=pd.to_numeric(df[lon].astype(str).str.replace(".","",regex=False).str.replace(",",".",regex=False),errors="coerce")
    # Some datasets store longitude as positive west; normalize.
    b=b.where(b<=0,-b)
    return a,b

def frame_json(df):
    la,lo=coords(df)
    if la is None:return []
    out=[]
    for i,row in df.iterrows():
        lat,lon=la.loc[i],lo.loc[i]
        if pd.isna(lat) or pd.isna(lon) or abs(float(lat))>40 or abs(float(lon))>75:continue
        d={"lat":float(lat),"lon":float(lon)}
        for c in df.columns:
            if c in []:continue
            v=clean(row[c])
            if v is not None:
                d[str(c)]=v
        out.append(d)
    return out

def write(name, obj):
    (DATA/name).write_text(json.dumps(obj,ensure_ascii=False,default=str),encoding="utf-8")

def prf():
    page=requests.get("https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf",headers=UA,timeout=40).text
    ids=re.findall(r"drive\.google\.com/file/d/([A-Za-z0-9_-]+)",page)
    if not ids:return
    r=requests.get(f"https://drive.google.com/uc?export=download&id={ids[0]}",headers=UA,timeout=120)
    z=zipfile.ZipFile(io.BytesIO(r.content))
    csvs=[n for n in z.namelist() if n.lower().endswith(".csv")]
    if not csvs:return
    with z.open(csvs[0]) as f:
        df=pd.read_csv(f,sep=";",encoding="latin1",low_memory=False)
    write("prf_acidentes.json",frame_json(df))

def ckan(pkg):
    u=f"https://servicos.dnit.gov.br/dadosabertos/api/3/action/package_show?id={pkg}"
    return requests.get(u,headers=UA,timeout=40).json()["result"]["resources"]

def latest(resources):
    cand=[r for r in resources if r.get("url")]
    cand.sort(key=lambda r:(str(r.get("last_modified") or r.get("created") or ""),str(r.get("name") or r.get("description") or "")),reverse=True)
    return cand[0] if cand else None

def dnit():
    r=latest(ckan("condicoes-do-pavimento"))
    if r:
        raw=requests.get(r["url"],headers=UA,timeout=120).content
        try:df=pd.read_csv(io.BytesIO(raw),sep=";",encoding="latin1",low_memory=False)
        except Exception:df=pd.read_csv(io.BytesIO(raw),low_memory=False)
        write("dnit_pavimento.json",frame_json(df))
    r=latest(ckan("controle-de-velocidade"))
    if r:
        raw=requests.get(r["url"],headers=UA,timeout=120).content
        df=pd.read_excel(io.BytesIO(raw))
        write("dnit_radares.json",frame_json(df))

if __name__=="__main__":
    for fn in (prf,dnit):
        try: fn()
        except Exception as e: print("Falha:",fn.__name__,e)
