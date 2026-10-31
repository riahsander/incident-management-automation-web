# Componente de Finalização de Incidente

## 1. Objetivo

O componente recebe os dados da normalização, salva as informações, encerra o chamado no Qualitor e envia o e-mail de normalização.

## 2. Arquivos relacionados

| Arquivo | Responsabilidade |
|---|---|
| `api/models/finalizacao_incidente.py` | Definir e validar os dados de entrada |
| `api/routers/finalizacao.py` | Disponibilizar o endpoint `POST /finalizar-incidente` |
| `backend/services/finalizacao/executar_finalizacao.py` | Coordenar o fluxo de finalização |

Serviços utilizados:

| Serviço | Responsabilidade |
|---|---|
| `salvar_incidente()` | Salvar os dados da finalização |
| `fecha_chamado()` | Encerrar o chamado no Qualitor |
| `fecha_email()` | Enviar o e-mail de normalização |
| `logger` | Registrar as etapas da execução |
| `AutomacaoException` | Padronizar as falhas da automação |

## 3. Entrada e validação

Endpoint:

`POST /finalizar-incidente`

Modelo utilizado:

```python
class FinalizacaoIncidente(BaseModel):
    hora_fim: str
    origem: str
    causa: str
    chamado: str
    escopo: str
```

Campos recebidos:

| Campo | Tipo | Descrição |
|---|---|---|
| `hora_fim` | `str` | Horário de normalização do incidente |
| `origem` | `str` | Origem identificada para o incidente |
| `causa` | `str` | Causa identificada para o incidente |
| `chamado` | `str` | Número do chamado no Qualitor |
| `escopo` | `str` | Escopo afetado pelo incidente |

Exemplo com dados fictícios:

```json
{
  "hora_fim": "11:20",
  "origem": "ORIGEM_EXEMPLO",
  "causa": "CAUSA_EXEMPLO",
  "chamado": "1234567",
  "escopo": "ESCOPO_EXEMPLO"
}
```

O modelo atual valida a presença e o tipo dos campos. O modelo não impede automaticamente strings vazias nem valida os formatos de `hora_fim` e `chamado`.

## 4. Endpoint

O router recebe os dados validados e converte o modelo Pydantic em um dicionário:

```python
resultado = Executar_Finalizacao(dados.model_dump())
```

Em caso de `AutomacaoException`, a API retorna HTTP `400`:

```python
raise HTTPException(
    status_code=400,
    detail=str(erro)
)
```

O formato da resposta é definido pelo modelo `IncidenteResponse`.

## 5. Fluxo de execução

```text
Frontend
    ↓
POST /finalizar-incidente
    ↓
Validação pelo modelo FinalizacaoIncidente
    ↓
Conversão com model_dump()
    ↓
salvar_incidente(dados)
    ↓
fecha_chamado()
    ↓
fecha_email()
    ↓
Resposta para o frontend
```

Ordem das etapas:

| Ordem | Etapa | Função |
|---:|---|---|
| 1 | Salvar os dados da finalização | `salvar_incidente(dados)` |
| 2 | Encerrar o chamado | `fecha_chamado()` |
| 3 | Enviar o e-mail de normalização | `fecha_email()` |
| 4 | Retornar o resultado | `return` |

## 6. Salvamento dos dados

A função `salvar_incidente()` grava os dados recebidos no arquivo:

`data/info_incidente.json`

O conteúdo anterior é substituído pelos dados da finalização.

## 7. Integrações e arquivos

| Recurso | Finalidade |
|---|---|
| Qualitor | Localizar e encerrar o chamado |
| Portal Transacional | Consultar dados usados na finalização |
| Outlook/MAPI | Enviar o e-mail de normalização |
| `data/info_incidente.json` | Armazenar os dados da finalização |
| `data/email_op.json` | Obter os destinatários |
| `output/logs/automacao.log` | Registrar a execução |

## 8. Retorno de sucesso

```json
{
  "success": true,
  "message": "Incidente encerrado com sucesso"
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| `success` | `bool` | Indica que o fluxo foi concluído |
| `message` | `str` | Mensagem de sucesso |

## 9. Logs

O componente registra o início das etapas:

```text
Salvando dados da finalização...
Encerrando chamado...
Enviando e-mail de normalização...
```

Os logs são gravados em:

`output/logs/automacao.log`

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
        f"Erro inesperado durante a finalização: {erro}"
    ) from erro
```

No router, a exceção é devolvida como HTTP `400`.

## 11. Execução parcial e restrições

Uma falha pode ocorrer depois que os dados já foram salvos ou durante o encerramento do chamado.

```text
Dados salvos
    ↓
Falha no encerramento
    ↓
API retorna erro
```

O e-mail de normalização é chamado depois de `fecha_chamado()`. Se `fecha_chamado()` lançar uma exceção, o fluxo vai para o bloco `except` e `fecha_email()` não é executado.

Antes de repetir uma finalização com erro, o analista deve confirmar:

1. se o chamado foi encerrado;
2. se os campos foram atualizados;
3. se o e-mail foi enviado.

Restrições atuais:

- uma execução por vez;
- armazenamento local em JSON;
- dependência do Qualitor, Portal Transacional, Outlook e rede corporativa;
- possibilidade de conclusão parcial.

## 12. Testes relacionados

| Cenário | Resultado esperado |
|---|---|
| Dados válidos | Chamado encerrado e resposta de sucesso |
| Campo obrigatório ausente | Requisição rejeitada pela API |
| Falha ao salvar o JSON | API retorna erro |
| Chamado não encontrado | API retorna erro |
| Qualitor indisponível | API retorna erro |
| Finalização com transações | Perda calculada e chamado encerrado |
| Finalização sem transações | Perda média definida como zero |
| Falha no encerramento | E-mail de normalização não é iniciado |
| Execução completa | Sucesso apresentado no frontend |
