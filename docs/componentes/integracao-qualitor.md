# Componente de Integração com o Qualitor

## 1. Objetivo

O componente utiliza Playwright para abrir e encerrar chamados no Qualitor com base nas informações armazenadas em `data/info_incidente.json`.

## 2. Arquivos relacionados

| Arquivo | Responsabilidade |
|---|---|
| `backend/services/qualitor/abertura_chamado.py` | Abrir o chamado e retornar o número criado |
| `backend/services/qualitor/encerra_chamado.py` | Localizar, atualizar e encerrar o chamado |

Serviços e recursos utilizados:

| Recurso | Responsabilidade |
|---|---|
| Playwright | Automatizar o navegador |
| `data/info_incidente.json` | Fornecer e armazenar dados do incidente |
| `.env` | Fornecer URL e credenciais do Qualitor |
| `calcula_perda()` | Calcular a perda média na finalização |
| `logger` | Registrar as etapas da execução |
| `AutomacaoException` | Padronizar as falhas da automação |

## 3. Configuração

As configurações são carregadas do arquivo `.env`:

```python
qualitor = os.getenv("QUALITOR")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
```

O arquivo `.env` não deve ser enviado ao repositório.

## 4. Abertura do chamado

Função principal:

```python
pega_chamado()
```

Fluxo:

```text
Ler info_incidente.json
    ↓
Converter parceiro e indisponibilidade
    ↓
Abrir navegador
    ↓
Realizar login no Qualitor
    ↓
Preencher o formulário
    ↓
Selecionar os status transacionais
    ↓
Processar a abertura
    ↓
Capturar o número do chamado
    ↓
Retornar o número
```

### Dados utilizados

| Campo | Uso no Qualitor |
|---|---|
| `parceiro` | Seleção do parceiro |
| `autorizador` | Seleção da conexão com o autorizador |
| `indisponibilidade` | Indicação de indisponibilidade total ou parcial |
| `status` | Seleção dos status transacionais |
| `hora_inicio` | Preenchimento do horário inicial |
| `tipo_transacao` | Composição da descrição do chamado |

### Conversões realizadas

- `BANCO TOPAZIO ATM` é convertido para `TOPAZIO PIX`.
- `indisponibilidade` igual a `Total` é convertida para `Sim`.
- Outros valores de indisponibilidade são convertidos para `Não`.

### Status suportados

A função `marcar_status()` trata:

- Negadas;
- Pendentes;
- Desfeitas;
- Erro;
- Negadas e Pendentes;
- Desfeitas e Pendentes.

### Retorno

A função retorna o número do chamado como texto:

```text
1234567
```

## 5. Encerramento do chamado

Função principal:

```python
fecha_chamado()
```

Fluxo:

```text
Ler info_incidente.json
    ↓
Abrir navegador e realizar login
    ↓
Pesquisar o chamado
    ↓
Abrir o atendimento
    ↓
Capturar parceiro, data e hora inicial
    ↓
Atualizar info_incidente.json
    ↓
Executar calcula_perda()
    ↓
Preencher os campos de encerramento
    ↓
Encerrar o atendimento
```

### Informações capturadas do Qualitor

| Informação | Destino no JSON |
|---|---|
| Parceiro | `parceiro` |
| Data de abertura | `data_inicio` |
| Hora de início | `hora_inicio` |

A data atual é gravada em `data_fim`.

### Informações usadas no encerramento

| Campo | Finalidade |
|---|---|
| `parceiro` | Descrição do acionamento |
| `data_inicio` | Data inicial do incidente |
| `hora_inicio` | Hora inicial do incidente |
| `data_fim` | Data de normalização |
| `hora_fim` | Hora de normalização |
| `perda_media` | Perda média calculada |

## 6. Atualização do arquivo de dados

Durante a finalização, o arquivo abaixo é atualizado:

`data/info_incidente.json`

O arquivo recebe os dados capturados do Qualitor e o resultado de `calcula_perda()`.

## 7. Logs

Principais eventos registrados:

```text
Iniciando abertura de chamado no Qualitor.
Iniciando Login no Qualitor...
Sucesso no Login.
Chamado aberto com sucesso.
Iniciando encerramento de chamado no Qualitor.
Chamado encontrado.
Iniciando a captura dos dados adicionais.
Arquivo info_incidente.json atualizado.
Campos preenchidos corretamente.
Chamado encerrado com sucesso.
```

Os logs são gravados em:

`output/logs/automacao.log`

## 8. Tratamento de erros

Na abertura, falhas são convertidas para:

```text
Falha ao abrir chamado no Qualitor.
```

No encerramento, as falhas podem ser classificadas como:

- falha ao atualizar os dados;
- falha ao preencher os dados de encerramento;
- falha ao encerrar o chamado no Qualitor.

As exceções são registradas com `logger.exception()` e convertidas para `AutomacaoException`.

## 9. Execução parcial e restrições

A abertura pode criar o chamado antes de ocorrer uma falha em outra etapa da automação.

O encerramento pode atualizar o JSON e calcular a perda antes de falhar no preenchimento final.

Antes de repetir a operação, o analista deve confirmar o estado do chamado no Qualitor.

Restrições:

- dependência da disponibilidade do Qualitor;
- dependência de seletores da interface;
- necessidade de sessão Windows ativa;
- necessidade dos navegadores do Playwright;
- uma execução por vez;
- dependência do arquivo `data/info_incidente.json`.

## 10. Testes relacionados

| Cenário | Resultado esperado |
|---|---|
| Login válido | Acesso ao Qualitor realizado |
| Credencial inválida | API retorna erro |
| Dados válidos na abertura | Chamado criado e número retornado |
| Status combinado | Campos correspondentes selecionados |
| Chamado existente | Atendimento localizado |
| Chamado inexistente | API retorna erro |
| Perda calculada | Campo de perda preenchido |
| Perda igual a zero | Encerramento realizado com valor zero |
| Falha ao preencher campos | Chamado não é encerrado |
| Execução completa | Chamado encerrado com sucesso |
