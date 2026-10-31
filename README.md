# Automação Incidente Transacional

Aplicação utilizada pelo S/NOC para automatizar o registro e a
finalização de incidentes transacionais.

A solução executa consultas, realiza cálculos, gera evidências,
integra-se ao Qualitor, envia e-mails e produz logs para diagnóstico
e rastreabilidade das execuções.

## Tecnologias

- Python
- FastAPI
- Uvicorn
- Playwright
- React
- React Router
- Vite
- Arquivos JSON
- Outlook e MAPI
- Qualitor

## Ambiente validado

A Automação Incidente Transacional foi desenvolvida e validada
inicialmente com as seguintes versões:

| Tecnologia | Versão validada |
|---|---:|
| Python | 3.14.6 |
| FastAPI | 0.141.1 |
| Uvicorn | 0.52.1 |
| Playwright para Python | 1.62.0 |
| Node.js | 24.18.0 |
| npm | 11.16.0 |
| React | 19.3.0 |
| React DOM | 19.3.0 |
| React Router DOM | 7.18.4 |
| Vite | 8.3.3 |
| Plugin React para Vite | 6.1.2 |

As versões acima representam o ambiente em que a aplicação foi
validada. A compatibilidade com outras versões deve ser testada antes
da implantação.

## Estrutura do projeto

- `api`: endpoints, modelos e configurações da API.
- `backend`: regras de negócio e serviços da automação.
- `data`: arquivos locais de dados e configuração.
- `frontend`: interface web desenvolvida em React.
- `output`: logs e evidências gerados pela automação.
- `docs`: documentação funcional, técnica e operacional do projeto.

## Pré-requisitos

Para executar a aplicação, são necessários:

- Windows com sessão de usuário ativa;
- Python;
- Node.js e npm;
- Microsoft Outlook instalado e configurado;
- acesso ao Qualitor;
- acesso ao Portal Transacional;
- acesso à rede corporativa;
- permissões de leitura e gravação nas pastas do projeto;
- navegadores utilizados pelo Playwright instalados.

## Instalação do backend

Na pasta principal do projeto, crie um ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

Confirme que o Python utilizado pertence ao ambiente virtual:

```powershell
python -c "import sys; print(sys.executable)"
```

O caminho apresentado deve terminar em:

```text
AutomacaoTeste\.venv\Scripts\python.exe
```

Instale as dependências do backend:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Instale os navegadores necessários ao Playwright:

```powershell
python -m playwright install
```

## Configuração do ambiente

O projeto utiliza um arquivo `.env` para armazenar configurações e
informações específicas do ambiente.

Para configurar a aplicação:

1. Copie o arquivo `.env.example`.
2. Renomeie a cópia para `.env`.
3. Preencha as variáveis conforme o ambiente.
4. Não envie o arquivo `.env` ao repositório.

O arquivo `.env` pode conter credenciais e está incluído no
`.gitignore`.

## Execução do backend

Na pasta principal do projeto, com o ambiente virtual ativado, execute:

```powershell
python -m uvicorn api.main:app --reload
```

O parâmetro `--reload` deve ser usado somente durante o
desenvolvimento. Ele monitora alterações nos arquivos e reinicia a API
automaticamente.

Para uma execução operacional sem recarregamento automático, use:

```powershell
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

A API estará disponível nos seguintes endereços:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- OpenAPI: `http://127.0.0.1:8000/openapi.json`

> A versão atual deve ser executada com apenas um processo. Não utilize
> múltiplos workers, pois a aplicação compartilha arquivos JSON,
> evidências, Outlook, Playwright e a sessão dos sistemas externos.

## Validação da API

A inicialização estará correta quando o Uvicorn apresentar:

```text
Application startup complete.
```

O logger da aplicação também deverá registrar:

```text
API da Automação Incidente Transacional iniciada.
```

O arquivo de log deve estar disponível em:

```text
output/logs/automacao.log
```

Para validar a API:

1. Acesse `http://127.0.0.1:8000`.
2. Confirme que a API retorna o status `online`.
3. Acesse `http://127.0.0.1:8000/docs`.
4. Confirme que as rotas de registro e finalização são exibidas.
5. Confira se o arquivo `automacao.log` foi criado.
6. Pressione `Ctrl + C` para encerrar a API de forma controlada.
7. Confirme se o encerramento foi registrado no log.

## Instalação do frontend

Acesse a pasta do frontend:

```powershell
cd frontend
```

Instale as dependências registradas no `package-lock.json`:

```powershell
npm ci
```

O comando `npm ci` instala as versões exatas registradas no
`package-lock.json`, garantindo maior consistência entre os ambientes.

## Execução do frontend

Dentro da pasta `frontend`, execute:

```powershell
npm run dev
```

O frontend será disponibilizado normalmente em:

```text
http://localhost:5173
```

Para interromper o frontend, pressione:

```text
Ctrl + C
```

## Validação do frontend

Após iniciar o frontend:

1. Acesse `http://localhost:5173`.
2. Confirme que a página inicial é apresentada.
3. Acesse a página de registro de incidente.
4. Acesse a página de finalização de incidente.
5. Confirme que o frontend consegue consultar a API.
6. Verifique se não existem erros de CORS no console do navegador.

## Execução completa em desenvolvimento

A aplicação exige dois terminais.

### Terminal 1: backend

Na pasta principal:

```powershell
.venv\Scripts\Activate.ps1
python -m uvicorn api.main:app --reload
```

### Terminal 2: frontend

Na pasta principal:

```powershell
cd frontend
npm run dev
```

Depois, acesse:

```text
http://localhost:5173
```

## Diretórios de saída

Durante a execução, a automação utiliza os seguintes diretórios:

| Diretório | Finalidade |
|---|---|
| `output/logs` | Logs da aplicação |
| `output/printGraf` | Evidências dos gráficos transacionais |
| `output/printOP` | Evidências gerais das operadoras |
| `output/printOP_detalhado` | Evidências detalhadas das operadoras |

A pasta `output/logs` não deve ser removida durante a execução, pois o
arquivo `automacao.log` permanece aberto pelo logger.

## Logs

A aplicação utiliza o `RotatingFileHandler` do Python.

O arquivo principal é:

```text
output/logs/automacao.log
```

A rotação ocorre quando o arquivo atinge 5 MB. São mantidos até cinco
arquivos de backup, além do arquivo atual.

Os arquivos podem ser apresentados da seguinte forma:

```text
automacao.log
automacao.log.1
automacao.log.2
automacao.log.3
automacao.log.4
automacao.log.5
```

## Restrições do ambiente

A versão atual da automação deve ser executada em ambiente Windows com
sessão de usuário ativa.

A execução depende de:

- Microsoft Outlook instalado e configurado;
- acesso ao Qualitor;
- acesso ao Portal Transacional;
- disponibilidade da rede corporativa;
- permissões de leitura e gravação;
- interface gráfica disponível para as automações;
- apenas uma execução ativa por vez.

A execução em servidor, serviço do Windows ou sessão sem interface
gráfica ainda não foi homologada.

## Documentação

A documentação completa está disponível na pasta `docs`:

- `01-visao-geral.md`: objetivo, contexto, escopo e benefícios.
- `02-funcionamento.md`: fluxos de registro e finalização.
- `03-arquitetura.md`: componentes e responsabilidades.
- `04-manual-usuario.md`: instruções para utilização.
- `05-suporte-e-erros.md`: diagnóstico e tratamento de falhas.
- `06-plano-de-testes.md`: cenários e resultados dos testes, quando disponível.

## Segurança

- O arquivo `.env` não deve ser enviado ao repositório.
- Senhas e tokens não devem ser gravados nos logs.
- Evidências não devem expor dados desnecessários.
- Arquivos JSON com dados operacionais devem ter acesso restrito.
- Credenciais não devem ser incluídas no código-fonte.
- Logs e evidências devem seguir a política interna de retenção.

## Status do projeto

A solução encontra-se em fase de desenvolvimento e validação.

Antes da implantação, devem ser validados:

- registro completo de incidente;
- finalização completa de incidente;
- geração de todas as evidências;
- cálculo de perda com transações;
- cálculo de perda sem transações;
- indisponibilidade do Qualitor;
- falha no envio de e-mail;
- interrupção do fluxo após falha crítica;
- rotação dos arquivos de log.