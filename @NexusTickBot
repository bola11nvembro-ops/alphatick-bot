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
        print(f"Aviso temporário na API ({par}): {e}")
    return None

def obter_preco_medio(par):
    precos = []
    for _ in range(2):
        p = verificar_preco_real(par)
        if p is not None:
            precos.append(p)
        time.sleep(2.0)  # Pausa maior para evitar bloqueio 429
    if precos:
        return sum(precos) / len(precos)
    return None

def analisar_tendencia_profissional(par):
    p1 = obter_preco_medio(par)
    time.sleep(2)
    p2 = obter_preco_medio(par)
    time.sleep(2)
    p3 = obter_preco_medio(par)
    
    if p1 is None or p2 is None or p3 is None:
        return random.choice(["ACIMA 🟢", "ABAIXO 🔴"])
        
    if p3 > p2 and p2 > p1:
        return "ACIMA 🟢"
    elif p3 < p2 and p2 < p1:
        return "ABAIXO 🔴"
    elif p3 > p1:
        return "ACIMA 🟢"
    else:
        return "ABAIXO 🔴"

def validar_resultado(preco_inicial, preco_atual, direcao):
    if preco_inicial is None or preco_atual is None:
        return False
    diferenca = preco_atual - preco_inicial
    if "ACIMA" in direcao:
        return diferenca > 0.00000
    elif "ABAIXO" in direcao:
        return diferenca < 0.00000
    return False

def iniciar_robo():
    print("🤖 AlphaTick Pro Iniciado com sucesso...")
    enviar_telegram(
        "🚀 **ALPHATICK PRO – ONLINE** 🚀 \n\n"
        "🔄 `Conexão com o Telegram estabelecida.`\n"
        "📋 `Sistema pronto a operar!`"
    )

def main():
    iniciar_robo()
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
                if restante > 5:
                    time.sleep(5)
                else:
                    time.sleep(0.5)
            
            par_atual = random.choice(PARES_ABERTOS)
            direcao = analisar_tendencia_profissional(par_atual)
            
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
            
            preco_inicio = obter_preco_medio(par_atual)
            
            while datetime.now() < (hora_fim_op + timedelta(seconds=5)):
                time.sleep(1)
                
            horario_str = hora_entrada.strftime('%H:%M')
            horario_atual_msg = (datetime.utcnow() + timedelta(hours=1)).strftime('%H:%M')
            
            win_direto = validar_resultado(preco_inicio, obter_preco_medio(par_atual), direcao)
            
            if win_direto:
                historico_sinais.append((par_atual, horario_str, "WIN"))
                enviar_telegram(f"`{horario_str} {par_atual}` — ✅\n\n`{horario_atual_msg}`\n\n **WIN** 🟢")
            else:
                enviar_telegram(f"⚠️ **Loss na 1ª vela** — A aguardar fecho do 1º GALE às `{hora_gale1.strftime('%H:%M')}`...")
                while datetime.now() < (hora_gale1 + timedelta(seconds=5)):
                    time.sleep(1)
                    
                win_gale1 = validar_resultado(preco_inicio, obter_preco_medio(par_atual), direcao)
                if win_gale1:
                    historico_sinais.append((par_atual, horario_str, "WIN GALE 1"))
                    enviar_telegram(f"`{horario_str} {par_atual}` — ✅ (GALE 1) 🟢")
                else:
                    enviar_telegram(f"⚠️ **Loss no GALE 1** — A aguardar fecho do 2º GALE às `{hora_gale2.strftime('%H:%M')}`...")
                    while datetime.now() < (hora_gale2 + timedelta(seconds=5)):
                        time.sleep(1)
                        
                    win_gale2 = validar_resultado(preco_inicio, obter_preco_medio(par_atual), direcao)
                    if win_gale2:
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
