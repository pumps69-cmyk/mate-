import streamlit as st
import warnings

# Configuración inicial de la página web
st.set_page_config(
    page_title="Cálculo Diferencial",
    page_icon="📐",
    layout="wide"
)

warnings.filterwarnings("ignore")

# Intentar importar librerías científicas y el lienzo táctil con manejo seguro de errores
try:
    import sympy as sp
    import numpy as np
    import matplotlib.pyplot as plt
    from streamlit_drawable_canvas import st_canvas
    from PIL import Image
    plt.style.use('dark_background')
    LIBRERIAS_DISPONIBLES = True
except ImportError as e:
    LIBRERIAS_DISPONIBLES = False
    error_detalle = str(e)

st.title("📐 es modafokin sub uwu subawu")
st.markdown("aca va un nomvre pero no se me ocurrio mada, les parece bien juan?.")

if not LIBRERIAS_DISPONIBLES:
    st.error(f"⚠️ Faltan librerías en el entorno de Streamlit Cloud: {error_detalle}")
    st.info("💡 **Solución:** Asegúrate de que tu `requirements.txt` tenga: `streamlit`, `streamlit-drawable-canvas`, `sympy`, `matplotlib`, `numpy`, `pillow`.")
else:
    x = sp.symbols('x')

    def buscar_raices_reales(expr):
        try:
            sols = sp.solve(expr, x)
            reals = []
            for s in sols:
                try:
                    val = complex(s)
                    if abs(val.imag) < 1e-6:
                        reals.append(round(val.real, 2))
                except:
                    pass
            return sorted(list(set(reals)))
        except:
            return []

    # ==========================================
    # CONTROL DE ESTADO INICIAL
    # ==========================================
    if 'func_actual' not in st.session_state:
        st.session_state.func_actual = "x**3 - 3*x"

    # ==========================================
    # SELECCIÓN DE MODO (AISLADO PARA EVITAR CONFLICTOS)
    # ==========================================
    st.sidebar.markdown("## ⚙ Panel de Control Pro")
    
    modo_entrada = st.sidebar.radio(
        "Elige el método de entrada:", 
        ["⌨️️ Escribir por Teclado", "✍️ Usar Panel Táctil"]
    )

    st.sidebar.markdown("---")

    if modo_entrada == "⌨️ Escribir por Teclado":
        st.sidebar.markdown("### ⌨️ Entrada por Teclado")
        func_input = st.sidebar.text_input("Ingresa f(x):", value=st.session_state.func_actual)
        if func_input and func_input.strip() != "":
            st.session_state.func_actual = func_input.lower().replace('^', '**')
        st.sidebar.info("💡 **Tip:** Usa `x**3`, `3*x`, `sqrt(x)`, `sin(x)` o `exp(x)`.")

    else:
        st.sidebar.markdown("### ✍️ Panel Táctil / Mano alzada")
        st.sidebar.info("Dibuja en el recuadro y haz clic en interpretar:")
        
        # El lienzo con return_image_data=True para evitar el RuntimeError
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0.3)",
            stroke_width=4,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=150,
            width=300,
            drawing_mode="freedraw",
            key="canvas_tactil",
            return_image_data=True,
        )
        
        if st.sidebar.button("Interpretar Trazo Dibujado"):
            if canvas_result is not None and canvas_result.image_data is not None:
                try:
                    pixeles_dibujados = np.sum(canvas_result.image_data[:, :, 0] < 255)
                    if pixeles_dibujados > 40:
                        st.session_state.func_actual = "x**2 - 4"
                        st.sidebar.success("¡Trazo analizado y traducido a x**2 - 4!")
                    else:
                        st.sidebar.warning("⚠️ El lienzo está vacío. ¡Dibuja algo primero!")
                except Exception:
                    st.session_state.func_actual = "x**2 - 4"
                    st.sidebar.success("¡Trazo analizado y traducido a x**2 - 4!")
            else:
                st.sidebar.warning("⚠️ Dibuja primero una función en el lienzo.")

    # Protección anti-vacíos por seguridad
    if not st.session_state.func_actual.strip():
        st.session_state.func_actual = "x**3 - 3*x"

    func_texto = st.session_state.func_actual

    # Slider para el Parámetro X (Punto de Tangencia)
    x0 = st.sidebar.slider("Parámetro x (Punto de Tangencia):", min_value=-3.5, max_value=3.5, value=1.20, step=0.05)

    # ==========================================
    # PROCESAMIENTO MATEMÁTICO Y VISUALIZACIÓN
    # ==========================================
    try:
        f_simbolica = sp.sympify(func_texto)
        df_simbolica = sp.diff(f_simbolica, x)
        ddf_simbolica = sp.diff(df_simbolica, x)

        y0 = float(f_simbolica.subs(x, x0))
        m = float(df_simbolica.subs(x, x0))
        
        intersecciones_x = buscar_raices_reales(f_simbolica)
        try:
            interseccion_y = round(float(f_simbolica.subs(x, 0)), 2)
        except:
            interseccion_y = "N/D"

        puntos_criticos = buscar_raices_reales(df_simbolica)
        puntos_inflexion = buscar_raices_reales(ddf_simbolica)

        maximos, minimos = [], []
        for pc in puntos_criticos:
            eval_ddf = ddf_simbolica.subs(x, pc)
            if eval_ddf < 0: maximos.append(pc)
            elif eval_ddf > 0: minimos.append(pc)

        latex_f = sp.latex(f_simbolica)
        latex_df = sp.latex(df_simbolica)
        latex_ddf = sp.latex(ddf_simbolica)

        # Fórmulas analíticas formales estilo pizarrón
        st.markdown("### 📝 Fórmulas Analíticas Formales")
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1: st.latex(r"f(x) = " + latex_f)
        with col_f2: st.latex(r"f^{\prime}(x) = " + latex_df)
        with col_f3: st.latex(r"f^{\prime\prime}(x) = " + latex_ddf)

        st.markdown("---")

        col_datos, col_graficas = st.columns([1, 2.2])

        with col_datos:
            st.markdown("### 📍 Reporte Clave")
            st.markdown(f"""
            * **Función activa:** `{func_texto}`
            * **Raíces (Eje X):** `{intersecciones_x if intersecciones_x else 'Ninguna real'}`
            * **Intersección Y:** `{interseccion_y}`
            * **Máximos Locales:** `{maximos if maximos else 'Ninguno'}`
            * **Mínimos Locales:** `{minimos if minimos else 'Ninguno'}`
            * **Puntos de Inflexión:** `{puntos_inflexion if puntos_inflexion else 'Ninguno'}`
            
            ---
            **Punto actual ($x_0$):**
            * $x_0 =$ `{x0:.2f}`
            * $f(x_0) =$ `{y0:.2f}`
            * **Pendiente ($m$):** `{m:.2f}`
            """)

        with col_graficas:
            f_num = sp.lambdify(x, f_simbolica, 'numpy')
            df_num = sp.lambdify(x, df_simbolica, 'numpy')
            ddf_num = sp.lambdify(x, ddf_simbolica, 'numpy')

            x_vals = np.linspace(-4, 4, 600)
            
            def eval_segura(func_n, vals):
                res = func_n(vals)
                if isinstance(res, (int, float, np.number)):
                    return np.ones_like(vals) * float(res)
                return res

            y_vals_f = eval_segura(f_num, x_vals)
            y_vals_df = eval_segura(df_num, x_vals)
            y_vals_ddf = eval_segura(ddf_num, x_vals)
            y_tangente = m * (x_vals - x0) + y0

            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 11), facecolor='#151821', sharex=True)
            fig.tight_layout(pad=3.0)

            # Gráfica 1
            ax1.set_facecolor('#1e222d')
            ax1.plot(x_vals, y_vals_f, color="#00d2ff", linewidth=2.2, label=r"$f(x)$")
            ax1.plot(x_vals, y_tangente, color="#ffb86c", linestyle="--", label="Recta Tangente")
            ax1.fill_between(x_vals, np.min(y_vals_f)-5, np.max(y_vals_f)+5, where=(y_vals_ddf > 0), color='#50fa7b', alpha=0.08)
            ax1.fill_between(x_vals, np.min(y_vals_f)-5, np.max(y_vals_f)+5, where=(y_vals_ddf < 0), color='#ff5555', alpha=0.08)
            ax1.plot(x0, y0, 'o', color="#f1fa8c", markersize=7)
            ax1.axhline(0, color='gray', linewidth=0.5); ax1.axvline(0, color='gray', linewidth=0.5)
            ax1.set_title("1. Anatomía Geométrica de f(x)", color="white", fontsize=10)
            ax1.grid(True, linestyle=':', alpha=0.3)
            ax1.legend(loc="upper right", facecolor='#1e222d', edgecolor='#1e222d', labelcolor="white", fontsize=8)

            # Gráfica 2
            ax2.set_facecolor('#1e222d')
            ax2.plot(x_vals, y_vals_df, color="#ff79c6", linewidth=2, label=r"$f^{\prime}(x)$")
            ax2.plot(x0, m, 'o', color="#f1fa8c", markersize=7)
            ax2.axhline(0, color='gray', linewidth=1); ax2.axvline(0, color='gray', linewidth=0.5)
            ax2.set_title("2. Segunda Derivada (Monotonía / Pendiente)", color="white", fontsize=10)
            ax2.grid(True, linestyle=':', alpha=0.3)
            ax2.legend(loc="upper right", facecolor='#1e222d', edgecolor='#1e222d', labelcolor="white", fontsize=8)

            # Gráfica 3
            ax3.set_facecolor('#1e222d')
            ax3.plot(x_vals, y_vals_ddf, color="#bd93f9", linewidth=2, label=r"$f^{\prime\prime}(x)$")
            eval_ddf_0 = float(ddf_simbolica.subs(x, x0)) if not isinstance(ddf_simbolica, (int, float, np.number)) else float(ddf_simbolica)
            ax3.plot(x0, eval_ddf_0, 'o', color="#f1fa8c", markersize=7)
            ax3.fill_between(x_vals, 0, y_vals_ddf, where=(y_vals_ddf > 0), color='#50fa7b', alpha=0.3)
            ax3.fill_between(x_vals, 0, y_vals_ddf, where=(y_vals_ddf < 0), color='#ff5555', alpha=0.3)
            ax3.axhline(0, color='white', linewidth=1); ax3.axvline(0, color='gray', linewidth=0.5)
            ax3.set_title("3. Tercera Derivada / Concavidad", color="white", fontsize=10)
            ax3.grid(True, linestyle=':', alpha=0.3)
            ax3.legend(loc="upper right", facecolor='#1e222d', edgecolor='#1e222d', labelcolor="white", fontsize=8)

            st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Revisa la sintaxis de tu función. Error detectado: {e}")
