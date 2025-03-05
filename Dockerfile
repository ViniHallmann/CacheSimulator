# Usando uma imagem base do Python
FROM python:3.11

# Criando e definindo o diretório de trabalho
WORKDIR /app

# Copiando os arquivos para dentro do container
COPY . .

# Garantindo que o script seja executável
RUN chmod +x main.py

# Mantém o container rodando aguardando comandos interativos
CMD ["tail", "-f", "/dev/null"]
