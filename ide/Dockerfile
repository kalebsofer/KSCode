FROM codercom/code-server:latest

WORKDIR /workspace

# Install VSCode extensions (optional)
RUN code-server --install-extension ms-python.python

# Copy customized VSCode files
COPY ./ide/vscode /home/coder/.local/share/code-server

EXPOSE 8080

CMD ["code-server", "--auth", "none", "--bind-addr", "0.0.0.0:8080", "/workspace"]
