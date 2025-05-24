import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify, diff, limit
import time

# --- Setup ---
st.set_page_config(page_title="CalCS: Interactive Visualizer", layout="centered")
st.title("CalCS Interactive Visualizer: Limits and Derivatives")

# --- About Section ---
with st.expander("ℹ️ About This Project"):
    st.markdown("""
    **CalCS** is a mathematical project focused on the fundamental concepts of **limits** and **derivatives**.

    🔍 **Goals:**
    - Create interactive tools and visualizations to explore calculus.
    - Provide step-by-step animations to show the transition from secants to tangents.
    - Include problems and real-world applications to reinforce learning.

    👥 **Group Members:**
    - Carolino, Marc Christian
    - Martinez, John Benedict
    - Hugo, Isiah Lourd
    - Penaflor, Joseph Ryan

    💡 This app is built using **Streamlit** and **SymPy**, designed for students to learn visually and interactively.
    """)

x = symbols('x')

# --- Sidebar Function Input ---
st.sidebar.header("Function Settings")
func_input = st.sidebar.text_input("Enter a function of x:", "sin(x)")

try:
    expr = sympify(func_input)
    f = lambdify(x, expr, modules=['numpy'])
    f_prime_expr = diff(expr, x)
    f_prime = lambdify(x, f_prime_expr, modules=['numpy'])
except Exception as e:
    st.error(f"Error parsing function: {e}")
    st.stop()

x_vals = np.linspace(-10, 10, 400)
y_vals = f(x_vals)

# --- Educational Explanations ---
st.header("Learn the Concepts")

with st.expander("🔹 What is a Limit?"):
    st.markdown(r"""
    A **limit** helps us understand how a function behaves as the input value gets close to a specific point—even if the function isn't defined at that exact point.

    For example:

    \[
    \lim_{x \to 2} x^2 = 4
    \]

    > **Why it matters:** Limits are the foundation of calculus and help define both derivatives and continuity.
    """)

with st.expander("🔹 What is a Derivative?"):
    st.markdown(r"""
    A **derivative** tells us how a function is changing **at a specific point**—it's the **instantaneous rate of change** or the slope of the curve at that point.

    It's defined using a limit:

    \[
    f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}
    \]

    > **In simple terms:** The derivative tells us how steep the function is at a particular x-value.
    """)

with st.expander("🔹 From Secant to Tangent"):
    st.markdown(r"""
    A **secant line** connects two points on a curve. As the two points get closer, the secant line turns into a **tangent line**, which just touches the curve at one point.

    This transition illustrates how we use limits to define a **tangent line**—which is exactly what a derivative represents.

    > **Key idea:** The derivative is the slope of the tangent, and the tangent is the "limit" of secant lines as the two points converge.
    """)

# --- Derivative Visualization ---
st.header("Tangent Line Visualizer")
a = st.slider("Choose x-value for tangent:", -10.0, 10.0, 1.0, 0.1)
tangent_line = f(a) + f_prime(a) * (x_vals - a)

fig1, ax1 = plt.subplots()
ax1.plot(x_vals, y_vals, label="f(x)", linewidth=2)
ax1.plot(x_vals, tangent_line, '--', label=f"Tangent at x={a:.2f}", color='red')
ax1.scatter([a], [f(a)], color='black')
ax1.set_title(f"Function and Tangent at x = {a:.2f}")
ax1.set_xlabel("x")
ax1.set_ylabel("f(x)")
ax1.grid(True)
ax1.legend()
st.pyplot(fig1)
plt.close(fig1)

st.markdown(f"**f'(x)** = `{f_prime_expr}`")
st.markdown(f"**f'({a:.2f})** = `{f_prime(a):.4f}`")

# --- Limit Calculator ---
st.header("Limit Calculator")
limit_point = st.slider("Choose x-value for limit:", -10.0, 10.0, 1.0, 0.1)

try:
    lim_left = limit(expr, x, limit_point, dir='-')
    lim_right = limit(expr, x, limit_point, dir='+')

    st.latex(f"\\text{{Left Limit: }} \\lim_{{x \\to {limit_point}^-}} f(x) = {lim_left}")
    st.latex(f"\\text{{Right Limit: }} \\lim_{{x \\to {limit_point}^+}} f(x) = {lim_right}")

    if lim_left == lim_right:
        st.success(f"✅ Limit exists and equals `{lim_left}`")
    else:
        st.error("❌ Limit does not exist (left ≠ right)")
except Exception as e:
    st.error(f"Limit error: {e}")

# --- Secant to Tangent Animation ---
st.header("Animation: Secant Line to Tangent")
if st.button("Run Animation"):
    placeholder = st.empty()
    h_vals = np.linspace(1.0, 0.01, 20)
    for h in h_vals:
        fig2, ax2 = plt.subplots()
        ax2.plot(x_vals, y_vals, label="f(x)", linewidth=2)
        x0, x1 = a, a + h
        y0, y1 = f(x0), f(x1)
        slope = (y1 - y0) / (x1 - x0)
        secant = slope * (x_vals - x0) + y0
        ax2.plot(x_vals, secant, '--', label=f"Secant h={h:.4f}", color='orange')
        ax2.scatter([x0, x1], [y0, y1], color='black')
        ax2.set_title(f"Secant → Tangent at x={a:.2f}")
        ax2.grid(True)
        ax2.legend()
        placeholder.pyplot(fig2)
        plt.close(fig2)
        time.sleep(0.2)

# --- Problem Set ---
st.header("Problem Set")
with st.expander("🧠 Try This: Derivative at a Point"):
    st.markdown("Find the derivative of \( f(x) = x^2 + 3x \) at \( x = 2 \)")
    if st.button("Show Solution 1"):
        st.latex("f'(x) = 2x + 3")
        st.latex("f'(2) = 2(2) + 3 = 7")

with st.expander("🧠 Try This: Limit at a Point"):
    st.markdown("Evaluate \( \lim_{x \to 1} \frac{x^2 - 1}{x - 1} \)")
    if st.button("Show Solution 2"):
        st.latex("= \lim_{x \to 1} \frac{(x - 1)(x + 1)}{x - 1} = \lim_{x \to 1} x + 1 = 2")

with st.expander("🧠 Try This: One-Sided Limit"):
    st.markdown("Evaluate the left-hand limit \( \lim_{x \to 0^-} \frac{|x|}{x} \)")
    if st.button("Show Solution 3"):
        st.latex(r"\lim_{x \to 0^-} \frac{-x}{x} = -1")

with st.expander("🧠 Try This: Power Rule"):
    st.markdown("Find the derivative of \( f(x) = 4x^3 - 2x^2 + x - 7 \)")
    if st.button("Show Solution 4"):
        st.latex("f'(x) = 12x^2 - 4x + 1")

with st.expander("🧠 Try This: Tangent Line Equation"):
    st.markdown("Find the equation of the tangent line to \( f(x) = x^2 \) at \( x = 3 \)")
    if st.button("Show Solution 5"):
        st.latex("f'(x) = 2x \\Rightarrow f'(3) = 6")
        st.latex("Point: (3, 9), Slope: 6")
        st.latex("Tangent Line: y - 9 = 6(x - 3) \\Rightarrow y = 6x - 9")

# --- Real-World Application ---
st.header("Real-World Application")
with st.expander("🚗 Velocity of a Moving Car"):
    st.markdown(r"""
    Suppose the position of a car is given by \( s(t) = 5t^2 \).

    The velocity is the derivative of position:
    \[ v(t) = s'(t) = 10t \]

    At \( t = 3 \) seconds, the car is moving at:
    \[ v(3) = 30 \text{ m/s} \]

    This shows how derivatives represent real-world rates of change.
    """)
