import streamlit as st
import json
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simulador de Compatibilidade de Vagas",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #8B5A2B;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Sobre este projeto")
st.sidebar.write("""
O mercado de trabalho atual está cada vez mais competitivo, e muitos processos seletivos utilizam sistemas automatizados de triagem de currículos (ATS), que filtram candidatos com base na compatibilidade entre o currículo e a descrição da vaga.

Este projeto é um simulador educacional desenvolvido como parte de um processo de aprendizado em Python, iniciado durante uma imersão da Alura e aprimorado com estudos práticos e apoio do ChatGPT.
""")

# Ler JSON
with open("skills.json", "r", encoding="utf-8") as f:
    data = json.load(f)

hard_skills = data["hard_skills"]
soft_skills = data["soft_skills"]
skills_base = hard_skills + soft_skills

experience_by_area = data["experience_by_area"]["experience_items"]

# Pesos
pesos = {skill: 2 for skill in hard_skills}
for skill in soft_skills:
    pesos[skill] = 1

# Equivalências
equivalencias = {
    "pacote office": ["excel", "word", "powerpoint"],
    "microsoft office": ["excel", "word", "powerpoint"],
    "excel avançado": ["excel"],
    "excel intermediário": ["excel"],
    "excel básico": ["excel"]
}

st.title("Simulador de Compatibilidade de Vagas")
st.write("Cole abaixo o texto do seu currículo e da vaga para analisar a compatibilidade.")

curriculo = st.text_area("Cole aqui o texto do seu currículo")
vaga = st.text_area("Cole aqui a descrição da vaga")

if st.button("Analisar compatibilidade"):

    if curriculo == "" or vaga == "":
        st.warning("Preencha os dois campos antes de analisar.")
    else:

        vaga_lower = vaga.lower()
        curriculo_lower = curriculo.lower()


        # detectar skills exigidas
        skills = []

        for skill in skills_base:
            if skill in vaga_lower:
                skills.append(skill)

        # equivalências na vaga
        for termo, equivalentes in equivalencias.items():
            if termo in vaga_lower:
                skills.extend(equivalentes)

        # equivalências no currículo
        for termo, equivalentes in equivalencias.items():
            if termo in curriculo_lower:
                curriculo_lower += " " + " ".join(equivalentes)

        skills = list(set(skills))

        # detectar encontradas
        encontradas = []

        for skill in skills:
            if skill in curriculo_lower:
                encontradas.append(skill)

        encontradas = list(set(encontradas))

        faltantes = list(set(skills) - set(encontradas))

        # score ponderado
        peso_total = 0
        peso_encontrado = 0

        for skill in skills:
            peso_total += pesos.get(skill, 1)
            if skill in encontradas:
                peso_encontrado += pesos.get(skill, 1)

        score = (peso_encontrado / peso_total) * 100 if peso_total > 0 else 0

#Resultados
        st.success(f"Compatibilidade aproximada: {score:.0f}%")

        st.write(f"{len(encontradas)} de {len(skills)} habilidades atendidas.")

        st.subheader("Resultado da análise")

        st.metric("Compatibilidade", f"{score:.0f}%")

        st.progress(score / 100)

        if score >= 80:
         st.success("Alta compatibilidade com a vaga.")
        elif score >= 50:
         st.warning("Compatibilidade moderada. Há pontos de melhoria.")
        else:
         st.error("Baixa compatibilidade. Recomendado revisar o currículo.")


        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Habilidades encontradas")
            if encontradas:
                for skill in sorted(encontradas):
                    st.markdown(f"- ✅ {skill.capitalize()}")
            else:
                st.write("Nenhuma habilidade identificada.")

        with col2:
            st.subheader("Habilidades faltantes")
            if faltantes:
                for skill in sorted(faltantes):
                    st.markdown(f"- ❌ {skill.capitalize()}")
            else:
                st.write("Você atende todas as habilidades identificadas.")

        if faltantes:
            st.divider()
            st.info(
                "Sugestão: destacar ou desenvolver as habilidades faltantes pode aumentar significativamente sua aderência à vaga."
            )

        st.divider()

        st.subheader("Visão gráfica da compatibilidade")

        labels = ["Encontradas", "Faltantes"]
        valores = [len(encontradas), len(faltantes)]

        fig, ax = plt.subplots()
        ax.bar(labels, valores)
        ax.set_ylabel("Quantidade de habilidades")
        ax.set_title("Comparação de habilidades")

        st.pyplot(fig)
           