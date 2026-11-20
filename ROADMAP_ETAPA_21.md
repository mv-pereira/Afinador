# Afinador — Roadmap da Etapa 21

## Arquitetura binária de armazenamento e intercâmbio de dados acústicos

**Data de referência:** 19/11/2026  
**Estado:** planejamento; nenhuma subetapa 21 implementada ou aprovada.  
**Versão de partida:** Etapa 20.11, `index.html` autocontido.  
**Repositório:** `https://github.com/mv-pereira/Afinador` — aplicação em `https://mv-pereira.github.io/Afinador/`.  
**Escopo:** persistência, intercâmbio, interoperabilidade, memória e segurança; não é uma revisão dos algoritmos acústicos.

Este documento foi elaborado para servir de referência autossuficiente caso a conversa de desenvolvimento seja perdida. Ele registra a motivação, as decisões já tomadas, os resultados experimentais, as hipóteses ainda abertas, a sequência de implementação, os entregáveis e os critérios para avançar de uma subetapa à seguinte. Não representa uma implementação concluída.

## 1. Contexto e motivação

O Afinador é uma aplicação web autocontida em um único HTML, com processamento acústico local, afinador em tempo real, analisador de parciais, aquisição de múltiplas execuções, estimação de inharmonicidade, perfis instrumentais, sintetizador e ferramentas de curvas de afinação. É particularmente importante que funcione em dispositivos móveis e sem dependências de rede depois que a página estiver disponível.

Nas etapas anteriores, o analisador passou a preservar medições detalhadas de frequência, amplitude, SNR, estabilidade temporal, atribuições de ordens, espectros, diferentes tentativas de ajuste, coeficientes físicos e diagnósticos das execuções. Esses registros são úteis tanto para o usuário consultar uma sessão quanto para a investigação científica independente, inclusive por meio do envio de arquivos ao ChatGPT e análise em Python. O objetivo é preservar essa riqueza, não reduzi-la para obter arquivos menores.

### 1.1. Escala do problema

Um cravo com 52 notas em cada um dos registros de 8′ e 4′ pode exigir 104 sessões (assumindo uma sessão por corda). Sessões recentes com 13–14 execuções ocupam aproximadamente 3–4 MB em JSON formatado. Logo, 104 × 3,5 MB ≈ 364 MB. Usando os três registros reais mais recentes como amostra, a projeção é ainda maior: aproximadamente 398 MB. Esses valores não são uma medição de um instrumento inteiro e podem aumentar com novas aquisições, múltiplas sessões por corda ou mais execuções por sessão.

| Sessão real | Execuções registradas | JSON original (bytes) |
|---|---:|---:|
| Cravo, Red Brass, Si1 | 13 | 3.805.795 |
| Cravo, Yellow Brass, Si2 | 13 | 4.101.191 |
| Cravo, Iron, Si3 | 14 | 3.580.322 |

A gravação local também preserva a sessão completa. O tamanho físico do IndexedDB não equivale necessariamente ao tamanho de um JSON, pois o navegador pode adotar representações de armazenamento próprias. Não confundir espaço persistente com heap JavaScript ou memória total do processo.

### 1.2. Problema mais grave: materialização integral do perfil

Na Etapa 20.11, o banco de perfis é `afinador-acoustic-profiles-v1`, versão 1, com stores `profiles` e `sessions`. O código de perfis utiliza, entre outras operações:

```js
r.index('profileId').getAll(profile.profileId, 2001)
```

A ponte `curveRead(pid)` também lê os registros completos do perfil via `getAll(pid,2001)`. Há operações semelhantes na importação/mesclagem. A auditoria detalhada deve examinar todos os consumidores e os caches, incluindo o sintetizador. O banco `afinador-curvas-experimentais-v1` mantém versões de curvas em `curveVersions`.

Essa arquitetura implica materialização simultânea de muitos objetos grandes, potencialmente acompanhada de cópias, serialização, verificação de hashes e estruturas derivadas. O custo tende a crescer com a quantidade de sessões. Há limites de segurança de 32 MiB (`32*1024*1024`) em módulos de importação/exportação e validação: o arquivo de perfil integral pode ultrapassá-los antes de completar o instrumento. Não resolver isso apenas elevando o limite.

### 1.3. Evidência experimental de consumo de RAM

Teste anterior em Chromium 144, com cópias independentes das sessões reais e medição do heap após coleta de lixo (baseline de 23.587.004 bytes):

| Sessões simultaneamente carregadas | Heap adicional aproximado |
|---:|---:|
| 1 | 1,47 MiB |
| 52 | 74,34 MiB |
| 104 | 148,70 MiB |
| Após liberação | praticamente zero |

O teste não representa memória residente total, buffers externos, GPU, memória linear WASM, buffers transitórios de exportação ou DSP. Não foi feito em celular físico. Ele demonstra a necessidade de carregamento seletivo, mesmo com compressão eficiente do arquivo.

### 1.4. DPX já removido; preservar a mediana

Na Etapa 20.11 foi removida a visualização de densidade DPX por decisão de uso, não para reduzir tamanho de arquivos. O histograma de densidade era construído durante a exibição, e não constituía um bloco persistido independente. `spectrumGrid202` permanece porque também é necessário ao espectro mediano consolidado. A grade é logarítmica, com até 4.096 células, valores inteiros quantizados em décimos de dB. O validador atual restringe os valores a −1600…0. A nova arquitetura não deve excluir esse campo nem reduzir sua resolução. Preservar `spectrumGrid202()`, `resumirEspectro14()`, `spectrumSource202()` e a mediana calculada por `buildSpectrum202()`/`drawConsolidated202()`, salvo adaptações estritamente de acesso aos dados. Não reintroduzir DPX ou P25–P75 na interface.

## 2. Decisões e invariantes

### 2.1. Decisões do projeto

- Criar uma Etapa 21 independente, dividida em **12 subetapas (21.1–21.12)**, com entregas incrementais e validação antes de avançar.
- Preservar o sistema atual de JSON e IndexedDB durante o desenvolvimento. Usar a Etapa 20.11 como baseline funcional; não sobrescrever os dados antigos.
- Adotar formato binário conhecido e publicamente documentado, não um formato opaco inventado de raiz. Não exigir legibilidade humana do arquivo final.
- Garantir leitura independente em Python, para que a investigação acústica possa continuar a partir dos arquivos enviados, sem depender de extrair dados do HTML.
- Manter todas as informações atualmente preservadas, inclusive diagnósticos experimentais; compressão sem perdas. Não acrescentar gravação de PCM ou áudio original.
- Manter o HTML autocontido, com todos os recursos de produção incorporados, funcionamento local e licenças de terceiros documentadas. Os arquivos auxiliares não serão dependências obrigatórias do funcionamento normal.
- Não manter indefinidamente dois sistemas completos no HTML. Não exigir migração universal de todos os esquemas históricos do IndexedDB. Preservar a possibilidade de backup e conversão dos JSONs exportados antes de qualquer retirada do legado.
- Não realizar gravação dupla obrigatória. Usar persistência paralela em casos explícitos de validação; não pagar o custo de armazenar toda medição em ambos os formatos por padrão.

### 2.2. Invariantes acústicos e de segurança

A etapa não autoriza mudanças em YIN, pYIN, SWIPE′, FFT, aquisição de áudio, seleção de janelas, atribuição de parciais, estimação de B, estabilidade, consolidação, temperamentos, síntese ou otimização de curvas. Preservar resultados, flags, critérios de validação, revisões, hashes semânticos quando existentes e o significado de cada unidade. Não utilizar a mudança de formato para aprovar curvas experimentais que hoje estão bloqueadas, promover B provisório a validado, confirmar notas não vinculadas ou relaxar vetos físicos. A investigação sobre descritores gerais de inharmonicidade fica fora desta etapa.

Nenhuma abertura desnecessária de banco, carga do codec ou alocação volumosa durante afinação normal. Nenhum trabalho de compressão síncrono bloqueante no caminho crítico do áudio. Não alterar a política CSP sem necessidade; recalcular hashes dos scripts editados e testar a política real, inclusive Workers e eventual WASM, sem recorrer indiscriminadamente a `unsafe-eval`, recursos remotos ou enfraquecimento de controles. Não confundir SHA-256 com assinatura criptográfica de autoria: hash detecta corrupção, não autentica por si só o remetente.

## 3. Evidência dos benchmarks já realizados

### 3.1. Premissas e rastreabilidade

Os testes preliminares utilizaram três JSONs das cordas Malcolm Rose, em Linux (AMD EPYC, Python 3.13.5, Zstandard 1.5.7) e Chromium 144. Compararam JSON compacto, MessagePack e CBOR, todos sem perdas. Os números abaixo foram conferidos nos CSVs já produzidos: 3 sessões × 3 formatos × 12 configurações (incluindo sem compressão) = 108 configurações. A maioria dos testes Python teve três repetições; níveis mais custosos tiveram menos. CBOR experimental em Python, MessagePack otimizado em código nativo: os tempos não são uma comparação intrínseca entre padrões. Os arquivos comprimidos foram reportados com recuperação integral dos dados; repetir a validação com o codec de produção e testes independentes.

MB = 10⁶ bytes; MiB = 2²⁰ bytes. Projeção de tamanho = média das três sessões × número de sessões, excluídos overhead de banco, manifesto, contêiner, duplicações/revisões e metadados adicionais. Não extrapolar tempos do computador para o celular sem medir.

### 3.2. Projeção de armazenamento para 104 sessões (MB)

| Compressão | JSON compacto | MessagePack | CBOR |
|---|---:|---:|---:|
| Nenhuma | 169,46 | 124,42 | 124,35 |
| GZIP 1 | 49,74 | 41,59 | 41,48 |
| GZIP 6 | 41,39 | 37,55 | 37,44 |
| GZIP 9 | 40,97 | 37,47 | 37,37 |
| Brotli 4 | 31,70 | 30,97 | 30,94 |
| Brotli 6 | 31,25 | 26,50 | 26,52 |
| Brotli 9 | 30,60 | 26,29 | 26,32 |
| Brotli 11 | 24,16 | 23,84 | 23,96 |
| Zstandard 1 | 35,60 | 34,94 | 34,87 |
| Zstandard 3 | 35,64 | 29,22 | 29,18 |
| Zstandard 9 | 31,82 | 27,83 | 27,84 |
| Zstandard 15 | 30,94 | 27,51 | 27,52 |

JSON original formatado: cerca de 398,23 MB. CBOR + Zstandard 3: cerca de 281 kB/sessão, 14,59 MB/52, 29,18 MB/104, 58,36 MB/208 e 84,17 MB/300; economia estimada de 92,7% frente ao original. O melhor tamanho absoluto não é o único critério: usar latência, RAM, interoperabilidade e complexidade de distribuição.

### 3.3. CBOR: compressão, latência e memória puramente exploratórias

| Configuração | Compressão mediana (ms) | Preparação gravação (ms) | Preparação leitura (ms) | RSS adicional gravação (MiB) |
|---|---:|---:|---:|---:|
| GZIP 6 | 24,88 | 80,98 | 74,41 | 4,18 |
| Brotli 6 | 24,87 | 80,40 | 71,04 | 12,12 |
| Brotli 11 | 1753,48 | 1806,43 | 83,21 | 27,56 |
| Zstandard 3 | 4,38 | 66,07 | 77,26 | 5,07 |
| Zstandard 9 | 17,07 | 81,42 | 80,55 | 14,25 |
| Zstandard 15 | 103,35 | 175,74 | 87,10 | 35,96 |

RSS medido em processos Python independentes; não corresponde ao heap JS ou à memória linear WASM. Tempos não incluem I/O de IndexedDB. O custo adicional do nível 9, para economizar apenas cerca de 1,34 MB por instrumento de 104 sessões, não parece justificável como padrão.

### 3.4. Benchmark preliminar no navegador

Cinco medições por formato/corda após aquecimento, usando o codec experimental e `CompressionStream('gzip')`:

| Indicador | JSON + GZIP | CBOR + GZIP |
|---|---:|---:|
| Tamanho mediano comprimido | 394 kB | 358 kB |
| Serialização | 13,9 ms | 50,2 ms |
| Compressão | 57,6 ms | 37,4 ms |
| Descompressão | 7,6 ms | 6,3 ms |
| Desserialização | 8,5 ms | 13,0 ms |
| Preparação para gravação | 70,7 ms | 89,1 ms |
| Preparação para leitura | 16,9 ms | 23,4 ms |

No Chromium usado, GZIP e Deflate foram aceitos pela API nativa, Brotli e Zstandard não. Isso é uma observação do navegador testado, não uma regra universal de compatibilidade. O suporte efetivo deve ser testado nos navegadores-alvo. Ainda não foi medido o Zstandard WASM que entraria em produção, nem o CBOR RFC 8746 com vetores tipados em todas as estruturas, nem o pico real de memória em dispositivo móvel.

## 4. Arquitetura-alvo proposta (consolidar em 21.2–21.3)

| Componente | Candidato principal | Alternativa / decisão pendente |
|---|---|---|
| Serialização | CBOR (RFC 8949) | MessagePack, se benchmark/complexidade recomendar |
| Vetores tipados | CBOR tags RFC 8746 | Uso seletivo, validar compatibilidade |
| Compressão | Zstandard nível 3 (RFC 8878), implementação WASM autocontida | GZIP nativo, configuração efetiva documentada; Brotli em teste comparativo |
| Banco local | IndexedDB, novo schema separado | Não introduzir outro motor sem justificativa |
| Contêiner de perfil | ZIP modular, entradas independentes já comprimidas, método STORE | Alternativa só se testes mostrarem vantagem clara |
| Especificação | CDDL (RFC 8610) + documentação semântica | Consolidar após escolha do codec |
| Integridade | SHA-256 de blocos + validação de vínculos/manifests | Não depender exclusivamente de CRC ZIP |
| Execução | Worker dedicado ao armazenamento, filas limitadas | Definir suporte a transferência e cancelamento |

CBOR e MessagePack têm tamanhos praticamente equivalentes. A preferência por CBOR decorre de padronização formal e vetores tipados, não de superioridade demonstrada em compressão. CBOR + Zstandard 3 é candidato, não decisão irreversível. Não prometer suporte nativo de Zstandard ou Brotli sem verificar cada navegador. Evitar Base64 em IndexedDB e arquivos: usar `ArrayBuffer`, arrays tipados ou `Blob`; se a biblioteca precisar ser incorporada no HTML como Base64, contabilizar overhead somente no HTML e não nas medições.

### 4.1. Camadas lógicas e unidades de leitura

1. **Metadados do perfil:** instrumento, layout, registros, teclas, vínculos, revisão do perfil e referências de integridade.
2. **Índice de sessões:** chaves de perfil, registro, corda/nota, sessão/revisão, B e estado de validade quando aplicável, referência, cobertura/qualidade, datas, tamanho, localização dos blocos. Deve ser pequeno e paginável.
3. **Projeções acústicas de leitura:** frequências e amplitudes necessárias ao sintetizador e dados necessários a curvas/auditoria. Derivadas dos dados visíveis e versionadas, nunca uma segunda fonte independente de verdade. Validar a associação à sessão/revisão/hash de origem; evitar duplicação volumosa de FFT e diagnósticos.
4. **Evidência completa:** sessão com todas as execuções, espectros, picos, candidatos, diagnósticos, tentativas, agregação, configurações e histórico já existentes. Unidade independente comprimida; caso uma sessão possa ser muito grande, definir sub-blocos limitados e manifesto da sessão.
5. **Curvas:** versões, frequências-alvo, contexto e proveniência; aplicação normal deve depender apenas do artefato consolidado necessário, não de carregar sessões de todo o instrumento.

A interface de repositório deve fornecer operações conceituais de listagem paginada de perfis/sessões, obtenção de índice/resumo, leitura de projeção acústica, leitura da evidência de uma sessão, gravação/atualização/exclusão atômicas, iteração limitada e exportação/importação. Os nomes de métodos serão definidos após a auditoria. Não usar `getAll` sobre evidências completas em caminhos de produção. Chaves pequenas e índices podem ser lidos em páginas limitadas.

### 4.2. Representação e precisão

- Grade espectral já quantizada: `Int16Array` (faixa atual −1600…0), sem alterar escala, comprimento ou valores.
- Ordens e índices: inteiros sem sinal quando o domínio permitir, dimensionados pelo máximo validado, sem truncamento silencioso.
- Frequências, amplitudes de precisão dupla, B, resíduos, demais resultados físicos: preservar Float64 e os valores efetivamente representados no JS. Não converter automaticamente para Float32.
- Identificadores, enums, textos Unicode, booleanos, `null`, campos opcionais e estruturas aninhadas: preservar significado e distinção entre ausência e valor nulo. Definir política de números não finitos, inteiros acima de 2⁵³−1, zeros com sinal e chaves duplicadas antes da implementação.
- Definir tags RFC 8746 permitidas, endianness explícita, validação de alinhamento e limites. Comparar objetos semanticamente e, para floats, testar bits quando apropriado. Não depender de igualdade de texto JSON (indentação e ordem de chaves não são dados acústicos).

### 4.3. Arquivos e documentação de intercâmbio

Extensões propostas: `.afs` (sessão acústica), `.afp` (perfil), `.afc` (curva). Extensão não basta para reconhecer conteúdo: especificar magic/envelope, versão maior/menor, tipo, codec, comprimento comprimido e descomprimido, identificadores, hashes e regras de rejeição. O contrato não será finalizado antes da etapa 21.3.

O perfil será um contêiner modular com manifesto e sessões independentes, com nomes de entradas seguros e determinísticos, sem caminhos absolutos ou travessia de diretório. ZIP não deve recomprimir blocos Zstandard: método STORE evita trabalho redundante. O manifesto associa cada entrada a IDs, revisão, tamanho e hash; o índice não deve carregar o espectro completo. Definir acesso aleatório, limites de entradas, ZIP64 caso necessário e política de duplicatas. O formato da curva deve preservar sua identidade e validação existente. Não depender de bibliotecas proprietárias nem de código executável embutido em dados importados.

Uma implementação independente em Python deverá ser capaz de listar, inspecionar, validar, extrair uma sessão, reconstruir dados acústicos e converter para JSON legível. O arquivo binário será dado, não programa executável; o significado dos campos deve estar em `SCHEMA.md` e nos esquemas versionados.

### 4.4. Estratégia de memória e consistência

Meta arquitetural: `RAM ≈ base + índice paginado + sessões/projeções em uso + buffers limitados do codec`, e não proporcional a todas as evidências descompactadas do perfil. A lista de índices ainda cresce com o número de entradas, mas muito mais lentamente que o conteúdo integral.

- Cache limitado por **bytes** e quantidade de blocos, política LRU ou equivalente; liberar referências em troca de ferramenta, sessão, perfil, cancelamento, erro e encerramento de Worker.
- Fila com backpressure, concorrência baixa (inicialmente uma sessão por vez), transferência de buffers quando segura, sem `structuredClone` volumoso desnecessário. Não transferir/destacar buffers que o DSP ainda usa.
- Compressão/validação fora de transações IndexedDB longas; preparar blocos e commit atômico de índice, projeções e dados. Não manter transação esperando Worker ou rede. Sucesso só após commit. Controle de revisão para concorrência entre abas; tratar `versionchange` e bloqueio.
- Importações de perfis grandes: staging invisível com journal/IDs de geração; validar todos os blocos antes de publicar via commit pequeno de manifestação ativa. Em falha, manter perfil anterior, descartar ou recuperar staging de forma explícita. Não depender de uma transação aberta durante toda a descompressão. Exclusão com tratamento de órfãos e integridade referencial.
- Exportação: ler/escrever incrementalmente. Não materializar o conjunto ao fazer hash, ZIP ou serialização. Se o navegador não permitir escrita diretamente em stream para arquivo, usar fallback Blob calculado com teto explícito e contabilizar seu pico; oferecer exportação por sessão/lotes quando o teto for excedido. Exportação não pode alterar conteúdo original.
- Definir cotas para tamanho comprimido e descomprimido por bloco/sessão, perfil, total de registros, estruturas, profundidade, quantidade de operações e tempo. O limite antigo de 32 MiB não deve ser simplesmente retirado; substituí-lo por limites calibrados de granularidade adequada. Solicitar persistência do navegador quando disponível e por ação apropriada, consultar estimativa de quota, tratar `QuotaExceededError`, avisar sobre backups. IndexedDB não é garantia de permanência.

## 5. Roadmap de implementação — 12 subetapas

Regras gerais de entrega: cada subetapa deve indicar versão de entrada, arquivos modificados, motivo das alterações, testes executados com evidência, testes não executados, limitações, instruções de uso e condição de rollback. Entregar `index.html` autocontido atualizado quando houver mudança de aplicação (não apenas um patch). Documentar novos arquivos em seu caminho no repositório. Não avançar sem verificar os critérios da subetapa anterior; se um critério depende de celular físico, registrar como pendente e não alegar aprovação. Não alterar simultaneamente algoritmos acústicos para facilitar um teste de armazenamento.

### 21.1 — Auditoria arquitetural e mapeamento de dependências

**Objetivo:** saber exatamente quais dados são gravados, consumidos, validados e duplicados antes de modificar a aplicação.

**Implementação/levantamento:**
- Inventariar todas as chamadas `indexedDB.open`, transações, stores, índices, `getAll`, leitura por ID, imports/exports, JSON stringify/parse, clones, hashes e limites. Mapear fluxos das ferramentas, callbacks, eventos entre módulos, caches e Workers. Classificar cada acesso por nível de dados necessário e ciclo de vida.
- Medir tamanhos por estrutura, seção e sessão; identificar duplicações reais, sem eliminar dados nesta subetapa. Revisar consumidores de `spectrumGrid202`, revisões, diagnósticos físicos e campos opcionais históricos.
- Identificar módulos existentes (incluindo `SECURITY13`, `AfinadorPerfis3`, ponte `curveRead`, auditoria de curvas e aplicação) e contratos que exigem compatibilidade semântica. Documentar dependências do sintetizador e interface de seleção de curvas.
- Definir baseline funcional e de memória, fixture representativa e cenários de regressão. Separar falhas já existentes de regressões novas.

**Entregáveis:** `docs/ROADMAP_ETAPA_21.md`, `docs/AUDITORIA_ARQUITETURAL.md`, `docs/MAPA_DE_DEPENDENCIAS.md`, baseline e hashes. HTML inalterado.

**Aceitação:** todos os caminhos relevantes identificados por evidência de código, mapa de leitura/escrita e plano de teste suficiente para implementação; nenhum consumidor desconhecido tratado como descartável.

### 21.2 — Benchmark final em JavaScript/WASM

**Objetivo:** escolher conscientemente os codecs que serão realmente incorporados ao HTML.

**Implementação/testes:**
- Benchmark com JSON nativo, CBOR e MessagePack selecionando implementações mantidas, licenças permissivas compatíveis e versões fixadas. Comparar arrays comuns e vetores tipados. Usar as 13 sessões para correção e as três recentes como referência de desempenho, incluindo outras de tamanho extremo.
- GZIP (nativo e/ou biblioteca), Brotli e Zstandard (principalmente níveis 1, 3 e 9). Medir inicialização fria/aquecida, serialização, compressão, leitura, descompressão, validação, tamanho e custo de I/O; medir tamanho do HTML, WASM e memória linear/externa, cópias e liberação de buffers. Testar custos de Worker/transferência. Comparar com JSON + GZIP, evitando concluir superioridade por benchmark de implementações desiguais.
- Benchmark com buffers/streams reais, execução em Worker, CSP e offline; navegadores Chromium/Firefox/WebKit disponíveis, testar Android/iOS reais quando possível. Usar detecção de capacidade, não inferir por user agent. Medir mediana, p95 ou distribuição, repetições, hardware/versão, baseline e limites do método. Separar pico de heap, memória externa e RSS quando disponíveis.
- Decidir codec primário e alternativa: se Zstandard WASM for viável, preferir nível 3; se não, considerar CBOR + GZIP. Se múltiplos codecs de intercâmbio forem aceitos, documentar todos e implementar decodificação compatível; nunca trocar silenciosamente para um codec que o destinatário não consegue ler.

**Entregáveis:** `benchmarks/benchmark.html`, `benchmarks/benchmark.py`, CSVs e `docs/BENCHMARK_FINAL.md` com matriz de decisão, versões/licenças e protocolo móvel. Protótipo isolado, sem mudança no afinador de produção.

**Aceitação:** round-trip sem perdas nos dados testados; escolha fundamentada pelo desempenho, memória, tamanho, compatibilidade, segurança e manutenção. Se mobile não estiver testado, escolha provisória com gate explícito antes do corte definitivo.

### 21.3 — Especificação formal do formato binário

**Objetivo:** fixar contrato independente da implementação atual do HTML.

**Implementação:**
- Definir envelope e formato de `.afs`, `.afp`, `.afc`, regras de versão, magic, flags, codecs, comprimentos, hashes, esquema dos contêineres, identificação de sessões e suas revisões. Separar versão do contêiner, versão do schema semântico e versões dos motores acústicos.
- Documentar campos, tipos, unidades, presença/ausência, limites, tags binárias, floats, referências entre objetos e semântica de qualidade, calibração e elegibilidade. Distinguir esquema de transporte e objetos equivalentes do legado.
- Especificar regras de canonicalização/determinismo para hashes, sem alterar hashes semânticos já necessários; rejeição de chaves duplicadas, versões desconhecidas, campos críticos não reconhecidos, números e tipos inválidos. Limites para ZIP, descompressão e alocação antes de aceitar dados.
- Definir contrato de compatibilidade futura (versão maior incompatível, evolução aditiva quando prevista), sem prometer suporte automático a todo schema antigo. Publicar exemplos mínimos e golden fixtures com checksums.

**Entregáveis:** `docs/FORMATO.md`, `docs/SCHEMA.md`, `docs/VERSIONAMENTO.md`, `docs/SEGURANCA_FORMATO.md`, `schemas/session.cddl`, `schemas/profile.cddl`, `schemas/curve.cddl` e esquemas auxiliares de envelope/manifesto conforme necessário. Se CBOR não for escolhido, usar linguagem de esquema equivalente documentada.

**Aceitação:** duas implementações independentes podem interpretar o formato a partir da especificação; todos os tipos encontrados nos dados reais mapeados, sem ambiguidade de bytes, unidades, limites ou integridade.

### 21.4 — Codificador e decodificador binário

**Objetivo:** serialização isolada, ainda sem substituir a persistência.

**Implementação:** módulo de encode/decode no HTML, correspondência entre objetos existentes e tipos binários; vetores tipados nos campos aprovados, conversão de volta fiel quando consumidores legados exigirem arrays comuns. Validação estrita de input antes e depois do codec. Limites de profundidade, tamanhos, chaves e alocação; não construir protótipos perigosos ao decodificar mapas. Não modificar objetos de aquisição em uso.

**Entregáveis:** `index.html` com módulo experimental isolado, testes de round-trip e fixtures de conformidade; atualização da documentação e schema se houver necessidade justificada.

**Aceitação:** as 13 sessões completas são convertíveis sem perda de estrutura semântica nem valores; diferenças históricas de schema devem ser tratadas como fixtures de codec, não como autorização para importação de todos os formatos antigos em produção. Testar Unicode, nulos, opcionais, números extremos válidos, arrays tipados, truncamento e entradas malformadas. Legado funciona sem carregar o codec na afinação normal.

### 21.5 — Compressão e Worker de armazenamento

**Objetivo:** criar o pipeline binário completo por sessão, fora do DSP.

**Implementação:** incorporar biblioteca versão fixa/licenciada, inicialização sob demanda, contrato Worker (IDs de requisição, versão, operação, resultado/erro, cancelamento), compressão e descompressão limitadas, hash, tamanho declarado versus real, timeout e liberação de memória. Testar memória linear WASM e estratégia de reutilizar ou encerrar Worker. Verificar CSP efetiva e operação offline. Evitar concatenar buffers gigantes ou gerar Base64 intermediário para dados persistidos. Reservar/tetar saída antes da descompressão; limitar janelas de Zstandard e demais parâmetros perigosos.

**Entregáveis:** `index.html`, testes codec/compressão/integridade, licenças e relatório 21.5. Binário operacional em modo de teste, JSON ainda principal.

**Aceitação:** recuperação integral e interoperabilidade com decodificador de referência para todas as fixtures aprovadas; corrupção, truncamento, bomb e codec desconhecido falham com mensagem clara e sem comprometer UI/áudio; sem regressão permanente de RAM após ciclos repetidos.

### 21.6 — Ferramentas científicas independentes em Python

**Objetivo:** antecipar interoperabilidade para utilizá-la nas próximas validações.

**Implementação:** CLI independente da aplicação com parser rigoroso e limites equivalentes. Leitura de manifesto/índice sem materializar perfil completo; extração seletiva, iteração por sessão, validação, codificação e conversão sem perdas. Especificar requisitos, versão mínima de Python, dependências fixadas/testadas e licenças. Não executar conteúdo importado. Gerar JSON legível opcional para pesquisa; não exigir que todo perfil seja convertido em um único arquivo enorme.

| Arquivo | Função |
|---|---|
| `tools/codec.py` (ou módulo de pacote) | Núcleo compartilhado de serialização, compressão, envelope e limites |
| `tools/encode.py` | Codificar dados de entrada compatíveis |
| `tools/decode.py` | Decodificar arquivo ou sessão selecionada |
| `tools/inspect_file.py` | Enumerar metadados, sessões, revisões, codecs e tamanhos |
| `tools/validate.py` | Validar estrutura, hashes, tamanhos e referências |
| `tools/convert.py` | Converter JSON exportado ↔ formato novo |
| `tools/requirements.txt` | Dependências reproduzíveis |
| `tools/README.md` | Instalação, comandos, exemplos e limites |
| `tests/test_codec.py` | Testes de conformidade e equivalência |

`inspect_file.py` é o nome recomendado em lugar do `inspect.py` inicialmente sugerido, para evitar sombrear o módulo `inspect` da biblioteca padrão do Python. A interface definitiva da CLI será documentada; exemplos conceituais:

```bash
python tools/decode.py medicao.afs --output medicao.json
python tools/inspect_file.py cravo.afp
python tools/validate.py cravo.afp
```

**Aceitação:** JavaScript → Python e Python → JavaScript, inclusive vetores tipados, hashes, compressão e casos negativos. Fixtures geradas independentemente, não apenas pelo mesmo codificador. Para perfis e curvas, testes de contêiner com fixtures provisórias nesta fase e completos depois da 21.10. Vínculos e precisão mantidos. A ferramenta funciona sem importar o HTML.

### 21.7 — IndexedDB modular e coexistência experimental

**Objetivo:** colocar a nova persistência em funcionamento sem comprometer dados antigos.

**Implementação:** novo banco/schema separado, stores de metadados, índice, projeções, evidências binárias e curvas, conforme auditoria; índices por perfil, sessão/revisão, corda, registro ou nota, conforme aplicável. Repositório assíncrono, escrita atômica, staging, revisão, detecção de conflitos, exclusão e limpeza de órfãos. Tratar quota, transações abortadas, múltiplas abas, falha de Worker e banco indisponível. Estados/proveniência dos dados preservados. Expor modo experimental explicitamente, sem gravar duas cópias por padrão. Não apagar/migrar banco antigo.

**Entregáveis:** `index.html`, `docs/ARQUITETURA_ARMAZENAMENTO.md`, testes de banco e rollback; mapa da versão do banco e política de atualização.

**Aceitação:** salvar, fechar, reabrir, ler, atualizar e excluir uma sessão no backend novo; estado consistente após falhas simuladas; banco legado inalterado. Índice e evidência correspondem à mesma revisão; nenhum resumo aponta para bloco inexistente.

### 21.8 — Carregamento sob demanda e gerenciamento de memória

**Objetivo:** resolver a causa principal da preocupação com RAM.

**Implementação:** paginação, leitura seletiva, cache com teto de bytes, cancelamento de buscas antigas, descarte de referências, LRU ou equivalente, filas limitadas e proteção contra repetidas cópias. Separar apresentação de índices das leituras pesadas; não obter evidências de outras cordas por mera navegação. Medir live heap, buffers, WASM, I/O, lecturas e quantidade de sessões materializadas; adicionar telemetria de teste local, sem enviar dados ou coletar áudio. Definir política de invalidação por revisão e quando ferramentas se fecham.

**Entregáveis:** `index.html`, testes de carga/cache e relatório de memória 21.8. Limites e métricas documentados.

**Aceitação:** abrir/listar 52, 104, 208 e 300 sessões sem decodificar todo o perfil. Inspecionar sessão e comparar conjunto limitado conforme ação do usuário. Conteúdo pesado carregado proporcionalmente ao conjunto ativo; não crescer linearmente com todo o perfil. Verificar por contagem de fetch/decode e medição real, não somente pelo tamanho do arquivo. Repetir abertura/troca/fechamento sem crescimento acumulativo fora do cache.

### 21.9 — Integração com todas as ferramentas

**Objetivo:** substituir os caminhos de acesso aos dados, mantendo a semântica acústica.

| Ferramenta | Dados a solicitar |
|---|---|
| Afinador | Curva/frequências-alvo selecionadas; nenhum conjunto integral de evidências |
| Curvas de afinação | Projeções acústicas estritamente necessárias, validadas, com proveniência |
| Sintetizador | Frequências, amplitudes e demais dados realmente usados na síntese |
| Perfis instrumentais | Índices e resumos; sessão completa só quando solicitada |
| Análise de parciais | Evidência da sessão em revisão, espectro mediano e dados individuais |
| Exportação científica | Evidências completas, processamento incremental |

**Implementação:** adaptar os consumidores levantados em 21.1 ao repositório. Auditar seleção/atualização de curva, alterações de temperamento, troca de ferramenta, navegação de perfis, exclusão e revisão. Garantir que projeções derivadas não eliminem informações usadas por auditoria ou pelo otimizador. Preservar as restrições atuais de curvas e o comportamento padrão sem curva aplicada. Comparar outputs com a versão 20.11 sobre os mesmos dados e contextos. Oferecer seleção experimental de backend sem alterar o caminho padrão até aprovação.

**Entregáveis:** `index.html`, matriz de equivalência por ferramenta e documentação atualizada de fluxos.

**Aceitação:** resultado acústico e estado de UI equivalentes; nenhum consumidor carrega todas as evidências sem justificativa; áudio e metodologia de curvas inalterados; uso normal de JSON continua operacional. Testes de regressão e CSP aprovados.

### 21.10 — Importação e exportação binárias modulares

**Objetivo:** disponibilizar intercâmbio completo em modo experimental, mantendo exportação/importação JSON.

**Implementação:** exportar/importar `.afs`, `.afp`, `.afc`; manifesto, hashes, entradas independentes, paginação e progresso/cancelamento. Receber arquivos em stream ou leitura seletiva quando suportado, impor teto para fallback. Rejeitar entradas duplicadas/ambíguas, travessia, compressão maliciosa, hashes inconsistentes, versões/codec desconhecidos, tamanhos inválidos e conflitos. Estágio invisível de importação com publicação atômica e recuperação de falha. Documentar condução de conflitos (importar como novo, restaurar ou recusar, conforme contrato) sem misturar evidências de revisões diferentes. Verificar que arquivos gerados pelo Python podem ser importados pelo app e vice-versa; testar restauração de backup.

**Entregáveis:** `index.html`, ferramentas Python completas para os três tipos, exemplos de arquivo, fixtures, documentação de backup e protocolos de recuperação.

**Aceitação:** ida e volta do perfil inteiro e de uma sessão/curva preserva dados, referências e validações. Exportação não carga integralmente o perfil descompactado; importação parcial/cancelada jamais publica perfil incompleto. Verificação de um bloco não depende de reconstruir todos os outros objetos. Exportação JSON continua disponível para comparação.

### 21.11 — Validação, segurança e escalabilidade

**Objetivo:** estabelecer evidência para decidir se a nova arquitetura pode substituir a antiga.

**Matriz mínima:** 13 sessões históricas de codec, dois JSONs individuais de parciais quando compatíveis com o escopo, sessões novas reais de 20.11 ou do protótipo, instrumentos simulados com 52, 104, 208, 300 cordas e estresse de 1.000 sessões. Variar quantidade de execuções, registros, tamanhos de evidência, sessões repetidas por corda e notas/associações. Fixtures de repetição devem ser identificadas como sintéticas, não novas medições físicas.

**Testes:**
- Integridade/precisão: round-trip JS↔Python↔JS, comparações de bits Float64 e árvores semânticas, vetores tipados e hashes. Mediana espectral antes/depois, B, atribuição, flags e estados de curvas equivalentes, sem alterações de regras.
- Segurança: arquivos vazios/truncados, magic/versão errados, chaves duplicadas ou perigosas, tipos inválidos, estruturas profundas, descompressão explosiva, ZIP bomb, caminhos perigosos, inteiros extremos, entradas/IDs repetidos, hashes errados, manifesto que aponta para entradas ausentes e tentativa de referência cruzada indevida. Não considerar um hash correto como prova de confiabilidade de entrada.
- Persistência: quota insuficiente, transação abortada, Worker encerrado, página fechada, importação interrompida, abas concorrentes, atualização de revisão, backup e restauração.
- Desempenho: abertura a frio/quente, save/load, inspeção e alternância de 100 ciclos ou amostra definida, import/export de perfil grande, limites de cache, magnitude do heap e buffers, tamanho do HTML, FPS/latência e responsividade durante gravação; medir memória total quando ferramenta permitir. Testar baixa RAM e fallback de arquivo. Instrumentar que afinação normal não abre banco nem inicializa codec desnecessariamente.
- Dispositivos: Chromium, Firefox, WebKit disponíveis e pelo menos celular físico do usuário, com microfone real; testar os navegadores móveis-alvo, offline, temas, telas estreitas, interrupções e recuperação. Teste automatizado de microfone não substitui teste físico.

**Entregáveis:** `docs/RELATORIO_VALIDACAO_21.md`, `docs/PROTOCOLO_TESTES_MOBILE.md`, `tests/test_roundtrip.py`, `tests/test_security.py`, `tests/generate_test_profiles.py`, resultados de navegador/CSV, testes JS de integração e logs relevantes.

**Aceitação:** nenhuma perda ou alteração semântica; sem regressões acústicas e de segurança; perfil de 300 cordas operacional com acesso seletivo; estresse de 1.000 com resultado/limites documentados e falha segura se atingir teto. Medidas móveis aprovadas pelo usuário. Se teste crítico falhar ou ficar pendente, manter sistema legado principal e corrigir/retestar; não saltar para 21.12.

### 21.12 — Transição definitiva e limpeza arquitetural

**Objetivo:** promover o backend novo após validação completa, sem pressupor migração universal do histórico.

**Implementação:** oferecer backup/exportação e verificar restaurabilidade dos dados que o usuário deseja preservar; documentar conversão dos JSONs existentes. Ativar novo backend como principal apenas após concordância explícita e aprovação da 21.11. Desativar caminhos antigos que se tornaram obsoletos, identificando funções compartilhadas antes de remover. Não apagar IndexedDB legado automaticamente; eventual exclusão exige ação consciente e separada. Preservar ferramenta externa de conversão para JSON e documentar opções de rollback, incluindo recuperar HTML 20.11 e dados antigos. Atualizar ajuda, README, guia e licenças. Revisar tamanho final, CSP, Workers, schema, versões e todas as instruções.

**Entregáveis:** `index.html` final autocontido, `README.md`, `GUIA_DE_USO.md` atualizado, documentos e esquemas consolidados, ferramentas Python, testes/fixtures e notas da versão com limitações e recuperação.

**Aceitação:** nova arquitetura é a principal e não requer o legado em operação normal; equivalência, segurança e escalabilidade aprovadas; documentação suficiente para desenvolvedor independente; backup e rollback demonstrados; nenhuma remoção de dependência compartilhada ou alteração acústica incidental.

## 6. Estratégia de transição e rollback

| Período | JSON e IndexedDB legado | Sistema binário |
|---|---|---|
| 21.1–21.3 | Principal; baseline intocado | Auditoria, benchmark e especificação |
| 21.4–21.6 | Principal | Codec e ferramentas independentes, experimentais |
| 21.7–21.8 | Principal | Banco paralelo, gravação opt-in e leitura seletiva |
| 21.9–21.10 | Disponível e principal por padrão | Fluxo completo experimental |
| 21.11 | Referência de equivalência, fallback | Validação e candidato à promoção |
| 21.12 | Desativado como backend principal; dados antigos preservados | Principal após aprovação explícita |

Reversibilidade: em qualquer falha até 21.11, manter ou retornar à versão estável de referência, sem depender de reescrever o banco antigo. Após 21.12, restaurar dados novos a partir de backup e/ou conversão é um procedimento documentado, não uma promessa de que um HTML antigo lerá o formato novo. Não apagar a única cópia de dados para realizar teste. Se um problema surgir no novo codec, pausar a transição e corrigir no mesmo backend experimental. Evitar gravação dupla automática, migração implícita ou coexistência permanente de duas arquiteturas por conveniência.

## 7. Critérios transversais de aprovação

| Critério | Meta/condição |
|---|---|
| Redução de armazenamento | Meta >90% frente ao JSON formatado para corpus de referência; confirmar com codec de produção |
| Precisão | Nenhuma perda adicional; resultados e estruturas semânticas preservados |
| Heap em abertura de perfil | Nenhuma sessão completa descompactada apenas para listar perfil; índices pagináveis |
| Leitura seletiva | Decodificar somente a sessão ou projeções necessárias à operação solicitada |
| Limites de memória | Cache, filas e buffers com tetos explícitos; definir valores numéricos em 21.2/21.3 e confirmar em 21.8/21.11 |
| Perfis grandes | 52, 104, 208 e 300 cordas testadas; teste de estresse de 1.000 sessões documentado |
| Tempo de gravação/leitura | Responsividade e latência medidas no ambiente real; definir orçamento quantitativo a partir do benchmark final, sem prometer tempos de computador em celular |
| Intercâmbio | JS e Python independentes interoperáveis, arquivos modulares versionados |
| Integridade | Hashes, semântica, referências, atomicidade, limites de descompressão e rollback testados |
| Áudio | Nenhuma regressão no DSP, seleção de notas, afinação, curvas ou critérios de validação |
| Interface | Manter funcionamento do analisador, espectro mediano, navegação e acessibilidade; não recriar DPX |
| Offline | Sem CDN, rede obrigatória ou código remoto em execução |
| Segurança | CSP válida; dados importados não são executáveis; testes adversariais aprovados |
| Compatibilidade | Dispositivos/navegadores-alvo e celular físico aprovados antes da promoção |
| Documentação | Reimplementação do formato possível sem conhecer o código-fonte do HTML |

As metas de redução, memória e latência são metas de engenharia; os valores já medidos estão na seção 3. Fixar critérios quantitativos de latência, bytes de cache e picos permitidos após os testes com as bibliotecas reais, respeitando hardware e navegador. Não inventar números de RAM de dispositivos não medidos.

## 8. Estrutura prevista do repositório ao final

```text
Afinador/
├── index.html
├── README.md
├── GUIA_DE_USO.md
├── LICENSE
├── docs/
│   ├── ROADMAP_ETAPA_21.md
│   ├── AUDITORIA_ARQUITETURAL.md
│   ├── MAPA_DE_DEPENDENCIAS.md
│   ├── BENCHMARK_FINAL.md
│   ├── ARQUITETURA_ARMAZENAMENTO.md
│   ├── FORMATO.md
│   ├── SCHEMA.md
│   ├── VERSIONAMENTO.md
│   ├── SEGURANCA_FORMATO.md
│   ├── RELATORIO_VALIDACAO_21.md
│   ├── PROTOCOLO_TESTES_MOBILE.md
│   └── licencas-de-terceiros.md
├── schemas/
│   ├── session.cddl
│   ├── profile.cddl
│   └── curve.cddl
├── tools/
│   ├── README.md
│   ├── requirements.txt
│   ├── codec.py
│   ├── encode.py
│   ├── decode.py
│   ├── inspect_file.py
│   ├── validate.py
│   └── convert.py
├── benchmarks/
│   ├── benchmark.html
│   ├── benchmark.py
│   └── resultados/
└── tests/
    ├── test_codec.py
    ├── test_roundtrip.py
    ├── test_security.py
    ├── generate_test_profiles.py
    └── fixtures/
```

Estrutura e nomes propostos, sujeitos ao detalhamento das fases 21.1–21.3. Os testes JS e de navegador serão acrescentados nas subetapas correspondentes; o código de produção e suas dependências devem permanecer incorporados ao HTML. Dados reais privados não precisam ser publicados no GitHub: usar fixtures sintetizadas ou amostras cuja publicação esteja autorizada. Se conveniente, agrupar arquivos auxiliares em um ZIP por entrega, com lista de arquivos, sem substituir o HTML completo.

## 9. Arquivos de referência e retomada em outra conversa

### 9.1. Baseline e evidências a preservar

- `etapa20_11/index.html` — última versão estável de referência (não substituir por um `index.html` mais antigo de mesmo nome). SHA-256 no arquivo disponível durante a elaboração deste roadmap: `82f63b46c75519d04528e4262e994cdd14469166d6d54330eaeefa71bd328c4b`.
- `etapa20_10/index.html` — referência imediatamente anterior à retirada do DPX, somente se necessária para regressões.
- `README.md` e `GUIA_DE_USO.md` — documentação existente; conferir versões antes de atualizar.
- `benchmark_armazenamento.csv` — 108 linhas de dados; resultados de serialização/compressão, tamanho, latências e RSS reportado pelo processo.
- `benchmark_memoria.csv` — 60 linhas de dados; operação de gravação/leitura, baseline, pico e diferença de RSS.
- `benchmark_navegador.csv` — medições JS no navegador, JSON/CBOR + GZIP.
- `benchmark_heap_navegador.json` — heap com 0, 1, 52, 104 sessões e após liberação.
- `etapa20_9/PROTOCOLO_VALIDACAO_20_9.md` — histórico e critérios anteriores de validação acústica, quando necessário.

### 9.2. Corpus de sessões para round-trip

Os arquivos abaixo já existiam no projeto. Os três marcados como benchmark principal são as medições mais recentes de cravo usadas para projeção de armazenamento. As demais sessões servem para diversidade de schema, forma e tamanho dos dados; não exigem uma migração permanente de esquemas históricos no HTML. Preservar os originais e usar cópias de teste, sem alterar os JSONs para fazê-los passar.

- `afinador-sessao-23d69d69-fb14-42e7-9b59-39ac8816a0fb.json` — Sessão histórica de cravo; 17 execuções; 3,976,776 bytes.
- `afinador-sessao-2e981d0b-3e5b-41b5-9998-5d1d684f2e71.json` — Cravo Red Brass, 20.8; 13 execuções; 3,674,249 bytes.
- `afinador-sessao-583f2664-8c63-4f3d-8ace-f374ad871148.json` — Pífano; 18 execuções; 1,339,910 bytes.
- `afinador-sessao-6949c5bb-51b7-4b0b-b59e-2f066ea77764.json` — Sessão histórica de cravo; 15 execuções; 2,147,236 bytes.
- `afinador-sessao-6e9520d5-f279-4793-b4b9-60403239646f.json` — Sessão histórica de cravo; 16 execuções; 3,038,957 bytes.
- `afinador-sessao-76cf3082-8de7-45da-a69b-7d7133da4eee.json` — Sessão histórica de cravo; 16 execuções; 3,215,731 bytes.
- `afinador-sessao-872db0bd-1418-4ace-9a9f-cfdb24991b19.json` — Sessão histórica de cravo; 13 execuções; 2,565,411 bytes.
- `afinador-sessao-a9447da0-e76b-4926-a6d1-1c0926364cf2.json` — Violão Mi2; 13 execuções; 2,847,635 bytes.
- `afinador-sessao-b2c1ce8a-32eb-4ad7-a36e-93b4990f1de8.json` — Yellow Brass — benchmark principal; 13 execuções; 4,101,191 bytes.
- `afinador-sessao-bb439a58-4ddd-4516-b05b-9a7e42534fe2.json` — Cravo Yellow Brass, 20.8; 13 execuções; 3,758,644 bytes.
- `afinador-sessao-cefedfca-321f-43c8-87a9-7b1dc4ae8a28.json` — Violão Mi4; 14 execuções; 2,776,279 bytes.
- `afinador-sessao-da23877e-ac92-4c17-b48a-ff25f4354c62.json` — Red Brass — benchmark principal; 13 execuções; 3,805,795 bytes.
- `afinador-sessao-e104cc38-4785-4543-a1db-cfefec331825.json` — Iron — benchmark principal; 14 execuções; 3,580,322 bytes.
- `afinador-parciais-2026-11-19T13-47-37.870Z.json` — inspeção individual de parciais; fixture complementar.
- `afinador-parciais-2026-11-19T13-57-15.890Z.json` — inspeção individual de parciais; fixture complementar.

### 9.3. Procedimento de retomada

1. Anexar este roadmap e o HTML correto da última etapa concluída. Em uma conversa nova, arquivos mencionados pelo nome podem não estar acessíveis; reenviar os arquivos necessários. Se possível, anexar também os relatórios de validação e CSVs de referência.
2. Informar a última subetapa efetivamente aprovada e as pendências. **No momento da criação deste documento, a próxima é a 21.1.** Não inferir que a arquitetura já foi implementada a partir deste planejamento.
3. Pedir a execução de uma subetapa de cada vez, com os entregáveis definidos na seção 5. Não repetir ou ampliar o escopo de uma etapa aprovada sem explicitar o motivo.
4. Conferir resultados, realizar testes físicos quando solicitado, guardar a versão completa entregue e registrar aprovação/pontos pendentes. Uma subetapa sem comprovação de critério obrigatório permanece em validação.
5. Atualizar o roadmap ou manter um registro incremental da execução, especialmente se os benchmarks levarem a uma decisão tecnológica diferente. Guardar HTML e arquivos auxiliares por versão; não confiar exclusivamente no histórico da conversa.

Sugestão de mensagem para retomada imediata:

> Este é o projeto Afinador. Estou anexando o ROADMAP_ETAPA_21.md e a versão estável 20.11 do index.html. Execute a subetapa 21.1 conforme o roadmap, fazendo a auditoria completa do código real. Preserve o sistema atual de JSON, IndexedDB e todos os algoritmos acústicos. Entregue os documentos previstos, registre os testes e limitações e não inicie a subetapa seguinte sem minha aprovação.

### 9.4. Registro de progresso (preencher nas próximas entregas)

| Subetapa | Estado inicial | Evidência/pendência |
|---|---|---|
| 21.1 | Não iniciada | Auditoria completa |
| 21.2 | Não iniciada | Benchmark do codec real JS/WASM e escolha |
| 21.3 | Não iniciada | Contrato formal de formato |
| 21.4 | Não iniciada | Codec binário |
| 21.5 | Não iniciada | Compressão e Worker |
| 21.6 | Não iniciada | Ferramentas Python |
| 21.7 | Não iniciada | IndexedDB paralelo |
| 21.8 | Não iniciada | Carregamento sob demanda |
| 21.9 | Não iniciada | Integração das ferramentas |
| 21.10 | Não iniciada | Importação/exportação |
| 21.11 | Não iniciada | Validação e testes móveis |
| 21.12 | Não iniciada | Aprovação e transição |

## 10. Referências técnicas para a implementação

Referências normativas e APIs a consultar na fase de especificação/implementação:

- CBOR — RFC 8949: <https://www.rfc-editor.org/rfc/rfc8949.html>
- Typed Arrays em CBOR — RFC 8746: <https://www.rfc-editor.org/rfc/rfc8746.html>
- CDDL — RFC 8610: <https://www.rfc-editor.org/rfc/rfc8610.html>
- Zstandard — RFC 8878: <https://www.rfc-editor.org/rfc/rfc8878.html>
- GZIP — RFC 1952: <https://www.rfc-editor.org/rfc/rfc1952.html>
- Brotli — RFC 7932: <https://www.rfc-editor.org/rfc/rfc7932.html>
- MessagePack: <https://github.com/msgpack/msgpack/blob/master/spec.md>
- IndexedDB: <https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API>
- Compression Streams: <https://developer.mozilla.org/en-US/docs/Web/API/Compression_Streams_API>
- Cotas e descarte de armazenamento: <https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria>
- ZIP Application Note: <https://support.pkware.com/pkzip/appnote>

## 11. Limitações e decisões ainda abertas

Este roadmap consolida as decisões da conversa e os benchmarks anteriores e inclui uma verificação pontual da versão 20.11 e dos CSVs. Não substitui a auditoria completa da 21.1 nem reexecuta os benchmarks. Não foram implementados ou aprovados novos codecs nesta entrega.

A escolha CBOR + Zstandard 3 permanece candidata até a 21.2. As bibliotecas concretas, licenças, compatibilidade móvel, limites quantitativos de RAM, detalhes do envelope, estrutura final dos stores, política de importação e os esquemas ainda devem ser formalizados. O contêiner ZIP e as extensões `.afs`, `.afp`, `.afc` são propostas. A granularidade dos sub-blocos, staging e paginação foi detalhada como orientação de engenharia para impedir alocação integral e favorecer atomicidade, não como requisito de implementação previamente validado. A nomenclatura `inspect_file.py` é uma melhoria em relação à proposta inicial para evitar conflito com a biblioteca padrão.

O princípio central permanece: reduzir espaço persistente de forma substancial, mas sobretudo evitar que a quantidade de evidência descompactada em RAM cresça com todas as cordas do instrumento; preservar a informação científica e o comportamento acústico; só substituir o sistema atual quando o novo estiver inteiramente operacional e validado.
