# Chat Real-Time

Um chat em tempo real simples, construído com **FastAPI**, **WebSockets** e front‑end mínimo em **HTML/JavaScript**, suportando:

- **Salas públicas e privadas** (com senha)
- **Nickname único** por sala (sem registro formal)
- **Mensagens de texto** com suporte a **emotes** (por códigos, ex.: `:smile:` → 😄)
- **Upload** e compartilhamento de **áudio**, **vídeo** e **PDF**
- **Front‑end** para testes (arquivo `index.html`)

---

## Tecnologias e dependências

- Python 3.8+
- FastAPI
- Uvicorn (ASGI server)
- starlette (via FastAPI)
- Pydantic (modelos de dados)
- JavaScript (WebSocket API nativa)

Você pode instalar tudo com:

```bash
pip install fastapi uvicorn
```

## Estrutura do Projeto

```
chat_real_time/
├─ app/
│  ├─ __init__.py
│  ├─ main.py                # FastAPI app, inclui routers e serve front-end
│  ├─ routers/
│  │  ├─ chat.py             # WebSocket de chat
│  │  ├─ room.py             # REST para criar/listar salas
│  │  └─ upload.py           # Upload de arquivos (áudio, vídeo, PDF)
│  ├─ services/
│  │  └─ connection_manager.py  # Gerencia salas, conexões e nicknames únicos
│  └─ schemas/
│     ├─ message.py          # Pydantic: username, message, timestamp
│     └─ room.py             # Pydantic: criação e retorno de sala
├─ index.html                # Front‑end de teste (HTML + JS)
├─ uploads/                  # Arquivos enviados via API
└─ README.md                 # Este arquivo
```

---

## Configuração e execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/8b1tz/chat_real_time.git
   cd chat_real_time
   ```

2. **Instale as dependências**:
   ```bash
   pip install fastapi uvicorn
   ```

3. **(Opcional) Crie a pasta de uploads**:
   ```bash
   mkdir uploads
   ```
   _Observação_: O endpoint de upload já chama `os.makedirs("uploads", exist_ok=True)`, logo, se preferir, basta usar o upload pela primeira vez que a pasta será criada automaticamente. Caso queira garantir, você pode criá-la manualmente antes de rodar o servidor.

4. **Inicie o servidor**:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

5. **Abra o front‑end** no navegador:
   - Acesse `http://127.0.0.1:8000/` para carregar `index.html`.

---

## Uso da API

### 1. Salas (REST)

- **Criar sala**

  ```http
  POST /rooms/
  Content-Type: application/json
  {
    "name": "geral",        # nome único da sala
    "password": "opcional"  # senha (se privada)
  }
  ```

  - Resposta (200 OK):
    ```json
    { "name": "geral", "private": false }
    ```

- **Listar salas**

  ```http
  GET /rooms/
  ```

  - Resposta (200 OK):
    ```json
    [
      { "name": "geral", "private": false },
      { "name": "privada", "private": true }
    ]
    ```

### 2. Chat (WebSocket)

Conecte-se ao chat usando a URL WebSocket:

```
ws://127.0.0.1:8000/ws/{room_name}?username={nickname}[&password={senha}]
```

- **room_name**: nome exato da sala existente.
- **nickname**: apelido do usuário (único na sala).
- **senha**: apenas se a sala for privada.

#### Formatos de mensagem enviadas pelo cliente

- Texto com emotes (após replace no front‑end):
  ```json
  { "type": "text", "message": "Olá 😄" }
  ```

- Arquivo (após upload via REST):
  ```json
  {
    "type": "file",
    "url": "/static/uploads/1234-abcd.mp3",
    "filename": "audio.mp3",
    "content_type": "audio/mpeg"
  }
  ```

#### Eventos recebidos pelo cliente

- **Text**: renderize como texto.
- **File**: detecte pelo `content_type` e crie:
  - `<audio controls>` para `audio/*`
  - `<video controls>` para `video/*`
  - Link para PDF ou download de outros arquivos.

---

## Front‑end de Teste

O `index.html` contém:

- Formulário de login (nickname + sala)
- Conexão WebSocket à entrada da sala
- Input de texto com emotes
- Botão de envio de mensagem
- Input e botão de upload de arquivo
- Área de mensagens que renderiza texto e mídia

Basta abrir a página e usar em duas abas/janelas para testar comunicação bidirecional.

---

## Personalização

- **Emotes**: edite o objeto `EMOTES` em `index.html`
- **Suporte a mais tipos de arquivo**: ajuste a lista de `content_type` em `upload.py`
- **Persistência**: substitua armazenamento em memória por Redis ou banco de dados

---

