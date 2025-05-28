import customtkinter as ctk
import threading
from ollama import chat
import speech_recognition as sr
import time
import numpy as np

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

recognizer = sr.Recognizer()
parar_resposta = False
gravando_audio = False
audio_data = None
audio_thread = None
escutando = False
parar_fala = False

def ask(prompt: str, update_callback):
    global parar_resposta
    parar_resposta = False
    stream = chat(
        model="gemma3:1b",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        if parar_resposta:
            break
        content = chunk["message"]["content"]
        update_callback(content)

def enviar_prompt():
    prompt = entry_prompt.get("0.0", "end").strip()
    text_resposta.configure(state="normal")
    text_resposta.delete("0.0", "end")
    text_resposta.configure(state="disabled")
    btn_enviar.configure(state="disabled")
    btn_falar.configure(state="disabled")
    entry_prompt.configure(state="disabled")
    btn_parar.configure(state="normal")
    threading.Thread(target=stream_ask, args=(prompt,)).start()

def stream_ask(prompt):
    def update_text(content):
        text_resposta.configure(state="normal")
        text_resposta.insert("end", content)
        text_resposta.see("end")
        text_resposta.configure(state="disabled")
    ask(prompt, lambda content: text_resposta.after(0, update_text, content))
    btn_enviar.configure(state="normal")
    btn_falar.configure(state="normal")
    entry_prompt.configure(state="normal")
    btn_parar.configure(state="disabled")

def parar_resposta_func():
    global parar_resposta
    parar_resposta = True
    btn_parar.configure(state="disabled")
    btn_enviar.configure(state="normal")
    btn_falar.configure(state="normal")
    entry_prompt.configure(state="normal")

def alternar_gravacao():
    global gravando_audio, audio_thread, audio_data, escutando, parar_fala
    if not gravando_audio:
        gravando_audio = True
        escutando = True
        parar_fala = False
        btn_falar.configure(text="Pronto", state="normal")
        btn_enviar.configure(state="disabled")
        btn_parar.configure(state="disabled")
        entry_prompt.configure(state="normal")
        entry_prompt.delete("0.0", "end")
        entry_prompt.insert("0.0", "Pode falar...")
        entry_prompt.configure(state="disabled")
        ajustar_altura_entry()
        audio_data = None
        audio_thread = threading.Thread(target=gravar_audio_silencio)
        audio_thread.start()
    else:
        parar_fala = True
        btn_falar.configure(state="disabled")
        btn_falar.configure(text="Falar")
        # Aguarda a thread terminar e processa o áudio
        audio_thread.join()
        threading.Thread(target=processar_audio).start()

def gravar_audio_silencio():
    global audio_data, gravando_audio, parar_fala
    with sr.Microphone() as source:
        recognizer.pause_threshold = 0.8  # mais sensível a pausas curtas
        frames = []
        start_time = time.time()
        last_voice_time = time.time()
        silence_limit = 5  # segundos de silêncio para encerrar
        chunk_duration = 0.5  # segundos
        sample_rate = int(source.SAMPLE_RATE)
        chunk_samples = int(sample_rate * chunk_duration)
        try:
            while True:
                if parar_fala:
                    break
                audio = source.stream.read(chunk_samples)
                frames.append(audio)
                # Converte para numpy para medir volume
                audio_np = np.frombuffer(audio, np.int16)
                volume = np.abs(audio_np).mean()
                if volume > 500:  # valor empírico, ajuste se necessário
                    last_voice_time = time.time()
                if time.time() - last_voice_time > silence_limit:
                    break
        except Exception:
            audio_data = None
            gravando_audio = False
            return
        # Monta o AudioData final
        audio_bytes = b"".join(frames)
        audio_data = sr.AudioData(audio_bytes, sample_rate, source.SAMPLE_WIDTH)
    gravando_audio = False

def processar_audio():
    global audio_data
    if audio_data is None:
        entry_prompt.configure(state="normal")
        entry_prompt.delete("0.0", "end")
        entry_prompt.insert("0.0", "Nenhum áudio capturado.")
        ajustar_altura_entry()
        entry_prompt.configure(state="disabled")
        btn_falar.configure(state="normal", text="Falar")
        btn_enviar.configure(state="normal")
        btn_parar.configure(state="disabled")
        return
    try:
        texto = recognizer.recognize_google(audio_data, language="pt-BR")
        entry_prompt.configure(state="normal")
        entry_prompt.delete("0.0", "end")
        entry_prompt.insert("0.0", texto)
        ajustar_altura_entry()
        entry_prompt.configure(state="disabled")
        btn_falar.configure(state="disabled", text="Falar")
        btn_enviar.configure(state="disabled")
        btn_parar.configure(state="normal")
        enviar_prompt()
    except sr.UnknownValueError:
        entry_prompt.configure(state="normal")
        entry_prompt.delete("0.0", "end")
        entry_prompt.insert("0.0", "Não entendi o que foi dito.")
        ajustar_altura_entry()
        entry_prompt.configure(state="disabled")
        btn_falar.configure(state="normal", text="Falar")
        btn_enviar.configure(state="normal")
        btn_parar.configure(state="disabled")
    except sr.RequestError:
        entry_prompt.configure(state="normal")
        entry_prompt.delete("0.0", "end")
        entry_prompt.insert("0.0", "Erro ao acessar o serviço de reconhecimento.")
        ajustar_altura_entry()
        entry_prompt.configure(state="disabled")
        btn_falar.configure(state="normal", text="Falar")
        btn_enviar.configure(state="normal")
        btn_parar.configure(state="disabled")
    except Exception as e:
        entry_prompt.configure(state="normal")
        entry_prompt.delete("0.0", "end")
        entry_prompt.insert("0.0", f"Erro: {str(e)}")
        ajustar_altura_entry()
        entry_prompt.configure(state="disabled")
        btn_falar.configure(state="normal", text="Falar")
        btn_enviar.configure(state="normal")
        btn_parar.configure(state="disabled")

def ajustar_altura_entry(event=None):
    texto = entry_prompt.get("0.0", "end")
    linhas = texto.count("\n") + 1
    linhas = max(1, min(linhas, 5))
    entry_prompt.configure(height=linhas * 25)

root = ctk.CTk()
root.title("J.A.R.V.I.S")
root.geometry("700x400")
root.minsize(400, 300)

root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

label_prompt = ctk.CTkLabel(root, text="Prompt:")
label_prompt.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="w")

entry_prompt = ctk.CTkTextbox(root, height=25, font=("Consolas", 12), wrap="word")
entry_prompt.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
entry_prompt.bind("<KeyRelease>", ajustar_altura_entry)

frame_botoes = ctk.CTkFrame(root, fg_color="transparent")
frame_botoes.grid(row=2, column=0, padx=10, pady=10, sticky="w")

btn_enviar = ctk.CTkButton(frame_botoes, text="Enviar", command=enviar_prompt)
btn_enviar.pack(side="left", padx=(0, 10))

btn_falar = ctk.CTkButton(frame_botoes, text="Falar", command=alternar_gravacao)
btn_falar.pack(side="left", padx=(0, 10))

btn_parar = ctk.CTkButton(frame_botoes, text="Parar", command=parar_resposta_func, state="disabled")
btn_parar.pack(side="left")

label_resposta = ctk.CTkLabel(root, text="Resposta:")
label_resposta.grid(row=3, column=0, padx=10, pady=(20, 0), sticky="w")

text_resposta = ctk.CTkTextbox(root, font=("Consolas", 12), state="disabled", wrap="word")
text_resposta.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

root.mainloop()