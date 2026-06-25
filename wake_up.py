import time
import sys
from playwright.sync_api import sync_playwright

# SUBSTITUA PELA URL REAL DO SEU PAINEL DA UEA
STREAMLIT_URL = "https://seu-painel-uea.streamlit.app"

def main():
    print(f"🔄 Iniciando monitorização do painel UEA: {STREAMLIT_URL}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("🌐 Navegando para o painel...")
            page.goto(STREAMLIT_URL, wait_until="networkidle", timeout=60000)
            
            # Pequena pausa para garantir a renderização completa da página do Streamlit
            page.wait_for_timeout(5000)
            
            # 🎯 O LOCALIZADOR DEFINITIVO: Procura diretamente pelo ID de teste do botão!
            botao_acordar = page.locator('[data-testid="wakeup-button-viewer"]')
            
            # ESTRATÉGIA REATIVA: Se o botão for detetado e estiver visível
            if botao_acordar.is_visible():
                print("🚨 [MODO REATIVO]: O painel está em hibernação ('sleep mode').")
                print("🖱️ Clicando no botão para acordar o servidor...")
                botao_acordar.click()
                
                print("⏳ Aguardando a inicialização do contentor do Streamlit...")
                # Esperar 45 segundos para a máquina virtual do Streamlit carregar na nuvem
                page.wait_for_timeout(45000)
                print("✅ Sucesso! Comando de inicialização enviado.")
            
            # ESTRATÉGIA PREVENTIVA: Se não encontrou o botão
            else:
                print("🌿 [MODO PREVENTIVO]: O botão de acordar não está visível. O painel já deve estar ativo.")
                print("⏱️ Mantendo a sessão aberta por 20 segundos para registar tráfego...")
                page.wait_for_timeout(20000)
                print("✅ Tráfego simulado com sucesso!")
                
        except Exception as e:
            print(f"❌ Ocorreu um erro durante a execução do RPA: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    main()
