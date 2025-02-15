from flask import Flask, request, render_template, jsonify
import steno

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/compare", methods=["POST"])
def compare():
    orig_text = request.form["orig_text"]
    typed_text = request.form["typed_text"]
    duration_seconds = float(request.form["duration_seconds"])

    diff_html, stats = steno.generate_diff_html_and_stats(
        original_text=orig_text,
        typed_text=typed_text,
        duration_seconds=duration_seconds,
    )

    return jsonify({"diff_html": diff_html, "stats": stats})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
