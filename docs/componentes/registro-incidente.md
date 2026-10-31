# Componente de Registro de Incidente

## 1. Objetivo

O componente recebe os dados do incidente, salva as informações, abre o chamado no Qualitor, gera as evidências e envia o e-mail de indisponibilidade.

## 2. Arquivos relacionados

| Arquivo | Responsabilidade |
|---|---|
| `api/models/incidente.py` | Definir e validar os dados de entrada |
| `api/routers/incidente.py` | Disponibilizar o endpoint `POST /incidente` |
| `backend/services/incidente/executar_incidente.py` | Coordenar o fluxo de registro |
| `backend/services/incidente/salvar_incidente.py` | Salvar os dados em JSON |

Serviços utilizados:

| Serviço | Responsabilidade |
|---|---|
| `limpar_output()` | Limpar evidências anteriores |
| `pega_chamado()` | Abrir o chamado no Qualitor |
| `gerar_screenshot()` | Gerar evidências visuais |
| `enviar_email()` | Enviar o e-mail de indisponibilidade |
| `logger` | Registrar as etapas da execução |
| `AutomacaoException` | Padronizar as falhas da automação |

## 3. Entrada e validação

Endpoint:

`POST /incidente`

Modelo utilizado:

```python
class Incidente(BaseModel):
    parceiro: str
    tipo_transacao: str
    autorizador: str
    status: str
    indisponibilidade: str
    hora_inicio: str
```

Campos recebidos:

| Campo | Tipo | Descrição |
|---|---|---|
| `parceiro` | `str` | Parceiro relacionado ao incidente |
| `tipo_transacao` | `str` | Tipo de transação afetada |
| `autorizador` | `str` | Autorizador relacionado ao processamento |
| `status` | `str` | Status informado |
| `indisponibilidade` | `str` | Classificação da indisponibilidade |
| `hora_inicio` | `str` | Horário de início do incidente |

Exemplo com dados fictícios:

```json
{
  "parceiro": "PARCEIRO_EXEMPLO",
  "tipo_transacao": "PIX",
  "autorizador": "AUTORIZADOR_EXEMPLO",
  "status": "INDISPONIVEL",
  "indisponibilidade": "TOTAL",
  "hora_inicio": "10:30"
}
```

O modelo atual valida a presença e o tipo dos campos. O modelo não impede automaticamente strings vazias nem valida o formato de `hora_inicio`.

## 4. Endpoint

O router recebe os dados validados e converte o modelo Pydantic em um dicionário:

```python
resultado = executar_incidente(dados.model_dump())
```

Em caso de `AutomacaoException`, a API retorna HTTP `400`:

```python
raise HTTPException(
    status_code=400,
    detail=str(erro)
)
```

## 5. Fluxo de execução

```text
Frontend
    ↓
POST /incidente
    ↓
Validação pelo modelo Incidente
    ↓
Conversão com model_dump()
    ↓
limpar_output()
    ↓
salvar_incidente(dados)
    ↓
pega_chamado()
    ↓
gerar_screenshot()
    ↓
enviar_email(chamado)
    ↓
Resposta para o frontend
```

Ordem das etapas:

| Ordem | Etapa | Função |
|---:|---|---|
| 1 | Limpar evidências anteriores | `limpar_output()` |
| 2 | Salvar os dados | `salvar_incidente(dados)` |
| 3 | Abrir o chamado | `pega_chamado()` |
| 4 | Gerar evidências | `gerar_screenshot()` |
| 5 | Enviar o e-mail | `enviar_email(chamado)` |
| 6 | Retornar o resultado | `return` |

## 6. Salvamento dos dados

A função `salvar_incidente()` grava os dados em:

`data/info_incidente.json`

Configuração utilizada:

```python
json.dump(
    dados,
    arquivo,
    ensure_ascii=False,
    indent=4
)
```

O arquivo é gravado em UTF-8 e o conteúdo anterior é substituído.

## 7. Integrações e arquivos

| Recurso | Finalidade |
|---|---|
| Qualitor | Abrir o chamado |
| Outlook/MAPI | Enviar o e-mail |
| `data/info_incidente.json` | Armazenar os dados do incidente |
| `data/email_op.json` | Obter os destinatários |
| `output/printOP` | Armazenar evidência geral |
| `output/printOP_detalhado` | Armazenar evidência detalhada |
| `output/printGraf` | Armazenar gráficos |
| `output/logs/automacao.log` | Registrar a execução |

## 8. Retorno de sucesso

```json
{
  "success": true,
  "message": "Incidente registrado com sucesso",
  "chamado": "1234567"
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| `success` | `bool` | Indica sucesso |
| `message` | `str` | Mensagem apresentada ao usuário |
| `chamado` | `str` | Número do chamado aberto |

## 9. Logs

O componente registra o início das etapas:

```text
Apagando registros antigos...
Salvando incidente...
Abrindo chamado...
Gerando evidências...
Enviando email...
```

No código atual, “Apagando registros antigos” corresponde à limpeza das evidências anteriores.

## 10. Tratamento de erros

Falhas conhecidas são propagadas:

```python
except AutomacaoException:
    raise
```

Falhas inesperadas são convertidas para `AutomacaoException`:

```python
except Exception as erro:
    raise AutomacaoException(
        f"Erro inesperado durante o registro: {erro}"
    ) from erro
```

## 11. Execução parcial e restrições

Uma falha pode ocorrer depois que o chamado já foi aberto.

```text
Chamado aberto
    ↓
Falha na geração de evidências ou no e-mail
    ↓
API retorna erro
    ↓
Chamado permanece aberto
```

Antes de repetir a execução, o analista deve confirmar:

1. se o chamado foi criado;
2. se as evidências foram geradas;
3. se o e-mail foi enviado.

Restrições atuais:

- uma execução por vez;
- armazenamento local em JSON;
- dependência do Qualitor, Outlook e rede corporativa;
- possibilidade de conclusão parcial.

## 12. Testes relacionados

| Cenário | Resultado esperado |
|---|---|
| Dados válidos | Chamado aberto e resposta de sucesso |
| Campo obrigatório ausente | Requisição rejeitada pela API |
| Falha ao salvar o JSON | API retorna erro |
| Qualitor indisponível | API retorna erro |
| Falha na geração de evidências | Erro registrado |
| Falha no envio do e-mail | API retorna erro |
| Execução completa | Número do chamado apresentado no frontend |
