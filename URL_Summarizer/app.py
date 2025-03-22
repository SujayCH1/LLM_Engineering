from flask import Flask, render_template, request, jsonify
from summarization import summarize_website  

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url.startswith("http"):
            url = "https://" + url
        
        summary_data = summarize_website(url)  
        return jsonify(summary_data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
