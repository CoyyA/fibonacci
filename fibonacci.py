import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title="Fibonacci sequence", page_icon="🌀")
st.title("🌀 Fibonacci Sequence 🌀")

# Initialize session state for quiz status
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False

# Show info section only if quiz hasn't started
if not st.session_state.quiz_started:
    with st.expander("ℹ️ About the Fibonacci Sequence", expanded=False):
        st.markdown("""
        ### What is the Fibonacci Sequence?
        The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones, 
        usually starting with 0 and 1. The sequence goes:

        0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ...

        Mathematically, it can be defined as:

        F₀ = 0, F₁ = 1

        Fₙ = Fₙ₋₁ + Fₙ₋₂ for n > 1

        ### Interesting Properties
        - The ratio of consecutive Fibonacci numbers approaches the **golden ratio** (≈1.618) as n increases
        - The sequence appears in biological settings, such as branching in trees, arrangement of leaves, fruit sprouts, etc.
        - Fibonacci numbers appear in the petals of flowers and spirals of shells

        ### Applications
        - Computer algorithms (Fibonacci heap, Fibonacci search)
        - Financial markets (Fibonacci retracements)
        - Art and architecture (aesthetic proportions)
        """)

    # Add a visual example
    st.subheader("Visual Representation")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("2D Fibonacci Spiral")


        def generate_fibonacci(n):
            sequence = []
            a, b = 0, 1
            for _ in range(n):
                sequence.append(a)
                a, b = b, a + b
            return sequence


        n_points = st.slider("Number of points for 2D visualization", 5, 50, 10, key="2d_slider")
        fib = generate_fibonacci(n_points)

        # Create golden spiral coordinates
        theta = np.linspace(0, 4 * np.pi, n_points)  # Reduced rotation for 2D
        radius = np.array(fib) / max(fib) * 5  # Normalized and scaled

        x = radius * np.cos(theta)
        y = radius * np.sin(theta)

        fig, ax = plt.subplots(figsize=(6, 6))

        # Plot quarter circles to approximate the spiral
        for i in range(n_points - 1):
            theta_arc = np.linspace(theta[i], theta[i + 1], 50)
            r = radius[i] + (radius[i + 1] - radius[i]) * (theta_arc - theta[i]) / (theta[i + 1] - theta[i])
            x_arc = r * np.cos(theta_arc)
            y_arc = r * np.sin(theta_arc)
            ax.plot(x_arc, y_arc, 'b-', alpha=0.7)

        ax.scatter(x, y, c='r', s=50)

        # Annotate points
        for i in range(0, n_points, 2):
            ax.text(x[i], y[i], f'F{i}={fib[i]}', fontsize=8, ha='right')

        ax.set_xlim(-5.5, 5.5)
        ax.set_ylim(-5.5, 5.5)
        ax.set_aspect('equal')
        ax.set_title('2D Fibonacci Spiral')
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

    with col2:
        st.subheader("3D Fibonacci Visualization")


        # Generate Fibonacci sequence
        def generate_fibonacci(n):
            sequence = []
            a, b = 0, 1
            for _ in range(n):
                sequence.append(a)
                a, b = b, a + b
            return sequence


        n_points = st.slider("Number of points for 3D visualization", 5, 50, 15, key="3d_slider")
        fib = generate_fibonacci(n_points)

        # Create smooth interpolation
        theta = np.linspace(0, 8 * np.pi, n_points)  # Original angles
        z = np.linspace(0, 10, n_points)  # Original heights

        # Create 300 smooth points
        theta_smooth = np.linspace(theta.min(), theta.max(), 300)
        fib_smooth = make_interp_spline(theta, fib)(theta_smooth)
        z_smooth = np.linspace(z.min(), z.max(), 300)

        # Convert to Cartesian coordinates
        x_smooth = fib_smooth * np.cos(theta_smooth)
        y_smooth = fib_smooth * np.sin(theta_smooth)
        x = fib * np.cos(theta)
        y = fib * np.sin(theta)

        # Create 3D plot
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Plot the smooth spiral
        ax.plot(x_smooth, y_smooth, z_smooth, 'b-', linewidth=2, alpha=0.7, label='Smooth Fibonacci Spiral')

        # Plot original points
        ax.scatter(x, y, z, c='r', s=50, label='Fibonacci Points')

        # Label every 3rd point to avoid clutter
        for i in range(0, n_points, 3):
            ax.text(x[i], y[i], z[i], f'F{i}={fib[i]}', fontsize=8, color='darkgreen')

        ax.set_xlabel('X (Fibonacci × cosθ)')
        ax.set_ylabel('Y (Fibonacci × sinθ)')
        ax.set_zlabel('Z (Height)')
        ax.set_title('Smooth 3D Fibonacci Spiral')
        ax.legend()
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

    # Add interactive calculator
    st.subheader("Fibonacci Calculator")
    n_terms = st.slider("How many Fibonacci numbers do you want to generate?", 1, 50, 10)

    fib_sequence = generate_fibonacci(n_terms)
    st.write(f"First {n_terms} Fibonacci numbers:")
    st.code(", ".join(map(str, fib_sequence)))

    st.subheader("Calculate Fibonacci Numbers")
    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Calculate Fₙ where n =", min_value=0, max_value=20, value=5)


        def fib_calc(n):
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            return a


        if st.button("Calculate"):
            st.info(f"F_{n} = {fib_calc(n)}")

    with col2:
        st.markdown("Given:")
        st.code("F₀ = 0\nF₁ = 1\nFₙ = Fₙ₋₁ + Fₙ₋₂")
        st.write("Try calculating F₇, F₁₀, etc!")

# ---- QUIZ SECTION ----
st.markdown("---")

# Show quiz button only if quiz hasn't started
if not st.session_state.quiz_started:
    if st.button("I'm ready for quiz!"):
        st.session_state.quiz_started = True
        st.rerun()
else:
    st.subheader("🧠 Test Your Fibonacci Knowledge")

    quiz_choice = st.radio("Choose a quiz type:",
                           ["Multiple Choice (15 Questions)", "Pattern Recognition"])

    if quiz_choice == "Multiple Choice (15 Questions)":
        st.markdown("### Fibonacci Knowledge Test (15 Questions)")

        # Store questions and correct answers
        questions = [
            {
                "number": 1,
                "question": "How is each Fibonacci number defined?",
                "options": ["Previous number + 2", "Sum of two preceding numbers", "Previous number × 1.618", "n² - 1"],
                "correct": "Sum of two preceding numbers"
            },
            {
                "number": 2,
                "question": "What are the first two Fibonacci numbers (F₀ and F₁)?",
                "options": ["0 and 1", "1 and 1", "1 and 2", "2 and 3"],
                "correct": "0 and 1"
            },
            {
                "number": 3,
                "question": "What does Fₙ₊₁/Fₙ approach as n increases?",
                "options": ["π (3.1416...)", "Golden Ratio (1.618...)", "Euler's Number (2.718...)", "√2 (1.414...)"],
                "correct": "Golden Ratio (1.618...)"
            },
            {
                "number": 4,
                "question": "Where is the Fibonacci sequence NOT commonly observed?",
                "options": ["Flower petal counts", "Hurricane spiral patterns", "Atomic electron configurations",
                            "Pineapple spiral patterns"],
                "correct": "Atomic electron configurations"
            },
            {
                "number": 5,
                "question": "What is F₋ₙ in the Fibonacci sequence?",
                "options": ["Same as Fₙ", "(-1)ⁿ⁺¹Fₙ", "Fₙ/φ", "Undefined"],
                "correct": "(-1)ⁿ⁺¹Fₙ"
            },
            {
                "number": 6,
                "question": "What does Binet's formula calculate?",
                "options": ["Golden ratio approximation", "Exact Fibonacci numbers", "Prime numbers in the sequence",
                            "Sum of first n Fibonacci numbers"],
                "correct": "Exact Fibonacci numbers"
            },
            {
                "number": 7,
                "question": "How do Lucas numbers relate to Fibonacci?",
                "options": ["Same recurrence with different starting points", "Squares of Fibonacci numbers",
                            "Every 3rd Fibonacci number", "No relation"],
                "correct": "Same recurrence with different starting points"
            },
            {
                "number": 8,
                "question": "What's special about the sum F₁² + F₂² + ... + Fₙ²?",
                "options": ["Equals Fₙ × Fₙ₊₁", "Always prime", "Forms geometric progression", "Equals φⁿ"],
                "correct": "Equals Fₙ × Fₙ₊₁"
            },
            {
                "number": 9,
                "question": "What's true about every 3rd Fibonacci number?",
                "options": ["Always even", "Always odd", "Always prime", "Always square"],
                "correct": "Always even"
            },
            {
                "number": 10,
                "question": "What is gcd(Fₙ, Fₘ)?",
                "options": ["Fₙ₊ₘ", "F_gcd(n,m)", "gcd(n,m)", "Always 1"],
                "correct": "F_gcd(n,m)"
            }
        ]

        # Display questions and collect answers
        user_answers = {}
        for q in questions:
            st.markdown(f"#### {q['number']}. {q['question']}")
            user_answers[q['number']] = st.radio(
                q['question'],
                q['options'],
                key=f"q{q['number']}"
            )

        if st.button("Check Answers"):
            score = 0
            wrong_answers = []

            for q in questions:
                if user_answers[q['number']] == q['correct']:
                    score += 1
                else:
                    wrong_answers.append({
                        "Question": q['number'],
                        "Your Answer": user_answers[q['number']],
                        "Correct Answer": q['correct']
                    })

            st.success(f"Your score: {score}/10 ({score * 10}%)")

            if score == 10:
                st.balloons()
                st.success("Perfect! Fibonacci Master!")
            elif score >= 7:
                st.success("Good job! You know your Fibonacci facts!")
            else:
                st.info("Keep learning about this fascinating sequence!")

            if wrong_answers:
                st.markdown("### Incorrect Answers Review")
                st.write("Here are the questions you answered incorrectly:")

                # Create a table of wrong answers
                st.table(wrong_answers)

                st.markdown("**Explanation of Key Concepts:**")
                st.markdown("""
                - **Definition**: Each Fibonacci number is the sum of the two preceding ones (Fₙ = Fₙ₋₁ + Fₙ₋₂)
                - **Golden Ratio**: The ratio of consecutive Fibonacci numbers approaches φ ≈ 1.618
                - **Negative Indices**: F₋ₙ = (-1)ⁿ⁺¹Fₙ (the sequence extends backwards with alternating signs)
                - **GCD Property**: gcd(Fₙ, Fₘ) = F_gcd(n,m) (Fibonacci numbers are divisibility sequences)
                - **Sum of Squares**: The sum of squares of first n Fibonacci numbers equals Fₙ × Fₙ₊₁
                """)

    elif quiz_choice == "Pattern Recognition":
        st.markdown("#### Complete the Sequence")
        st.write("What are the next three numbers in this sequence?")

        seq = [0, 1, 1, 2, 3, 5, 8, "?", "?", "?"]
        st.code(" ".join(map(str, seq)))

        answers = st.text_input("Enter the next three numbers (space separated):")

        if answers:
            user_ans = answers.split()
            correct_ans = ["13", "21", "34"]

            if len(user_ans) != 3:
                st.warning("Please enter exactly 3 numbers")
            else:
                if user_ans == correct_ans:
                    st.success("Perfect! You recognized the pattern")
                    st.balloons()
                else:
                    st.error("Almost! Check the sequence again: each number is the sum of the two before it")
                    st.write(f"Correct answer: {' '.join(correct_ans)}")

    # Add a button to return to info
    if st.button("Back to Info"):
        st.session_state.quiz_started = False
        st.rerun()

# Add a fun fact at the end
st.markdown("---")
st.markdown(
    "💡 **Did You Know?** The Fibonacci sequence appears in sunflower seed patterns, pineapple scales, and galaxy spirals!")
