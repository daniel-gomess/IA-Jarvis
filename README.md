J.A.R.V.I.S - Assistente de Voz Local com Interface Gráfica

    Este projeto implementa um assistente de voz local com interface gráfica desenvolvida em Python utilizando a biblioteca CustomTkinter. O sistema permite que o usuário interaja por texto ou por voz, recebendo respostas de um modelo de linguagem local via Ollama.

Funcionalidades
- Interface gráfica moderna e responsiva baseada em CustomTkinter
- Envio de perguntas por texto ou por voz
- Reconhecimento de voz automático: a gravação é encerrada após 5 segundos de silêncio ou manualmente pelo usuário
- Campo de entrada de perguntas e botões são bloqueados durante o processamento para evitar conflitos
- Exibição da resposta do modelo de linguagem em tempo real, com opção de interromper a resposta a qualquer momento
- Integração com modelos locais via Ollama, sem necessidade de conexão com serviços externos de IA

Como funciona
1. O usuário pode digitar uma pergunta ou clicar em "Falar" para iniciar a gravação de voz.
2. Durante a gravação, o botão "Pronto" permanece habilitado para que o usuário possa finalizar a fala manualmente, ou a gravação é encerrada automaticamente após 5 segundos de silêncio.
3. Após o reconhecimento da fala, a pergunta é enviada ao modelo de linguagem e a resposta é exibida na interface.
4. O botão "Parar" permite interromper a resposta do modelo a qualquer momento.

Requisitos
- Python 3.8 ou superior
- Bibliotecas: customtkinter, speech_recognition, numpy, ollama

Observações
- O reconhecimento de voz é feito localmente e não depende de serviços externos, exceto para a transcrição (Google Speech Recognition).
- O modelo de linguagem é executado localmente via Ollama, garantindo privacidade e independência de nuvem.