import time
import sys
from playwright.sync_api import sync_playwright

# 🌐 URL REAL DO SEU PAINEL DA UEA
STREAMLIT_URL = "https://painel-execucao-uea-ehehdodxwmzduvxmjgw78f.streamlit.app/"

def main():
    print(f"🔄 Iniciando monitorização do painel UEA: {STREAMLIT_URL}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("🌐 Navegando para o painel...")
            page.goto(STREAMLIT_URL, wait_until="networkidle", timeout=60000)
            
            # Pausa de 5 segundos para garantir que tudo carregou internamente
            page.wait_for_timeout(5000)
            
            botao_acordar = None
            
            # 1. Tentar encontrar o botão na página principal
            botao_principal = page.locator('[data-testid="wakeup-button-viewer"]')
            if botao_principal.is_visible():
                botao_acordar = botao_principal
                print("🎯 Botão de hibernação encontrado na página principal!")
            
            # 2. Se não encontrar, procurar dentro de possíveis IFRAMEs (janelas internas)
            if not botao_acordar:
                print("🔍 Botão não visível na página principal. Procurando dentro de frames internos...")
                for frame in page.frames:
                    botao_no_frame = frame.locator('[data-testid="wakeup-button-viewer"]')
                    if botao_no_frame.is_visible():
                        botao_acordar = botao_no_frame
                        print("🎯 Botão de hibernação localizado dentro de um frame interno!")
                        break
            
            # ESTRATÉGIA REATIVA: Se o botão foi encontrado em algum lugar
            if botao_acordar:
                print("🚨 [MODO REATIVO]: O painel está em hibernação ('sleep mode').")
                print("🖱️ Clicando no botão para acordar o servidor...")
                botao_acordar.click()
                
                print("⏳ Aguardando a inicialização do contentor do Streamlit...")
                # Esperar 45 segundos para dar tempo do Streamlit subir a aplicação
                page.wait_for_timeout(45000)
                print("✅ Sucesso! Comando de inicialização enviado.")
            
            # ESTRATÉGIA PREVENTIVA: Se o botão não apareceu em lado nenhum
            else:
                print("🌿 [MODO PREVENTIVO]: O botão de acordar não foi visto. O painel já deve estar ativo.")
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
