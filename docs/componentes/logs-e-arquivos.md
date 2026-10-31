# Componente de Logs e Arquivos

## 1. Objetivo

O componente centraliza os logs, os caminhos do projeto, as exceções da automação e o armazenamento temporário do incidente.

## 2. Arquivos relacionados

| Arquivo | Responsabilidade |
|---|---|
| `backend/services/logger_config.py` | Configurar logs em arquivo e console |
| `backend/services/path_utils.py` | Resolver caminhos e criar diretórios de saída |
| `backend/services/exceptions.py` | Definir a exceção padrão da automação |
| `data/info_incidente.json` | Armazenar o estado atual do incidente |

## 3. Configuração dos logs

O logger utiliza o nome:

```text
AutomacaoIncidente
```

Formato das mensagens:

```text
DATA E HORA | NÍVEL | MÓDULO | MENSAGEM
```

Exemplo:

```text
2026-10-26 11:04:24,353 | INFO | avg_perda | Total de registros encontrados: 160
```

A função principal é:

```python
configurar_logger(output_dir)
```

Ela cria a pasta `logs`, configura os handlers e devolve o logger principal. citeturn48search27

## 4. Destinos e níveis

| Destino | Handler | Nível mínimo |
|---|---|---|
| `output/logs/automacao.log` | `RotatingFileHandler` | `DEBUG` |
| Console | `StreamHandler` | `INFO` |

O logger principal opera no nível `DEBUG` e utiliza `propagate = False` para evitar duplicação no logger raiz. citeturn48search27

## 5. Rotação dos logs

Configuração atual:

| Configuração | Valor |
|---|---:|
| Tamanho máximo | 5 MB |
| Backups mantidos | 5 |
| Codificação | UTF-8 |

Arquivos possíveis:

```text
output/logs/automacao.log
output/logs/automacao.log.1
output/logs/automacao.log.2
output/logs/automacao.log.3
output/logs/automacao.log.4
output/logs/automacao.log.5
```

O espaço máximo aproximado é 30 MB, considerando o arquivo atual e cinco backups. citeturn48search27

## 6. Inicialização única

Antes de adicionar handlers, o código verifica:

```python
if logger.handlers:
    return logger
```

Isso evita mensagens duplicadas quando `configurar_logger()` é chamado novamente. citeturn48search27

## 7. Resolução de caminhos

O arquivo `path_utils.py` calcula `BASE_DIR` a partir da localização do próprio módulo. citeturn48search28

### Caminho comum

```python
get_path(relative_path)
```

Retorna o caminho completo sem criar diretórios.

Exemplo:

```python
get_path("data/info_incidente.json")
```

Resultado esperado:

```text
CAMINHO_DO_PROJETO/data/info_incidente.json
```

### Caminho de saída

```python
get_output_path(relative_path)
```

Retorna o caminho completo e cria o diretório quando ele não existe.

Exemplo:

```python
get_output_path("output/printOP")
```

As duas funções registram e propagam erros de resolução de caminhos. citeturn48search28

## 8. Exceção padrão

A exceção da aplicação é:

```python
class AutomacaoException(Exception):
    """Exceção padrão da automação."""
    pass
```

Ela permite diferenciar falhas conhecidas da automação de exceções inesperadas do Python ou de bibliotecas externas. citeturn48search26

Uso típico:

```python
raise AutomacaoException(
    "Erro ao salvar informações do incidente."
) from erro
```

## 9. Arquivo do incidente

Arquivo:

`data/info_incidente.json`

O arquivo armazena o estado atual utilizado entre as etapas de registro, finalização, evidências, cálculo de perda e envio de e-mail.

Estrutura sanitizada:

```json
{
  "hora_fim": "10:58",
  "origem": "ORIGEM_EXEMPLO",
  "causa": "CAUSA_EXEMPLO",
  "chamado": "0000000",
  "escopo": "GERAL",
  "parceiro": "PARCEIRO_EXEMPLO",
  "data_inicio": "01/01/2000",
  "hora_inicio": "10:50",
  "data_fim": "01/01/2000",
  "perda_media": 160
}
```

## 10. Campos do JSON

| Campo | Tipo | Finalidade |
|---|---|---|
| `hora_fim` | `str` | Horário de normalização |
| `origem` | `str` | Origem do incidente |
| `causa` | `str` | Causa informada |
| `chamado` | `str` | Número do chamado |
| `escopo` | `str` | Escopo afetado |
| `parceiro` | `str` | Parceiro do incidente |
| `data_inicio` | `str` | Data de início |
| `hora_inicio` | `str` | Hora de início |
| `data_fim` | `str` | Data de normalização |
| `perda_media` | `int` | Quantidade estimada de transações afetadas |

Durante o registro, o arquivo também pode receber os caminhos das evidências:

```json
{
  "print_operadora": "CAMINHO_DA_EVIDENCIA",
  "print_op_detalhado": "CAMINHO_DA_EVIDENCIA",
  "print_grafico": "CAMINHO_DA_EVIDENCIA"
}
```

## 11. Segurança dos arquivos

Os arquivos reais da pasta `data/` podem conter informações internas e não devem ser enviados ao repositório.

O `.gitignore` deve manter:

```gitignore
data/*
!data/.gitkeep
!data/*.example.json
!data/README.md
```

Somente modelos sanitizados devem ser versionados.

Os logs não devem registrar:

- senhas;
- tokens;
- conteúdo do `.env`;
- listas reais de destinatários;
- dados internos desnecessários.

## 12. Tratamento de erros

| Componente | Comportamento |
|---|---|
| Logger | Cria a pasta e os handlers durante a inicialização |
| `get_path()` | Registra e propaga a falha |
| `get_output_path()` | Registra e propaga a falha |
| `AutomacaoException` | Encaminha falhas conhecidas às camadas superiores |
| JSON | Depende dos serviços que fazem a leitura e gravação |

## 13. Pontos de atenção

### Armazenamento único

`info_incidente.json` é substituído durante as execuções. O arquivo não mantém histórico.

### Concorrência

Duas execuções simultâneas podem sobrescrever os mesmos dados, evidências e logs relacionados ao incidente.

### Pasta de logs

`output/logs` não deve ser removida durante a execução, pois `automacao.log` permanece aberto pelo `RotatingFileHandler`.

### Caminhos

`get_path()` não cria pastas. Quando o diretório for necessário, o serviço chamador deve criá-lo ou utilizar `get_output_path()`.

### Separadores

`os.path.join()` adapta os separadores ao sistema operacional, mas a aplicação atual depende de Windows por causa do Outlook e COM.

## 14. Testes relacionados

| Cenário | Resultado esperado |
|---|---|
| Inicializar a API | `automacao.log` criado |
| Emitir `DEBUG` | Mensagem gravada no arquivo |
| Emitir `INFO` | Mensagem gravada no arquivo e exibida no console |
| Configurar novamente | Handlers não duplicados |
| Log atingir 5 MB | Rotação automática realizada |
| Resolver caminho existente | Caminho completo retornado |
| Criar diretório de saída | Pasta criada automaticamente |
| Falha de permissão | Erro registrado e propagado |
| Salvar incidente | JSON atualizado |
| Duas execuções simultâneas | Risco de sobrescrita identificado |
| Limpar evidências | Pasta de logs preservada |
