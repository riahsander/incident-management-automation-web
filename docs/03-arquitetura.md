# Arquitetura da Solução

## 1. Arquitetura geral

A solução está dividida em três partes:

- frontend em React;
- API em FastAPI;
- serviços de automação em Python.

Fluxo principal:

```text
Analista do NOC
    ↓
Frontend React
    ↓
API FastAPI
    ↓
Serviços Python
    ↓
Qualitor, Portal Transacional e Outlook
```

## 2. Frontend

Localização: `frontend/`

Responsabilidades:

- apresentar as telas;
- coletar os dados do analista;
- enviar requisições para a API;
- apresentar mensagens de sucesso ou erro.

Principais arquivos:

| Arquivo | Responsabilidade |
|---|---|
| `src/pages/Home.jsx` | Página inicial |
| `src/pages/RegistrarIncidente.jsx` | Formulário de registro |
| `src/pages/FinalizarIncidente.jsx` | Formulário de finalização |
| `src/services/api.js` | Comunicação com a API |

## 3. API

Localização: `api/`

Responsabilidades:

- receber requisições HTTP;
- validar os dados com Pydantic;
- encaminhar as solicitações ao backend;
- retornar respostas de sucesso ou erro.

Principais arquivos:

| Arquivo | Responsabilidade |
|---|---|
| `api/main.py` | Inicialização e configuração da API |
| `api/models/incidente.py` | Modelo de entrada do registro |
| `api/models/finalizacao_incidente.py` | Modelo de entrada da finalização |
| `api/models/responses.py` | Modelos de resposta |
| `api/routers/incidente.py` | Endpoint de registro |
| `api/routers/finalizacao.py` | Endpoint de finalização |

## 4. Backend

Localização: `backend/`

Responsabilidades:

- executar as regras da automação;
- salvar informações;
- abrir e encerrar chamados;
- gerar evidências;
- calcular a perda transacional;
- enviar e-mails;
- registrar logs.

### Serviços

| Serviço | Responsabilidade |
|---|---|
| `incidente` | Coordenar e salvar o registro |
| `finalizacao` | Coordenar a finalização |
| `qualitor` | Abrir e encerrar chamados |
| `gerar_screenshots` | Produzir evidências visuais |
| `avg_transacional` | Calcular a perda transacional |
| `email` | Enviar comunicações por e-mail |
| `zerador_evidencias` | Limpar evidências anteriores |

## 5. Armazenamento local

A solução utiliza arquivos JSON na pasta `data/`:

| Arquivo | Finalidade |
|---|---|
| `data/info_incidente.json` | Armazenar dados do incidente atual |
| `data/email_op.json` | Armazenar destinatários por parceiro |
| `data/operadoras.json` | Relacionar operadoras aos gráficos transacionais |

Os arquivos reais contêm informações internas e não devem ser enviados ao repositório. Somente arquivos `.example.json` devem ser versionados.

## 6. Arquivos gerados

A pasta `output/` contém:

| Diretório | Finalidade |
|---|---|
| `output/logs` | Logs da aplicação |
| `output/printGraf` | Evidências dos gráficos transacionais |
| `output/printOP` | Evidências gerais das operadoras |
| `output/printOP_detalhado` | Evidências detalhadas das operadoras |

## 7. Configurações

O arquivo `.env` contém configurações específicas do ambiente e não deve ser versionado.

Senhas, tokens e credenciais não devem aparecer:

- no código-fonte;
- nos logs;
- nos arquivos de exemplo;
- na documentação.

## 8. Logs

A aplicação utiliza o `RotatingFileHandler`.

Arquivo principal:

`output/logs/automacao.log`

Configuração atual:

- tamanho máximo por arquivo: 5 MB;
- quantidade de backups: 5;
- codificação: UTF-8;
- saída em arquivo e console.

A pasta `output/logs` não deve ser removida pela limpeza de evidências.

## 9. Restrições atuais

- execução em ambiente Windows;
- sessão de usuário ativa;
- Outlook instalado e configurado;
- acesso ao Qualitor e ao Portal Transacional;
- apenas uma execução por vez;
- armazenamento local em JSON;
- dependência da rede corporativa e dos sistemas externos.

## 10. Documentação dos componentes

- [Registro de incidente](componentes/registro-incidente.md)
- [Finalização de incidente](componentes/finalizacao-incidente.md)
- [Integração com o Qualitor](componentes/integracao-qualitor.md)
- [Geração de evidências](componentes/geracao-evidencias.md)
- [Envio de e-mail](componentes/envio-email.md)
- [Cálculo de perda](componentes/calculo-perda.md)
- [Logs e arquivos](componentes/logs-e-arquivos.md)
