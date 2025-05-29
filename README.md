J.A.R.V.I.S - Assistente Virtual Local com Interface Gráfica

Este projeto implementa o J.A.R.V.I.S, um assistente virtual local com interface gráfica desenvolvida em Python utilizando a biblioteca CustomTkinter. O sistema permite que o usuário interaja por texto ou por voz, recebendo respostas de um modelo de linguagem local via Ollama.

Funcionalidades
- Interface gráfica moderna, responsiva e centralizada baseada em CustomTkinter
- Envio de perguntas por texto ou por voz
- Reconhecimento de voz automático: a gravação é encerrada após 5 segundos de silêncio ou manualmente pelo usuário
- Botões de interação centralizados na interface
- Campo de entrada de perguntas e botões são bloqueados durante o processamento para evitar conflitos
- Exibição da resposta do assistente em tempo real, com opção de interromper a resposta a qualquer momento
- Integração com modelos locais via Ollama, sem necessidade de conexão com serviços externos de IA

Como funciona
- O usuário pode digitar uma pergunta ou clicar em "Falar" para iniciar a gravação de voz.
- Durante a gravação, o botão "Pronto" permanece habilitado para que o usuário possa finalizar a fala manualmente, ou a gravação é encerrada automaticamente após 5 segundos de silêncio.
- Após o reconhecimento da fala, a pergunta é enviada ao assistente J.A.R.V.I.S e a resposta é exibida na interface.
- O botão "Parar" permite interromper a resposta do assistente a qualquer momento.
- O assistente só informa sua identidade e autoria se for questionado sobre isso.

Requisitos
- Python 3.8 ou superior
- Bibliotecas: customtkinter, speech_recognition, numpy, ollama

Observações
- O reconhecimento de voz é feito localmente e não depende de serviços externos, exceto para a transcrição (Google Speech Recognition).
- O assistente J.A.R.V.I.S utiliza modelos de linguagem executados localmente via Ollama, garantindo privacidade e independência de nuvem.