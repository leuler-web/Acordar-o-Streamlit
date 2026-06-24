import time
import sys
from playwright.sync_api import sync_playwright

# SUBSTUIE PELA URL DO SEU PAINEL DA UEA
STREAMLIT_URL = "https://painel-execucao-uea-ehehdodxwmzduvxmjgw78f.streamlit.app/"

def main():
    print(f"🔄 Iniciando monitorização do painel UEA: {STREAMLIT_URL}")
    
    with sync_playwright() as p:
        # Lançar o navegador em modo headless (sem interface gráfica)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Aceder à aplicação e aguardar até que a rede acalme
            print("🌐 Navegando para o painel...")
            page.goto(STREAMLIT_URL, wait_until="networkidle", timeout=60000)
            
            # Localizar o botão de "Wake up app" pelo texto visível
            wake_up_button = page.get_by_role("button", name="Wake up app", exact=False)
            
            # ESTRATÉGIA REATIVA: Detetar se a app está a dormir
            if wake_up_button.is_visible():
                print("🚨 [MODO REATIVO]: O painel está em hibernação ('sleep mode').")
                print("🖱️ Clicando no botão 'Wake up app' para acordar o servidor...")
                wake_up_button.click()
                
                # Aguardar que o botão desapareça ou que a app carregue (tempo limite de 3 minutos)
                print("⏳ Aguardando a inicialização do contentor do Streamlit...")
                page.wait_for_selector("text=Wake up app", state="hidden", timeout=180000)
                print("✅ Sucesso! O painel foi acordado e está pronto para uso.")
            
            # ESTRATÉGIA PREVENTIVA: Se já estiver acordada, apenas simular tráfego
            else:
                print("🌿 [MODO PREVENTIVO]: O painel já se encontra ativo.")
                print("⏱️ Mantendo a sessão aberta por 20 segundos para registar tráfego e resetar o temporizador...")
                time.sleep(20)
                print("✅ Tráfego simulado com sucesso. Temporizador de hibernação renovado!")
                
        except Exception as e:
            print(f"❌ Ocorreu um erro durante a execução do RPA: {e}")
            # Capturar um screenshot do erro para facilitar o debug nos artefactos do GitHub
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