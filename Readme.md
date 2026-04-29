# 🏦 Sistema de Processamento Bancário com Antifraude IA

Sistema distribuído de processamento de pagamentos com detecção de fraudes em tempo real, utilizando arquitetura de microsserviços, comunicação assíncrona via Apache Kafka, observabilidade com Datadog e modelo de IA com scikit-learn.

---

## 📌 Sobre o Projeto

O projeto simula um fluxo real de processamento de pagamentos em ambiente financeiro. Usuários externos enviam requisições de pagamento, o sistema valida, analisa o risco de fraude com Inteligência Artificial e processa ou bloqueia a transação automaticamente.

O sistema foi desenvolvido com foco em:

- Arquitetura orientada a eventos
- Microsserviços desacoplados
- Observabilidade e monitoramento
- Testes unitários
- Dockerização completa
- Simulação de fluxo bancário real

---

## 🏗️ Arquitetura

O sistema é composto por microsserviços independentes, cada um com seu próprio banco de dados, comunicando-se de forma assíncrona via Apache Kafka.

Fluxo principal:
<img width="1289" height="733" alt="Captura de tela 2026-04-28 141539" src="https://github.com/user-attachments/assets/ab9a7da6-9c4d-4dd8-a58e-7f3a2ff82e36" />


Transação → Kafka → Antifraude → Kafka → Pagamento

O Datadog atua paralelamente realizando observabilidade dos containers, logs, métrtricas e traces.

---

## 🐳 Containers Docker

| Container | Função |
|---|---|
| transacao | API REST de transações |
| antifraude | Análise antifraude com IA |
| pagamento | Processamento de pagamento |
| kafka | Broker de mensageria |
| zookeeper | Coordenação do Kafka |
| mysql | Persistência de dados |
| datadog-agent | Observabilidade |

---

## 🛠️ Stack Tecnológica

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python 3.13 |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Banco de Dados | MySQL 8 |
| Mensageria | Apache Kafka |
| IA | scikit-learn |
| Containerização | Docker + Docker Compose |
| Observabilidade | Datadog |
| Testes | Pytest |

---

## 🔗 Tópicos Kafka

| Tópico | Publicado por | Consumido por |
|---|---|---|
| transacao_criada | TransacaoService | AntifraudeService |
| transacao_aprovada | AntifraudeService | PagamentoService |
| transacao_reprovada | AntifraudeService | Fluxo de bloqueio |

---

## 🧪 Testes Unitários

O projeto possui testes unitários para validar as regras principais dos serviços.

### Testes implementados

### Transação

- criação de transação
- persistência em banco
- publicação no Kafka
- flush do producer

### Antifraude

- cálculo de score de fraude
- validação de score
- aprovação automática
- análise manual
- bloqueio de transação

### Pagamento

- processamento de pagamento aprovado
- persistência do status
- confirmação final do pagamento

### Execução dos testes

```bash
pytest
```

 Saída esperada:

<img width="1441" height="60" alt="Teste transacao" src="https://github.com/user-attachments/assets/97350655-fed5-4fa2-b37f-3c4e6a039ea6" />

---
<img width="1459" height="84" alt="antifraude test" src="https://github.com/user-attachments/assets/fdac347e-7a05-4ae9-a4b7-df92816d05bd" />

---
<img width="1467" height="34" alt="pagamento teste" src="https://github.com/user-attachments/assets/6867210b-792c-414e-a54d-77845ce2d5d8" />


---

## 📊 Observabilidade com Datadog

O projeto conta com integração com Datadog para:

- monitoramento de containers Docker
- logs centralizados
- métricas de aplicação
- traces distribuídos
- acompanhamento de falhas
- análise de performance

O Datadog não participa do fluxo de negócio, apenas monitora toda a arquitetura.

---

## 🗄️ Modelagem de Dados

Cada microsserviço possui seu próprio banco de dados para manter baixo acoplamento e independência entre domínios.

Relacionamentos principais:

- Transação → Antifraude (1:N)
- Antifraude → Pagamento (1:1)

---

## 🚀 Como Executar

```bash
docker-compose up --build
```

Swagger disponível em:

http://localhost:8000/docs

Payload de exemplo:

```json
{
  "conta_origem": "1234",
  "conta_destino": "5678",
  "valor": 5000.00,
  "tipo_transacao": "PIX"
}
```

---

## 👨‍💻 Autor

Herik Kou Homma Kato

LinkedIn:
https://www.linkedin.com/in/herik-kato-dev/

GitHub:
https://github.com/HerikKou
