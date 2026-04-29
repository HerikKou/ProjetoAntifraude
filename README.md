# 🏦 Sistema de Processamento Bancário com Antifraude IA

Sistema distribuído de processamento de pagamentos com detecção de fraudes em tempo real, utilizando arquitetura de microsserviços, comunicação assíncrona via Apache Kafka e modelo de IA com scikit-learn.

---

## 📌 Sobre o Projeto

O projeto simula um fluxo real de processamento de pagamentos em ambiente financeiro. Usuários externos enviam requisições de pagamento, o sistema valida, analisa o risco de fraude com Inteligência Artificial e processa ou bloqueia a transação automaticamente.

---

## 🏗️ Arquitetura

O sistema é composto por **4 microsserviços independentes**, cada um com seu próprio banco de dados, comunicando-se de forma assíncrona via **Apache Kafka**.

<img width="1289" height="733" alt="Captura de tela 2026-04-28 141539" src="https://github.com/user-attachments/assets/642c6c6b-2769-468e-890f-01d55d15a44f" />

### Containers Docker

| Container | Imagem | Função |
|---|---|---|
| transacao | transacaopython | API REST de transações |
| antifraude | antifraudepython | Análise de fraude com IA |
| pagamento | pagamentopython | Processamento de pagamento |
| kafka | confluentinc/cp-kafka:7.4.0 | Mensageria |
| zookeeper | confluentinc/cp-zookeeper:7.4.0 | Coordenação do Kafka |
| mysql | mysql:8.0 | Banco de dados |
| datadog | datadog/agent | Observabilidade |

---

## 🛠️ Stack Tecnológica

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python 3.13 |
| Framework API | FastAPI + Uvicorn |
| ORM | SQLAlchemy |
| Banco de Dados | MySQL 8.0 |
| Mensageria | Apache Kafka |
| IA / ML | scikit-learn (RandomForestClassifier) |
| Dados | pandas, numpy |
| Containerização | Docker + Docker Compose |
| Observabilidade | Datadog |
| Validação | Pydantic |

---

## 📁 Estrutura de Pastas

```
projetoantifraude/
├── transacao/
│   ├── app/
│   │   ├── controller/
│   │   ├── service/
│   │   ├── models/
│   │   ├── repository/
│   │   ├── dto/
│   │   └── config/
│   ├── Dockerfile
│   └── requirements.txt
├── antifraude/
│   ├── app/
│   │   ├── service/
│   │   ├── models/
│   │   ├── repository/
│   │   ├── dto/
│   │   └── config/
│   ├── Dockerfile
│   └── requirements.txt
├── pagamento/
│   ├── app/
│   │   ├── service/
│   │   ├── models/
│   │   ├── repository/
│   │   ├── dto/
│   │   └── config/
│   ├── Dockerfile
│   └── requirements.txt
├── init.sql
└── docker-compose.yaml
```

---

## 🚀 Como Executar

### Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose

### Subindo o projeto

```bash
# Clone o repositório
git clone https://github.com/HerikKou/ProjetoAntifraude
cd projetoantifraude

# Suba todos os serviços
docker-compose up
```

### Testando a API

Acesse o Swagger em: [http://localhost:8000/docs](http://localhost:8000/docs)

Exemplo de payload:

```json
{
  "conta_origem": "1234-5",
  "conta_destino": "6789-0",
  "valor": 5000.00,
  "tipo_transacao": "PIX"
}
```

---

## 🔗 Tópicos Kafka

| Tópico | Publicado por | Consumido por |
|---|---|---|
| `transacao_criada` | TransacaoService | AntifraudeService |
| `transacao_aprovada` | AntifraudeService | PagamentoService |
| `fraude_detectada` | AntifraudeService | PagamentoService |

---

## 🗄️ Bancos de Dados

Cada microsserviço possui seu próprio banco de dados, garantindo baixo acoplamento e independência.

| Serviço | Banco |
|---|---|
| TransacaoService | transacaodb |
| AntifraudeService | antifraudedb |
| PagamentoService | pagamentodb |

---

## 📊 Observabilidade

O projeto conta com integração ao **Datadog** para monitoramento de logs, métricas e rastreamento dos containers em tempo real.

---

## 👨‍💻 Autor

**Herik Kou Homma Kato**
[LinkedIn](https://www.linkedin.com/in/herik-kato-dev/) | [GitHub](https://github.com/HerikKou)
