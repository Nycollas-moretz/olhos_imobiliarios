# ADR 001: Monolito modular com worker de vídeo separado

- **Status:** Aceita
- **Data:** 07/10/2026

## Contexto

O Olhos Imobiliários gera vídeos-tour a partir de fotos de imóveis. O sistema tem duas naturezas de carga bem diferentes:

- **API e painel:** leves, precisam responder rápido (cadastro de anúncios, upload, status).
- **Geração de vídeo:** pesada, demorada (minutos) e dependente de GPU.

Fatores do projeto:

- O desenvolvimento é feito por uma pessoa, em ritmo de aprendizado.
- O escopo ainda está mudando; as fronteiras entre responsabilidades não estão estáveis.
- O volume esperado é pequeno (meta do primeiro ano: 5 a 20 imobiliárias e algumas centenas de anúncios).
- O diferencial do produto é o gerador de vídeo, não a infraestrutura.

## Decisão

1. **A parte de negócio é um monolito modular.** Um único backend (FastAPI), um repositório e um deploy, dividido internamente em módulos com responsabilidade clara (por exemplo: autenticação, anúncios, mídia, vídeo). Um módulo não acessa as tabelas internas de outro; conversam por funções e contratos explícitos.
2. **O gerador de vídeo roda em um processo separado (worker)**, que lê pedidos pendentes registrados pela API, processa em segundo plano e atualiza o status. A separação existe por necessidade técnica (GPU, tempo de execução, não travar o site), não por divisão de domínio.
3. **Contrato entre API e worker:** a API grava o pedido (anúncio, fotos, opções) e o worker devolve o MP4 e o status (na fila, processando, pronto, erro).

```
API monolítica (FastAPI, módulos internos) ── banco ── worker de vídeo (GPU)
```

## Alternativas consideradas

- **Microserviços desde o início.** Descartada. Resolvem problemas de organização de times grandes e de escala independente, que o projeto não tem. Em troca, trazem custos imediatos: comunicação por rede e suas falhas, dados distribuídos e consistência, vários deploys, depuração entre serviços. Dividir cedo também fixaria fronteiras que provavelmente estão erradas, já que o escopo ainda muda.
- **Monolito único, incluindo a geração de vídeo na mesma requisição.** Descartada. Gerar vídeo leva minutos e travaria o site, violando o requisito de não bloquear a plataforma. Também mistura código que precisa de GPU com código que não precisa.

## Consequências

**Positivas**
- Menos infraestrutura e menos código de comunicação; mais tempo para o gerador de vídeo.
- Mudar uma responsabilidade de módulo é uma edição de código, não uma migração de APIs e dados.
- Testes e depuração mais simples (um processo para a parte de negócio).
- O worker pode escalar e evoluir separado (outra máquina, com GPU) sem mexer na API.

**Negativas / custos**
- A modularidade depende de disciplina: sem fronteiras respeitadas, o monolito vira bagunça.
- Todo o código de negócio é publicado junto; um erro grave pode afetar tudo.
- Escalar a parte de negócio horizontalmente exigirá cuidado com estado, caso o volume cresça muito.

## Condição para revisar

Extrair um módulo para um serviço próprio apenas quando houver um problema concreto: por exemplo, o gerador de vídeo ser consumido por terceiros via API, uma parte exigir escala muito diferente do resto, ou a equipe crescer a ponto de precisar de deploys independentes.
