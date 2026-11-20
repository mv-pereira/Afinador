# Afinador — Roadmap da Etapa 21 (revisão pós-validação móvel)

## Arquitetura binária de armazenamento, intercâmbio e otimização de desempenho

**Data de revisão:** 20/11/2026  
**Estado:** 21.11 em validação parcial; feedback e latência insatisfatórios no Chrome móvel.  
**Subetapa atual:** 21.11.1 — implementação entregue, validação móvel pendente. Próxima após aprovação: 21.11.2.  
**Baseline de execução:** HTML 21.10 inalterado na entrega 21.11; JSON principal, binário experimental.  
**Baseline estável:** 20.11.  
**Repositório:** `https://github.com/mv-pereira/Afinador` — aplicação em `https://mv-pereira.github.io/Afinador/`.  
**Escopo:** armazenamento, intercâmbio, interoperabilidade, segurança, memória, latência e UX de armazenamento; não é revisão dos algoritmos acústicos.

Este documento substitui o roadmap anterior como guia de execução. Preserva as 12 subetapas originais e introduz oito subetapas corretivas dentro da 21.11. Os registros históricos de 21.1–21.6 foram preservados ao final: seus estados, propostas e instruções de avanço referem-se à data de cada entrega, não à situação atual. O contrato AFB 1.0 e os documentos normativos de 21.3 permanecem válidos; as novas otimizações não alteram esse contrato. Não autoriza 21.12, publicação definitiva ou migração automática.

**Fontes e rastreabilidade:** versão de roadmap contida em `ETAPA_21_6_FERRAMENTAS_PYTHON.zip` (mais recente das duas entregas reabertas), documentos normativos e relatórios contidos também em `ETAPA_21_3_ESPECIFICACAO.zip`, HTML/LEIA-ME 21.11 fornecidos nesta conversa, resultados e relato móvel registrados pelo usuário. Os relatórios completos de 21.7–21.11, corpus de 13 sessões e AFP de teste não foram reenviados nesta revisão. O estado desses gates não será presumido; recuperar evidências originais quando necessárias. Esta revisão é documental: não houve novo benchmark, alteração de HTML, execução de testes de aplicativo nem aprovação técnica de caminho rápido.

**Princípio de execução:** primeiro visibilidade e controle, depois instrumentação, depois otimização incremental baseada em evidência, finalmente revalidação. Qualquer subetapa pode produzir resultado negativo e conservar o caminho defensivo; não sacrificar informação científica, segurança, RAM ou DSP para obter velocidade.

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

- Criar uma Etapa 21 independente, dividida em **12 subetapas originais (21.1–21.12)**, com extensão corretiva de oito subetapas dentro da 21.11, entregas incrementais e validação antes de avançar.
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

## 3. Evidência dos benchmarks já realizados (histórico preliminar)

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

## 4. Arquitetura-alvo (propostas históricas e decisões consolidadas)

| Componente | Decisão de referência após 21.3 |
|---|---|
| Serialização | CBOR (RFC 8949), CBOR-X 1.6.6, sem tags proprietárias |
| Vetores tipados | Int16 opcional apenas na grade quantizada; tags RFC 8746 73/77 |
| Compressão | Zstandard nível 3 WASM pinado, STORE e GZIP explícitos conforme kind/contrato |
| Banco local | IndexedDB modular separado; JSON segue principal até 21.12 |
| Contêiner | AFB 1.0, AFS sessão, AFP/AFC ZIP clássico STORE, manifesto primeiro |
| Especificação | FORMATO, SCHEMA, CDDL, VERSIONAMENTO, SEGURANCA_FORMATO |
| Integridade | CRC ZIP, SHA-256 de transporte e JCS semântico original, vínculos e validação física |
| Execução | Worker dedicado sob demanda, uma tarefa ativa; reutilização a investigar na 21.11.3 |

As decisões de 21.2–21.3 constam dos registros históricos ao final. Não confundir escolha técnica para o backend experimental com aprovação de produção. Mantêm-se as pendências de licenças, memória, interoperabilidade integral e segurança. Os parágrafos 4.1–4.4 descrevem a motivação de projeto e as unidades lógicas; onde houver propostas antigas, prevalecem o contrato 21.3 e os limites da nova seção 21.11. Não introduzir Base64 para dados persistidos.

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

## 5. Roadmap de implementação — 12 subetapas originais e extensão 21.11.1–21.11.8

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

**Aceitação (ampliada pelas subetapas abaixo):** nenhuma perda ou alteração semântica; sem regressões acústicas e de segurança; perfil de 300 cordas operacional com acesso seletivo; estresse de 1.000 com resultado/limites documentados e falha segura se atingir teto. Medidas móveis aprovadas pelo usuário. Se teste crítico falhar ou ficar pendente, manter sistema legado principal e corrigir/retestar; não saltar para 21.12.

### 21.11.0 — Fechamento do diagnóstico inicial (registro histórico, não nova implementação)

**Situação em 20/11/2026:** a entrega 21.11 é uma validação parcial sobre o HTML 21.10 inalterado, conforme o `LEIA-ME.md` da entrega. O novo backend continua experimental e JSON é o padrão. O usuário autorizou este novo planejamento, não a promoção do backend nem a execução antecipada de todas as otimizações. A primeira subetapa planejada era 21.11.1; ver registro de execução abaixo.

#### Evidência de utilização real

| Teste | Resultado comunicado |
|---|---|
| Dispositivo | Celular, Chrome; modelo, SO e versões não informados |
| Importação AFP representativo com 104 sessões | Concluída; espera considerada muito longa, sem cronômetro |
| Reexportação AFP com 104 sessões | Concluída; demora percebida semelhante à importação |
| Responsividade | Usuário não observou travamento nem perda de responsividade |
| Comunicação de progresso | Reprovada: usuário não percebia que o arquivo estava sendo processado e acionou importação várias vezes |
| Persistência após fechar e reabrir | Não testada pelo usuário |
| Inspeção/comparação seletiva de sessões | Sem resposta registrada; pendente |
| Aquisição física e exportação AFS | Pendente |
| Pico de memória real | Não medido |

A resposta registrada na conversa anterior relatou igualdade integral dos dois arquivos originais e reexportados: 846.854 bytes (3 sessões) e 29.324.709 bytes (104 sessões), SHA-256 iguais dentro de cada par, 8/8 e 210/210 blocos ZIP com CRC íntegro, respectivamente, 107 sessões preservadas. A checagem semântica adicional em Python terminou para o perfil menor e alcançou pelo menos 20 registros do maior antes do limite de execução. Não confundir comparação integral de bytes com validação física completa ou paridade semântica Python. Os quatro AFP não acompanham esta revisão do roadmap; estes resultados são evidência histórica informada, não novo teste independente. Preservar originais e reexportados como fixtures, com hashes efetivos e logs na próxima entrega. Não são instrumentos físicos completos nem fontes autorizadas de curvas. O teste de 104 registros pequenos de 21.6 é outra fixture, não substitui o perfil representativo de 21.11.

O comportamento satisfatório da UI durante espera é uma evidência qualitativa, não uma medida de latência/RAM/DSP. Acionamentos repetidos não comprovam que operações simultâneas realmente ocorreram. A aprovação de integridade observada nesses pares permanece válida; o desempenho e o feedback da operação permanecem reprovados. Não avançar a 21.12.

#### Confronto entre documentação e código de partida

Fontes: `RELATORIO_VALIDACAO_21_4.md` §2, `RELATORIO_VALIDACAO_21_5.md` §§1,4–7, `RELATORIO_VALIDACAO_21_6.md` §§3–5, `SEGURANCA_FORMATO.md` §§2–3, `FORMATO.md` §§4–5, `ARQUITETURA_ARMAZENAMENTO.md`, registro 21.2 complementado e o HTML de partida (hash na seção 9.1). Ver também o relatório 21.11 completo quando reenviado.

| Indicador por sessão | 21.2 (codec real, benchmark isolado) | 21.5 (pipeline defensivo completo) |
|---|---:|---:|
| CBOR comum/Zstd 3, gravação | 13,70 ms | 375,3 ms |
| CBOR comum/Zstd 3, leitura | 9,45 ms | 229,5 ms |

Os números 21.5 são medianas exploratórias no Chromium desktop, uma passagem por arquivo, incluindo validação, inicialização e clone, sem I/O IndexedDB; as medianas internas do Worker eram 350,7 e 202,6 ms. As razões aritméticas ~27,4× e ~24,3× mostram diferença de escopo/custo, não regressão isolada do compressor nem aceleração recuperável garantida. Não extrapolar para o tempo no celular. 21.2: CBOR/Zstd3 projetado em 29,18 MB/104, CBOR/GZIP 37,44 MB (39,60/12,85 ms), JSON/GZIP 41,39 MB (73,65/14,85 ms); Int16 seletivo economizou apenas ~0,54 MB na projeção da 21.6. Manter CBOR-X 1.6.6 e Zstd 3, sem trocar codec, nível, resolução ou precisão para mascarar latência. O formato 1.0 admite alternativas explícitas, não fallback silencioso.

- A 21.4 optou deliberadamente por validação redundante para priorizar conformidade; a 21.5 recomenda avaliar redundância demonstravelmente segura, Worker por lote, transferência e reutilização sob orçamento. A decisão de Worker por tarefa foi defensiva, voltada a liberar memória linear e evitar filas pesadas. Não foi demonstrado que reutilização seja segura em qualquer dispositivo.
- `SEGURANCA_FORMATO.md` §2.5 prevê validar sessão/revisão uma vez por importação. O HTML ainda verifica registro na entrada, em `prep()` e em `recordAt()` durante `validateStaging()`. Todos acionam `curveVerify`; predicados e hashes podem aparecer também internamente. Verificar o grafo e o contrato de cada passagem antes de deduplicar; leitura posterior independente precisa manter garantia de integridade e semântica, não basta uma flag de “validado”.
- `FORMATO.md` admite prepass ou spool persistente para manifesto em primeiro lugar. O repositório prevê evidência imutável por hash/revisão. `archive()` hoje recodifica blocos, escreve spool, relê, verifica e emite; são oportunidades, não falhas de segurança por si.
- `importFile()` identifica o arquivo antes de entrar em `binaryTransfer2110`; callbacks de `importProfile()` e `writeProfile()` escrevem texto em `p3Status`, possivelmente fora da tela; o botão cancelamento `p3AFBCancel` só aparece no wrapper. O lock já impede outra transferência por esse wrapper; não há prova de duas importações simultâneas, porém o seletor de arquivo pode ser reaberto e início/fases/finalização não são suficientemente visíveis. Auditar também `run`, lifecycle, `render`, outras ferramentas e controles; melhorar desde a seleção, não somente após parse.

| Caminho no HTML de partida | Evidência estática (linhas da cópia de referência; procurar nomes, pois linhas mudarão) | Hipótese de custo |
|---|---|---|
| `AFB21Storage` (14776) | `new Worker` e Blob URL por requisição | inicialização, teardown, parse e clone |
| `block` / `unBlock` (14821–14822) | codec, hash externo, Blob/ArrayBuffer | cópia, SHA, codec |
| `prep` (14826) | clone, `curveVerify`, encode evidência/header, índice | percurso completo, JCS, recodificação |
| `meta` / `stageRecord` (14833/14863) | lê e valida metadado a cada registro | I/O e Worker adicionais |
| `recordAt` / `readSession` (14841–14842) | lê três stores, decode, `curveVerify`, índice, recheck de geração | reconstrução e verificação |
| `validateStaging` (14865) | relê e valida todos os registros | segundo percurso e transações |
| `publishGeneration` (14866) | CAS, journal e commit de ponteiro | requisito de atomicidade, não remover |
| `openArchive` (14983) | manifesto, diretório, inspeção de headers | fase inicial antes de progresso por registro |
| `archive` / `writeProfile` (14993–14997) | encode, spool, CRC/SHA, manifesto, escrita incremental | recodificação e I/O temporário |
| `importProfile` (15000) | lê par, verifica, stageRecord, validateStaging, publica | validação e transformação repetidas |

Contagem estática aproximada, caminho principal AFP sem conflito e sem operações auxiliares de UI: `importProfile` a partir da abertura de arquivo 7N+4 chamadas ao codec (2 decode de entrada + 1 decode meta + 2 encode + 2 decode staging por registro; fixos manifesto/perfil, encode meta, decode meta na validação). `writeProfile` 5N+2 (3 decode incluindo meta + 2 encode por registro; fixos meta de saída e manifesto). Para N=104: 732 e 522, somando 1.254 possíveis criações de Worker; **não** número de inicializações WASM (STORE/GZIP não instanciam Zstd), nem medição em dispositivo. Recontar em 21.11.2, incluindo erros, escolhas do usuário e chamadas complementares; os números podem divergir por versão/caminho. Pelo menos 3N acionamentos de `curveVerify(profile,[record])` no fluxo de importação principal; não inferir tempo percentual a partir de contagens.

Prioridades de investigação: criação/encerramento Worker; validações e JCS; recompressão; múltiplas passagens CBOR; spool/transações; clone/cópias; metadado repetido; SHA/CRC. A ordem é hipótese, a instrumentação decide a prioridade efetiva. Não atribuir a espera a Zstd, RAM insuficiente ou IndexedDB sem evidência.

### Regras adicionais comuns às 21.11.1–21.11.8

1. Mudanças isoladas, mensuráveis, reversíveis; comparar cada versão com sua predecessora e a baseline 21.10/21.11. Entregar HTML autocontido completo quando houver mudança, relatório, testes, hashes, arquivos auxiliares e instruções de rollback. Não implementar várias hipóteses ao mesmo tempo sem ablação. Resultado negativo justifica não ativar uma otimização, com documentação; não fabricar ganho para fechar etapa. Nenhuma subetapa implica autorização automática da próxima.
2. Preservar byte/semântica de todos os campos e valores (incluindo Float64, -0, Unicode, ausência/nulo, `spectrumGrid202`, mediana, flags, IDs, revisões, JCS legado); zero alteração acústica, permissões e vetos de curvas intactos. Preservar .afs/.afp/.afc AFB 1.0, leitores existentes, ZIP STORE, ordenação, manifesto, SHA/CRC e compatibilidade Python; não introduzir schema novo por conveniência. Igualdade byte a byte é meta de regressão no mesmo arquivo e configuração quando aplicável; representação CBOR não canônica, codec alternativo e novo profileId podem mudar bytes legitimamente, sem mudar semântica. Toda diferença deve ser explicada, não aceita por conveniência.
3. Não reduzir garantias da ordem de validação: preflight antes de alocação/descompressão/decodificação, hashes do envelope e do bloco inteiro, CRC ZIP, validação semântica SECURITY13 original, reconstrução e vínculos, verificações de índice e fonte, controle de revisão e publicação atômica. SHA comprova integridade, não autoria. Dados externos são não confiáveis mesmo com todos os hashes recalculados. Não usar a implementação Python parcial como autoridade de importação. Não confiar em hashes ou metadados persistidos isoladamente se ambos puderem ser alterados. Validar evidência completa conforme requisitos do consumidor (inclusive fontes de curva). Não criar API pública `skipValidation`/`trusted=true` manipulável por dados; comprovar precondições e fronteira de confiança de toda via rápida, invalidar por geração, revisão, digest e versão de validador. Na dúvida usar caminho defensivo ou rejeitar inconsistência, nunca aceitar automaticamente.
4. Preservar tetos normativos (ver seção seguinte), uma tarefa pesada por vez, sem filas de evidências, leitura paginada, cache limitado em bytes e itens, liberar objetos/buffers/URLs/Workers e trabalho temporário em sucesso/erro/cancelamento. Não reter decodificados de N sessões. Não abrir banco, iniciar Worker/codec ou instrumentação contínua enquanto apenas afina. Não transferir buffers do DSP, não manter transação IndexedDB à espera de Worker, não apagar trabalho não salvo. Guardar CSP e recalcular hashes somente dos scripts editados; sem recursos externos, relaxamento de CSP ou `unsafe-eval`. Manter os dois temas e acessibilidade.
5. Operações em duas abas: CAS de geração/revisão e serial de journal, checagem no ponto de commit, invalidação e notificações pós-commit, cancelamento/epoch e recuperação. Limpar apenas staging/spool próprios, não a geração ativa anterior; journals abandonados recuperáveis. Se falhar limpeza, relatar pendência sem confundir com rollback da geração já publicada. Exportar não altera conteúdo fonte. Não afirmar download concluído quando apenas solicitado pelo navegador.
6. Continuam em vigor todos os gates originais de 21.1–21.11 não comprovadamente encerrados. Concluir otimizações não basta para 21.12. Não publicar versão definitiva antes de validação/acordo e licenças. Testes com mock, Node, origem opaca e aparelho físico são categorias distintas; não usar equivalência de código como prova de comportamento nativo.

#### Limites normativos e orçamentos de runtime

Resumo vinculante do contrato 21.3 (`SEGURANCA_FORMATO.md` prevalece para detalhes); não elevar os limites com uma otimização. Limites do SECURITY13 mais estritos continuam.

| Recurso | Teto/condição |
|---|---|
| AFB/header, raw por objeto, payload | 128 B, 32 MiB, 34 MiB |
| Chunks | até 16, raw 2 MiB, armazenado 2 MiB + 64 KiB; janela Zstd 2 MiB |
| Manifesto / diretório central | 2 MiB raw STORE / 2 MiB |
| ZIP / soma raw | 1 GiB / 8 GiB |
| Registros / teclas / entradas | 2.000 / 1.000 / 4.002 |
| Revisões de curva / fontes por revisão | 128 / 512 |
| Árvore / tokens / profundidade raiz 0 | 2.500.000 nós / 5.000.000 tokens / 60 |
| Mapa / array / texto | 4.096 chaves / 200.000 elementos / 100.000 UTF-16, 400.000 bytes UTF-8; limites de chaves específicos SECURITY13 |
| Execuções / ordens / grade | 2.000 / 256 / 4.096, demais regras semânticas aplicáveis |
| WASM | máximo 32 MiB, inicial 16,125 MiB na versão testada |
| Cache de evidência / comparação | 8 MiB lógicos e 2 entradas conforme AFB21Access atual; conferir semântica do orçamento ativo separado |
| Projeções | contrato prevê 8 MiB/64 entradas; cache de projeções atual declara 0; não ampliar por conveniência |
| Página de índice | até 100 itens; orçamento lógico inicial de 1 MiB/página e 4 MiB ativos, verificar código e limites reais |
| Fallback Blob | 128 MiB ZIP final; acima disso streaming suportado ou lotes, sem elevar teto |
| Prazo de codec | 30 s por tarefa de objeto; cancelamento e timeout com teardown, não timeout global de 30 s para perfil |

Os limites de runtime especificados em 21.3 são orçamentos iniciais a verificar, não prova de implementação nem de pico de RAM. Cache lógico, heap, backing storage, WASM e RSS do processo são medidas distintas. Comparação de duas sessões e sessão ativa não salva exigem contabilização separada. A etapa 21.11.2 deverá registrar limites efetivos observados no código (incluindo single-object/índice/comparação), sem prometer que 32 MiB raw implica 32 MiB de RAM. Divergência de implementação com contrato deve ser tratada e testada, não normalizada silenciosamente.

### 21.11.1 — Interface de progresso, cancelamento e exclusão mútua

**Objetivo:** resolver primeiro o problema observado pelo usuário, independentemente da aceleração real. Não alterar pipeline de validação, codec, banco ou formato nesta entrega, exceto hooks de progresso, cancelamento e exclusão mútua necessários ao controle seguro da operação.

**Escopo e comportamento:** painel/janela centralizada visível independentemente da rolagem, seguindo tokens de tema existentes (marfim/grafite), compacta em tela estreita, com título, nome e tamanho quando conhecidos, fase, contagem, percentual quando determinável, barra e ação de cancelamento. Não mostrar interface durante afinação normal. Feedback imediato após seleção do arquivo e ao acionar exportação, antes de `identify`, leitura, válidas operações longas e confirmação. Adquirir lock síncrono antes do primeiro await; manter por todo o trabalho, inclusive limpeza/finalização, aceitar no máximo uma transferência pesada. Adotar bloqueio explícito de importação/exportação, seleção/edição de perfil, troca de backend e demais controles conflitantes, sem bloquear redraw ou cancelamento. Prevenir dupla seleção de arquivo, duplo clique/toque, reentrada por teclado/eventos e callbacks tardios. Preservar `confirm` de restauração/cópia, e interação com seletor de destino (gesto de usuário necessário ao File System Access; não introduzir await que o perca). Se houver seletor aberto, distinguir espera por ação do usuário de processamento; cancelamento do diálogo não é erro de arquivo.

| Fase de importação AFP | Unidade real / mensagem |
|---|---|
| Arquivo selecionado / identificando | indeterminada enquanto total desconhecido; nome/tamanho |
| Examinando arquivo / manifesto | contagem de entradas/headers examinados quando disponível |
| Confirmação de destino | aguardando usuário; sem percentual falso |
| Importando e validando registros | n/N após stageRecord concluído |
| Verificando armazenamento temporário | n/N efetivamente conferido por validateStaging |
| Publicando perfil / atualizando interface | finalização; 100% só após commit e estado de resultado conhecido |

| Fase de exportação AFP | Unidade real / mensagem |
|---|---|
| Preparando exportação / escolhendo destino | indeterminada ou aguardando usuário |
| Preparando blocos | n/(1+2N), conforme pipeline atual |
| Construindo manifesto / escrevendo arquivo | entradas efetivamente escritas ou bytes confirmados; manifesto + perfil + pares, incluindo diretório/EOCD na finalização |
| Finalizando arquivo | até fechamento bem-sucedido do stream ou Blob e disparo do download |
| Resultado | arquivo preparado/transferência solicitada; não afirmar que navegador salvou quando não há confirmação |

Para n/N, informar percentual da fase ou uma barra global claramente rotulada como fração das unidades de trabalho concluídas (não estimativa de tempo). Se global, definir denominador por fases/contagens reais, garantir monotonicidade, reservar conclusão até commit/close/download solicitado, não inferir progresso por relógio. Quando total desconhecido, usar barra indeterminada (sem `%` falso); em fase sem contador significativo, mostrar fase indeterminada/estado de finalização. Não chegar a 100% antes do final nem congelar em 99% sem mensagem. Progresso pode ser atualizado por bloco/registro, com coalescência/throttling apenas durante transferência (por exemplo 100–250 ms e mudança de fase imediata, calibrar e testar); não simular atividade. Permitir paint inicial respeitando o gesto do seletor; minimizar trabalho síncrono da UI.

Cancelamento: `AbortController` por operação/epoch, integração com Worker, loops, transações e escrita. Mostrar “Cancelando… / limpando dados temporários”, manter lock até fim e não liberar cedo. Antes de publicação não deixar perfil parcial visível; após commit não prometer cancelamento retroativo. Na fase indivisível informar finalização ou desabilitar cancelar justificadamente. Diferenciar commit bem-sucedido seguido de falha da UI/limpeza. Se erro, mostrar mensagem útil (formato, integridade, quota, conflito, timeout, cancelamento distinto), manter perfil anterior e trabalho não salvo. Fechar e restaurar foco/controles; não limpar input de dados pendentes. Não permitir que Escape/backdrop faça parecer cancelado sem abortar; tratar pagehide/aba em background. Sem animações permanentes; `prefers-reduced-motion`, sem overflow, contraste e `aria-live` para fases, `role=progressbar` valores só quando conhecidos, gestão de foco, teclado, toque, leitor de tela. Não anunciar cada tick.

Aplicar a todo intercâmbio binário disponível (.AFP, .AFS, .AFC) onde a espera pode ocorrer, inclusive ferramenta de curvas e captura/exportação de sessão; auditar handlers reais e conservar política de importação legada. Prioridade AFP no celular; fases unitárias AFS/AFC adaptadas à operação real, não inventar número de sessões. Avaliar JSON longo e unificar apenas UI de progresso se seguro, sem reescrever backend; registrar qualquer caminho não coberto e tratar no gate. Evitar mudanças laterais na disposição de outras ferramentas.

**Entregáveis:** `index.html`, `docs/RELATORIO_21_11_1.md`, especificação curta de estados/callbacks de progresso e cancelamento, testes automatizados `tests/test_progress2111_1.*`, protocolo de smoke móvel (3/104 AFP, temas, cancelamento, duplicidade, erro). Atualizar ajuda apenas nos pontos de importação/exportação e mensagens pertinentes.

**Aceitação:** painel realmente visível desde início (não só depois do primeiro registro); unidades/percentual reais e conclusão correta; repetidos toques não abrem nova operação, não há deadlock ou comandos conflitantes; cancelamento e falhas antes/depois do commit têm semântica correta; responsividade e integridade equivalentes; 3/104 AFP passam antes/depois, CSP e offline; teste do usuário confirma clareza no celular. Se o ambiente físico não estiver disponível, entregar como experimental e pedir teste, não alegar aprovação. Latência longa é admitida nesta subetapa apenas porque será investigada a seguir. Rollback para HTML de referência sem alterar banco ou arquivos.

### 21.11.2 — Instrumentação e benchmark de desempenho real

**Objetivo:** medir integralmente o pipeline antes de otimizar. A 21.11.1 preserva a lógica; medir impacto do próprio painel. Não alterar codec ou validação nesta subetapa.

Implementar uma sessão de diagnóstico local, explícita e vinculada à operação. Pode integrar o resultado ao painel (ex.: opção “Registrar diagnóstico de desempenho” antes da operação e “Baixar relatório” ao terminar) sem interferir no DSP; formato exato é decisão de UI a documentar. Não exigir cronômetro nem devtools do usuário. Usar `performance.now()` monotônico, medir durações dentro de cada contexto e correlacionar por IDs de operação/tarefa; não subtrair clocks de threads com origens diferentes. Separar eventos de UI/tempo de confirmação ou seletor, espera em fila, CPU/latência por estágio, total, custos de instrumentação. Contagens e durações agregadas por fase/kind/codec, histogramas/reservatório ou amostra limitada, sem logs ilimitados por sessão. Não gravar dados acústicos, áudio, IDs reais, nomes de arquivo/perfil/caminhos, notas, valores de medições ou identificadores de dispositivo/usuário. Relatório JSON pequeno, versionado, local, exportado por ação do usuário inclusive falha/cancelamento, sem telemetria de rede. Informar dados que serão incluídos. Não inserir em AFB/IndexedDB acústico, não persistir automaticamente. Deixar desabilitado por padrão ou limitado a contadores baratos durante operações; nada periódico no modo afinação.

| Métrica | O que distinguir |
|---|---|
| Ponta a ponta | clique/seleção, primeiro paint, inspeção, espera confirmação, trabalho ativo, commit, UI, cleanup |
| AFB/ZIP | slices e bytes, diretório/headers, CRC, SHA, manifesto, I/O stream/Blob, fechamento |
| Worker | criações/terminate/URL, tarefas, fila, tempo startup (handshake quando possível), mensagens/clones/transferências estimadas, timeout |
| WASM | instâncias, inicialização fria/quente, memória linear inicial/pico observado, malloc/free/chunks dentro do escopo mensurável |
| CBOR | preflight encode/decode, normalização, tree, calc-size, serialização/deserialização, cópias/typed arrays |
| Zstd/GZIP/STORE | compressão/descompressão por bloco, bytes raw/stored, frame preflight, CRC |
| Semântica | SECURITY13/curveVerify/verifyRecord/makeRecord/validateSession, JCS, hash e vinculação, distinguir chamadas aninhadas |
| IndexedDB | transações, tempo de abertura/espera/oncomplete, get/put/cursor, bytes, contagem spool/staging, cleanup e conflitos |
| Memória | pico lógico de evidências ativas/cache, bytes de buffers controlados, memória WASM, heap/RSS somente quando API/ferramenta permitir; marcar indisponível |
| Responsividade | atraso de evento/paint, long tasks se suportado, FPS/amostra de frame ou sonda limitada durante operação; medir impacto do observador |

Durações inclusivas e exclusivas devem ser rotuladas para evitar dupla contagem de fases aninhadas; trabalho concorrente não soma diretamente a wall-clock. Contabilizar custo da instrumentação com teste A/B ligado/desligado. Medir tempo entre eventos, não inventar tempo de clone a partir de única diferença sem distinguir transferência e agendamento. Usar contadores de ciclo de vida em pontos reais. Em Chrome Android, APIs de heap/memória total podem não existir; `performance.memory` quando disponível é indicativo e não mede Worker/RSS; `measureUserAgentSpecificMemory` exige condições especiais, não alterar CSP ou isolamento/headers para forçar. Nenhuma coleta invasiva. Diagnóstico do navegador inclui só versão/engine/plataforma grosseira se disponível e consentida; modelo/SO podem ser informados manualmente. Registrar `unavailable` em métricas ausentes, método, granularidade e frequência de amostragem. Nunca afirmar pico real com base em tamanho de arquivo.

Protocolo: usar os mesmos AFP de 3 e 104 (ver hashes), mesma versão HTML, mesmo dispositivo/Chrome, origem e backend, mesmo caminho de destino e política de colisão, sem abas competindo. Não destruir perfis reais; usar instrumento/ambiente de teste, anotar restauração versus cópia. Primeira execução a frio e repetições aquecidas (preferir ≥3 por operação e condição para mediana e faixa; p95 apenas se amostra suficiente; registrar se menor), exportar diagnóstico ao final. Condições de energia/temperatura/carga/anotações sem dados pessoais; evitar misturar tempo de confirmação ou download manual no tempo ativo. Medir desktop nativo sem mock se possível e Node isolado apenas para microbenchmark. Comparar escala 52/104/208/300 representativos e 1.000 pequenos posteriormente, garantindo que tamanho e complexidade sejam explicitados. O perfil 104 é principal teste físico inicial; não exigir que usuário faça dezenas de ciclos. Priorizar qualidade do resultado, não forçar sobrecarga.

Antes de 21.11.3, estabelecer com usuário orçamento de latência e RAM realista, registrar mediana/variação e metas quantitativas para o perfil 104, tolerância de regressão no pequeno e em responsividade. Sem números inventados nesta revisão. Se medição de RAM do celular for impossível via navegador, definir método externo adequado (Android remoto/CDP, ferramentas do SO quando disponíveis) ou documentar bloqueio; proxy não encerra gate de pico total. A ausência de cronômetro manual não bloqueia instrumentação automatizada. Maiores custos medidos guiam ordem/ativação das hipóteses; reordenar subetapas apenas documentando e com anuência, manter numeração e pré-requisitos.

**Entregáveis:** `index.html`, `docs/RELATORIO_21_11_2.md`, `docs/PROTOCOLO_DESEMPENHO_MOBILE.md`, `schemas/performance-report.schema.json` (se útil, independente do formato acústico), script para agregar JSON/CSV e testes de contadores, exportação, não retenção e sobrecarga; baseline de diagnóstico e perfil de custo por fase. Guardar versão de código/relatório, fixture, hashes e método.

**Aceitação:** relatório reproduzível e legível independentemente do HTML; contagens batem com operações reais, erros/cancelamento e métricas indisponíveis representados; duração total explicada por fases sem dupla contagem; teste 3/104 no Chrome do usuário, com resultados disponíveis antes de otimizar, e critérios acordados. Não inicializar nada na afinação, não mudar resultado binário/semântico. Se não houver ambiente representativo, manter gate aberto. Rollback só da instrumentação (sem perda de dados).

### 21.11.3 — Reutilização controlada de Workers e instâncias WASM

**Objetivo:** reduzir criação/encerramento de Worker, custo de inicialização do codec e WASM, mantendo o isolamento e o perfil de memória. Comparar primeiro com o caminho atual instrumentado, sem mudar codificação ou semântica.

Investigar sessão de Worker com escopo explícito de transferência e pedido único em voo (`operationId`, `requestId`, protocolo/versionamento, signal/epoch). Opções: um Worker por operação; Worker reciclado a cada lote limitado de objetos/bytes/tempo de vida; fallback por tarefa. Escolher com dados de 21.11.2 e testes. Uma instância WASM reutilizada por Worker com init lazy somente quando codec Zstd; STORE não aloca WASM. Não criar pool paralelo. O lote é sequencial, não juntar evidências nem executar N tarefas concorrentes. Limitar duração, número de objetos e volume acumulado do lote com parâmetros explícitos; não fixar valor final sem medir. Verificar memória linear de 16,125 MiB inicial e 32 MiB máxima e que malloc/free e estados de CBOR/hash/compressor são reiniciados por tarefa. WASM não encolhe automaticamente; reciclar quando orçamento/pico/ciclo atingido. Não reter objetos de pedidos anteriores, listeners, promises, buffers, URLs ou cache interno indevido. Evitar clone de buffer que pertence exclusivamente ao pipeline, respeitando ownership; não destacar dados ainda usados ou fixture fonte.

Preservar deadline por tarefa (30 s), `BUSY`/backpressure e abort imediato via terminate quando necessário. Erro de formato/semântica ou exceção não deixa Worker reutilizável em estado incerto; terminar e liberar. Ignorar mensagens tardias, validar ID e tipo/versão, `messageerror`, `error`, timeout, pagehide, encerramento de ferramenta. Cleanup em `finally`, abort/cancelamento de qualquer fase, sem Worker ocioso após operação. Nunca transferir o DSP para esse cliente. Garantir que operações unitárias independentes e caminhos antigos continuem seguros. Preservar fallback defensivo por tarefa, configurável apenas por política interna de teste, não por arquivo. Não alterar outros workers acústicos.

Testar byte/hashes e semântica idênticos, múltiplas tarefas sequenciais incluindo codecs diferentes e bloco máximo, erro após sucesso, cancelamento durante compilação/init e tarefa, timeout, message atrasada/duplicada, falha de malloc, reinício, URLs balanceadas, 100 ciclos e estresse. Medir contagens originais versus otimização e overhead cold/warm, heap/linear/external/RSS quando possível, liberação após finalizar, comparação A/B no desktop e celular. O ganho de inicialização não basta se memória ou latência de outras operações piorar além do orçamento. Usar relatório 21.5 como baseline defensiva, não como prova de memória real.

**Entregáveis:** HTML, `docs/RELATORIO_21_11_3.md`, contrato de runtime/ownership atualizado, testes de lifecycle e memória, benchmark A/B, política de lote e justificativa/fallback.

**Aceitação:** redução mensurada de inicializações/tempo quando relevante, preservação de hashes/semântica/segurança, limite e teardown comprovados, sem regressão de RAM/responsividade além do orçamento; ou não ativar a alteração, registrar hipótese refutada/fallback. Rollback para cliente por tarefa, sem mudar dados persistidos.
### 21.11.4 — Eliminação de validações, hashes e cópias comprovadamente redundantes

**Objetivo:** reduzir trabalho sobre a mesma representação imutável, sem diminuir o conjunto de entradas rejeitadas nem a integridade do repositório. Auditoria de equivalência de garantias, não autorização para remover SECURITY13 ou preflight. A reutilização direta de blocos depende desta etapa.

Mapear cada validação, objeto/bytes, autoridade, estado, local, limite, mutabilidade, entradas não confiáveis e consequência de falha. Em particular `AFB21Codec`, `AFB21Storage`, `curveVerify`, `verifyRecord`, `makeRecord`, `validateSession`, `prep`, `meta`, `recordAt`, `validateStaging`, `summary`, SHA de envelope/manifesto e JCS. Separar proteção contra alocação antes de parse (obrigatória), integridade de bytes, validação estrutural e física, vínculo/revisão, verificação de persistência e consistência transacional. Uma etapa de mesmo nome não necessariamente supre outra; elaborar matriz de predicados/garantias antes/depois. Não alterar lógica dos predicados originais, números, ordem física ou vetos.

Investigar contexto de validação privado, de vida curta, criado somente por validação bem-sucedida de objeto e bytes exatos (referências controladas, sem mutação/alias externo, digest AFB e semântico JCS, identidade de perfil, registro, sessão, revisão/geração, versão/política de validador e serial do journal). Não reconstruir de campos de arquivo, índice ou flag persistida; não expor privilégios a chamadores externos. Se remapear profileId, revalidar vínculos afetados e provar independência dos demais predicados; se não demonstrável, manter validação integral. Se houver re-encode, demonstrar correspondência com representação validada; hash semântico não atesta toda estrutura (por exemplo +0/-0). Identidade de bytes não substitui preflight inicial.

Modelo possível para staging: compromisso privado dos digests e índices preparados a partir dos objetos efetivamente validados, progresso e serial do journal; reler em lotes limitados, recalcular digests dos bytes realmente gravados, comparar contra compromisso originado na operação e conferir índice/header/evidence/meta, contagem, tamanhos, unicidade, associações entre registros, generation/revision e serial. Publicação exige CAS e commit. Não aceitar digest persistido junto ao blob como única prova; adulterar ambos e índice deve falhar. Compromisso temporário limitado em bytes e itens, sem reter objetos descompactados; se perdido/alterável, abortar ou revalidar integralmente, nunca retomar com confiança antiga. Considerar corrida entre verificação e publicação: impedir alteração da geração staged pelos caminhos permitidos e garantir invariantes transacionais; se não provar equivalência manter `validateStaging` integral. Não alegar proteção criptográfica contra código hostil com privilégio da mesma origem; explicitar modelo de ameaça.

Validar meta uma vez por snapshot fixado quando possível, confirmar token/digest e revisão em leituras/commit. SHA de raw, payload, cabeçalho, AFB inteiro e JCS têm domínio diferente; só consolidar chamadas inequivocamente sobre mesmos bytes com precondições idênticas, sem remover comparações com valores esperados. Preservar clone quando protege propriedade de objetos; retirar só se ownership/lifetime excluem mutação compartilhada. Otimizar por passos isolados e comparação diferencial contra implementação defensiva sobre corpus positivo e adversarial, incluindo hashes corretos e semântica inválida. Python parcial não é oráculo único.

**Entregáveis:** HTML, `docs/RELATORIO_21_11_4.md`, `docs/MATRIZ_EQUIVALENCIA_VALIDACAO.md` (predicado, ameaça, ponto original, novo, prova, teste, limite e fallback), testes de equivalência e concorrência, A/B de passagens/cópias/digests/RAM. Atualizar segurança/arquitetura apenas para detalhar equivalência, sem relaxar contrato.

**Aceitação:** positivos equivalentes e negativos do caminho antigo continuam rejeitados no contexto equivalente; nenhum bypass em chamadas públicas, índice, staging, cópia, recuperação ou curvas. Sem prova suficiente, preservar checagem. Ganho medido ou justificativa de manter caminho defensivo. Rollback restaura validação original e aceita os mesmos dados; nenhum marcador persistente de confiança necessário.

### 21.11.5 — Importação com reutilização de blocos binários validados

**Objetivo:** evitar reserialização/recompressão de evidências já recebidas em AFB compatível, aproveitando sua imutabilidade. Depende da prova de 21.11.4; manter caminho conservador como fallback.

1. Adquirir lock/signal; identificar arquivo, ler diretório, manifesto e headers seletivamente, validar estrutura, limites, CRC e digests como hoje. Confirmar novo/restauração ou cópia independente; não sobrescrever silenciosamente.
2. Por par, obter bytes limitados, validar CRC/SHA externo, envelope, frames, raw, CBOR/preflight; reconstituir registro e validar integralmente SECURITY13, JCS e vínculos. Guardar bytes imutáveis exatamente correspondentes ao decode; se `decodeOwned` transfere/destaca o buffer, preservar Blob/ownership ou retorno controlado de buffer, contabilizando cópias. Não reler arquivo mutável e presumir identidade sem conferir digest.
3. Gerar `summary`/projeções com mesma função/policyVersion, vincular meta/header/evidence, IDs, digests e revisão. Reutilizar AFB kind 1 quando policy de codec/tag/versão e vínculos permitirem. Kind 2/3 só se campos e IDs idênticos; se `profileId` mudar, reconstruir meta/header afetados e revalidar layout, corda e modelo. Não confundir hash AFB com sessionHash/recordId.
4. STORE/GZIP aceitos pelo leitor; writer atual de evidência Zstd 3 e metadata/header STORE. Definir se preservar codec recebido no armazenamento é compatível com exportador e leitores anteriores. Se regra vigente exigir normalização/recodificação, usar caminho defensivo explícito. Não alterar formato, fallback silencioso, -0 ou tags. Manter padrão de escrita para novas sessões.
5. Commit curto de índice/header/evidence/journal por registro, controles cross-record e orçamento, staging conforme 21.11.4, CAS e publicação após oncomplete; limpeza segura. Cancelamento/quota/abort/conflito não deixam perfil incompleto visível. Liberar bytes e objetos antes do par seguinte; não cachear todas as sessões.

AFS: sessão recebida em pending não equivale a vínculo confirmado; publicar somente após confirmação e validação contextual. AFC: regras de parentesco, manifestos de fonte e bloqueios físicos preservados. Prioridade AFP; manter caminhos conservadores dos demais quando sem prova/benefício. Não introduzir deduplicação global entre perfis ou novo schema; não alterar edição/aquisição normal.

Testes: 3/104 representativos, 52/208/300; zero registros se permitido, mesma sessão mesma corda e conflito entre cordas, colisão de profileId, mudança de revisão/flag/nota, codecs/tags/versões, manifesto adulterado, hashes corretos e semântica inválida, CRC/SHA/raw, índice falsificado, mutação/TOCTOU, cancelamento por fase, quota, conflito de abas, publicação. Confirmar bytes kind 1 reutilizado idênticos e objetos/índices semanticamente equivalentes; remapeamento lista diferenças esperadas. Medir recodificações evitadas, latência, RAM, cópias e disco contra 21.11.4.

**Entregáveis:** HTML, `docs/RELATORIO_21_11_5.md`, matriz de reutilização kind/codec/tag/remapeamento, testes de staging e diferencial, A/B e fixtures interoperáveis; atualização de arquitetura.

**Aceitação:** perfil restaurável e semântica idêntica, bytes de evidência originais quando elegíveis, garantias demonstradas e ganho medido sem regressão RAM; fallback ou manutenção do caminho antigo quando vantagem insuficiente. Rollback lê dados escritos pelo caminho novo sem migração, testar expressamente.

### 21.11.6 — Exportação incremental de blocos existentes e otimização do spool

**Objetivo:** reduzir recodificação e I/O temporário, mantendo manifesto primeiro e consistência. Depende de 21.11.4; atender blocos anteriores e posteriores a 21.11.5. Exportar não altera conteúdo nem revisão fonte.

Candidato de duas passagens (prepass): fixar token de geração/revisão e contagem. Paginar índices na ordem de exportação contratada; recuperar meta/header/evidence do snapshot; verificar bytes, semântica e vínculos por registro (ou prova equivalente de 21.11.4); gerar descritores pequenos com path/kind/ID, tamanho, rawBytes, SHA total e CRC dos bytes verificados. Não confiar isoladamente em digest/CRC armazenado ou índice. Manter apenas descritores/compromissos limitados em memória. Preservar ordem da lista, caminhos e ZIP, não reordenar musicalmente. Gerar manifesto kind 5/6 STORE, central/local e tamanho com inteiros seguros e limites. Caso precise recodificar bloco não elegível, guardar apenas aquele bloco em spool limitado; não reserializar na escrita sem verificar identidade.

Segunda passagem: ler blob por chave exata e token, recalcular digest/CRC dos bytes efetivamente emitidos contra compromisso da primeira passagem; validar tamanho/kind/ID conforme prova e offsets; abortar se ausente/alterado. IDB não fornece snapshot implícito entre transações. Usar pin/snapshot de vida limitada comprovado ou abortar em mudança de geração/revisão; recheck ao ler e antes de finalização, evitar mistura e coleta prematura de geração. Regra vigente: abortar se geração mudar; não flexibilizar unilateralmente. Definir ponto de commit do arquivo e corrida imediatamente antes do fechamento; se não demonstrar equivalência, manter spool completo. Não manter transação aberta aguardando Worker/download/stream.

File System Access quando suportado: preservar gesto e permissões, escrita incremental com backpressure, close após verificações finais, abort em erro quando possível. Não chamar arquivo parcial de backup. Blob cap 128 MiB e contabilizar cópias; acima streaming suportado ou lotes, sem concatenar tudo em ArrayBuffer. Blob limitado do ZIP comprimido não é materialização integral descompactada. Limpar spool/descritores próprios em todo resultado. Comparar prepass, spool e híbrido conforme latência, disco e RAM. AFC preserva lineage/sourceManifest; AFS pode reaproveitar bloco validado apenas quando corresponde à sessão solicitada, sem alterar aquisição. JSON disponível.

Testes: dados antes/depois da otimização, restauração byte a byte no mesmo contexto, alterações/exclusões concorrentes durante prepass/escrita/fechamento, corrupção após prepass, digest+índice adulterados, ordem/número de entradas, offsets, limites, 0/3/104/300 e cap; fallback Blob e stream separadamente; cancelamento/quota/falha de destino/limpeza, validação Python independente. Medir leituras/escritas, bytes temporários, CPU/Worker, latência e RAM. Justificar diferenças de bytes legítimas.

**Entregáveis:** HTML, `docs/RELATORIO_21_11_6.md`, contrato de snapshot/prepass/spool, testes de exportação/concorrência/interoperabilidade, A/B e instruções de backup.

**Aceitação:** semântica íntegra, manifesto e bytes verificáveis, nenhuma mistura de revisões, falha segura; redução mensurável de recodificação/I/O/tempo ou justificativa para manter spool. Memória sob orçamento; não confundir disparo do download com salvamento. Rollback restaura spool original sem converter banco.

### 21.11.7 — Otimizações complementares orientadas por medições

**Objetivo:** atacar apenas custos residuais relevantes após 21.11.3–6. Não realizar refatoração geral nem reescrever SECURITY13 por velocidade. Cada hipótese recebe teste A/B e rollback próprio.

| Hipótese | Experimento permitido e condição |
|---|---|
| CBOR / preflight / normalização | Reduzir travessias inequivocamente repetidas sobre bytes/árvore idênticos; preservar preflight de duplicatas, Unicode, profundidade, tamanho/limites antes de alocação, tags 73/77 exclusivamente na grade, -0 e inteiro seguro. Provar equivalência adversarial. |
| JCS / hash semântico | Reduzir recálculo no mesmo registro/contexto provado; preservar canonicalização, ordenação UTF-16, números ECMAScript e domínios; não substituir JCS por hash CBOR. |
| SHA-256 | Benchmark `crypto.subtle.digest('SHA-256', ...)` sobre buffers limitados versus SHA incremental JS por tamanho, frio/quente; detecção de capacidade e fallback incremental quando indisponível/streaming. Não materializar perfil só para WebCrypto; comparar vetores FIPS/extremos e digests independentes. |
| CRC32 | Consolidar apenas passagens sobre bytes idênticos; manter CRC ZIP e SHA. |
| Transfer/clone | Ownership exclusivo comprovado, medir heap/external e pico, não destacar DSP/pending. |
| IndexedDB | Meta reutilizável sob token validado; avaliar cursores/transações com lotes pequenos e tetos explícitos, preparar codec fora da tx; abandonar se aumentar memória ou prejudicar atomicidade/cancelamento. |
| UI / diagnóstico | Reduzir overhead sem perder feedback; nada periódico na afinação. |

Não mudar nível Zstd 3, tornar Int16 obrigatório, reduzir espectro/precisão ou trocar codec sem estudo e revisão explícita. Se segurança/licenças exigirem atualização de biblioteca, tratar separadamente com fixtures, versões e testes. Medir ponta a ponta, não só microbenchmark. Se metas já atingidas, fechar com relatório e nenhuma mudança desnecessária.

**Entregáveis:** HTML se modificado, `docs/RELATORIO_21_11_7.md`, perfis de custo residuais, benchmarks/testes e decisão por hipótese (adotar/rejeitar/adiar com motivo).

**Aceitação:** equivalência semântica e contrato preservados, nenhuma regressão de segurança, otimizações com benefício reproduzível sob orçamento ou justificativa para não alterar. Não promover técnica sem prova.

### 21.11.8 — Revalidação integral antes de 21.12

**Objetivo:** completar todos os gates da validação original 21.11 e as novas condições de UX, desempenho e memória. Não basta o 104 AFP funcionar.

| Grupo | Casos mínimos / critério |
|---|---|
| Corpus | 13 sessões históricas de codec, duas inspeções individuais conforme compatibilidade, fixtures positivas/negativas/extremos, novas sessões físicas, AFP 3/104 representativos; 52/104/208/300 de tamanho representativo e 1.000 pequenos para estresse com cap/falha segura. Distinguir fixtures de medições. |
| Integridade e interop | JS↔Python↔JS, bytes, CRC, hashes, árvore/Float64/-0/Unicode, vínculos/IDs/revisões, AFS/AFP/AFC, codecs/tags aceitos, novo ciclo físico 3/104 e confronto com originais. Nenhuma diferença semântica; diferenças de representação/remapeamento precisam ser justificadas. |
| Segurança | Matriz anterior toda (ZIP/AFB/CBOR/frames/limites/chaves, hashes corretos e semântica forjada, corrupção, vínculos, flags, fontes/lineage), diferencial fast path versus defensivo, alteração de geração, staged/spool adulterados, cancelamento, timeout, quota. |
| Persistência nativa | IndexedDB em origem válida; salvar/ler/editar/excluir, abort, restauração, fechamento/reabertura, interrupção antes/depois commit, recuperação journal, abas/versionchange, quota, legado intacto. |
| Leitura seletiva | Listar sem decode de evidências, abrir/comparar conjunto limitado, 100 ciclos, invalidar cache e liberar referências, curvas/sintetizador com dados necessários e fonte conferida; medir contagem/bytes. |
| Latência/UX | Baseline 21.11.2 versus final no mesmo Chrome/dispositivo, frio/quente, arquivos 3/104 e escala adicional, tempo ativo/fases, mediana/faixa/metas acordadas, feedback, bloqueio/erro/cancelamento e ambos temas. Avaliação explícita do usuário. |
| Memória/lifecycle | Heap, backing/external, WASM, buffers controlados, RSS/processo quando possível; pico import/export, retenção pós-operação/100 ciclos, Worker/URL balanceados; limites, RAM celular por método adequado; não tratar proxy como pico real. |
| Áudio/ferramentas | YIN, pYIN, SWIPE′, Pico, FFT, captura física, revisão, mediana, B, flags, sintetizador, temperamento/nota fixa, curvas e vetos; antes/depois em mesmo contexto, sem banco/codec/sondas na afinação normal. |
| Dispositivos | Chrome físico do usuário, Chromium/Firefox/WebKit em origens suportadas, Android/iOS conforme alvos, offline, CSP real, microfone; registrar versões/bloqueios, não chamar mock de teste nativo. |
| Licença e ciência independente | Procedência/revisão exata do núcleo Zstd, MIT/BSD/notices e build auditável, segurança de dependências, CDDL por ferramenta independente, port integral/adversarial de predicados SECURITY13 em Python e fontes conforme especificação. |

21.6 reportou 181/181 conversões, 18/18 grupos unitários e 15.552/15.552 números confrontados; não portou todos predicados internos. Verificar estado posterior nos relatórios 21.7–21.11 e ferramentas atuais. Python é complementar; validar importação no navegador. Se port completo/CDDL exigir trabalho adicional, manter gate e planejar correção isolada; eventual redefinição exige decisão explícita, não revogação implícita. Resolver licenças antes da publicação definitiva.

**Protocolo físico:** mesmo celular/Chrome/arquivos, modelo/SO/versões anotados se possível. Backup; importar 3/104, observar fases, verificar bloqueio de toque repetido, exportar e enviar JSONs de desempenho e AFP reexportados. Cancelar importação de teste sem afetar perfis anteriores; fechar completamente e reabrir na mesma origem/backend, conferir lista, acessar e comparar sessões; realizar aquisição real de uma nota/sessão, salvar e exportar AFS, verificar interop e áudio. Medir RAM conforme método da 21.11.2; se indisponível, declarar bloqueio. Receber avaliação do usuário; repetir após correções críticas. Estresse 1.000 não precisa ocorrer no celular, registrar ambiente/falha segura.

**Entregáveis:** HTML candidato experimental, `docs/RELATORIO_VALIDACAO_21.md` e `docs/PROTOCOLO_TESTES_MOBILE.md` consolidados, matriz de gates com evidência/arquivo/hash/ambiente, CSV/JSON e testes de regressão, ferramentas Python/documentação atualizadas onde necessário, checklist de backup/rollback comprovado. Repetir scripts do LEIA-ME com baseline/pacotes corretos e testes novos; registrar incompatibilidades, não reconstruir HTML final de build histórico. Se arquivos históricos faltarem, solicitar precisamente, não alegar execução.

**Aceitação:** toda condição crítica original e novas condições aprovadas; metas acordadas em 21.11.2 cumpridas em ambiente real, usuário aprova UX, memória/estabilidade demonstradas, sem regressão acústica/semântica/segurança, licenças prontas. Solicitar autorização explícita para 21.12 somente após apresentar matriz final. Senão manter JSON padrão e retornar à subetapa responsável. Não apagar banco ou mudar backend padrão para encerrar roadmap.

### 21.12 — Transição definitiva e limpeza arquitetural

**Objetivo:** promover o backend novo após validação completa, sem pressupor migração universal do histórico.

**Implementação:** oferecer backup/exportação e verificar restaurabilidade dos dados que o usuário deseja preservar; documentar conversão dos JSONs existentes. Ativar novo backend como principal apenas após concordância explícita e aprovação integral da 21.11 e 21.11.1–21.11.8. Não iniciar enquanto qualquer gate obrigatório permanecer aberto. Desativar caminhos antigos que se tornaram obsoletos, identificando funções compartilhadas antes de remover. Não apagar IndexedDB legado automaticamente; eventual exclusão exige ação consciente e separada. Preservar ferramenta externa de conversão para JSON e documentar opções de rollback, incluindo recuperar HTML 20.11 e dados antigos. Atualizar ajuda, README, guia e licenças. Revisar tamanho final, CSP, Workers, schema, versões e todas as instruções.

**Entregáveis:** `index.html` final autocontido, `README.md`, `GUIA_DE_USO.md` atualizado, documentos e esquemas consolidados, ferramentas Python, testes/fixtures e notas da versão com limitações e recuperação.

**Aceitação:** nova arquitetura é a principal e não requer o legado em operação normal; equivalência, segurança e escalabilidade aprovadas; documentação suficiente para desenvolvedor independente; backup e rollback demonstrados; nenhuma remoção de dependência compartilhada ou alteração acústica incidental.

## 6. Estratégia de transição e rollback

| Período | JSON e IndexedDB legado | Sistema binário |
|---|---|---|
| 21.1–21.3 | Principal; baseline intocado | Auditoria, benchmark e especificação |
| 21.4–21.6 | Principal | Codec e ferramentas independentes, experimentais |
| 21.7–21.8 | Principal | Banco paralelo, gravação opt-in e leitura seletiva |
| 21.9–21.10 | Disponível e principal por padrão | Fluxo completo experimental |
| 21.11 e 21.11.1–21.11.8 | Principal por padrão; referência de equivalência e fallback | Validação parcial, correções de UX e desempenho, revalidação |
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
| Tempo de gravação/leitura | Metas quantitativas acordadas em 21.11.2 e aprovadas em 21.11.8, no dispositivo real; não extrapolar tempos desktop |
| Progresso e cancelamento | Feedback imediato visível, progresso real/indeterminado, exclusão mútua, cancelamento, cleanup e resultado inequívoco |
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
│   ├── PROTOCOLO_DESEMPENHO_MOBILE.md
│   ├── MATRIZ_EQUIVALENCIA_VALIDACAO.md
│   ├── RELATORIO_21_11_1.md … RELATORIO_21_11_7.md
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

- `index.html` de partida para 21.11.1 (21.10, entregue na 21.11), 1,858,761 bytes, SHA-256 `8c479898c1f2118508529e90dce9b8add8b48cf9b53b04c9ad722a89b8ba35b6`. Preservar cópia exata antes de qualquer alteração.
- `LEIA-ME.md` da 21.11, com comandos de reprodução, distinção de testes nativos/modelos e bloqueios. Recuperar pacote completo 21.11 e código/testes das etapas 21.7–21.10 quando necessários; não reconstruir HTML com build antigo.
- `ETAPA_21_3_ESPECIFICACAO.zip`, `ETAPA_21_6_FERRAMENTAS_PYTHON.zip`: contrato, relatórios, schemas, ferramentas e fixtures; preservar também pacotes 21.2/21.4/21.5 e bibliotecas pinadas originais se houver mudança no build.
- AFP originais/reexportados de 3 e 104 sessões: obter as quatro cópias e checksums antes de repetir validação diferencial; não usar perfis representativos como dados físicos. Preservar JSONs de diagnóstico quando produzidos.

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

1. Anexar este roadmap, o HTML correspondente à última subetapa entregue e seu LEIA-ME/relatório; conferir versão e SHA. Anexar apenas pacotes, fixtures e corpus requeridos para os testes da próxima etapa. Não pressupor acesso a anexos de outro chat.
2. Informar última etapa entregue, aprovações e pendências efetivamente comprovadas. Executar uma subetapa por vez; documentar mudanças, invariantes, testes executados/não executados, resultados e rollback. Não presumir encerramento de gates históricos.
3. Atualizar a matriz abaixo e entregar o HTML autocontido quando houver alterações. Guardar cópias de referência e relatórios; não sobrescrever dados ou baseline. Validar fisicamente quando necessário.
4. Não iniciar 21.12 nem promover o binário sem cumprir 21.11.8 e obter concordância explícita.

Mensagem sugerida para nova conversa:

> Este é o projeto Afinador. Estou anexando o roadmap revisado pós-validação móvel, o HTML e o LEIA-ME da 21.11. Execute a próxima subetapa registrada na matriz (atualmente 21.11.1), mantendo JSON padrão, contrato AFB 1.0, segurança, memória e DSP. Entregue HTML completo e testes/relatório; não avance sem revisão. Não confunda resultados de testes históricos com aprovação de produção.

### 9.4. Registro de progresso atual (atualizar a cada entrega)

| Subetapa | Estado em 20/11/2026 | Evidência / condição |
|---|---|---|
| 21.1 | Entregue experimental | Auditoria e corpus, registro histórico; pendências dinâmicas a conferir |
| 21.2 | Entregue experimental | Benchmark com bibliotecas reais e escolha técnica, gates móveis/licença |
| 21.3 | Entregue | Contrato AFB 1.0; CDDL independente a confirmar |
| 21.4 | Entregue experimental | Codec, testes documentados; não aprovação de produção |
| 21.5 | Entregue experimental | Envelope, Worker e WASM; custos/ram/licenças |
| 21.6 | Entregue experimental | CLI, interop; paridade integral Python pendente nos documentos |
| 21.7 | Implementação presente no HTML | Repositório modular; relatórios completos não reenviados |
| 21.8 | Implementação presente no HTML | Acesso seletivo; gates nativos/memória a confirmar |
| 21.9 | Implementação presente no HTML | Integração experimental; testes completos a recuperar |
| 21.10 | Implementação presente no HTML | Intercâmbio; feedback de progresso insuficiente |
| 21.11 | Validação parcial, gate aberto | Igualdade binária relatada 3/104; latência e UX reprovadas, demais pendências |
| 21.11.1 | Implementação entregue; gate aberto | Modal, cancelamento e exclusão mútua; UI e modelo aprovados nos cenários testados; validação nativa 3/104 e móvel pendente |
| 21.11.2 | Não iniciada | Instrumentação e benchmark móvel |
| 21.11.3 | Não iniciada | Reutilização controlada Worker/WASM |
| 21.11.4 | Não iniciada | Equivalência e redundâncias defensivas |
| 21.11.5 | Não iniciada | Reuso de blocos validado na importação |
| 21.11.6 | Não iniciada | Exportação incremental e spool |
| 21.11.7 | Não iniciada | Otimizações complementares conforme dados |
| 21.11.8 | Não iniciada | Revalidação integral, matriz de gates |
| 21.12 | Bloqueada | Aprovação integral + concordância do usuário |

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

A revisão não reexecuta benchmarks, não altera HTML ou formatos e não declara subetapas aprovadas para produção. CBOR + Zstd 3 e o contrato AFB 1.0 estão estabelecidos para o backend experimental; não se reabre a escolha sem nova evidência. Os valores de latência, pico real de RAM, tamanho seguro de lote e ganhos de reutilização ainda não foram medidos em celular. Não presumir que a arquitetura de Worker por lote ou o prepass são necessariamente mais rápidos ou seguros. Os novos critérios explicitam como decidir.

Ainda recuperar relatórios 21.7–21.11 e ferramentas atualizadas para verificar se pendências históricas foram encerradas: paridade integral SECURITY13 em Python, CDDL independente, procedência/licenças exatas WASM, IndexedDB nativo, testes multiplataforma, pico de RAM, persistência, comparação seletiva, regressão acústica física e aquisição/exportação AFS. O relato do usuário confirma responsividade percebida e sucesso de importação/exportação, não timings, RAM ou encerramento dessas pendências. Não remover gates por falta de evidência.

## 12. Registros históricos de execução (21.1–21.6)

Os registros seguintes são preservados da versão 21.6 do roadmap e descrevem o estado da época. Suas instruções de próxima etapa e bloqueios históricos não substituem a matriz atual 9.4; pendências não comprovadamente encerradas continuam no gate 21.11.8.

### Adendo — execução da subetapa 21.1

Baseline 20.11 inalterada (1.360.798 bytes, SHA-256 já registrado em 9.1). Entregas: `AUDITORIA_ARQUITETURAL.md`, `MAPA_DE_DEPENDENCIAS.md`, `evidencias/baseline.json`, `modulos.csv`, `ocorrencias_estaticas.csv`, `sessoes.csv`, `secoes.csv`, `campos_observados.csv`, `duplicacoes_observadas.csv`, `testes_baseline.json`, scripts `auditar.py` e `testar_baseline.py`. Corpus original de 13 sessões (188 execuções, 177 elegíveis) e duas inspeções individuais, hashes registrados no baseline. Nenhum arquivo de dados original modificado.

#### Achados que passam a orientar as próximas subetapas

- São dois bancos acústicos, três pontos de abertura e oito `getAll` (não só o carregamento em Perfis). Incluir histórico de curvas 4B, emissor, ponte de leitura e reprodução de aplicação 5. `project` da 4A já delimita a projeção canônica usada no motor. O novo caminho deverá verificá-la incrementalmente, sem carregar todas as evidências.
- `recordId` não inclui `profileId`; preservar identidade em chave composta. `sessionHash` e `baseSnapshotHash` têm significados distintos; SHA-256/JCS semântico não pode ser substituído por hash do CBOR. O índice deve estar vinculado à geração/revisão e às evidências, não tem autoridade isolada. `discardedFromModeling` e `note` são metadados editáveis. Preservar atomicidade, pós-commit, cancelamentos, integridade entre abas, `sourceManifest`, reprodução exata e aprovação experimental.
- A memória da sessão ativa permanece sob as regras acústicas atuais. A nova persistência deve limitar o custo incremental de leitura e escrita; não confundir orçamento estimado por JSON com heap medido. `pending`, `recent` e versões temporárias podem manter trabalho intencionalmente: não apagar sem consentimento ou commit.
- O benchmark 21.2 deve incluir estruturas normais e `Int16` da grade existente, sem mudar resolução/quantização, reconstruindo arrays legados no round-trip. A escolha CBOR + Zstandard 3 continua provisória. Verificar Worker, CSP, memória linear, cold/warm, tamanho embutido, compatibilidade, licença, inicialização e encerramento. Nenhum codec foi escolhido definitivamente nesta auditoria.
- Manter biblioteca musical, preferências locais e diagnóstico técnico separados da persistência acústica; a especificação 21.3 decidirá o escopo de formatos auxiliares sem regressão. Não reintroduzir DPX.

#### Gate e pendências

Sintaxe dos 21 scripts e hashes CSP conferidos. O `SECURITY13` original aceitou os 13 JSONs no teste de parse/envelope isolado; isso não comprova hash de sessão nem importação completa no IndexedDB. Chromium 144 neste ambiente bloqueou navegação (ERR_BLOCKED_BY_ADMINISTRATOR); teste de UI e banco original pendente, sem diagnóstico de falha do app. Repetir o script de smoke em navegador acessível antes de assumir baseline dinâmico; rodar benchmark real JS/WASM antes da decisão de codec. Guardar os resultados novos separadamente; a 21.2 não deve avançar para a especificação se o teste de navegador estiver bloqueado.

A 21.1 não modifica HTML, não migra dados e não altera política física. Aprovação do usuário ainda necessária para encerrar esta entrega e prosseguir para 21.2.

### Registro de execução — 21.2 (parcial, gate aberto)

A 21.2 foi iniciada após a solicitação expressa do usuário. Base 20.11 e corpus intactos; relatório `BENCHMARK_FINAL.md` e pacote `ETAPA_21_2_BENCHMARK.zip`. Foram aprovados 880 round-trips em Node (compressão nativa, não WASM), 176 em Chromium Worker (sem compressão/GZIP), 39 testes interop JS→Python. Projeção CBOR/GZIP no Chromium 37,44 MB/104 cordas; CBOR/Zstd 3 no Node 30,00 MB, CBOR-Int16/Zstd 3 29,38 MB. Candidato CBOR + Zstd 3 permanece provisório; CBOR/GZIP é alternativa comprovada no protótipo. Não adotado nenhum codec em produção. DNS do registro npm indisponível; pacote Zstd WASM e bibliotecas JS mantidas não obtidos. Teste de WASM vazio e Worker passou com CSP, não equivale a teste do compressor. IDB e navegação em origem válida bloqueados, mobile e RAM linear/pico pendentes. **Não avançar 21.3.** Completar benchmark com bundle real, testes de interoperabilidade bidirecional, medições de memória/I/O e protocolo móvel antes de fechar decisão, conforme gate da 21.2. Nenhuma alteração no HTML estável.


### Registro de execução — 21.2 complementação com bibliotecas reais (supera o registro parcial acima)

As três distribuições pinadas fornecidas pelo usuário permitiram testar CBOR-X 1.6.6, MessagePack 3.1.3 e @bokuweb/zstd-wasm 0.0.27. HTML 20.11 e 13 sessões confirmados contra hashes 21.1. 440/440 round-trips em Chromium Worker com CSP/offline e 78/78 testes bidirecionais entre mesmo bundle JS/WASM em Node e Python/libzstd. CBOR/Zstd3: 29,18 MB/104 cordas, 13,70 ms gravação e 9,45 ms leitura (sem I/O); CBOR/GZIP: 37,44 MB, 39,60/12,85 ms; JSON/GZIP: 41,39 MB, 73,65/14,85 ms. Zstd9: 27,84 MB, compressão 34,30 ms contra 7,10 ms do nível 3. Int16 seletivo economiza apenas 0,54 MB. Decisão de engenharia proposta para especificação: CBOR convencional sem tags proprietárias + Zstd nível 3; GZIP explícito como alternativa, Int16 seletivo opcional. Não consolidar um envelope nesta subetapa. Não iniciar 21.3 sem aprovação do usuário.

O WASM recebido declara 16,125 MiB iniciais / 2 GiB máximo; benchmark altera apenas limite da seção de memória e glue para máximo de 32 MiB. Capacidade ficou 16,125 MiB em todo corpus; crescimento para 513 páginas rejeitado no teste Node. Protótipo copia entrada/saída e libera malloc, examina janela/tamanho/frame, rejeitou cinco casos de frame inválido. Esses não são validadores de produção. Payload bruto CBOR+WASM/glue de 379.037 bytes; lazy Worker requerido. Segurança completa, schema, limites de buffer e cache, hash, importação e atomicidade a especificar/implementar. CBOR-X int64AsNumber só funciona sem perda com inteiro seguro; testar domínio antes de conversão. Os 13 JSONs não têm inteiros inseguros nem -0; testes sintéticos mostram -0 normalizado por todos os encoders testados; definir e testar explicitamente política de zero/sinal e extremos em 21.3/21.4. Não confundir sucesso do corpus com suporte a todas as entradas.

Pendências ainda abertas: IndexedDB (origem normal bloqueada por ERR_BLOCKED_BY_ADMINISTRATOR; SecurityError na origem opaca), heap/external/pico exclusivo do Worker e memória mobile (RSS somado apenas amostrado), outros navegadores, Brotli WASM secundário não testado, revisão exata e notices MIT/BSD do Zstd não presentes no pacote. Documentar fonte/licença/procedência antes de publicar; não afirmar binário auditado. O gate central WASM foi superado. Entregue 21.2 para revisão, não aprovação final de produção. Próxima 21.3 condicionada à decisão explícita do usuário sobre passagem à especificação com estes gates ainda abertos; completar protocolos móveis/I/O e licenças antes do corte definitivo e não relaxar segurança. Nenhuma modificação no Afinador, no armazenamento legado ou no DSP. Pacote `ETAPA_21_2_COMPLEMENTO_WASM.zip`, relatório atual `BENCHMARK_FINAL.md`, relatório preliminar arquivado e scripts reproduzíveis. O benchmark mobile agora já contém o Zstandard real.


### Registro de execução — 21.3 (contrato formal para revisão)

Solicitação expressa do usuário autoriza iniciar a 21.3 com as pendências 21.2 registradas. Ficam escolhidos para a especificação CBOR-X 1.6.6 com mapa convencional, Zstandard nível 3 em WASM, GZIP explícito como alternativa, Int16 seletivo opcional. Não autoriza publicação nem modifica o HTML.

- Formato AFB 1.0: cabeçalho fixo de 128 bytes em big-endian com três hashes SHA-256; chunks independentes de 2 MiB; máximo 32 MiB CBOR lógico por objeto; ZIP STORE clássico para perfil e histórico, manifesto primeiro, caminhos numéricos fixos; AFS sessão única. Não confundir hashes semânticos JCS com hashes de transporte. Não exigir CBOR canônico.
- Semântica: formato legado v1, chaves e IDs preservados, número seguro/float64, -0 explicitamente preservado via float64 (JCS continua normalizando); rejeitar não finitos, inteiros fora da faixa exata, duplicatas, chaves perigosas. Tags RFC 8746 73/77 apenas em spectrumGrid202.values, sem perda de resolução, mediana preservada.
- Segurança: 2 MiB janela Zstd, 32 MiB memória linear WASM (experimental), 1 GiB ZIP, 8 GiB soma raw, 2.000 registros/128 revisões, 4.002 entradas, caps de árvore originais por registro/objeto. Fallback Blob 128 MiB. Uma tarefa pesada ativa, cache lógico por bytes, sessão não salva protegida; números de runtime a aferir.
- Arquitetura de repositorio: novo IndexedDB separado, índices paginados, evidence/headers imutáveis por revisão, projeções derivadas, staging/geração e spool, notificação após commit. Manter validadores originais e reprodução de fontes; nenhuma mudança na aprovação de curvas.
- Entregues FORMATO, SCHEMA, VERSIONAMENTO, SEGURANCA_FORMATO, ARQUITETURA_ARMAZENAMENTO, esquemas CDDL e referências estáticas dos validadores, inventário de 1.713 caminhos (incluindo raiz), 54 mapas/562 ocorrências de campos estruturais, fixtures sintéticas, scripts e resultados. 13/13 verificações estruturais de corpus no verificador de subconjunto, 26/26 round-trips Python com AFB/Zstd (13 normais e 13 Int16), 8/8 fixtures positivas e 5/5 negativas em leitura JS independente, 5/5 verificações dos validadores originais sobre fixtures. O teste JS usa CBOR-X e compressores nativos do Node, não repete benchmark WASM.
- Pendências específicas: compilação/validação CDDL por ferramenta externa indisponível neste ambiente; mapas internos livres mantêm predicados do legado; catálogo de unidades não inventa unidades não documentadas. Fixtures são prova de bytes/leitura, não provas de segurança completa ou aprovação física. Preflight completo, writer/reader 21.4, encoder -0, JCS em Python, envelopes comprimidos no Worker 21.5, protocolo móvel/I/O e licenças continuam gates. Excesso de 32 MiB CBOR lógico não deve ser truncado; preservar JSON e tratar evolução.

21.3 entregue para revisão técnica; 21.4 é a próxima etapa de implementação isolada de serialização. Não declarar 21.3 aprovada para produção antes dos testes de implementação. Nenhum algoritmo acústico ou persistência antiga alterado.


### Registro de execução — 21.4

Implementado `AFB21Codec` no `index.html`, com CBOR-X 1.6.6 incorporado no-eval e inicialização por `create()` explícita. Módulo experimental de CBOR bruto, sem envelope, Zstd, Worker, I/O ou acesso a IndexedDB; JSON permanece principal. Inteiros seguros, float64, -0, Unicode, mapas sem protótipo, preflight defensivo, arrays Int16 opcionais exclusivamente na grade. Patches mínimos reproduzíveis: preservação de -0, BOM UTF-8, correção de leitura de inteiros negativos 64-bit em Number. Licença MIT incorporada; SHA do pacote pinado. O formato AFB 1.0 permanece inalterado.

148/148 casos Node (26 round-trips reais, 12 positivos, 102 negativos, 8 fixtures); 26/26 round-trips Chromium offline em conteúdo integral; 52/52 interop bidirecional com Python de referência da 21.3. 22/22 scripts executáveis válidos e CSP; 40 scripts anteriores preservados byte a byte. A comparação de texto inicial e em quatro ferramentas passou; localhost bloqueado, sem teste de IndexedDB/microfone. O HTML novo é a baseline para 21.5, e 20.11 continua referência estável. Relatório `RELATORIO_VALIDACAO_21_4.md` e pacote `ETAPA_21_4_CODEC.zip`.

Aceitação experimental para revisão: gates de CDDL independente, segurança completa de importação, validação de hashes e relações entre blocos, pico RAM móvel, testes em origem válida e revisão/licença do Zstd continuam abertos. Não usar a API de árvore genérica como autorização de importação. Próxima 21.5: compressão limitada, envelope e Worker de armazenamento, sem desativar JSON. Não alterar DSP, persistência legada ou autorização de curvas.

### Registro de execução — 21.5

Implementado pipeline por bloco AFB 1.0 em `AFB21Storage` + Worker dedicado, com CBOR-X anterior, Zstd WASM real 0.0.27 nível 3, GZIP explícito e STORE, header 128 B, chunks independentes de 2 MiB, três SHA-256 incrementais, preflight Zstd e GZIP/DEFLATE antes de descompactar, CRC32/ISIZE e tamanhos exatos. Limites: 32 MiB CBOR, 34 MiB payload, 32 MiB memória linear WASM; manifestos STORE e <=2 MiB. Nenhum novo caminho de importação/UI/IndexedDB, nenhum fallback silencioso e nenhuma alteração dos contratos acústicos. A API de baixo nível não autoriza fonte ou curva. One-shot Worker (uma operação ativa, sem fila, timeout máximo 30s, ID/protocolo, AbortSignal/cancel e teardown em sucesso/erro); WASM lazy somente no codec 1. Codec 214 original intacto, 41 scripts anteriores idênticos; 23/23 sintaxe e CSP. HTML final 1.772.241 B SHA-256 `06548933cebf1d7685e45f745470fa1a447f8c42cdad5c3c1e11c11055e10793`.

208/208 Node (78 roundtrips corpus nos 3 codecs e dois modos CBOR, 130 demais, 45 rejeições esperadas incluídas), 26/26 corpus Chromium Zstd, 20/20 casos adicionais no HTML integral, 39/39 interoperabilidade direcional Python. Total 293/293 casos. 98 Workers e 98 URLs revogados; heap principal estável em 12 ciclos após GC, capacidade linear 16,125 MiB; **não** é medição de RSS/pico real Worker/mobile. Projeção 104 cordas 29,195 MB AFB comum ou 28,650 MB Int16, sem overhead contêiner/meta; tempo cliente pipeline Zstd completo mediano 375,3/229,5 ms encode/decode (corpus 13, desktop, sem IndexedDB), superior ao microbenchmark 21.2 em latência por causa de validação, hashing, clone e inicialização one-shot, não relaxar segurança para acelerar. Medir e otimizar custos nas próximas etapas. Localhost bloqueado; Chromium fallback offline origem opaca, texto inicial e das quatro ferramentas igual, CSP bloqueou script não autorizado, não validou microfone ou IDB. `RELATORIO_VALIDACAO_21_5.md`, `LICENCAS_E_PROCEDENCIA_21_5.md`, resultados e scripts em `ETAPA_21_5_COMPRESSAO.zip`. Licenças Zstd/revisão núcleo, CDDL independente, integridade semântica entre blocos, importador ZIP, memória total/mobile e I/O permanecem gates para produção. 21.5 entregue para revisão experimental; 21.6 é a próxima, CLI independente rigorosa Python sobre contrato AFB e ZIP, não reutilizar leitor de fixtures como leitor não confiável. JSON continua principal até gate 21.12.


### Registro de execução — 21.6

Entregues ferramentas científicas autônomas Python em `ETAPA_21_6_FERRAMENTAS_PYTHON.zip`: `codec.py`, `semantics.py`, `archive.py`, `cli.py`, `encode.py`, `decode.py`, `inspect_file.py`, `validate.py`, `convert.py`, documentação, requisitos, schemas e fixtures. HTML 21.5 integralmente preservado; JSON e DSP inalterados. Zstd 3 via libzstd de sistema (1.5.7 testado), CBOR próprio com preflight, GZIP limitado, STORE, Int16 73/77 e -0, envelope AFB 1.0 invariável. Acesso seletivo ao ZIP, manifesto e headers antes dos payloads, spool em disco, exportação JSON incremental e escrita temporária com publicação ao final. Entrada JSON legado limitada a 32 MiB. Sem dependência pip, sem execução do HTML para utilizar CLI.

Validação: 78/78 ida-e-volta Python, 78/78 Python→JS/WASM congelado 21.5 (SECURITY13 original e hashes JCS), 13/13 AFS JS anteriores→Python; 12/12 testes adicionais do escritor JS com Red Brass e extremos sintéticos nos seis modos. 181 conversões; 18/18 grupos unitários; 15.552/15.552 números confrontados contra JSON.stringify. Teste de perfis e revisões com fixtures; 104 registros sintéticos pequenos, acesso seletivo e reconstrução. Não é benchmark de RAM ou perfil gravado integralmente em mobile. Projeção 104 cordas 29,196 MB normal/28,654 MB Int16. Relatório `RELATORIO_VALIDACAO_21_6.md`, instruções `tools/README.md`, resultados e provas.

Gate ainda aberto: port integral dos predicados internos SECURITY13 e equivalência adversarial de validadores Python/JS (não basta CDDL e hash), ferramenta CDDL independente, histórias reais de curvas e conferência de fontes externas, compatibilidade multi-SO. `validate` é verificador de transporte, estrutura e vínculos implementados, não autorização de importação ou aplicação de curva. Comparação JCS no domínio ensaiado não é certificação exaustiva. 21.6 entregue experimentalmente para revisão, não promoção definitiva. 21.7 é próxima no roadmap, IndexedDB modular isolado, aplicando obrigatoriamente validadores originais JS; manter as pendências como gates da 21.11/21.12, além dos testes de banco, RAM, mobile e licenças WASM.


## Registro de execução — 21.11.1 (20/11/2026)

HTML experimental entregue, sem otimização de desempenho. A referência anterior 21.10 continua sendo a baseline para comparação e rollback. A implementação passou por testes de interface em origem opaca e por testes de integração do ZIP real com codec e repositório modelados. Localhost e file foram bloqueados por política do ambiente; não foram repetidos os AFP reais 3/104. Gate permanece aberto, conforme `docs/RELATORIO_21_11_1.md` e `docs/PROTOCOLO_TESTE_MOBILE_21_11_1.md`. Não iniciar 21.11.2 nem promover backend antes de avaliação do usuário. As seções anteriores relativas à revisão documental original conservam seu sentido histórico.
