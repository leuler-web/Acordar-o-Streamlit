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
            page.goto(STREAMLIT_URL, wait_until="domcontentloaded", timeout=60000)
            
            botao_acordar = None
            seletor_botao = '[data-testid="wakeup-button-viewer"]'
            
            # 1. Tentar aguardar ativamente o botão surgir na página principal (até 15 segundos)
            print("🔍 Verificando se a tela de hibernação vai carregar...")
            try:
                loc = page.locator(seletor_botao)
                loc.wait_for(state="visible", timeout=15000)
                botao_acordar = loc
                print("🎯 Botão de hibernação detectado na página principal!")
            except Exception:
                # 2. Se não aparecer na principal, procurar ativamente nos frames internos
                print("🔍 Botão não surgiu na página principal. Verificando frames internos...")
                for frame in page.frames:
                    try:
                        loc_frame = frame.locator(seletor_botao)
                        loc_frame.wait_for(state="visible", timeout=3000)
                        botao_acordar = loc_frame
                        print("🎯 Botão de hibernação localizado num frame interno!")
                        break
                    except Exception:
                        pass
            
            # ESTRATÉGIA REATIVA: Se o botão for confirmado
            if botao_acordar:
                print("🚨 [MODO REATIVO]: O painel está em hibernação ('sleep mode').")
                print("🖱️ Clicando no botão para acordar o servidor...")
                botao_acordar.click()
                
                print("⏳ Aguardando a inicialização do contentor do Streamlit...")
                page.wait_for_timeout(45000)
                print("✅ Sucesso! Comando de inicialização enviado.")
            
            # ESTRATÉGIA PREVENTIVA: Se após a espera o botão realmente não existir
            else:
                print("🌿 [MODO PREVENTIVO]: Nenhum botão de hibernação apareceu. O painel está ativo.")
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
