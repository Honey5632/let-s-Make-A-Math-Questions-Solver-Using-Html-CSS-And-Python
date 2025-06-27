from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, Eq, solve, sympify
import io

app = Flask(__name__)

x = symbols('x')

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    graph_generated = False
    question = ""

    if request.method == "POST":
        question = request.form["question"]
        try:
            if "plot" in question.lower() or "graph" in question.lower():
                expr = question.lower().replace("plot", "").replace("graph", "").strip()
                expr = expr.replace("=", "-(") + ")"
                f = sympify(expr)
                f_lambdified = sympify(f).lambdify(x, modules=["numpy"])

                x_vals = np.linspace(-10, 10, 400)
                y_vals = f_lambdified(x_vals)

                plt.figure()
                plt.plot(x_vals, y_vals, label=f"y = {question}")
                plt.axhline(0, color="black", linewidth=0.5)
                plt.axvline(0, color="black", linewidth=0.5)
                plt.title("Graph of the Equation")
                plt.grid(True)
                plt.legend()

                buf = io.BytesIO()
                plt.savefig("static/graph.png", format="png")
                buf.seek(0)
                plt.close()
                graph_generated = True
                result = "Graph generated below."

            else:
                if "=" in question:
                    left, right = question.split("=")
                    eq = Eq(sympify(left), sympify(right))
                    sol = solve(eq)
                    result = f"Solution: {sol}"
                else:
                    result = f"Result: {sympify(question).evalf()}"

        except Exception as e:
            result = f"Error: {e}"

    return render_template("index.html", result=result, graph=graph_generated, question=question)

@app.route("/graph")
def graph():
    return send_file("static/graph.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
