# Componente de Envio de E-mail

## 1. Objetivo

O componente utiliza o Microsoft Outlook para enviar o e-mail de abertura do incidente e o e-mail de normalização.

## 2. Arquivos relacionados

| Arquivo | Responsabilidade |
|---|---|
| `backend/services/email/envio_email.py` | Criar, anexar e enviar as mensagens |
| `data/email_op.json` | Armazenar os destinatários reais por parceiro |
| `data/email_op.example.json` | Demonstrar a estrutura sem dados reais |

O arquivo real contém endereços internos e não deve ser enviado ao repositório. citeturn45search19turn45search20

## 3. Dependências e dados

| Recurso | Finalidade |
|---|---|
| Microsoft Outlook | Criar e enviar mensagens |
| `pywin32` | Acessar Outlook e MAPI pelo Windows COM |
| `pythoncom` | Inicializar e encerrar o COM em cada execução |
| `data/info_incidente.json` | Fornecer os dados do incidente |
| `data/email_op.json` | Fornecer os destinatários por parceiro |
| Assinaturas do Outlook | Incluir a assinatura HTML na mensagem |

O componente exige Windows, Outlook instalado, perfil configurado e sessão de usuário ativa. citeturn45search18

## 4. Estrutura dos destinatários

Estrutura esperada:

```json
{
  "PARCEIRO_EXEMPLO": {
    "emails": [
      "noc@example.com",
      "servicedesk@example.com"
    ]
  }
}
```

A função `get_emails()` consulta o parceiro e transforma a lista em uma string separada por ponto e vírgula:

```text
noc@example.com;servicedesk@example.com
```

Quando nenhum destinatário é encontrado, a função retorna uma string com espaço. Falhas de leitura são convertidas para `AutomacaoException`. citeturn45search18

## 5. E-mail de abertura

Função principal:

```python
enviar_email(chamado)
```

Fluxo:

```text
Inicializar COM
    ↓
Ler info_incidente.json
    ↓
Buscar assinatura do Outlook
    ↓
Buscar destinatários do parceiro
    ↓
Montar assunto e corpo HTML
    ↓
Anexar evidências existentes
    ↓
Sincronizar Outlook
    ↓
Enviar mensagem
    ↓
Sincronizar novamente
    ↓
Encerrar COM
```

### Dados utilizados

| Campo | Uso no e-mail |
|---|---|
| `parceiro` | Destinatários, assunto e corpo |
| `status` | Assunto e descrição da ocorrência |
| `tipo_transacao` | Assunto, quando aplicável |
| `autorizador` | Corpo da mensagem |
| `indisponibilidade` | Corpo da mensagem |
| `hora_inicio` | Corpo da mensagem |
| número do chamado | Assunto da mensagem |

Se o parceiro for `BANCO TOPAZIO ATM`, o nome apresentado no e-mail é convertido para `TOPAZIO PIX`. citeturn45search18

### Anexos

As evidências são anexadas somente quando o caminho existe:

| Campo no JSON | Evidência |
|---|---|
| `print_operadora` | Card principal |
| `print_grafico` | Gráfico transacional |
| `print_op_detalhado` | Card detalhado |

O e-mail também utiliza uma lista fixa de cópia configurada no código. Os endereços reais não são reproduzidos nesta documentação. citeturn45search18

## 6. E-mail de normalização

Função principal:

```python
fecha_email()
```

Fluxo:

```text
Inicializar COM
    ↓
Ler info_incidente.json
    ↓
Buscar assinatura do Outlook
    ↓
Montar assunto e corpo HTML
    ↓
Sincronizar Outlook
    ↓
Enviar mensagem
    ↓
Sincronizar novamente
    ↓
Encerrar COM
```

### Dados utilizados

| Campo | Uso no e-mail |
|---|---|
| `parceiro` | Assunto e corpo |
| `chamado` | Assunto e corpo |
| `data_inicio` | Corpo da mensagem |
| `hora_inicio` | Corpo da mensagem |
| `data_fim` | Corpo da mensagem |
| `hora_fim` | Corpo da mensagem |
| `causa` | Corpo da mensagem |
| `perda_media` | Corpo da mensagem |
| `escopo` | Assunto e corpo |
| `origem` | Corpo da mensagem |

O destinatário da normalização está configurado diretamente no código. O endereço real não é reproduzido nesta documentação. citeturn45search18

## 7. Sincronização do Outlook

Função:

```python
sincronizar_outlook(outlook)
```

A função tenta três estratégias:

1. `Session.SendAndReceive(True)`;
2. `MAPI SendAndReceive(False)`;
3. `SendReceiveAll` pelo `ActiveExplorer`.

A função retorna `True` quando pelo menos uma estratégia funciona. A indisponibilidade do `ActiveExplorer` não impede o envio quando outra estratégia foi concluída. citeturn45search18

## 8. Assinatura

A assinatura é procurada em:

```text
%APPDATA%/Microsoft/Signatures
```

O primeiro arquivo `.htm` encontrado é incluído no corpo da mensagem.

Se a busca falhar, a função retorna uma mensagem padrão e interrompe a criação do e-mail atual. citeturn45search18

## 9. Logs

Principais eventos:

```text
Enviando e-mail...
Buscando assinatura...
Criando conexão e corpo do e-mail...
Buscando e-mails de destino...
E-mails de destino encontrados.
Session.SendAndReceive executado com sucesso
MAPI SendAndReceive executado com sucesso
E-mail enviado com sucesso
```

Avisos como `ActiveExplorer não disponível` podem ocorrer sem impedir o envio. citeturn45search18

## 10. Tratamento de erros

### E-mail de abertura

Falhas são registradas e convertidas para:

```text
Falha ao enviar email.
```

A exceção é propagada como `AutomacaoException`.

### E-mail de normalização

Falhas são registradas com `logger.exception()`, mas não são relançadas.

Em ambos os fluxos, `pythoncom.CoUninitialize()` é executado no bloco `finally`. citeturn45search18

## 11. Execução parcial e restrições

O Outlook pode enviar a mensagem mesmo quando uma estratégia de sincronização apresenta aviso.

O e-mail de abertura pode ser enviado sem algum anexo quando o caminho da evidência não existe.

O e-mail de normalização pode falhar sem interromper o fluxo chamador, pois `fecha_email()` não relança a exceção. citeturn45search18

Restrições atuais:

- funcionamento somente em Windows;
- Outlook instalado e configurado;
- sessão do usuário ativa;
- destinatários reais armazenados fora do Git;
- dependência de `info_incidente.json`;
- destinatários de cópia e normalização configurados diretamente no código;
- uma execução por vez.

## 12. Segurança

- `data/email_op.json` não deve ser versionado;
- somente `data/email_op.example.json` deve ir ao repositório;
- a documentação não deve reproduzir destinatários reais;
- credenciais não devem aparecer no código ou nos logs;
- anexos devem ser conferidos antes do envio.

## 13. Testes relacionados

| Cenário | Resultado esperado |
|---|---|
| Parceiro cadastrado | Destinatários encontrados |
| Parceiro não cadastrado | Ausência de destinatários registrada |
| Evidências existentes | Arquivos anexados |
| Evidência ausente | E-mail enviado sem o anexo ausente |
| Outlook disponível | Mensagem enviada |
| `ActiveExplorer` indisponível | Aviso registrado sem bloquear outras estratégias |
| Falha no e-mail de abertura | `AutomacaoException` propagada |
| E-mail de normalização | Corpo preenchido com os dados finais |
| Arquivo de destinatários inválido | Erro registrado e propagado |
