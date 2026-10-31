# Funcionamento da Automação

## 1. Visão geral

A Automação Incidente Transacional possui dois processos principais:

1. Registro de incidente.
2. Finalização de incidente.

As operações são iniciadas pelos analistas do NOC por meio do
frontend. Os dados são enviados para a API, validados e encaminhados
aos serviços responsáveis pela execução.

## 2. Registro do incidente

### 2.1 Ação do analista

1. O analista acessa a página de registro.
2. Preenche os dados solicitados.
3. Confere as informações.
4. Solicita a execução.
5. Aguarda o resultado apresentado pela aplicação.

### 2.2 Processamento da aplicação

1. O frontend envia os dados para a API.
2. A API valida os dados recebidos.
3. O serviço de registro inicia a execução.
4. A automação remove evidências de execuções anteriores.
5. Os dados do incidente são salvos.
6. A automação acessa o Qualitor.
7. O login no Qualitor é realizado.
8. O chamado é aberto.
9. O número do chamado é registrado.
10. A geração de evidências é iniciada.
11. A evidência geral da operadora é gerada.
12. A evidência detalhada da operadora é gerada.
13. A evidência dos gráficos transacionais é gerada, quando aplicável.
14. O e-mail de indisponibilidade é enviado.
15. O resultado é registrado nos logs.
16. O resultado é devolvido ao frontend.

### 2.3 Arquivos gerados

As evidências são armazenadas nos seguintes diretórios:

- `output/printOP`: evidência geral da operadora;
- `output/printOP_detalhado`: evidência detalhada;
- `output/printGraf`: evidências dos gráficos transacionais;
- `output/logs`: logs da execução.

### 2.4 Resultado esperado

Ao final do registro:

- o chamado deve estar aberto no Qualitor;
- o número do chamado deve estar disponível;
- os dados do incidente devem estar salvos;
- as evidências aplicáveis devem estar disponíveis;
- o e-mail de indisponibilidade deve ter sido enviado;
- a aplicação deve apresentar o resultado ao analista.

## 3. Finalização do incidente

### 3.1 Ação do analista

1. O analista acessa a página de finalização.
2. Informa os dados solicitados.
3. Confere as informações.
4. Solicita a finalização.
5. Aguarda o resultado apresentado pela aplicação.

### 3.2 Processamento da aplicação

1. O frontend envia os dados para a API.
2. A API valida os dados recebidos.
3. Os dados da finalização são salvos.
4. A automação acessa o Qualitor.
5. O login no Qualitor é realizado.
6. O chamado informado é localizado.
7. O formulário de encerramento é aberto.
8. A automação captura o parceiro relacionado ao incidente.
9. A hora de início do incidente é capturada.
10. A data de abertura é capturada.
11. A automação acessa o Portal Transacional.
12. O login no Portal Transacional é realizado.
13. É calculado um período equivalente do mês anterior.
14. A quantidade de transações desse período é consultada.
15. A perda média é calculada.
16. O arquivo `data/info_incidente.json` é atualizado.
17. Os campos de encerramento são preenchidos no Qualitor.
18. O chamado é encerrado.
19. O e-mail de normalização é enviado.
20. O resultado é registrado nos logs.
21. O resultado é devolvido ao frontend.

### 3.3 Tratamento de consulta sem transações

Quando o Portal Transacional não apresentar registros no período
consultado, a automação deve considerar a quantidade de transações e
a perda média como zero.

A ausência da mensagem de quantidade de registros não deve causar
timeout ou interromper o encerramento do chamado.

Evento esperado no log:

`Nenhuma transação encontrada. Perda média definida como 0.`

### 3.4 Resultado esperado

Ao final da finalização:

- o chamado deve estar localizado;
- os dados adicionais devem estar capturados;
- a perda média deve estar calculada;
- o arquivo de informações deve estar atualizado;
- os campos do Qualitor devem estar preenchidos;
- o chamado deve estar encerrado;
- o e-mail de normalização deve ter sido enviado;
- o resultado deve ser apresentado ao analista.

## 4. Sistemas envolvidos

| Sistema | Responsabilidade |
|---|---|
| Frontend React | Coletar dados e apresentar o resultado |
| API FastAPI | Validar e encaminhar as solicitações |
| Backend Python | Coordenar as etapas da automação |
| Qualitor | Registrar e encerrar os chamados |
| Portal Transacional | Consultar transações e calcular a perda |
| Outlook/MAPI | Enviar os e-mails |
| Arquivos JSON | Armazenar informações temporárias |
| Sistema de arquivos | Armazenar evidências e logs |