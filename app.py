import streamlit as st

alap_ber = 1860
esti_bonusz = 1.30
unnepnapok = ["01/01", "15/03", "01/05", "20/08", "23/10", "01/11", "25/12", "26/12"]
orankenti_bonusz = {
    150: 40000,
    120: 25000,
    100: 20000,
    80: 15000
    }

def atvaltas(ido_szoveg):
    ora, perc = ido_szoveg.split(":")
    return int(ora) + (int(perc) / 60)

def szunet_szamitas(teljes_hossz):
    if teljes_hossz > 9:
        return 1.0
    if teljes_hossz > 6:
        return 0.5
    return 0.0

def muszak_bontas(kezdes, vegzes):
    if vegzes < kezdes:
        vegzes += 24
        
    szunet = szunet_szamitas(vegzes - kezdes)
    
    hat_elott = max(0, min(vegzes, 18) - kezdes)
    hat_utan = max(0, vegzes - max(kezdes, 18))
    
    levonas_elott = min(hat_elott, szunet)
    hat_elott -= levonas_elott
    hat_utan -= (szunet - levonas_elott)
    
    return hat_elott, hat_utan

def havi_bonusz_szamitas(osszes_ora):
    for ora_hatar, bonusz in orankenti_bonusz.items():
        if osszes_ora >= ora_hatar:
            return bonusz
    return 0
    
st.title("Fizetés Számoló")
szoveg = st.text_area("Illeszd be a műszakokat (NN/HH ÓÓ:PP-ÓÓ:PP):", height=200)

if st.button("Számolás", type="primary"):
    osszes_ora = 0
    alap_fizu = 0
    for sor in szoveg.strip().splitlines():
        if not sor.strip():
            continue
        datum, muszak = sor.strip().split(" ")
        kezdes, vegzes = map(atvaltas, muszak.split("-"))
        hat_elott, hat_utan = muszak_bontas(kezdes, vegzes)
        napi_szorzo = 2 if datum in unnepnapok else 1
        osszes_ora += hat_elott + hat_utan
        alap_fizu += ((hat_elott * alap_ber) + (hat_utan * alap_ber * esti_bonusz)) * napi_szorzo

    havi_bonusz = havi_bonusz_szamitas(osszes_ora)
    vegso_fizu = alap_fizu + havi_bonusz

    st.metric("Kifizetendő összeg", f"{round(vegso_fizu)} Ft")
    st.write(f"**Ledolgozott órák:** {round(osszes_ora, 2)} | **Havi bónusz:** {havi_bonusz} Ft")
