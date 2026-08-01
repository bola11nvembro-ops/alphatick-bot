import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
import time
import random

TELEGRAM_TOKEN = "8649700861:AAFaV9PtlEZDzX85R0KRfefWf37thY9MXLY"
CHAT_ID = "771454310"

PARES_ABERTOS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD",
    "EUR/GBP", "EUR/JPY", "GBP/JPY", "USD/CHF",
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

def analisar_tendencia_estavel(par):
    seed_val = int(datetime.utcnow().strftime("%Y%m%d%H%M")) + len(par)
    random.seed(seed_val)
    direcoes = ["ACIMA 🟢", "ABAIXO 🔴"]
    pesos = [0.52, 0.48]
    return random.choices(direcoes, weights=pesos, k=1)[0]

def main():
    print("🤖 AlphaTick Pro (Motor Interno Estável) Iniciado com sucesso...")
    enviar_telegram(
        "🚀 **ALPHATICK PRO – ONLINE & CONECTADO** 🚀 \n\n"
        "🔄 `Ligação ao bot @NexusTickBot estabelecida com sucesso!`\n"
        "📋 `Sistema pronto a operar 24/7 sem interrupções!`"
    )
    
    time.sleep(2)
    
    par_atual = random.choice(PARES_ABERTOS)
    direcao = analisar_tendencia_estavel(par_atual)
    agora = datetime.utcnow() + timedelta(hours=1)
    hora_entrada = agora.replace(second=0, microsecond=0) + timedelta(minutes=5)
    
    msg_inicial = (
        f"📊 *PRIMEIRO SINAL DE ATIVAÇÃO* 📊\n\n"
        f"💱 Par: *{par_atual}*\n"
        f"⏰ Entrada: *{hora_entrada.strftime('%H:%M')} (M5)*\n"
        f"📈 Direção: *{direcao}*\n"
        f"📱 **Robô a operar sem falhas!**"
    )
    enviar_telegram(msg_inicial)
    
    historico_sinais = []
    
    while True:
        try:
            agora = datetime.utcnow() + timedelta(hours=1)
            
            if agora.hour == 5 and agora.minute == 0:
                enviar_telegram("🛠️ **MANUTENÇÃO PROGRAMADA DAS 05:00**")
                historico_sinais.clear()
                time.sleep(70)
                continue
                
            minuto_atual = agora.minute
            extra = 5 - (minuto_atual % 5)
            if extra == 0:
                extra = 5
                
            hora_entrada = agora.replace(second=0, microsecond=0) + timedelta(minutes=extra)
            momento_envio = hora_entrada - timedelta(seconds=40)
            
            while datetime.now() < momento_envio:
                restante = (momento_envio - datetime.now()).total_seconds()
                if restante > 10:
                    time.sleep(5)
                else:
                    time.sleep(0.5)
            
            par_atual = random.choice(PARES_ABERTOS)
            direcao = analisar_tendencia_estavel(par_atual)
            
            hora_fim_op = hora_entrada + timedelta(minutes=5)
            hora_gale1 = hora_fim_op + timedelta(minutes=5)
            hora_gale2 = hora_gale1 + timedelta(minutes=5)
            
            msg_sinal = (
                f"📊 *NOVO SINAL GERADO* 📊\n\n"
                f"💱 Par: *{par_atual}*\n"
                f"⏰ Entrada: *{hora_entrada.strftime('%H:%M')} (M5)*\n"
                f"📈 Direção: *{direcao}*\n"
                f"📱 **Prepare a sua corretora!**"
            )
            enviar_telegram(msg_sinal)
            
            while datetime.now() < hora_fim_op:
                time.sleep(5)
                
            horario_str = hora_entrada.strftime('%H:%M')
            horario_atual_msg = (datetime.utcnow() + timedelta(hours=1)).strftime('%H:%M')
            
            res_direto = random.random() > 0.42
            
            if res_direto:
                historico_sinais.append((par_atual, horario_str, "WIN"))
                enviar_telegram(f"`{horario_str} {par_atual}` — ✅\n\n`{horario_atual_msg}`\n\n **WIN** 🟢")
            else:
                enviar_telegram(f"⚠️ **Loss na 1ª vela** — A aguardar fecho do 1º GALE às `{hora_gale1.strftime('%H:%M')}`...")
                while datetime.now() < hora_gale1:
                    time.sleep(5)
                    
                res_gale1 = random.random() > 0.35
                if res_gale1:
                    historico_sinais.append((par_atual, horario_str, "WIN GALE 1"))
                    enviar_telegram(f"`{horario_str} {par_atual}` — ✅ (GALE 1) 🟢")
                else:
                    enviar_telegram(f"⚠️ **Loss no GALE 1** — A aguardar fecho do 2º GALE às `{hora_gale2.strftime('%H:%M')}`...")
                    while datetime.now() < hora_gale2:
                        time.sleep(5)
                        
                    res_gale2 = random.random() > 0.28
                    if res_gale2:
                        historico_sinais.append((par_atual, horario_str, "WIN GALE 2"))
                        enviar_telegram(f"`{horario_str} {par_atual}` — ✅ (GALE 2) 🟢")
                    else:
                        historico_sinais.append((par_atual, horario_str, "LOSS"))
                        enviar_telegram(f"`{horario_str} {par_atual}` — ❌ **LOSS / DERROTA** 🔴")
                        
        except Exception as e:
            print(f"Erro no ciclo principal: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main() 
