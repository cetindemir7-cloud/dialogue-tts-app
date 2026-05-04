from flask import Flask, request, send_file
from openai import OpenAI
import tempfile
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return """
    <html>
    <body style="background:black;color:white;font-family:sans-serif;padding:40px">
    <h2>Senaryo Seslendirme</h2>

    <textarea id="text" style="width:100%;height:200px;">
KEMAL: Geldin mi?
YELİZ: Geldim.
    </textarea><br><br>

    <button onclick="play()">Oynat</button>

    <script>
    async function play(){
        const text = document.getElementById("text").value;

        const res = await fetch("/tts", {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({text})
        });

        const blob = await res.blob();
        const audio = new Audio(URL.createObjectURL(blob));
        audio.play();
    }
    </script>
    </body>
    </html>
    """

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json["text"]

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.write(response.content)
    tmp.close()

    return send_file(tmp.name, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
