import streamlit as st
import pandas as pd

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Perfumes Originales | Catálogo",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ESTILO PERSONALIZADO (CSS)
# ============================================
st.markdown("""
<style>
    /* Fondo general */
    .stApp {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Título principal */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #d4af37, #f4e5c2, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        letter-spacing: 2px;
    }

    .subtitle {
        text-align: center;
        color: #b8b8d1;
        font-size: 1.1rem;
        margin-top: 0;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }

    /* Tarjeta de producto */
    .perfume-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        transition: transform 0.2s, border-color 0.2s;
        height: 100%;
    }

    .perfume-card:hover {
        transform: translateY(-5px);
        border-color: #d4af37;
    }

    .perfume-name {
        color: #f4e5c2;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }

    .perfume-brand {
        color: #b8b8d1;
        font-size: 0.9rem;
        font-style: italic;
        margin-bottom: 0.6rem;
    }

    .perfume-notes {
        color: #d1d1e0;
        font-size: 0.85rem;
        margin-bottom: 0.8rem;
        line-height: 1.4;
    }

    .perfume-price {
        color: #d4af37;
        font-size: 1.4rem;
        font-weight: 700;
    }

    .category-badge {
        display: inline-block;
        background: rgba(212, 175, 55, 0.2);
        color: #d4af37;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        margin-bottom: 0.5rem;
    }

    /* Botón de WhatsApp */
    .whatsapp-btn {
        display: inline-block;
        background: #25D366;
        color: white !important;
        text-align: center;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        width: 100%;
        margin-top: 0.5rem;
    }

    .whatsapp-btn:hover {
        background: #1ebe5a;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0f0f1e;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATOS DE EJEMPLO (luego se conecta a Google Sheets)
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
    "Notas": [
        "Bergamota, pimienta, ámbar",
        "Cítrico, madera, incienso",
        "Café, vainilla, flor de naranjo",
        "Almendra, jazmín, cacao",
        "Piña, abedul, almizcle",
        "Cedro, lima, jazmín",
        "Canela, cuero, ámbar",
        "Iris, praliné, pachulí",
        "Bergamota, jazmín acuático",
        "Naranja, jazmín, pachulí"
    ],
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
st.markdown('<p class="main-title">✨ PERFUMES ORIGINALES ✨</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Fragancias auténticas para cada ocasión</p>', unsafe_allow_html=True)

# ============================================
# SIDEBAR - FILTROS
# ============================================
st.sidebar.header("🔍 Filtrar catálogo")

categorias = ["Todas"] + sorted(df["Categoria"].unique().tolist())
categoria_seleccionada = st.sidebar.selectbox("Categoría", categorias)

marcas = ["Todas"] + sorted(df["Marca"].unique().tolist())
marca_seleccionada = st.sidebar.selectbox("Marca", marcas)

precio_max = st.sidebar.slider(
    "Precio máximo (USD)",
    min_value=int(df["Precio"].min()),
    max_value=int(df["Precio"].max()),
    value=int(df["Precio"].max())
)

busqueda = st.sidebar.text_input("Buscar por nombre")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total de perfumes:** {len(df)}")

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
# MOSTRAR CATÁLOGO EN TARJETAS
# ============================================
if len(df_filtrado) == 0:
    st.warning("No se encontraron perfumes con esos filtros.")
else:
    cols_per_row = 3
    rows = [df_filtrado.iloc[i:i+cols_per_row] for i in range(0, len(df_filtrado), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for col, (_, perfume) in zip(cols, row.iterrows()):
            with col:
                mensaje_wpp = f"Hola! Me interesa el perfume {perfume['Nombre']} de {perfume['Marca']} (${perfume['Precio']})"
                link_wpp = f"https://wa.me/{WHATSAPP_NUMBER}?text={mensaje_wpp.replace(' ', '%20')}"

                st.image(perfume["Foto"], use_container_width=True)
                st.markdown(f"""
                <div class="perfume-card">
                    <span class="category-badge">{perfume['Categoria']}</span>
                    <div class="perfume-name">{perfume['Nombre']}</div>
                    <div class="perfume-brand">{perfume['Marca']}</div>
                    <div class="perfume-notes">🌿 {perfume['Notas']}</div>
                    <div class="perfume-price">${perfume['Precio']} USD</div>
                    <a href="{link_wpp}" target="_blank" class="whatsapp-btn">💬 Consultar por WhatsApp</a>
                </div>
                """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #8888a8; font-size: 0.85rem;'>
© 2026 Perfumes Originales — Todos los productos son 100% originales y garantizados
</p>
""", unsafe_allow_html=True)
