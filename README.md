# Olhos Imobiliários

Plataforma que gera, a partir de fotos, um **vídeo de tour** de casas e apartamentos: a câmera "caminha" pelos cômodos e passa de um para o outro de forma natural, sem que ninguém precise ir ao local gravar. A imobiliária envia as fotos e recebe o vídeo pronto para publicar onde já divulga seus imóveis (Instagram, WhatsApp, site, portais).

**Objetivo:** reduzir o tempo e o custo de produzir vídeos de imóveis e aumentar as vendas das imobiliárias.

## Visão do produto

O produto é a **geração do vídeo-tour**. Ele não é um slideshow: cada cômodo vira um clipe com movimento de câmera e a passagem entre cômodos é feita de modo contínuo, para parecer uma visita de verdade.

A entrega principal é o **arquivo de vídeo** (formato vertical 9:16 para Reels e Stories, e horizontal 16:9 para site e portais). Imobiliárias já têm sites e canais de divulgação, então o sistema não tenta substituí-los. Uma página simples de compartilhamento por vídeo pode existir como conveniência, mas não é o foco.

O mapa 3D da cidade continua na visão do projeto, como fase posterior e independente do núcleo.

## Como o sistema funciona

**Imobiliária (usuário autenticado)**
1. Entra no painel.
2. Cria um anúncio (endereço, preço, metragem, descrição) e envia as fotos.
3. Confere a ordem sugerida dos cômodos e ajusta, se quiser.
4. Solicita a geração do vídeo e acompanha o status.
5. Baixa o vídeo nos dois formatos e divulga.

**Geração do vídeo (em segundo plano, num worker separado da API)**

```
fotos → classificar cômodos e ordenar
      → por cômodo: clipe de câmera (parallax 2.5D; reconstrução 3D como alternativa)
      → entre cômodos: transição (match cut / avanço guiado pela abertura)
      → pós-produção: correção de cor, tremor de câmera, música, legendas, marca
      → MP4 em 9:16 e 16:9
```

## Glossário

- **Imobiliária:** cliente que paga pelo sistema.
- **Imóvel:** a coisa física (endereço, coordenadas, andar, metragem).
- **Anúncio:** oferta de uma imobiliária sobre um imóvel, com preço, fotos e vídeo.
- **Clipe:** trecho de vídeo gerado a partir das fotos de um cômodo.
- **Transição:** trecho que liga um cômodo ao seguinte.
- **Vídeo (tour):** arquivo final, montado com clipes e transições, com um status de processamento.

## Requisitos funcionais

- **RF1** A imobiliária se autentica no painel.
- **RF2** A imobiliária cadastra, edita e exclui anúncios.
- **RF3** A imobiliária envia fotos de um anúncio.
- **RF4** O sistema classifica o cômodo de cada foto e sugere a ordem do tour; a imobiliária pode ajustar.
- **RF5** O sistema gera o vídeo-tour de forma assíncrona e informa o status (na fila, processando, pronto, erro).
- **RF6** O vídeo é entregue em formato vertical (9:16) e horizontal (16:9).
- **RF7** A imobiliária pode baixar, reprocessar e excluir vídeos.
- **RF8** A identidade da imobiliária (logo, cores, contato) é aplicada automaticamente ao vídeo.

## Requisitos não funcionais

> Os números são pontos de partida, a validar.

- **RNF1** A geração pode demorar, com meta de até 10 minutos, mas não pode travar o site.
- **RNF2** Cada vídeo aceita de 5 a 30 fotos, de até 10 MB cada.
- **RNF3** O sistema suporta várias imobiliárias; meta do primeiro ano: de 5 a 20 imobiliárias e algumas centenas de anúncios.
- **RNF4** Uma imobiliária nunca acessa dados de outra (isolamento entre clientes).
- **RNF5** Os dados da imobiliária são armazenados com segurança e em conformidade com a LGPD.
- **RNF6** O custo de GPU e armazenamento por vídeo deve ser medido, pois define o preço do serviço.
- **RNF7** O vídeo não pode alterar a aparência real do imóvel: nada de objetos inventados ou cômodos modificados. Qualquer uso de IA generativa fica restrito às transições, é configurável e documentado nos termos de uso.
- **RNF8** A imobiliária declara ter autorização para usar as fotos enviadas.
- **RNF9** O motor de geração de clipes é substituível (parallax, reconstrução 3D etc.) sem alterar o restante do sistema.

## Fora do escopo por enquanto

- Mapa 3D da cidade (fase posterior)
- Vitrine pública por imobiliária
- Tour navegável em tempo real
- Sol por horário
- Formulário de leads e relatório de contatos
- Cobrança automatizada e cadastro público (no início as contas são criadas manualmente)

## Fases

0. **Protótipo de validação:** 2 cômodos e 1 transição, rodando num script isolado, para decidir se o resultado "parece uma visita".
1. **Núcleo do gerador:** pipeline completo (classificação, clipes, transições, pós-produção) como módulo com contrato simples: fotos entram, MP4 sai.
2. **Plataforma:** API, painel da imobiliária, upload, fila e worker, armazenamento.
3. **Qualidade:** reconstrução 3D como motor alternativo de clipe, transições mais elaboradas, guia de captura de fotos para o cliente.
4. **Mapa 3D:** pins nos imóveis que abrem o vídeo do anúncio.

## Decisões de arquitetura (a registrar como ADRs)

- **Foco no gerador de vídeo**, não em vitrine ou marketplace. Motivo: imobiliárias já têm canais de divulgação, e o vídeo é o que elas não têm.
- **Motor de clipe plugável**, com fallback: reconstrução 3D quando as fotos permitem, parallax 2.5D quando não. Isola o risco técnico.
- **Geração assíncrona** em worker separado da API.
- **Multi-tenant desde o início:** toda tabela relevante carrega o identificador da imobiliária.
- **Monolito modular:** um único backend com módulos bem separados, sem microserviços.
- **Sem IA generativa no conteúdo dos cômodos**, para evitar propaganda enganosa.

## Decisões em aberto

- Qual método de profundidade e de reconstrução usar (a decidir pelo protótipo).
- Como fazer a transição entre cômodos quando não há foto de corredor ou porta.
- Onde rodar a GPU em produção (máquina própria, nuvem sob demanda, serviço terceirizado) e quanto custa por vídeo.
- Modelo comercial: preço por vídeo ou assinatura mensal.
- Validação de mercado: conversar com 3 a 5 imobiliárias pequenas com um vídeo de exemplo.

## Primeira tarefa: protótipo

1. Reunir fotos de dois cômodos conectados.
2. Estimar profundidade (por exemplo, Depth Anything V2) e gerar um clipe de câmera por cômodo.
3. Fazer a passagem entre os dois com avanço em direção à abertura e desfoque de movimento.
4. Aplicar correção de cor, tremor leve e música com FFmpeg.
5. Avaliar o resultado de cerca de 15 segundos: parece uma visita de verdade?