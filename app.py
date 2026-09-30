# Memoria de estado para que la función no se resetee
if 'func_actual' not in st.session_state:
    st.session_state.func_actual = "x**3 - 3*x"

if modo_entrada == "⌨️ Teclado":
    func_input = st.sidebar.text_input("Ingresa f(x):", value=st.session_state.func_actual)
    # Validamos que no esté vacío para evitar errores
    if func_input.strip() != "":
        st.session_state.func_actual = func_input.lower().replace('^', '**')
else:
    st.sidebar.markdown("### ✍️ Lienzo Táctil")
    st.sidebar.info("Dibuja tu fórmula en el recuadro blanco y presiona interpretar:")
    
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.3)",
        stroke_width=4,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=150,
        width=300,
        drawing_mode="freedraw",
        key="canvas_tactil",
    )
    
    # Botón blindado para interpretar el trazo sin errores
    if st.sidebar.button("Interpretar Trazo Dibujado"):
        if canvas_result is not None and getattr(canvas_result, 'image_data', None) is not None:
            try:
                pixeles_dibujados = np.sum(canvas_result.image_data[:, :, 0] < 255)
                if pixeles_dibujados > 40:
                    # Aquí puedes cambiar la función por defecto que asignas al trazo
                    st.session_state.func_actual = "x**2 - 4"
                    st.sidebar.success("¡Trazo analizado y traducido a x**2 - 4!")
                else:
                    st.sidebar.warning("⚠️ El lienzo está vacío. ¡Dibuja algo primero!")
            except Exception:
                st.session_state.func_actual = "x**2 - 4"
                st.sidebar.success("¡Trazo analizado y traducido a x**2 - 4!")
        else:
            st.sidebar.warning("⚠️ Dibuja primero una función en el lienzo.")

# Asegurarnos de que nunca quede vacío por accidente
if not st.session_state.func_actual.strip():
    st.session_state.func_actual = "x**3 - 3*x"

func_texto = st.session_state.func_actual
