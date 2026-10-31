# Componente de Cálculo de Perda

## 1. Objetivo

O componente consulta um período histórico semelhante ao incidente e usa a quantidade de transações encontradas como estimativa de perda média.

## 2. Arquivos relacionados

| Arquivo | Responsabilidade |
|---|---|
| `backend/services/avg_transacional/avg_perda.py` | Calcular o período de referência e consultar as transações |
| `data/operadoras.json` | Relacionar parceiros aos gráficos transacionais |
| `data/operadoras.example.json` | Demonstrar a estrutura sem dados reais |

O arquivo real de operadoras contém informações internas e não deve ser enviado ao repositório. citeturn46search22turn46search23

## 3. Dependências e dados

| Recurso | Finalidade |
|---|---|
| Playwright | Automatizar o Portal Transacional |
| `python-dateutil` | Calcular a data equivalente do mês anterior |
| `holidays` | Identificar feriados brasileiros |
| `data/info_incidente.json` | Fornecer e receber os dados do cálculo |
| `.env` | Fornecer URL e credenciais do portal |

Variáveis de ambiente utilizadas:

```text
PORTAL
USER
PASSWORD
```

## 4. Estrutura do mapeamento de operadoras

Estrutura esperada:

```json
{
  "OPERADORA_EXEMPLO_A": "Transações OPERADORA EXEMPLO A",
  "OPERADORA_EXEMPLO_B": "Transações OPERADORA EXEMPLO B"
}
```

A chave representa o parceiro e o valor representa o nome do gráfico correspondente. citeturn46search22turn46search23

## 5. Cálculo do período de referência

Função:

```python
validador_data(data_de_inicio, data_de_fim, hora_inicio, hora_fim)
```

Fluxo:

```text
Converter data e hora do incidente
    ↓
Calcular a duração real
    ↓
Classificar o dia como alta ou baixa transacional
    ↓
Voltar um mês
    ↓
Procurar uma data com o mesmo perfil
    ↓
Aplicar a mesma duração do incidente
    ↓
Retornar o período histórico
```

Classificação usada:

| Tipo | Regra |
|---|---|
| `ALTA_TRANSACIONAL` | Dia útil que não seja feriado |
| `BAIXA_TRANSACIONAL` | Sábado, domingo ou feriado brasileiro |

A busca verifica até 31 dias em torno da data equivalente do mês anterior. citeturn46search24

### Entrada

```text
Data inicial: DD/MM/AAAA
Data final: DD/MM/AAAA
Hora inicial: HH:MM
Hora final: HH:MM
```

### Saída

```text
Data inicial: AAAA/MM/DD
Data final: AAAA/MM/DD
Hora inicial: HH:MM
Hora final: HH:MM
```

## 6. Consulta da perda

Função principal:

```python
calcula_perda(browser)
```

Fluxo:

```text
Ler info_incidente.json
    ↓
Normalizar o nome da operadora
    ↓
Abrir o Portal Transacional
    ↓
Realizar login
    ↓
Selecionar a operadora
    ↓
Selecionar o escopo
    ↓
Calcular o período histórico
    ↓
Executar a consulta
    ↓
Ler a quantidade de registros
    ↓
Salvar perda_media no JSON
```

A função recebe uma instância de navegador Playwright criada pelo fluxo de encerramento do chamado. citeturn46search24

## 7. Conversão das operadoras

Antes da seleção no portal, alguns nomes são ajustados:

| Nome no incidente | Nome usado no portal |
|---|---|
| `TOPAZIO PIX` | `Banco Topazio Atm` |
| `PLUS - VISA` | `Visa` |
| `CIRRUS - MASTERCARD` | `Cirrus` |
| Demais parceiros | Nome convertido com `title()` |

citeturn46search24

## 8. Seleção do escopo

Para `Banco Topazio Atm`:

| Escopo | Tipo selecionado |
|---|---|
| `GERAL` | Todos os tipos |
| `SAQUE` | `PIX SAQUE` |
| `DEPOSITO` | `PIX DEPOSITO` |
| `SALDO` | `Saldo em Tela` e `Saldo Impresso` |

Para as demais operadoras:

| Escopo | Tipo selecionado |
|---|---|
| `GERAL` | Todos os tipos |
| `SAQUE` | `Saque` |
| `DEPOSITO` | `Depósito Varejista` |

citeturn46search24

## 9. Resultado da consulta

Quando o portal mostra registros, o componente extrai o primeiro número do texto:

```text
Total de registros encontrados: 160
```

Quando o portal mostra `Nenhum resultado encontrado.`, o valor é definido como zero:

```text
Nenhuma transação encontrada. Perda média definida como 0.
```

O resultado é salvo em:

```json
{
  "perda_media": 160
}
```

Apesar do nome `perda_media`, o valor armazenado atualmente é a quantidade total de registros encontrada no período histórico. citeturn46search24

## 10. Logs

Principais eventos:

```text
Entrando no Portal Transacional...
Login concluído!
Calculando data mais próxima do incidente no último mês...
Campo 'Data Inicial' preenchido com: DATA HORA
Campo 'Data Final' preenchido com: DATA HORA
Total de registros encontrados: QUANTIDADE
Nenhuma transação encontrada. Perda média definida como 0.
```

Os logs são gravados em:

`output/logs/automacao.log`

## 11. Tratamento de erros

Erros no cálculo da data são registrados e propagados para `calcula_perda()`.

Erros na consulta são convertidos para:

```text
Erro no calculo de perda: DETALHE
```

A exceção é lançada como `AutomacaoException`. A página do portal é fechada no bloco `finally`. citeturn46search24

### Erros conhecidos

| Erro | Causa provável | Efeito |
|---|---|---|
| `ValueError` em `strptime()` | Data ou hora fora do formato esperado | Cálculo interrompido |
| `KeyError` no JSON | Campo obrigatório ausente | Cálculo interrompido |
| Timeout do Playwright | Portal ou elemento indisponível | Cálculo interrompido |
| Operadora não encontrada | Nome diferente do portal | Seleção falha |
| Escopo não reconhecido | Valor diferente dos casos tratados | Tipo de transação pode não ser selecionado |
| Texto de registros alterado | Expressão regular não encontra número | Valor pode ser definido como zero |

## 12. Pontos de atenção no código atual

### Variável `page`

A variável `page` é criada dentro do bloco `try`, mas é usada no `finally`:

```python
finally:
    if page:
        page.close()
```

Se ocorrer uma falha antes de `page = browser.new_page()`, pode ocorrer `UnboundLocalError` durante o tratamento do erro. citeturn46search24

### Datas invertidas

O código não valida se a data final é anterior à data inicial. Nesse caso, a duração calculada pode ser negativa. citeturn46search24

### Operadora e escopo

A seleção depende de correspondência exata com os nomes disponíveis no Portal Transacional. Mudanças nos nomes ou seletores podem causar falhas. citeturn46search24

### Resultado numérico

A expressão regular utiliza o primeiro número encontrado no texto. Se o formato do portal mudar, o valor extraído pode ser incorreto. citeturn46search24

## 13. Execução parcial e restrições

O período pode ser calculado e a consulta executada antes de ocorrer uma falha na gravação do JSON.

```text
Consulta realizada
    ↓
Quantidade encontrada
    ↓
Falha ao gravar info_incidente.json
    ↓
perda_media não é salva
```

Restrições atuais:

- dependência do Portal Transacional;
- dependência de seletores da interface;
- feriados considerados pelo calendário `holidays.BR()`;
- uma execução por vez;
- uso de arquivos JSON locais;
- dependência de formatos específicos de data e hora;
- valor estimado com base em um único período histórico.

## 14. Testes relacionados

| Cenário | Resultado esperado |
|---|---|
| Dia útil | Referência encontrada em dia útil |
| Final de semana | Referência encontrada em baixa transacional |
| Feriado brasileiro | Referência encontrada em baixa transacional |
| Incidente atravessa a meia-noite | Mesma duração aplicada ao período histórico |
| Escopo geral | Todos os tipos selecionados |
| Escopo saque | Tipo de saque selecionado |
| Escopo depósito | Tipo de depósito selecionado |
| Escopo saldo no Topazio | Tipos de saldo selecionados |
| Consulta com registros | Quantidade salva em `perda_media` |
| Consulta sem registros | `perda_media` definida como zero |
| Operadora não encontrada | Erro registrado e propagado |
| Portal indisponível | `AutomacaoException` propagada |
| JSON sem campo obrigatório | Erro registrado e propagado |
