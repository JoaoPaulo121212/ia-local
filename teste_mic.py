import sounddevice as sd # type: ignore

print("--- LISTA DE DISPOSITIVOS DE ÁUDIO ---")
print(sd.query_devices())

print("\n--- TESTE DO DISPOSITIVO PADRÃO ---")
try:
    padrao = sd.query_devices(kind='input')
    print(f"Microfone Padrão: {padrao['name']}")
    print(f"Canais: {padrao['max_input_channels']}")
except Exception as e:
    print(f"ERRO: Não encontrei nenhum microfone padrão! Detalhe: {e}")