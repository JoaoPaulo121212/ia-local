import sounddevice as sd #type: ignore
import scipy.io.wavfile as wav #type: ignore
import whisper #type: ignore
import ollama #type: ignore
import numpy as np
import os
import time
import subprocess 

# --- CONFIGURAÇÕES ---
ARQUIVO_AUDIO = "comando_voz.wav"
MODELO_WHISPER = "base"
MODELO_LLAMA = "llama3"

def gravar_audio(duracao=5):
    print("\n🎤 Listening... (Speak now!)")
    freq = 44100 
    try:
        gravacao = sd.rec(int(duracao * freq), samplerate=freq, channels=1, dtype='float32')
        for i in range(duracao):
            time.sleep(1)
            print("." * (i+1), end="\r")
        sd.wait()
        
        volume_maximo = np.max(np.abs(gravacao))
        if volume_maximo > 0:
            gravacao = gravacao / volume_maximo * 0.9
        
        gravacao = gravacao.squeeze()
        wav.write(ARQUIVO_AUDIO, freq, (gravacao * 32767).astype(np.int16))
        print("\n Recording complete.")
        return True
    except Exception as e:
        print(f"\n Recording Error: {e}")
        return False

def transcrever_audio():
    if not os.path.exists(ARQUIVO_AUDIO): return ""
    print("Transcribing...")
    try:
        model = whisper.load_model(MODELO_WHISPER)
        result = model.transcribe(ARQUIVO_AUDIO, fp16=False, language='en')
        return result["text"]
    except Exception as e:
        print(f"Whisper Error: {e}")
        return ""

def falar_resposta(texto):
    if not texto: return
    texto_limpo = texto.replace("'", "").replace('"', '').replace('\n', ' ')
    os.system(f"say '{texto_limpo}'")

def extrair_nome_app(texto):
    try:
        resposta = ollama.chat(model=MODELO_LLAMA, messages=[
            {
                'role': 'system',
                'content': 'You are an extraction tool. Extract ONLY the application name from the user command. Return just the name, nothing else. Example: "Open Google Chrome" -> "Google Chrome".'
            },
            {
                'role': 'user',
                'content': texto
            },
        ])
        nome_app = resposta['message']['content'].strip()
        # Remove pontuação final se houver (ex: "Spotify.")
        return nome_app.replace(".", "")
    except:
        return None

def abrir_app_generico(texto):
    
    app_name = extrair_nome_app(texto)
    
    if not app_name:
        return False

    falar_resposta(f"Attempting to open {app_name}")
    
    try:
        resultado = subprocess.run(
            ["open", "-a", app_name], 
            capture_output=True, 
            text=True
        )
        
        if resultado.returncode == 0:
            print(f"Opened {app_name}")
            return True
        else:
            # Se falhar, o Mac geralmente retorna erro
            erro_msg = f"I couldn't find an app named {app_name} installed on your Mac."
            print(f" Error: {erro_msg}")
            falar_resposta(erro_msg)
            return True # Retorna True para dizer que tentamos executar um comando
            
    except Exception as e:
        falar_resposta("Something went wrong trying to open that app.")
        return True

def perguntar_ia(texto):
    print(f"Thinking...")
    try:
        resposta = ollama.chat(model=MODELO_LLAMA, messages=[
            {'role': 'system', 'content': 'You are Jarvis. Answer in ONE short sentence in English.'},
            {'role': 'user', 'content': texto},
        ])
        return resposta['message']['content']
    except:
        return "Offline."

def main():
    os.system('clear') 
    print("--- FRIDAY ---")
    print("Commands: Type 'exit' to quit.")
    
    while True:
        try:
            print("\n" + "-"*40)
            entrada = input("[Press ENTER to Speak] or type: ").strip()
            texto_final = ""

            if entrada:
                if entrada.lower() in ['exit', 'quit']: break
                texto_final = entrada
                print(f" Typed: '{texto_final}'")
            else:
                if not gravar_audio(duracao=5): continue
                texto_final = transcrever_audio()
                print(f" Said: '{texto_final}'")

            if not texto_final.strip(): continue
            
            texto_lower = texto_final.lower()
            
            # Se tiver "open", "start" ou "launch", assumimos que é um App
            palavras_gatilho = ["open", "start", "launch", "abrir"]
            
            if any(p in texto_lower for p in palavras_gatilho):
                if abrir_app_generico(texto_final):
                    continue

            resposta_ia = perguntar_ia(texto_final)
            print(f"🤖 Jarvis: {resposta_ia}")
            falar_resposta(resposta_ia)
            
        except KeyboardInterrupt:
            print("\nBye!")
            break

if __name__ == "__main__":
    main()