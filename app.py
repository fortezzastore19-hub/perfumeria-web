import streamlit as st
import pandas as pd

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Atelier — Perfumes Originales",
    page_icon="🥃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ESTILO — CONCEPTO: ETIQUETA DE ATELIER
# Papel marfil, verde botella, ámbar líquido.
# Cada perfume se presenta como una ficha de
# etiqueta, con las notas en pirámide olfativa
# en vez de una lista genérica.
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,500&family=Jost:wght@300;400;500&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Jost', sans-serif;
    }

    .stApp {
        background-color: #F3EEE4;
    }

    /* Encabezado */
    .atelier-header {
        text-align: left;
        border-bottom: 1px solid #B8863E;
        padding-bottom: 1.2rem;
        margin-bottom: 2.2rem;
    }

    .atelier-eyebrow {
        font-family: 'Jost', sans-serif;
        font-weight: 400;
        font-size: 0.8rem;
        color: #6B5D4A;
        letter-spacing: 0.15em;
        margin-bottom: 0.3rem;
    }

    .atelier-title {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        font-size: 3.2rem;
        color: #1F2E28;
        margin: 0;
        line-height: 1.1;
    }

    .atelier-subtitle {
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        font-size: 1.15rem;
        color: #6B5D4A;
        margin-top: 0.4rem;
    }

    /* Ficha de perfume */
    .perfume-label {
        border-top: 1px solid #B8863E;
        padding-top: 0.9rem;
        margin-top: 0.6rem;
        margin-bottom: 2.4rem;
    }

    .perfume-house {
        font-size: 0.78rem;
        color: #6B5D4A;
        letter-spacing: 0.05em;
        margin-bottom: 0.15rem;
    }

    .perfume-name {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        font-size: 1.7rem;
        color: #1F2E28;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }

    /* Pirámide olfativa */
    .pyramid-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.72rem;
        color: #6B5D4A;
        margin-top: 0.6rem;
        margin-bottom: 0.6rem;
        border-top: 1px dotted #C9BBA3;
        padding-top: 0.5rem;
    }

    .pyramid-item {
        flex: 1;
    }

    .pyramid-label {
        display: block;
        color: #B8863E;
        font-size: 0.65rem;
        margin-bottom: 0.15rem;
    }

    .perfume-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0.8rem;
    }

    .perfume-price {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.4rem;
        color: #1F2E28;
    }

    .whatsapp-link {
        color: #1F2E28 !important;
        text-decoration: none;
        font-size: 0.8rem;
        border-bottom: 1px solid #B8863E;
        padding-bottom: 2px;
    }

    .whatsapp-link:hover {
        color: #B8863E !important;
        border-bottom-color: #1F2E28;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #EAE3D3;
        border-right: 1px solid #C9BBA3;
    }

    section[data-testid="stSidebar"] * {
        color: #1F2E28 !important;
        font-family: 'Jost', sans-serif;
    }

    /* Imagen */
    div[data-testid="stImage"] img {
        filter: sepia(8%);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATOS DE EJEMPLO (luego se conecta a Google Sheets)
# Cada nota tiene 3 partes: salida, corazón, fondo
# ============================================
data = {
    "Nombre": [
        "Sauvage", "Bleu de Chanel", "Black Opium", "Good Girl",
        "Aventus", "Light Blue", "One Million", "La Vie Est Belle",
        "Acqua di Gio", "Coco Mademoiselle"
    ],
    "Marca": [
        "Dior", "Chanel", "Yves Saint Laurent", "Carolina Herrera",
        "Creed", "Dolce & Gabbana", "Paco Rabanne", "Lancôme",
        "Giorgio Armani", "Chanel"
    ],
    "Precio": [85, 95, 78, 82, 250, 65, 70, 88, 72, 98],
    "Salida": ["Bergamota", "Limón", "Café", "Almendra", "Piña", "Cedro", "Canela", "Iris", "Bergamota", "Naranja"],
    "Corazon": ["Pimienta", "Jengibre", "Vainilla", "Jazmín", "Abedul", "Manzana", "Cuero", "Praliné", "Jazmín acuático", "Jazmín"],
    "Fondo": ["Ámbar", "Incienso", "Flor de naranjo", "Cacao", "Almizcle", "Cedro", "Ámbar", "Pachulí", "Almizcle blanco", "Pachulí"],
    "Categoria": [
        "Hombre", "Hombre", "Mujer", "Mujer",
        "Hombre", "Mujer", "Hombre", "Mujer",
        "Hombre", "Mujer"
    ],
    "Foto": [
        "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400",
        "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=400",
        "https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=400",
        "https://images.unsplash.com/photo-1587017539504-67cfbddac569?w=400",
        "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=400",
        "https://images.unsplash.com/photo-1547887538-e3a2f32cb1cc?w=400",
        "https://images.unsplash.com/photo-1595425964272-5eb8a45f3ac4?w=400",
        "https://images.unsplash.com/photo-1615397349754-cfa2066a298e?w=400",
        "https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=400",
        "https://images.unsplash.com/photo-1600612253971-422e7f7faeb6?w=400",
    ]
}

df = pd.DataFrame(data)

# ============================================
# NÚMERO DE WHATSAPP (cámbialo por el tuyo)
# ============================================
WHATSAPP_NUMBER = "521234567890"  # formato: código país + número, sin + ni espacios

# ============================================
# ENCABEZADO
# ============================================
st.markdown("""
<div class="atelier-header">
    <div class="atelier-eyebrow">CATÁLOGO DE FRAGANCIAS ORIGINALES</div>
    <p class="atelier-title">Atelier</p>
    <p class="atelier-subtitle">Cada frasco, una composición completa — de la primera impresión al fondo que queda en la piel.</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR - FILTROS
# ============================================
st.sidebar.markdown("**Filtrar catálogo**")

categorias = ["Todas"] + sorted(df["Categoria"].unique().tolist())
categoria_seleccionada = st.sidebar.selectbox("Categoría", categorias)

marcas = ["Todas"] + sorted(df["Marca"].unique().tolist())
marca_seleccionada = st.sidebar.selectbox("Casa de perfumería", marcas)

precio_max = st.sidebar.slider(
    "Precio máximo (USD)",
    min_value=int(df["Precio"].min()),
    max_value=int(df["Precio"].max()),
    value=int(df["Precio"].max())
)

busqueda = st.sidebar.text_input("Buscar por nombre")

st.sidebar.markdown("---")
st.sidebar.markdown(f"{len(df)} fragancias en el catálogo")

# ============================================
# APLICAR FILTROS
# ============================================
df_filtrado = df.copy()

if categoria_seleccionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria_seleccionada]

if marca_seleccionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Marca"] == marca_seleccionada]

df_filtrado = df_filtrado[df_filtrado["Precio"] <= precio_max]

if busqueda:
    df_filtrado = df_filtrado[df_filtrado["Nombre"].str.contains(busqueda, case=False)]

# ============================================
# MOSTRAR CATÁLOGO COMO FICHAS DE ETIQUETA
# ============================================
if len(df_filtrado) == 0:
    st.warning("No se encontraron perfumes con esos filtros.")
else:
    cols_per_row = 3
    rows = [df_filtrado.iloc[i:i+cols_per_row] for i in range(0, len(df_filtrado), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for col, (_, p) in zip(cols, row.iterrows()):
            with col:
                mensaje_wpp = f"Hola! Me interesa el perfume {p['Nombre']} de {p['Marca']} (${p['Precio']})"
                link_wpp = f"https://wa.me/{WHATSAPP_NUMBER}?text={mensaje_wpp.replace(' ', '%20')}"

                st.image(p["Foto"], use_container_width=True)
                st.markdown(f"""
                <div class="perfume-label">
                    <div class="perfume-house">{p['Marca'].upper()} · {p['Categoria']}</div>
                    <div class="perfume-name">{p['Nombre']}</div>
                    <div class="pyramid-row">
                        <div class="pyramid-item"><span class="pyramid-label">SALIDA</span>{p['Salida']}</div>
                        <div class="pyramid-item"><span class="pyramid-label">CORAZÓN</span>{p['Corazon']}</div>
                        <div class="pyramid-item"><span class="pyramid-label">FONDO</span>{p['Fondo']}</div>
                    </div>
                    <div class="perfume-footer">
                        <span class="perfume-price">${p['Precio']}</span>
                        <a href="{link_wpp}" target="_blank" class="whatsapp-link">Consultar →</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div style='border-top: 1px solid #C9BBA3; margin-top: 2rem; padding-top: 1rem; text-align: center; color: #6B5D4A; font-size: 0.78rem;'>
Atelier de Fragancias — todos los productos son 100% originales y garantizados
</div>
""", unsafe_allow_html=True)
