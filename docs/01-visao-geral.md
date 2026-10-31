# Visão Geral da Automação Incidente Transacional

## 1. Identificação

| Informação | Descrição |
|---|---|
| Nome da solução | Automação Incidente Transacional |
| Setor responsável | S/NOC |
| Usuários | Analistas do NOC |
| Responsável pelo desenvolvimento | Riah Sander Cavalheiro |
| Status | Em desenvolvimento |
| Versão | 0.1.0 |

## 2. Contexto

Antes da implementação da automação, os analistas do NOC precisavam
executar manualmente diferentes consultas, realizar cálculos, capturar
evidências, registrar informações no sistema de chamados e enviar
comunicações relacionadas aos incidentes.

A execução manual dessas atividades exigia que o analista alternasse
entre diferentes sistemas e realizasse diversas etapas repetitivas.
Esse processo aumentava o tempo necessário para o tratamento dos
incidentes e ampliava a possibilidade de erros em cálculos, registros
e evidências.

## 3. Objetivo

A Automação Incidente Transacional tem como objetivo automatizar e
padronizar as atividades necessárias para o registro e a finalização
de incidentes transacionais tratados pelo S/NOC.

A solução centraliza as informações inseridas pelos analistas,
realiza consultas e cálculos, gera evidências, interage com o sistema
de chamados Qualitor, envia comunicações e registra os resultados
das execuções.

## 4. Público-alvo

A automação destina-se aos analistas do NOC responsáveis pelo
registro, acompanhamento e finalização de incidentes transacionais.

Os analistas utilizam uma interface web para informar os dados
necessários e iniciar os processos da automação.

## 5. Processos automatizados

A solução possui dois processos principais:

1. Registro do incidente.
2. Finalização do incidente.

### 5.1 Registro do incidente

#### Ação do analista

1. O analista acessa a página de registro.
2. Preenche as informações solicitadas.
3. Confere os dados informados.
4. Solicita a execução da automação.
5. Aguarda a apresentação do resultado.

#### Ação da aplicação

1. O frontend envia os dados para a API.
2. A API valida os dados recebidos.
3. O router de incidente inicia o serviço de execução.
4. A automação realiza as consultas necessárias.
5. A automação calcula as informações relacionadas à perda.
6. As evidências da execução são geradas.
7. O chamado é aberto no Qualitor.
8. Os dados do incidente são salvos.
9. A execução é registrada nos logs.
10. O resultado é devolvido ao frontend.
11. O resultado é apresentado ao analista.

#### Resultado esperado

Ao final do processamento, o incidente deve estar registrado no
Qualitor, as evidências devem estar disponíveis e o analista deve
receber uma mensagem com o resultado da execução.

### 5.2 Finalização do incidente

#### Ação do analista

1. O analista acessa a página de finalização.
2. Informa os dados solicitados.
3. Confere as informações.
4. Solicita a finalização do incidente.
5. Aguarda a apresentação do resultado.

#### Ação da aplicação

1. O frontend envia a solicitação para a API.
2. A API valida os dados recebidos.
3. A automação recupera as informações do incidente.
4. As consultas finais são executadas.
5. Novas evidências são geradas.
6. O chamado é atualizado ou encerrado no Qualitor.
7. O e-mail relacionado à operação é enviado.
8. A execução é registrada nos logs.
9. O resultado é devolvido ao frontend.
10. O resultado é apresentado ao analista.

#### Resultado esperado

Ao final do processamento, o incidente deve estar finalizado no
Qualitor, as evidências devem estar atualizadas e as comunicações
necessárias devem ter sido enviadas.

## 6. Escopo

A automação contempla:

- recebimento dos dados por meio de uma interface web;
- validação das informações recebidas pela API;
- execução de consultas relacionadas ao incidente;
- realização de cálculos relacionados à perda;
- geração automática de evidências;
- abertura de chamados no Qualitor;
- atualização ou encerramento de chamados no Qualitor;
- envio de comunicações por e-mail;
- armazenamento local de informações necessárias para a execução;
- geração de logs para acompanhamento e diagnóstico;
- apresentação do resultado ao analista.

## 7. Fora do escopo

A versão atual da solução não contempla:

- correção automática de indisponibilidades em sistemas externos;
- operação independente do Qualitor e dos sistemas consultados;
- armazenamento histórico das execuções em banco de dados;
- execução simultânea por vários analistas;
- recuperação automática de todas as falhas;
- administração de usuários e permissões pela própria aplicação.

## 8. Benefícios

A implementação da automação proporciona os seguintes benefícios:

- redução de tarefas manuais e repetitivas;
- padronização do registro de incidentes;
- padronização da finalização de incidentes;
- redução da possibilidade de erros em cálculos e registros;
- geração automática de evidências;
- centralização do processo em uma interface web;
- maior rastreabilidade das etapas executadas;
- facilidade para diagnosticar falhas por meio dos logs;
- redução da necessidade de alternar manualmente entre sistemas;
- maior consistência nas informações registradas no Qualitor.

## 9. Dependências

O funcionamento da automação depende dos seguintes recursos:

- disponibilidade do frontend;
- disponibilidade da API;
- disponibilidade do Qualitor;
- disponibilidade dos sistemas utilizados nas consultas;
- acesso à rede corporativa;
- permissões adequadas para o usuário de execução;
- acesso de leitura e gravação às pastas `data` e `output`;
- configuração correta das variáveis presentes no arquivo `.env`;
- ambiente Windows preparado para a execução da automação.

## 10. Limitações conhecidas

A versão atual utiliza arquivos JSON locais para armazenar
configurações e informações necessárias para a execução.

Por utilizar armazenamento local, a automação deve operar com apenas
uma execução por vez. A execução simultânea pode provocar
sobrescrita, leitura incorreta ou perda de informações.

A automação também depende da disponibilidade dos sistemas externos.
Uma indisponibilidade no Qualitor, nos sistemas consultados ou na
rede corporativa pode impedir a conclusão do processo.

As evidências e os logs são armazenados localmente na pasta `output`.
Essa pasta deve possuir permissões adequadas e uma política de
retenção para evitar crescimento contínuo.

## 11. Rastreabilidade

Cada processamento deve gerar registros nos logs da aplicação.

Os logs têm como objetivo:

- registrar o início e o encerramento das execuções;
- identificar as etapas concluídas;
- registrar avisos e falhas;
- facilitar o diagnóstico de problemas;
- auxiliar na identificação da última etapa executada;
- apoiar a análise de execuções incompletas.

Os arquivos de log são armazenados em:

`output/logs/`

Logs, arquivos JSON e evidências não devem conter senhas, tokens,
credenciais ou outras informações sensíveis sem necessidade
operacional.

## 12. Controle do documento

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 26/10/2026 | Riah Sander Cavalheiro | Criação da visão geral da solução |