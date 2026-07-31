import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
import time
import random

TELEGRAM_TOKEN = "8649700861:AAGtH_jiMasG9kw9RdrAqdiesPDsEB6-MwQ"
CHAT_ID = "771454310"

PARES_ABERTOS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD",
    "EUR/GBP", "EUR/JPY", "USD/CHF",
    "USD/CAD", "NZD/USD", "EUR/AUD", "GBP/AUD"
]

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"}
    data = urllib.parse.urlencode(payload).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"Erro Telegram: {e}")

def verificar_preco_real(par):
    try:
        simbolo = par.replace("/", "")
        url = f"https://economia.awesomeapi.com.br/json/last/{simbolo}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            dados = json.loads(response.read().decode())
            chave = simbolo
            if chave in dados:
                return float(dados[chave]["bid"])
    except Exception as e:
        print(f"Aviso temporário na API {par}: {e}")
    return None

def obter_preco_medio(par):
    precos = []
    for _ in range(3):
        p = verificar_preco_real(par)
        if p is not None:
            precos.append(p)
        time.sleep(0.5)
    if precos:
        return sum(precos) / len(precos)
    return None

def analisar_tendencia_profissional(par):
    p1 = obter_preco_medio(par)
    time.sleep(1)
    p2 = obter_preco_medio(par)
    time.sleep(1)
    p3 = obter_preco_medio(par)
    
    if p1 is None or p2 is None or p3 is None:
        return None
        
    if p3 > p2 > p1:
        return "CALL (COMPRA) 🟢"
    elif p3 < p2 < p1:
        return "PUT (VENDA) 🔴"
    return None

def main():
    enviar_telegram("🤖 AlphaTick Pro (Nuvem 24/7) Ativo e Operacional!")
    print("🤖 Robô iniciado com sucesso!")
    
    while True:
        try:
            par_escolhido = random.choice(PARES_ABERTOS)
            direcao = analisar_tendencia_profissional(par_escolhido)
            
            if direcao:
                agora = datetime.utcnow() + timedelta(hours=1)
                hora_sinal = agora.strftime('%H:%M')
                
                mensagem = (
                    f"📊 *NOVO SINAL INSTITUCIONAL* 📊\n\n"
                    f"💱 Par: *{par_escolhido}*\n"
                    f"⏰ Hora: *{hora_sinal} (M5)*\n"
                    f"📈 Direção: *{direcao}*\n"
                    f"⚠️ Estratégia: *Price Action & Média Móvel*"
                )
                enviar_telegram(mensagem)
            
            time.sleep(300)
        except Exception as e:
            print(f"Erro no ciclo principal: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
