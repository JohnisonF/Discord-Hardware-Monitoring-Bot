# Um template para seu bot Discord em Javascript

Este projeto foi feito com o Discord.py com o intuito de fornecer informações sobre o hardware, como temperatura, velocidade das fans e etc. 
Ele fornece também um alerta caso a temperatura de seu processador seja maior que determinado valor (ele utiliza seu client id para mensagem direta e os valores podem ser alterado nas variáveis de ambiente). 
IMPORTANTE: Este projeto apenas foi feito e testado no Windows 11 64-bits, sendo assim, pode ocorrer falhas em outros sistemas operacionais.

# Requisitos

Esse projeto funciona com python 3.12.0, haverá testes e correções futuras para versões mais atualizadas.
É necessário baixar o [Libre Hardware Monitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases) e habilitar o servidor remoto padrão dele (http://localhost:8085). 
Obs: você pode mudar caso queira dentro do código.

# Linguagens e pacotes

Esse projeto é feito na linguagem python e instala os pacotes: discord.py, dotenv e psutil.

# Comandos

Existem dois comandos: `/ping` que mostra o ping do bot e o `/hardwarestatus` que mostra as informações do seu hardware(computador).

# Tutorial

Abra o terminal na raiz do projeto e use o comando `pip install -r requirements.txt` para instalar todas as dependências do python.
Transforme o arquivo `.env.example` para `.env` e edite as variáveis conforme as suas.
Rode o projeto com `python bot.py`.

# Pasta e Arquivos

`bot.py`: Arquivo principal para o Bot, que apenas instancio as funções e inicio a aplicação.

`/slashCommands`: Pasta onde ficam guardados os `Slash Commands`.

`/cogs`: Pasta para as demais funções do bot como o alerta de temperatura por segundos.

`/cogs/monitor.py`: Arquivo onde fica a função de alerta de temperatura do bot.

`/slashCommands/harwarestatus.py`: Um slash command que o bot responde com as demais informações do seu computador.

`/slashCommands/ping.py`: Slash command para o comando simples de ping.

`.env.example`: Transforme esse arquivo em `.env` e edite as variáveis conforme seu bot e client.

