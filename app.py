import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração profissional da plataforma
st.set_page_config(page_title="J&P MEC - Gestão de Equipamentos", page_icon="⚙️", layout="wide")

# -----------------------------------------------------------------------------
# CABEÇALHO CORPORATIVO FIXO (PADRÃO GRANDES EMPRESAS)
# -----------------------------------------------------------------------------
st.title("⚙️ J&P MEC - SERVIÇOS")
st.subheader("Soluções confiáveis para: Máquinas, Veículos e Equipamentos em geral.")

# Box com os dados oficiais informados para validação visual
st.info(
    "📍 **Endereço:** Av. Dionísio Gomes, 1130, Veneza, Ribeirão das Neves - MG | "
    "📄 **CNPJ:** 37.825.666/0001-99\n\n"
    "📞 **Contato:** (31) 99288-8039 | ✉️ **E-mail:** jpmecservicos@gmail.com"
)
st.markdown("---")

# Inicialização do banco de dados na memória do sistema
if "dados_oficina" not in st.session_state:
    st.session_state.dados_oficina = []

# Divisão das telas de trabalho por abas de processo
aba_entrada, aba_orcamento, aba_painel = st.tabs([
    "📋 1. Entrada e Inspeção Visual", 
    "💰 2. Orçamentos e Laudo Técnico", 
    "🔍 3. Painel Geral de Ordens (Pátio)"
])

# -----------------------------------------------------------------------------
# ABA 1: ENTRADA DO EQUIPAMENTO E CHECK-IN DE SEGURANÇA
# -----------------------------------------------------------------------------
with aba_entrada:
    st.header("Formulário de Entrada e Recebimento")
    
    with st.form("form_entrada_jpmec", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Identificação do Cliente")
            cliente = st.text_input("Razão Social / Nome Completo do Cliente")
            contato_cliente = st.text_input("Telefone ou Responsável Direto")
            
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

        # Seção de Inspeção Visual Obrigatória (Proteção Jurídica)
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
        if cliente and modelo and serial_chassi:
            # Gerador automático do número da OS sequencial
            numero_os = len(st.session_state.dados_oficina) + 1001
            
            novo_registro = {
                "OS": f"#{numero_os}",
                "Data Entrada": datetime.now().strftime("%d/%m/%Y"),
                "Cliente": cliente,
                "Contato": contato_cliente,
                "Equipamento": tipo_equipamento,
                "Modelo": modelo,
                "Ano": ano_fabricacao,
                "Nº Série": serial_chassi,
                "Horímetro": horimetro,
                "KM": list([kilometragem]),
                "Partida": status_partida,
                "Queixa Cliente": reclamacao_cliente,
                "Vazamentos": insp_vazamentos,
                "Carenagem": insp_carenagem,
                "Painel": insp_painel,
                "Faltantes": insp_faltantes,
                "Rodado": insp_rodado,
                "Obs Visuais": obs_inspecao,
                # Financeiro e técnico que iniciam zerados
                "Laudo Técnico": "Não diagnosticado",
                "Mão de Obra (R$)": 0.0,
                "Peças (R$)": 0.0,
                "Total Geral (R$)": 0.0,
                "Status": "Aguardando Diagnóstico"
            }
            
            st.session_state.dados_oficina.append(novo_registro)
            st.success(f"✔️ Equipamento registrado! **OS J&P MEC #{numero_os}** criada com sucesso.")
        else:
            st.error("❌ Atenção: Cliente, Modelo e Número de Série são campos obrigatórios para garantir o rastreio.")

# -----------------------------------------------------------------------------
# ABA 2: LAUDO TÉCNICO E COMPOSIÇÃO DE ORÇAMENTO
# -----------------------------------------------------------------------------
with aba_orcamento:
    st.header("Análise Técnica e Valores")
    
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
                        novo_status = st.selectbox(
                            "Situação Atual do Equipamento",
                            ["Aguardando Diagnóstico", "Orçamento em Análise pelo Cliente", "Aprovado - Em Manutenção", "Pronto para Retirada", "Entregue / Concluído", "Recusado / Sem Conserto"],
                            index=["Aguardando Diagnóstico", "Orçamento em Análise pelo Cliente", "Aprovado - Em Manutenção", "Pronto para Retirada", "Entregue / Concluído", "Recusado / Sem Conserto"].index(reg["Status"])
                        )
                    
                    atualizar_dados = st.form_submit_button("Salvar Alterações 💾")
                    
                    if atualizar_dados:
                        reg["Laudo Técnico"] = laudo
                        reg["Mão de Obra (R$)"] = v_mao_de_obra
                        reg["Peças (R$)"] = v_pecas
                        reg["Total Geral (R$)"] = v_mao_de_obra + v_pecas
                        reg["Status"] = novo_status
                        st.success(f"OS {os_selecionada} atualizada no sistema!")
                        st.rerun()
    else:
        st.info("Nenhum equipamento cadastrado no pátio para gerar laudos.")

# -----------------------------------------------------------------------------
# ABA 3: PAINEL DE CONTROLE DE PÁTIO (MONITORAMENTO)
# -----------------------------------------------------------------------------
with aba_painel:
    st.header("🔍 Controle Geral do Pátio J&P MEC")
    
    if st.session_state.dados_oficina:
        df = pd.DataFrame(st.session_state.dados_oficina)
        
        # Filtros Rápidos de Linha Pesada
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            busca_cliente = st.text_input("Filtrar por nome de Cliente")
        with col_f2:
            busca_status = st.selectbox("Filtrar por Situação", ["Todos", "Aguardando Diagnóstico", "Orçamento em Análise pelo Cliente", "Aprovado - Em Manutenção", "Pronto para Retirada", "Entregue / Concluído"])
            
        if busca_cliente:
            df = df[df["Cliente"].str.contains(busca_cliente, case=False, na=False)]
        if busca_status != "Todos":
            df = df[df["Status"] == busca_status]
            
        # Exibição organizada
        st.dataframe(df, use_container_width=True)
        
        # Ferramenta de Backup e Relatórios
        csv = df.to_csv(index=False).encode('utf-8')
