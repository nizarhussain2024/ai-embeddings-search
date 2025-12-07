from flask import Flask

app = Flask(__name__)

@app.get("/health")
def health():
    return "AI Embeddings Search Running"

if __name__ == "__main__":
    app.run(port=5000)
