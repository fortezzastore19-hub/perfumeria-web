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
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,500&family=Jost:wght@300;400;500&display=swap');

    html, body, [class*="css"]  { font-family: 'Jost', sans-serif; }
    .stApp { background-color: #F3EEE4; }

    /* Barra de anuncio superior */
    .promo-bar {
        background-color: #1F2E28;
        color: #F3EEE4;
        text-align: center;
        padding: 0.5rem;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        margin: -1rem -1rem 1.5rem -1rem;
    }

    /* Encabezado */
    .atelier-header { border-bottom: 1px solid #B8863E; padding-bottom: 1.2rem; margin-bottom: 1.8rem; }
    .atelier-eyebrow { font-size: 0.8rem; color: #6B5D4A; letter-spacing: 0.15em; margin-bottom: 0.3rem; }
    .atelier-title { font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: 3.2rem; color: #1F2E28; margin: 0; line-height: 1.1; }
    .atelier-subtitle { font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 1.15rem; color: #6B5D4A; margin-top: 0.4rem; }

    /* Sección: título con línea */
    .section-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.7rem;
        color: #1F2E28;
        border-bottom: 1px solid #C9BBA3;
        padding-bottom: 0.5rem;
        margin: 2.2rem 0 1.2rem 0;
    }

    /* Mosaico de categorías */
    .category-tile {
        position: relative;
        border: 1px solid #C9BBA3;
        text-align: center;
        padding: 1.4rem 0.5rem;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.2rem;
        color: #1F2E28;
        background-color: #EAE3D3;
    }

    /* Ficha de perfume */
    .perfume-label { border-top: 1px solid #B8863E; padding-top: 0.9rem; margin-top: 0.6rem; margin-bottom: 2.4rem; }
    .perfume-house { font-size: 0.78rem; color: #6B5D4A; letter-spacing: 0.05em; margin-bottom: 0.15rem; }
    .perfume-name { font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: 1.7rem; color: #1F2E28; margin-bottom: 0.5rem; line-height: 1.1; }
    .pyramid-row { display: flex; justify-content: space-between; font-size: 0.72rem; color: #6B5D4A; margin-top: 0.6rem; margin-bottom: 0.6rem; border-top: 1px dotted #C9BBA3; padding-top: 0.5rem; }
    .pyramid-item { flex: 1; }
    .pyramid-label { display: block; color: #B8863E; font-size: 0.65rem; margin-bottom: 0.15rem; }
    .perfume-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 0.8rem; }
    .perfume-price { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; color: #1F2E28; }
    .whatsapp-link { color: #1F2E28 !important; text-decoration: none; font-size: 0.8rem; border-bottom: 1px solid #B8863E; padding-bottom: 2px; }
    .whatsapp-link:hover { color: #B8863E !important; border-bottom-color: #1F2E28; }

    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #EAE3D3; border-right: 1px solid #C9BBA3; }
    section[data-testid="stSidebar"] * { color: #1F2E28 !important; font-family: 'Jost', sans-serif; }

    div[data-testid="stImage"] img { filter: sepia(8%); }

    /* Botón flotante de WhatsApp */
    .whatsapp-float {
        position: fixed;
        bottom: 1.5rem;
        right: 1.5rem;
        background-color: #1F2E28;
        color: #F3EEE4 !important;
        padding: 0.7rem 1.1rem;
        border-radius: 30px;
        text-decoration: none;
        font-size: 0.85rem;
        border: 1px solid #B8863E;
        z-index: 999;
    }
    .whatsapp-float:hover { background-color: #B8863E; color: #1F2E28 !important; }

    /* Footer */
    .atelier-footer {
        border-top: 1px solid #C9BBA3;
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        color: #6B5D4A;
        font-size: 0.82rem;
    }
    .atelier-footer a { color: #1F2E28; text-decoration: none; border-bottom: 1px solid #B8863E; }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATOS DESDE GOOGLE SHEETS
# ============================================
# 1. En tu Google Sheet: Archivo > Compartir > Publicar en la Web
# 2. Selecciona la hoja, formato CSV, Publicar, y pega el link aquí:
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRTT173GepzryFHTMSZJdxEbrYL4v-iA8LDV39T4A7lDBo3dX5ciZNW9--UrpIiXmtWpAGiqe8p2kTh/pub?output=csv"
FOTO_RESPALDO = "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400"

@st.cache_data(ttl=300)
def cargar_catalogo(url):
    df = pd.read_csv(url)

    # Normaliza los nombres de columna: quita espacios, tildes y mayúsculas
    # para que no importe si en el Sheet escribiste "Categoria", "Categoría " o "CATEGORIA"
    reemplazos_tilde = str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU")
    columnas_normalizadas = {}
    for col in df.columns:
        limpio = col.strip().translate(reemplazos_tilde).lower()
        columnas_normalizadas[col] = limpio
    df = df.rename(columns=columnas_normalizadas)

    columnas_esperadas = {
        "nombre": "Nombre", "marca": "Marca", "precio": "Precio",
        "salida": "Salida", "corazon": "Corazon", "fondo": "Fondo",
        "categoria": "Categoria", "foto": "Foto"
    }
    faltantes = [c for c in columnas_esperadas if c not in df.columns]
    if faltantes:
        st.error(f"A tu hoja de Google Sheets le faltan estas columnas (revisa tildes/espacios en los encabezados): {', '.join(faltantes)}")
        st.stop()
    df = df.rename(columns=columnas_esperadas)

    df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce").fillna(0)
    df["Foto"] = df["Foto"].fillna(FOTO_RESPALDO)
    df = df.dropna(subset=["Nombre", "Marca"])
    return df

try:
    df = cargar_catalogo(SHEET_URL)
except Exception:
    st.error("No se pudo cargar el catálogo desde Google Sheets. Revisa el link publicado y las columnas: Nombre, Marca, Precio, Salida, Corazon, Fondo, Categoria, Foto.")
    st.stop()

# ============================================
# DATOS DE CONTACTO Y MARCA (personaliza aquí)
# ============================================
WHATSAPP_NUMBER = "521234567890"
INSTAGRAM = "atelierperfumes"
CIUDAD = "Tu ciudad"
HORARIO = "Lunes a sábado: 9am a 7pm"

# ============================================
# ESTADO: categoría elegida desde los mosaicos
# ============================================
if "categoria_activa" not in st.session_state:
    st.session_state.categoria_activa = "Todas"

# ============================================
# BARRA DE PROMOCIÓN
# ============================================
st.markdown('<div class="promo-bar">ENVÍOS A TODA LA CIUDAD · PERFUMES 100% ORIGINALES GARANTIZADOS</div>', unsafe_allow_html=True)

# ============================================
# ENCABEZADO / HERO
# ============================================
st.markdown("""
<div class="atelier-header">
    <div class="atelier-eyebrow">CATÁLOGO DE FRAGANCIAS ORIGINALES</div>
    <p class="atelier-title">Atelier</p>
    <p class="atelier-subtitle">Cada frasco, una composición completa — de la primera impresión al fondo que queda en la piel.</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# MOSAICO DE CATEGORÍAS
# ============================================
st.markdown('<div class="section-title">Explora por categoría</div>', unsafe_allow_html=True)

categorias_disponibles = sorted(df["Categoria"].dropna().unique().tolist())
tile_cols = st.columns(len(categorias_disponibles) + 1)

with tile_cols[0]:
    if st.button("Ver todas", use_container_width=True):
        st.session_state.categoria_activa = "Todas"

for i, cat in enumerate(categorias_disponibles):
    with tile_cols[i + 1]:
        if st.button(cat, use_container_width=True):
            st.session_state.categoria_activa = cat

# ============================================
# SIDEBAR - FILTROS ADICIONALES
# ============================================
st.sidebar.markdown("**Filtrar catálogo**")

marcas = ["Todas"] + sorted(df["Marca"].unique().tolist())
marca_seleccionada = st.sidebar.selectbox("Casa de perfumería", marcas)

precio_min_valor = int(df["Precio"].min())
precio_max_valor = int(df["Precio"].max())

if precio_min_valor == precio_max_valor:
    # Solo hay un precio (o un perfume) en el catálogo todavía — no se puede mostrar un rango
    precio_max = precio_max_valor
    st.sidebar.markdown(f"Precio: ${precio_max_valor}")
else:
    precio_max = st.sidebar.slider(
        "Precio máximo (USD)",
        min_value=precio_min_valor,
        max_value=precio_max_valor,
        value=precio_max_valor
    )

busqueda = st.sidebar.text_input("Buscar por nombre")

st.sidebar.markdown("---")
st.sidebar.markdown(f"{len(df)} fragancias en el catálogo")

# ============================================
# APLICAR FILTROS
# ============================================
df_filtrado = df.copy()

if st.session_state.categoria_activa != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Categoria"] == st.session_state.categoria_activa]

if marca_seleccionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Marca"] == marca_seleccionada]

df_filtrado = df_filtrado[df_filtrado["Precio"] <= precio_max]

if busqueda:
    df_filtrado = df_filtrado[df_filtrado["Nombre"].str.contains(busqueda, case=False)]

# ============================================
# SECCIÓN: EN TENDENCIA (los 3 más caros como destacados de ejemplo)
# ============================================
st.markdown('<div class="section-title">En tendencia</div>', unsafe_allow_html=True)

destacados = df.sort_values("Precio", ascending=False).head(3)
dest_cols = st.columns(3)
for col, (_, p) in zip(dest_cols, destacados.iterrows()):
    with col:
        st.image(p["Foto"], use_container_width=True)
        st.markdown(f"""
        <div style="text-align:center; font-family:'Cormorant Garamond', serif; font-size:1.1rem; color:#1F2E28;">
            {p['Nombre']}<br><span style="font-size:0.85rem; color:#6B5D4A;">${p['Precio']}</span>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# CATÁLOGO COMPLETO (filtrado)
# ============================================
titulo_catalogo = "Catálogo completo" if st.session_state.categoria_activa == "Todas" else f"Categoría: {st.session_state.categoria_activa}"
st.markdown(f'<div class="section-title">{titulo_catalogo}</div>', unsafe_allow_html=True)

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
st.markdown(f"""
<div class="atelier-footer">
    <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:1.5rem;">
        <div>
            <strong>Atelier de Fragancias</strong><br>
            Perfumes 100% originales y garantizados.
        </div>
        <div>
            <strong>Contacto</strong><br>
            <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank">WhatsApp</a> ·
            <a href="https://instagram.com/{INSTAGRAM}" target="_blank">@{INSTAGRAM}</a>
        </div>
        <div>
            <strong>Horario</strong><br>
            {HORARIO}<br>{CIUDAD}
        </div>
    </div>
    <div style="text-align:center; margin-top:1.5rem;">Atelier de Fragancias © 2026</div>
</div>

<a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank" class="whatsapp-float">💬 Escríbenos</a>
""", unsafe_allow_html=True)
