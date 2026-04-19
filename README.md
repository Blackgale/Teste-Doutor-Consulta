
# Case Data Engineering - Resolução 

## Objetivo
Resolver um case de engenharia de dados envolvendo:
- Análise de commodities
- Arquitetura de pipeline
- Pipeline de ingestão de dados

---

## 1. Análise de Commodities

### O que foi feito
- Coleta de dados históricos
- Padronização das séries
- Criação de indicadores:
  - média móvel
  - variação percentual
  - volatilidade

### Principais insights
- O cobre apresentou maior estabilidade
- O níquel apresentou maior volatilidade

### Interpretação
Commodities mais voláteis exigem estratégias mais ativas de monitoramento.

---

## 2. Arquitetura de Pipeline

### Estrutura
Fontes -> Ingestão -> Raw -> Validação -> Data Warehouse -> Consumo

### Decisões
- Dados versionados para permitir backfill
- Pipeline idempotente
- Separação de camadas

### Observabilidade
- Alertas de falha
- Monitoramento de volume
- Detecção de dados inconsistentes

---

## 3. Pipeline de Ingestão

### Etapas
1. Extração
2. Transformação
3. Validação
4. Carga

### Validações
- Tipos corretos
- Valores não negativos
- Estrutura consistente

### SQL
- Tabelas particionadas
- Uso de MERGE para atualização

---

## Conclusão

A solução foi pensada para ser:
- Simples
- Reprodutível
- Próxima de produção

Foco principal:
Clareza > Complexidade
