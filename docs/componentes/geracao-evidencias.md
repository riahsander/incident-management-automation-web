# Componente de Geração de Evidências

## 1. Objetivo

O componente remove evidências antigas, identifica o parceiro do incidente e gera capturas do monitoramento de operadoras e dos gráficos transacionais.

## 2. Arquivos relacionados

| Arquivo | Responsabilidade |
|---|---|
| `backend/services/gerar_screenshots/geral_function.py` | Coordenar a geração das evidências |
| `backend/services/gerar_screenshots/screenshot_op.py` | Capturar o card principal da operadora |
| `backend/services/gerar_screenshots/screenshot_detalhado.py` | Capturar o detalhamento transacional |
| `backend/services/gerar_screenshots/screenshot_trans.py` | Capturar o gráfico transacional |
| `backend/services/zerador_evidencias/zerar_evidencias.py` | Limpar evidências de execuções anteriores |

## 3. Configuração e dados

O componente utiliza:

| Recurso | Finalidade |
|---|---|
| `data/info_incidente.json` | Identificar o parceiro e salvar os caminhos das imagens |
| `data/operadoras.json` | Relacionar o parceiro ao nome do gráfico |
| `.env` | Fornecer URLs e credenciais dos portais |
| Playwright | Automatizar o navegador e capturar as imagens |

Variáveis de ambiente utilizadas:

```text
MON_OPERADORAS
TRANSACIONAL_GRAF
USER
PASSWORD
```

Os arquivos reais da pasta `data` e o arquivo `.env` não devem ser enviados ao repositório.

## 4. Limpeza das evidências

Função principal:

```python
limpar_output()
```

Pastas removidas e recriadas:

```text
output/printGraf
output/printOP
output/printOP_detalhado
```

A pasta abaixo não é removida:

```text
output/logs
```

Essa separação evita a tentativa de apagar `automacao.log` enquanto o arquivo está aberto pelo logger. citeturn44search16

## 5. Fluxo de geração

Função principal:

```python
gerar_screenshot()
```

Fluxo:

```text
Ler info_incidente.json
    ↓
Identificar o parceiro
    ↓
Preparar as pastas de saída
    ↓
Capturar o card principal
    ↓
Capturar o detalhamento transacional
    ↓
Verificar se existe gráfico configurado
    ↓
Capturar o gráfico, quando aplicável
    ↓
Salvar os caminhos no JSON
```

Ordem das etapas:

| Ordem | Etapa | Função |
|---:|---|---|
| 1 | Ler os dados do incidente | `json.load()` |
| 2 | Capturar o card principal | `print_operadora()` |
| 3 | Capturar o card detalhado | `print_opdetalhado()` |
| 4 | Capturar o gráfico, quando configurado | `print_grafico()` |
| 5 | Atualizar os caminhos das imagens | `json.dump()` |

O parceiro é lido de `info_incidente.json`. Se o campo não existir, o valor padrão utilizado é `DESCONHECIDO`. citeturn44search15

## 6. Evidência principal da operadora

Função:

```python
print_operadora(operadora, pasta_saida)
```

Etapas:

1. acessar o monitoramento de operadoras;
2. realizar login;
3. fechar o menu lateral;
4. localizar o card pelo nome da operadora;
5. salvar a imagem.

Arquivo gerado:

```text
output/printOP/NOME_DA_OPERADORA.png
```

O card é localizado pelo nome exato, sem diferenciar letras maiúsculas e minúsculas. citeturn43search13

## 7. Evidência detalhada

Função:

```python
print_opdetalhado(operadora, pasta_saida)
```

Etapas:

1. acessar o monitoramento de operadoras;
2. localizar o card da operadora;
3. clicar em `TOTAL`;
4. abrir a nova janela;
5. localizar o conteúdo detalhado;
6. salvar a imagem.

Arquivo gerado:

```text
output/printOP_detalhado/NOME_DA_OPERADORA_detalhado.png
```

O conteúdo detalhado é localizado pelo seletor `.css-1wux2l8`. citeturn43search12

## 8. Evidência do gráfico transacional

Função:

```python
print_grafico(operadora, pasta_saida)
```

O gráfico é gerado somente quando o parceiro existe no mapeamento de `data/operadoras.json`.

Etapas:

1. acessar o portal de gráficos;
2. realizar login;
3. fechar o menu lateral;
4. localizar o gráfico pelo título;
5. salvar a imagem.

Arquivo gerado:

```text
output/printGraf/NOME_DO_GRAFICO.png
```

O gráfico é localizado pelo título presente em um elemento `h2`. citeturn43search14

## 9. Atualização do incidente

Depois das capturas, o componente adiciona os caminhos ao arquivo `data/info_incidente.json`:

```json
{
  "print_operadora": "CAMINHO_DO_CARD_PRINCIPAL",
  "print_op_detalhado": "CAMINHO_DO_CARD_DETALHADO",
  "print_grafico": "CAMINHO_DO_GRAFICO"
}
```

O campo `print_grafico` é incluído somente quando existe um gráfico configurado para o parceiro. citeturn44search15

## 10. Logs

Principais eventos:

```text
Iniciando a criação de evidências...
Capturando evidências do Transacional Operadoras
Capturando o card detalhado das Operadoras...
Capturando evidências dos Gráficos Transacionais...
Arquivo salvo em: CAMINHO
Evidências antigas removidas: CAMINHO
```

Os logs são gravados em:

`output/logs/automacao.log`

## 11. Tratamento de erros

Os módulos registram falhas com `logger.exception()`.

Exemplos:

- card da operadora não encontrado;
- conteúdo detalhado não encontrado;
- gráfico transacional não encontrado;
- falha de login;
- timeout do Playwright;
- falha ao salvar a imagem;
- falha ao limpar um diretório.

A limpeza propaga erros de sistema de arquivos com `raise`. As funções de captura registram a falha, mas não relançam a exceção. citeturn43search12turn43search13turn43search14turn44search16

## 12. Execução parcial e restrições

Uma imagem pode falhar enquanto as demais são geradas.

```text
Card principal salvo
    ↓
Falha no card detalhado
    ↓
Gráfico salvo
```

Como as funções de captura registram o erro sem relançá-lo, o fluxo principal pode continuar e registrar caminhos de imagens que não foram criadas. citeturn43search12turn43search13turn43search14turn44search15

Restrições atuais:

- dependência das páginas e seletores dos portais;
- necessidade dos navegadores do Playwright;
- dependência da rede corporativa;
- necessidade de credenciais válidas;
- uma execução por vez;
- nomes de arquivos baseados no parceiro ou gráfico.

## 13. Testes relacionados

| Cenário | Resultado esperado |
|---|---|
| Limpeza das evidências | Pastas recriadas e logs preservados |
| Parceiro válido | Card principal salvo |
| Detalhamento disponível | Imagem detalhada salva |
| Gráfico configurado | Gráfico salvo |
| Gráfico não configurado | Fluxo continua sem `print_grafico` |
| Card não encontrado | Erro registrado no log |
| Timeout do portal | Erro registrado no log |
| Falha de permissão | Limpeza interrompida com erro |
| Execução completa | Caminhos atualizados no JSON |
