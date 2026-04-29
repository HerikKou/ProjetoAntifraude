# Documentação Técnica
## Sistema de Processamento Bancário com Antifraude IA

---

## 1. Objetivo

O sistema tem como objetivo simular um fluxo real de processamento de pagamentos em ambiente financeiro, onde usuários externos enviam requisições de pagamento e o sistema interno é responsável por validar, analisar o risco de fraude com Inteligência Artificial e retornar o status final da operação.

A proposta representa um cenário comum em grandes empresas e bancos, onde sistemas internos precisam ser disponibilizados de forma segura, escalável e resiliente para usuários externos, com capacidade de processar alto volume de transações sem perda de dados.

---

## 2. Planejamento

O projeto resolve o problema de processamento de pagamentos em massa com detecção de fraudes em tempo real.

Quando um grande volume de transações é enviado simultaneamente, sistemas tradicionais tendem a ficar lentos, perder dados ou falhar. A solução utiliza microsserviços para separar as responsabilidades, filas com Kafka para absorver o volume sem sobrecarregar o sistema, e um modelo de IA para analisar o risco de fraude de forma automatizada.

**Resultado:** um sistema escalável, resiliente e preparado para evoluir conforme a demanda cresce.

---

## 3. Arquitetura

### 3.1 Visão Geral

O acesso de usuários externos acontece pelo **TransacaoService**, responsável por receber as requisições via API REST. A comunicação entre os microsserviços ocorre de forma assíncrona via **Apache Kafka**, escolhido pela capacidade de lidar com alto volume de eventos, retenção de mensagens e possibilidade de reprocessamento.

Cada microsserviço possui seu próprio banco de dados MySQL, garantindo independência, baixo acoplamento e maior facilidade de escalabilidade.

### 3.2 Fluxo Principal

```
1. Usuário envia requisição POST /transacao
2. TransacaoService salva no banco e publica no tópico transacao_criada
3. AntifraudeService consome transacao_criada
4. AntifraudeService calcula o score de fraude (regras + modelo IA)
5. Se score < 41  → publica em transacao_aprovada  → status APROVADA
   Se score 41-70 → publica em transacao_aprovada  → status ANALISE_MANUAL
   Se score > 70  → publica em fraude_detectada    → status BLOQUEADA
6. PagamentoService consome transacao_aprovada e confirma o pagamento
```

### 3.3 Containers

| Container | Imagem | Porta | Função |
|---|---|---|---|
| transacao | transacaopython | 8000 | API REST |
| antifraude | antifraudepython | — | Análise de fraude |
| pagamento | pagamentopython | — | Processamento |
| kafka | confluentinc/cp-kafka:7.4.0 | 9092 | Mensageria |
| zookeeper | confluentinc/cp-zookeeper:7.4.0 | 2181 | Coordenação |
| mysql | mysql:8.0 | 3306 | Banco de dados |
| datadog | datadog/agent | — | Observabilidade |

---

## 4. Modelagem de Dados

### TransacaoService — banco: transacaodb

**Tabela: transacao**

| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer PK | Identificador único |
| contaOrigem | String(255) | Número da conta de origem |
| contaDestino | String(255) | Número da conta de destino |
| valor | Float | Valor da transação |
| status | String(255) | PENDENTE / APROVADA / BLOQUEADA |
| tipo_transacao | String(255) | PIX / TED / DOC |
| Score_fraude | Float nullable | Score calculado pela IA |
| data_transacao | DateTime | Data e hora da transação |

### AntifraudeService — banco: antifraudedb

**Tabela: antifraude**

| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer PK | Identificador único |
| transacao_id | Integer | Referência à transação |
| conta_origem | String(255) | Conta de origem |
| conta_destino | String(255) | Conta de destino |
| valor | Float | Valor analisado |
| score | Float nullable | Score de fraude (0-110) |
| status | String(255) | APROVADA / ANALISE_MANUAL / BLOQUEADA |
| data_analise | DateTime | Data da análise |

### PagamentoService — banco: pagamentodb

**Tabela: pagamento**

| Campo | Tipo | Descrição |
|---|---|---|
| id | Integer PK | Identificador único |
| transacao_id | Integer | Referência à transação |
| status | String(255) | PAGO / BLOQUEADO |
| score_fraude | Float nullable | Score recebido |
| tipo_pagamento | String(255) | PIX / BLOQUEADO |
| data_pagamento | DateTime | Data do pagamento |

---

## 5. Antifraude IA

### 5.1 Regras Manuais

O score é calculado pela soma de 4 critérios:

| Método | Condição | Pontuação |
|---|---|---|
| `verificar_valor()` | Valor > R$ 7.000 | +30 |
| `verificar_horario()` | Entre 00h e 06h | +30 |
| `verificar_frequencia()` | Mesma conta origem em < 10 min | +30 |
| `verificar_conta_destino()` | Conta destino sem histórico | +20 |

**Score máximo pelas regras: 110**

### 5.2 Modelo de Machine Learning

Além das regras manuais, o sistema utiliza um **RandomForestClassifier** do scikit-learn treinado com dados históricos de transações.

**Features utilizadas:**
- `valor` — valor da transação
- `hora` — hora do dia
- `frequencia` — número de transações recentes
- `conta_destino_nova` — 1 se conta nova, 0 se já existe

**Score final:** média entre o score das regras manuais e a probabilidade de fraude predita pelo modelo (0-100).

### 5.3 Classificação do Score

| Score | Status | Ação |
|---|---|---|
| 0 – 40 | APROVADA | Publica em transacao_aprovada |
| 41 – 70 | ANALISE_MANUAL | Publica em transacao_aprovada |
| 71+ | BLOQUEADA | Publica em fraude_detectada |

---

## 6. Tópicos Kafka

| Tópico | Publicado por | Consumido por | Dados |
|---|---|---|---|
| `transacao_criada` | TransacaoService | AntifraudeService | id, contaOrigem, contaDestino, valor, tipo_transacao |
| `transacao_aprovada` | AntifraudeService | PagamentoService | transacao_id, status, score |
| `fraude_detectada` | AntifraudeService | PagamentoService | transacao_id, status, score |

---

## 7. Stack Tecnológica

| Categoria | Tecnologia | Versão |
|---|---|---|
| Linguagem | Python | 3.13 |
| Framework API | FastAPI + Uvicorn | Latest |
| ORM | SQLAlchemy | 2.x |
| Banco de Dados | MySQL | 8.0 |
| Mensageria | Apache Kafka | 7.4.0 |
| IA / ML | scikit-learn | 1.x |
| Dados | pandas, numpy | Latest |
| Containerização | Docker + Compose | Latest |
| Observabilidade | Datadog Agent | Latest |
| Validação | Pydantic | 2.x |

---

## 8. Observabilidade

O projeto conta com integração ao **Datadog** via container Docker, responsável por coletar métricas, logs e traces de todos os serviços em tempo real.

O agente Datadog monitora:
- Logs dos containers
- Métricas de CPU, memória e rede
- Status de saúde dos serviços
- Eventos do Kafka

---

## 9. Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|---|---|---|
| `DATABASE_URL` | String de conexão com o MySQL | `mysql+pymysql://root:@mysql:3306/transacaodb` |
| `KAFKA_BOOTSTRAP_SERVERS` | Endereço do broker Kafka | `kafka:9092` |

---

## 10. Autor

**Herik Kou Homma Kato**
Desenvolvedor Backend Java / Python

[LinkedIn](https://www.linkedin.com/in/herik-kato-dev/) | [GitHub](https://github.com/HerikKou)
