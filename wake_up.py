import time
import sys
import re  # <--- Módulo adicionado para lidar com múltiplos idiomas
from playwright.sync_api import sync_playwright

# SUBSTITUA PELA URL DO SEU PAINEL DA UEA
STREAMLIT_URL = "https://seu-painel-uea.streamlit.app"

def main():
    print(f"🔄 Iniciando monitorização do painel UEA: {STREAMLIT_URL}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Configurar o idioma do navegador do robô (opcional, mas ajuda na estabilidade)
        page = browser.new_page(locale="pt-BR")
        
        try:
            print("🌐 Navegando para o painel...")
            page.goto(STREAMLIT_URL, wait_until="networkidle", timeout=60000)
            
            # NOVO SELETOR: Deteta o botão em Inglês OU em Português
            padrao_botao = re.compile(r"Wake up app|Sim, vamos restaurar", re.IGNORECASE)
            wake_up_button = page.get_by_role("button", name=padrao_botao)
            
            # ESTRATÉGIA REATIVA: Detetar se a app está a dormir
            if wake_up_button.is_visible():
                print("🚨 [MODO REATIVO]: O painel está em hibernação ('sleep mode').")
                print("🖱️ Clicando no botão para acordar o servidor...")
                wake_up_button.click()
                
                print("⏳ Aguardando a inicialização do contentor do Streamlit...")
                # Aguardar que o próprio botão que acabámos de clicar desapareça
                wake_up_button.wait_for(state="hidden", timeout=180000)
                print("✅ Sucesso! O painel foi acordado e está pronto para uso.")
            
            # ESTRATÉGIA PREVENTIVA: Se já estiver acordada, apenas simular tráfego
            else:
                print("🌿 [MODO PREVENTIVO]: O painel já se encontra ativo.")
                print("⏱️ Mantendo a sessão aberta por 20 segundos para registar tráfego e resetar o temporizador...")
                time.sleep(20)
                print("✅ Tráfego simulado com sucesso. Temporizador de hibernação renovado!")
                
        except Exception as e:
            print(f"❌ Ocorreu um erro durante a execução do RPA: {e}")
            try:
                page.screenshot(path="screenshot_erro.png")
                print("📸 Screenshot do estado do erro guardado como 'screenshot_erro.png'.")
            except Exception:
                pass
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    main()
