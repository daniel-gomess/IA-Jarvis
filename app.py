import customtkinter as ctk
import threading
from ollama import chat

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def ask(prompt: str, update_callback):
    stream = chat(
        model="gemma3:1b",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        content = chunk["message"]["content"]
        update_callback(content)

def enviar_prompt():
    prompt = entry_prompt.get()
    text_resposta.configure(state="normal")
    text_resposta.delete("0.0", "end")
    text_resposta.configure(state="disabled")
    btn_enviar.configure(state="disabled")
    threading.Thread(target=stream_ask, args=(prompt,)).start()

def stream_ask(prompt):
    def update_text(content):
        text_resposta.configure(state="normal")
        text_resposta.insert("end", content)
        text_resposta.see("end")
        text_resposta.configure(state="disabled")
    ask(prompt, lambda content: text_resposta.after(0, update_text, content))
    btn_enviar.configure(state="normal")

root = ctk.CTk()
root.title("JARVIS")
root.geometry("400x500")
root.minsize(400, 300)

# Apenas a linha e coluna do campo de resposta são expansíveis
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

label_prompt = ctk.CTkLabel(root, text="Prompt:")
label_prompt.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="w")

entry_prompt = ctk.CTkEntry(root)
entry_prompt.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

btn_enviar = ctk.CTkButton(root, text="Enviar", command=enviar_prompt)
btn_enviar.grid(row=2, column=0, padx=10, pady=10)  # Não é expansível

label_resposta = ctk.CTkLabel(root, text="Resposta:")
label_resposta.grid(row=3, column=0, padx=10, pady=(20, 0), sticky="w")

# Apenas este campo é responsivo
text_resposta = ctk.CTkTextbox(root, font=("Consolas", 12), state="disabled", wrap="word")
text_resposta.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

root.mainloop()