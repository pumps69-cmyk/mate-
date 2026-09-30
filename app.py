import streamlit as st
import warnings
import re
import random

# Configuración inicial de la página web
st.set_page_config(
    page_title="Cálculo Diferencial",
    page_icon="📐",
    layout="wide"
)

warnings.filterwarnings("ignore")

# Intentar importar librerías científicas
try:
    import sympy as sp
    import numpy as np
    import matplotlib.pyplot as plt
    from streamlit_drawable_canvas import st_canvas
    plt.style.use('dark_background')
    LIBRERIAS_DISPONIBLES = True
except ImportError as e:
    LIBRERIAS_DISPONIBLES = False
    error_detalle = str(e)

st.title("📐 es modafokin sub uwu subawu")
st.markdown("Acá va un nombre pero no se me ocurrió nada, ¿les parece bien Juan?")

if not LIBRERIAS_DISPONIBLES:
    st.error(f"⚠️ Faltan librerías: {error_detalle}")
else:
    x, y_sym = sp.symbols('x y')

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
    # ALGORITMO DE ADAPTACIÓN HUMANO-MÁQUINA
    # ==========================================
    def procesar_entrada_usuario(raw_input):
        t = raw_input.lower().replace(' ', '').replace('^', '**')
        t = t.replace('f(x)', 'y')
        
        t = re.sub(r'(\d)([xy(])', r'\1*\2', t)
        t = re.sub(r'([xy])(\d+)', r'\1**\2', t)
        
        if '=' in t:
            try:
                lhs_str, rhs_str = t.split('=', 1)
                lhs_expr = sp.sympify(lhs_str)
                rhs_expr = sp.sympify(rhs_str)
                
                if y_sym in lhs_expr.free_symbols or y_sym in rhs_expr.free_symbols:
                    sols = sp.solve(sp.Eq(lhs_expr, rhs_expr), y_sym)
                    if sols:
                        return str(sols[-1]), "y"
                return str(rhs_expr), "f(x)"
            except:
                return "", "f(x)"
        else:
            return t, "f(x)"

    # ==========================================
    # MEMORIA DE ESTADO
    # ==========================================
    if 'func_actual' not in st.session_state:
        st.session_state.func_actual = ""
        st.session_state.display_text = ""
        st.session_state.majoraga = "f(x)"
        st.session_state.sugerencia_humana = ""
        st.session_state.sugerencia_maquina = ""

    # ==========================================
    # SELECCIÓN DE MODO
    # ==========================================
    st.sidebar.markdown("## ⚙ Panel de Control Pro")
    modo_entrada = st.sidebar.radio("Método de trabajo:", ["⌨️️ Teclado", "✍️ Pizarrón Táctil"])
    st.sidebar.markdown("---")

    if modo_entrada == "⌨️ Teclado":
        func_input = st.sidebar.text_input("Ingresa tu ecuación:", value=st.session_state.display_text, placeholder="Ej: y^2 = 3*x")
        
        if func_input and func_input.strip() != "":
            st.session_state.display_text = func_input
            nueva_func, nuevo_pref = procesar_entrada_usuario(func_input)
            if nueva_func:
                st.session_state.func_actual = nueva_func
                st.session_state.majoraga = nuevo_pref
        else:
            st.session_state.func_actual = ""

    else:
        st.sidebar.info("Dibuja tu ecuación en el pizarrón táctil:")
        
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0.3)",
            stroke_width=4,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=200,
            width=300,
            drawing_mode="freedraw",
            key="canvas_tactil",
            return_image_data=True,
        )

        # ==========================================
        # MINI BASE DE DATOS DE TRADUCCIÓN (HUMANO <-> MÁQUINA)
        # ==========================================
        base_datos_mahoraga = [
            {"humano": "y^2 = 3*x", "maquina": "y2 = 3x"},
            {"humano": "x^3 - 3*x", "maquina": "x**3 - 3*x"},
            {"humano": "x^2 - 5*x + 6", "maquina": "x**2 - 5*x + 6"},
            {"humano": "sin(x)", "maquina": "sin(x)"},
            {"humano": "cos(x)", "maquina": "cos(x)"},
            {"humano": "x^3 - 3*x + 1", "maquina": "x**3 - 3*x + 1"}
        ]

        if st.sidebar.button("🔍 Interpretar Trazo"):
            if canvas_result is not None and canvas_result.image_data is not None:
                if np.sum(canvas_result.image_data[:, :, 0] < 255) > 20:
                    # Simulamos la "adaptación" tomando un par al azar de nuestra mini base de datos
                    seleccion = random.choice(base_datos_mahoraga)
                    st.session_state.sugerencia_humana = seleccion["humano"]
                    st.session_state.sugerencia_maquina = seleccion["maquina"]
                else:
                    st.sidebar.warning("⚠️ Dibuja algo en el lienzo primero.")
                    st.session_state.sugerencia_humana = ""
                    st.session_state.sugerencia_maquina = ""

        # MOSTRAR LA SUGERENCIA DIRECTAMENTE DEBAJO DEL PIZARRÓN TÁCTIL
        if st.session_state.sugerencia_humana:
            st.sidebar.markdown("---")
            st.sidebar.markdown("🌀 **Mahoraga se ha adaptado:**")
            st.sidebar.info(f"Lo que tú ves (Humano): `{st.session_state.sugerencia_humana}`\n\nLo que entiende la PC: `{st.session_state.sugerencia_maquina}`")
            
            col_si, col_no = st.sidebar.columns(2)
            with col_si:
                if st.button("✅ Aplicar", key="mahoraga_si"):
                    st.session_state.display_text = st.session_state.sugerencia_humana
                    nueva_func, nuevo_pref = procesar_entrada_usuario(st.session_state.sugerencia_maquina)
                    st.session_state.func_actual = nueva_func
                    st.session_state.majoraga = nuevo_pref
                    # Limpiamos la sugerencia temporal para reiniciar el ciclo
                    st.session_state.sugerencia_humana = ""
                    st.session_state.sugerencia_maquina = ""
                    st.rerun()
            with col_no:
                if st.button("🔄 Borrar / Reintentar", key="mahoraga_no"):
                    st.session_state.sugerencia_humana = ""
                    st.session_state.sugerencia_maquina = ""
                    st.rerun()

    func_texto = st.session_state.func_actual
    majoraga = st.session_state.majoraga

    # Verificamos si hay función activa para procesar
    if not func_texto or not func_texto.strip():
        st.info("👈 Por favor, ingresa una ecuación usando el teclado o el pizarrón táctil en la barra lateral para comenzar.")
    else:
        x0 = st.sidebar.slider("Punto x (Evaluación):", min_value=-5.0, max_value=5.0, value=1.20, step=0.05)

        # ==========================================
        # PROCESAMIENTO MATEMÁTICO
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

            # ==========================================
            # PRESENTACIÓN VISUAL
            # ==========================================
            st.markdown("### 📝 Ecuación Adaptada")
            
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1: st.latex(f"{majoraga} = " + latex_f)
            with col_f2: st.latex(f"{majoraga}" + r"^{\prime} = " + latex_df)
            with col_f3: st.latex(f"{majoraga}" + r"^{\prime\prime} = " + latex_ddf)

            st.markdown("---")
            col_datos, col_graficas = st.columns([1, 2.2])

            with col_datos:
                st.markdown("### 📍 Reporte Clave")
                def format_math_set(titulo, valores):
                    if valores:
                        str_vals = ", ".join([str(v) for v in valores])
                        return r"\text{" + titulo + r": } \{ " + str_vals + r" \}"
                    return r"\text{" + titulo + r": } \emptyset"

                st.latex(format_math_set("Raíces (X)", intersecciones_x))
                st.latex(r"\text{Corte Y: } " + str(interseccion_y))
                st.latex(format_math_set("Máximos", maximos))
                st.latex(format_math_set("Mínimos", minimos))
                st.latex(format_math_set("Inflexión", puntos_inflexion))
                
                st.markdown("---")
                st.markdown("### 🎯 Evaluación en Punto")
                st.latex(f"x_0 = {x0:.2f}")
                st.latex(f"{majoraga}({x0:.2f}) = {y0:.2f}")
                st.latex(f"{majoraga}'({x0:.2f}) = {m:.2f} " + r"\quad \text{(Pendiente)}")

            with col_graficas:
                f_num = sp.lambdify(x, f_simbolica, 'numpy')
                df_num = sp.lambdify(x, df_simbolica, 'numpy')
                ddf_num = sp.lambdify(x, ddf_simbolica, 'numpy')

                x_vals = np.linspace(-5, 5, 800)
                
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
                ax1.plot(x_vals, y_vals_f, color="#00d2ff", linewidth=2.2, label=f"${majoraga}$")
                ax1.plot(x_vals, y_tangente, color="#ffb86c", linestyle="--", label="Tangente")
                ax1.fill_between(x_vals, np.min(y_vals_f)-5, np.max(y_vals_f)+5, where=(y_vals_ddf > 0), color='#50fa7b', alpha=0.08)
                ax1.fill_between(x_vals, np.min(y_vals_f)-5, np.max(y_vals_f)+5, where=(y_vals_ddf < 0), color='#ff5555', alpha=0.08)
                ax1.plot(x0, y0, 'o', color="#f1fa8c", markersize=7)
                ax1.axhline(0, color='gray', linewidth=0.5); ax1.axvline(0, color='gray', linewidth=0.5)
                ax1.set_title(f"1. Anatomía de {majoraga}", color="white", fontsize=10)
                ax1.grid(True, linestyle=':', alpha=0.3)
                ax1.legend(loc="upper right", facecolor='#1e222d', edgecolor='#1e222d', labelcolor="white")

                # Gráfica 2
                ax2.set_facecolor('#1e222d')
                ax2.plot(x_vals, y_vals_df, color="#ff79c6", linewidth=2, label=f"${majoraga}'$")
                ax2.plot(x0, m, 'o', color="#f1fa8c", markersize=7)
                ax2.axhline(0, color='gray', linewidth=1); ax2.axvline(0, color='gray', linewidth=0.5)
                ax2.set_title("2. Segunda Derivada (Monotonía)", color="white", fontsize=10)
                ax2.grid(True, linestyle=':', alpha=0.3)
                ax2.legend(loc="upper right", facecolor='#1e222d', edgecolor='#1e222d', labelcolor="white")

                # Gráfica 3
                ax3.set_facecolor('#1e222d')
                ax3.plot(x_vals, y_vals_ddf, color="bd93f9", linewidth=2, label=f"${majoraga}''$")
                eval_ddf_0 = float(ddf_simbolica.subs(x, x0)) if not isinstance(ddf_simbolica, (int, float, np.number)) else float(ddf_simbolica)
                ax3.plot(x0, eval_ddf_0, 'o', color="#f1fa8c", markersize=7)
                ax3.fill_between(x_vals, 0, y_vals_ddf, where=(y_vals_ddf > 0), color='#50fa7b', alpha=0.3)
                ax3.fill_between(x_vals, 0, y_vals_ddf, where=(y_vals_ddf < 0), color='#ff5555', alpha=0.3)
                ax3.axhline(0, color='white', linewidth=1); ax3.axvline(0, color='gray', linewidth=0.5)
                ax3.set_title("3. Tercera Derivada / Concavidad", color="white", fontsize=10)
                ax3.grid(True, linestyle=':', alpha=0.3)
                ax3.legend(loc="upper right", facecolor='#1e222d', edgecolor='#1e222d', labelcolor="white")

                st.pyplot(fig)

        except Exception as e:
            st.error(f"⚠️ Revisa la sintaxis. Error: {e}")
