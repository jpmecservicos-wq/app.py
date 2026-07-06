import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração profissional da plataforma
st.set_page_config(page_title="J&P MEC - Gestão de Equipamentos", page_icon="⚙️", layout="wide")

# -----------------------------------------------------------------------------
# EXIBIÇÃO DO LOGO OFICIAL DA J&P MEC
# -----------------------------------------------------------------------------
logo_url = "https://githubusercontent.com"
st.image(logo_url, width=350)

st.markdown("---")

# Inicialização dos bancos de dados na memória do sistema
if "dados_oficina" not in st.session_state:
    st.session_state.dados_oficina = []

if "cadastro_empresas" not in st.session_state:
    # Exemplo inicial de empresa cadastrada para teste
    st.session_state.cadastro_empresas = [
        {"Empresa": "Cliente Particular / Sem CNPJ", "CNPJ": "00.000.000/0000-00", "Contato": "N/A"}
    ]

# Divisão das telas de trabalho por abas de processo
aba_clientes, aba_entrada, aba_orcamento, aba_painel = st.tabs([
    "🏢 1. Cadastro de Empresas",
    "📋 2. Entrada e Inspeção Visual", 
    "💰 3. Orçamentos e Laudo Técnico", 
    "🔍 4. Painel Geral de Ordens (Pátio)"
])

# -----------------------------------------------------------------------------
# ABA 1: CADASTRO DE EMPRESAS / CLIENTES FIXOS
# -----------------------------------------------------------------------------
with aba_clientes:
    st.header("🏢 Cadastro de Novas Empresas / Clientes")
    st.markdown("Registre aqui os dados das empresas parceiras para usá-los nas Ordens de Serviço.")
    
    with st.form("form_cadastro_empresa", clear_on_submit=True):
        col_emp1, col_emp2 = st.columns(2)
        with col_emp1:
            nome_empresa = st.text_input("Razão Social / Nome da Empresa")
            cnpj_empresa = st.text_input("CNPJ / CPF")
        with col_emp2:
            contato_empresa = st.text_input("Telefone de Contato (WhatsApp)")
            
        botao_empresa = st.form_submit_button("Salvar Cadastro de Empresa 💾")
        
    if botao_empresa:
        if nome_empresa:
            nova_empresa = {
                "Empresa": nome_empresa,
                "CNPJ": cnpj_empresa if cnpj_empresa else "Não informado",
                "Contato": contato_empresa if contato_empresa else "Não informado"
            }
            st.session_state.cadastro_empresas.append(nova_empresa)
            st.success(f"✔️ Empresa **{nome_empresa}** cadastrada com sucesso! Ela já está disponível na aba de Entrada.")
        else:
            st.error("❌ Erro: O nome da empresa é obrigatório.")
            
    st.markdown("### 📋 Empresas Registradas")
    df_empresas = pd.DataFrame(st.session_state.cadastro_empresas)
    st.dataframe(df_empresas, use_container_width=True)

# -----------------------------------------------------------------------------
# ABA 2: ENTRADA DO EQUIPAMENTO E CHECK-IN DE SEGURANÇA
# -----------------------------------------------------------------------------
with aba_entrada:
    st.header("Formulário de Entrada e Recebimento")
    
    with st.form("form_entrada_jpmec", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("#️⃣ Seleção do Cliente")
            lista_empresas_disponiveis = [emp["Empresa"] for emp in st.session_state.cadastro_empresas]
            empresa_selecionada = st.selectbox("Selecione a Empresa Cadastrada", lista_empresas_disponiveis)
            
            st.subheader("🚜 Ficha do Equipamento")
            tipo_equipamento = st.selectbox(
                "Categoria", 
                ["Compressor a Diesel", "Gerador de Energia", "Caminhão / Linha Pesada", "Veículo Leve", "Outro"]
            )
            modelo = st.text_input("Modelo / Marca (Ex: Atlas Copco XA 125 / Doosan 7/41)")
            ano_fabricacao = st.text_input("Ano de Fabricação")
            serial_chassi = st.text_input("Número de Série / Placa (Chave de Rastreabilidade)")
            
        with col2:
            st.subheader("📊 Condições Operacionais de Entrada")
            horimetro = st.number_input("Horímetro Atual (Horas de Uso - Crítico)", min_value=0, step=1)
            kilometragem = st.number_input("Quilometragem (Se aplicável)", min_value=0, step=1)
            
            status_partida = st.selectbox(
                "Condição Mecânica de Entrada",
                ["Funciona / Operacional", "Liga mas não Comprime/Gera", "Motor Diesel Travado", "Equipamento Desmontado"]
            )
            reclamacao_cliente = st.text_area("Sintomas relatados pelo cliente")

        st.markdown("---")
        st.subheader("🔍 1ª Inspeção Visual de Recebimento")
        col_insp1, col_insp2 = st.columns(2)
        
        with col_insp1:
            insp_vazamentos = st.selectbox("Vazamentos Externos Aparentes", ["Nenhum visível", "Óleo Lubrificante Motor", "Óleo Unidade Compressora", "Líquido de Arrefecimento", "Diesel"])
            insp_carenagem = st.selectbox("Estado de Carenagens e Portas", ["Intactas", "Amassados leves", "Portas desalinhadas/Sem travas", "Faltando tampas protetoras"])
            insp_painel = st.selectbox("Painel Elétrico / Controladores", ["Perfeito estado", "Visor quebrado/Digital ilegível", "Sem botões / Chave de partida danificada"])
            
        with col_insp2:
            insp_faltantes = st.text_input("Acessórios ou Itens Faltantes (Ex: Sem Bateria, Sem Engate)", value="Nenhum")
            insp_rodado = st.selectbox("Eixo / Pneus / Sistema de Reboque", ["Bom estado", "Pneus danificados", "Sem rodas (Fixo sobre base)", "Não se aplica"])
            obs_inspecao = st.text_area("Observações Técnicas Visuais Complementares")

        st.markdown("---")
        botao_salvar = st.form_submit_button("Emitir Ordem de Entrada 🚀")

    if botao_salvar:
        if modelo and serial_chassi:
            numero_os = len(st.session_state.dados_oficina) + 1001
            
            cnpj_v = "Não informado"
            contato_v = "Não informado"
            for emp in st.session_state.cadastro_empresas:
                if emp["Empresa"] == empresa_selecionada:
                    cnpj_v = emp["CNPJ"]
                    contato_v = emp["Contato"]
            
            novo_registro = {
                "OS": f"#{numero_os}",
                "Data Entrada": datetime.now().strftime("%d/%m/%Y"),
                "Cliente": empresa_selecionada,
                "CNPJ Cliente": cnpj_v,
                "Contato": contato_v,
                "Equipamento": tipo_equipamento,
                "Modelo": modelo,
                "Ano": ano_fabricacao,
                "Nº Série": serial_chassi,
                "Horímetro": horimetro,
                "KM": kilometragem,
                "Partida": status_partida,
                "Queixa Cliente": reclamacao_cliente,
                "Vazamentos": insp_vazamentos,
                "Carenagem": insp_carenagem,
                "Painel": insp_painel,
                "Faltantes": insp_faltantes,
                "Rodado": insp_rodado,
                "Obs Visuais": obs_inspecao,
                "Laudo Técnico": "Não diagnosticado",
                "Mão de Obra (R$)": 0.0,
                "Peças (R$)": 0.0,
                "Total Geral (R$)": 0.0,
                "Status": "Aguardando Diagnóstico"
            }
            
            st.session_state.dados_oficina.append(novo_registro)
            st.success(f"✔️ Equipamento registrado! **OS J&P MEC #{numero_os}** vinculada à empresa **{empresa_selecionada}**.")
        else:
            st.error("❌ Atenção: Modelo e Número de Série são campos obrigatórios para garantir o rastreio.")

# -----------------------------------------------------------------------------
# ABA 3: LAUDO TÉCNICO E COMPOSIÇÃO DE ORÇAMENTO
# -----------------------------------------------------------------------------
with aba_orcamento:
    st.header("Análise Técnico-Comercial")
    
    if st.session_state.dados_oficina:
        lista_os = [reg["OS"] for reg in st.session_state.dados_oficina]
        os_selecionada = st.selectbox("Selecione a Ordem de Serviço:", lista_os)
        
        for reg in st.session_state.dados_oficina:
            if reg["OS"] == os_selecionada:
                st.markdown(f"⚙️ **Equipamento:** {reg['Equipamento']} {reg['Modelo']} | **Série:** {reg['Nº Série']} | **Cliente:** {reg['Cliente']}")
                
                with st.form("form_valores_jpmec"):
                    st.subheader("🔬 Diagnóstico do Especialista")
                    laudo = st.text_area("Laudo Técnico Real (Defeitos encontrados após desmontagem/testes)", value=reg["Laudo Técnico"])
                    
                    st.subheader("💸 Orçamento Comercial")
                    col_orc1, col_orc2 = st.columns(2)
                    with col_orc1:
                        v_mao_de_obra = st.number_input("Mão de Obra Técnica (R$)", min_value=0.0, value=float(reg["Mão de Obra (R$)"]), format="%.2f")
                        v_pecas = st.number_input("Peças e Insumos Aplicados (R$)", min_value=0.0, value=float(reg["Peças (R$)"]), format="%.2f")
                    
                    with col_orc2:
                        opcoes_status = [
                            "Aguardando Diagnóstico", 
                            "Orçamento em Análise pelo Cliente", 
                            "Aprovado - Em Manutenção", 
                        with col_orc2:
                        opcoes_status = [
                            "Aguardando Diagnóstico", 
                            "Orçamento em Análise pelo Cliente", 
                            "Aprovado - Em Manutenção", 
                            "Pronto para Retirada", 
                            "Entregue / Concluído", 
                            "Recusado / Sem Conserto"
                        ]
                        
                        if reg["Status"] in opcoes_status:
                            idx_atual = opcoes_status.index(reg["Status"])
                        else:
                            idx_atual = 0
                            
                        novo_status = st.selectbox(
                            "Situação Atual do Equipamento",
                            options=opcoes_status,
                            index=idx_atual
                        )
