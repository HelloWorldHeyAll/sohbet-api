from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = genai.Client(api_key=os.getenv("API_KEY"))

with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

chat = client.chats.create(
    model="gemini-3.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.7
    )
)

# Tarayıcıda açılacak arayüzü sunan kök dizin (/)
@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kasideler Diyarı</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            h2 { color: #333; }
            #chat-container { width: 100%; max-width: 600px; height: 400px; background: white; border: 1px solid #ccc; border-radius: 8px; padding: 15px; overflow-y: scroll; display: flex; flex-direction: column; gap: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .message { padding: 10px 14px; border-radius: 6px; max-width: 80%; line-height: 1.4; word-wrap: break-word; }
            .user { background: #007bff; color: white; align-self: flex-end; }
            .ai { background: #e9ecef; color: #333; align-self: flex-start; }
            #input-container { width: 100%; max-width: 600px; display: flex; margin-top: 15px; gap: 10px; }
            input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 6px; font-size: 16px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
            button:hover { background: #0056b3; }
        </style>
    </head>
    <body>

        <h2>📜 probot robot 3000</h2>
        <div id="chat-container"></div>

        <div id="input-container">
            <input type="text" id="mesajInput" placeholder="Probot robot 3000 ile sohbet et..." onkeypress="handleKeyPress(event)">
            <button onclick="mesajGonder()">Gönder</button>
        </div>

        <script>
            async function mesajGonder() {
                const input = document.getElementById('mesajInput');
                const container = document.getElementById('chat-container');
                const mesaj = input.value.trim();
                
                if (!mesaj) return;

                // Kullanıcı mesajını ekrana bas
                container.innerHTML += `<div class="message user"><b>Sen:</b> ${mesaj}</div>`;
                input.value = '';
                container.scrollTop = container.scrollHeight;

                try {
                    // Senin tanımladığın /chat endpoint'ine istek atıyoruz
                    const response = await fetch(`/chat?mesaj=${encodeURIComponent(mesaj)}`);
                    const data = await response.json();

                    // AI yanıtını ekrana bas
                    container.innerHTML += `<div class="message ai"><b>Yapay Zekâ:</b> ${data.AI}</div>`;
                    container.scrollTop = container.scrollHeight;
                } catch (error) {
                    container.innerHTML += `<div class="message ai" style="color:red;"><b>Hata:</b> Sunucuya ulaşılamadı.</div>`;
                }
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    mesajGonder();
                }
            }
        </script>

    </body>
    </html>
    """

# Senin kodundaki orijinal /chat endpoint'i ve fonksiyonun
@app.get("/chat")
async def sor(mesaj: str):
    response = chat.send_message(mesaj)
    return {"AI": response.text}