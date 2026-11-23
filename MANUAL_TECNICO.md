# Manual técnico — Afinador · Oficina Pernambuco

[README do projeto](README.md) · [Guia de uso](GUIA_DE_USO.md)

Referência única para manutenção do aplicativo, formatos de intercâmbio, persistência, validação, ferramentas Python e interoperabilidade. O `index.html` é a referência executável para os predicados completos de aceitação e autorização de curvas. AFB 1.0 e schemaVersion 1 identificam contratos de dados, não etapas de desenvolvimento.

## Sumário

1. [Formato de intercâmbio](#formato)
2. [Modelo semântico e schemas](#modelo)
3. [Segurança e limites](#seguranca)
4. [Arquitetura de armazenamento](#armazenamento)
5. [Versionamento](#versionamento)
6. [Ferramentas Python](#python)
7. [Fixtures e verificação](#verificacao)
8. [Licenças e procedência](#licencas)

## Organização e uso

| Local | Finalidade |
|---|---|
| `schemas/` | Sete CDDL: definições comuns, envelope, manifesto, perfil, sessão, curva e mapas detalhados. Manter todos, inclusive `legacy-maps.cddl`, utilizado diretamente por `tools/semantics.py`. |
| `docs/DICIONARIO_CAMPOS.csv` | Inventário auxiliar de caminhos e unidades observados; não é schema exaustivo. |
| `tools/` | CLI Python independente do aplicativo e requisitos de execução. |
| `fixtures/` e `tests/` | Exemplos sintéticos, hashes e testes reproduzíveis. |
| `docs/NOTICE_LIBZSTD_SISTEMA.txt` | Avisos originais de licença da biblioteca de sistema, preservados integralmente. |
| `SHA256SUMS` | Integridade do pacote consolidado. |

Mantenha `tools/`, `schemas/` e `fixtures/` no mesmo diretório pai. Esses recursos não são necessários para executar o aplicativo no GitHub Pages. O HTML não é duplicado aqui. A CLI valida apenas parte da semântica; não autoriza curvas e não substitui o aplicativo. A procedência completa do Zstd WASM é uma pendência de redistribuição (ver [Licenças](#licencas)).


<a id="formato"></a>
## 1. Formato de intercâmbio AFB 1.0

**Contrato de intercâmbio AFB 1.0.** Leia em conjunto com os capítulos [Modelo semântico](#modelo), [Versionamento](#versionamento), [Segurança](#seguranca) e os CDDL. O transporte binário está implementado no aplicativo; esta especificação não certifica as regras acústicas, a segurança completa ou a interoperabilidade de todo arquivo possível. Ver também as limitações da [CLI](#python).

### 1. Decisão tecnológica

CBOR RFC 8949 (CBOR-X 1.6.6, sem extensões próprias), Zstandard RFC 8878 nível 3 como escritor principal, GZIP RFC 1952 alternativa explícita, ZIP STORE como contêiner de perfil/histórico. RFC 8746 Int16 opcional exclusivamente para grade espectral. Inteiros seguros JS, float64 e zeros com sinal conforme o capítulo [Modelo semântico](#modelo). Bibliotecas pinadas, WASM isolado até 32 MiB; desempenho depende do dispositivo e dos dados. Sem Base64 nos dados. Base64 somente para incorporar código WASM no HTML, se necessário.

### 2. Três arquivos de intercâmbio e blocos internos

| Extensão | Formato exterior | Conteúdo |
|---|---|---|
| `.afs` | bloco AFB 1.0 | uma sessão completa (objeto legado `afinador.acquisition-session` v1) |
| `.afp` | ZIP clássico STORE | manifesto, metadado de perfil, pares cabeçalho de registro + sessão |
| `.afc` | ZIP clássico STORE | manifesto e revisões completas de uma exportação de histórico de curvas |
| `.afb` | bloco AFB 1.0 | extensão interna; não é novo tipo de importação pela UI |

`.afc` conserva inclusive histórico de várias linhagens, como exportação atual; uma revisão é um histórico de tamanho 1, sujeito às mesmas regras de ancestralidade do legado. `.afp` mantém `curves: []` no objeto legado reconstruído; não mistura o banco de curvas no perfil. As preferências, biblioteca musical, inspeção individual e diagnósticos técnicos independentes continuam em seu caminho atual. Arquivos são dados, não executáveis. Reconhecer por magic e tipo interno, não pela extensão.

### 3. Envelope AFB 1.0 (todos os inteiros do envelope, big-endian, unsigned)

Offset zero; bytes exatos; sem padding implícito. Tamanho do cabeçalho = 128 bytes. A assinatura ASCII é `AFBLOCK\n` (hex `41 46 42 4c 4f 43 4b 0a`).

| Offset | Bytes | Campo | Regra |
|---:|---:|---|---|
| 0 | 8 | magic | acima |
| 8 | 2 | major | 1 |
| 10 | 2 | minor | 0 |
| 12 | 1 | kind | 1 sessão, 2 perfil, 3 cabeçalho de registro, 4 revisão de curva, 5 manifesto de perfil, 6 manifesto de curvas |
| 13 | 1 | codec | 0 STORE (sem compressão), 1 Zstandard, 2 GZIP |
| 14 | 2 | flags | zero |
| 16 | 4 | rawLength | total de bytes CBOR descomprimidos, 1..32 MiB |
| 20 | 4 | payloadLength | total de bytes após cabeçalho, incluindo cabeçalhos de chunks, 1..34 MiB |
| 24 | 4 | chunkCount | ceil(rawLength / 2.097.152), 1..16 |
| 28 | 4 | reserved | zero |
| 32 | 32 | rawSHA256 | SHA-256 dos bytes CBOR concatenados, binário, não texto |
| 64 | 32 | payloadSHA256 | SHA-256 de todos os bytes após offset 128 |
| 96 | 32 | headerSHA256 | SHA-256 dos bytes 0..95 inclusive |

O tamanho total deve ser exatamente 128 + payloadLength. Rejeitar truncamento e sufixos. `kind` seleciona CDDL e validadores; não utilizar informações de uma extensão de arquivo para escolher o validador. Hashes não são assinaturas de autoria. Não há nonce, chave ou metadado temporal no envelope. Identidade e versão semântica ficam nos objetos CBOR.

#### 3.1. Payload em chunks

Repete-se `u32 rawChunkLength || u32 storedChunkLength || storedBytes` por chunk, sem padding. Cada chunk menos o último tem exatamente 2 MiB de bytes CBOR descomprimidos. Último tem o resto, ou 2 MiB se divisível. Cada storedChunkLength: 1..2 MiB+64 KiB. Codec único por envelope. Cada chunk é independente: STORE exige igualdade dos tamanhos; Zstd um frame ordinário com content size presente, igual a rawChunkLength, janela <=2 MiB, sem dicionário, sem frames skippable/concatenados; GZIP um único membro RFC 1952, CM=8, FLG=0, CRC32 e ISIZE conferidos, DEFLATE completo sem bytes restantes. Nível 3 é política do codificador, não um campo inferível dos frames; leitores não dependem de nível. GZIP writer usa MTIME=0, demais campos permitidos pela RFC/lê sem inferir nível. Checksum Zstd opcional; quando presente deve validar. Sem compressão de segunda camada. Codec 0 permitido para pequenas estruturas e testes/contingência explícita, não fallback silencioso.

Exemplo de leitura: validar cabeçalho e cap, percorrer limites de todos os chunks sem alocação dos tamanhos declarados, conferir payloadSHA256 de forma incremental, descomprimir cada chunk com limite, conferir rawSHA256, preflight CBOR antes de decodificar, normalizar tipos, validar semântica. Chunks dividem bytes, não objetos CBOR; fronteira pode cair dentro de um valor. Uma sessão continua unidade lógica completa. Não alegar acesso aleatório a uma execução dentro do bloco; o acesso aleatório é por sessão/revisão. Suporte a sessão que exceda 32 MiB CBOR requer evolução de schema/particionamento lógico: em 1.0 rejeitar com aviso e preservar o JSON legado, nunca truncar. Limite não substitui limites de nós e semânticos.

### 4. Perfil e histórico ZIP

ZIP APPNOTE método 0 (STORE), sem criptografia, sem ZIP64, sem multi-disco, sem data descriptor, sem extras, sem comentário, nomes ASCII; central directory e cabeçalhos locais devem corresponder exatamente em nomes, tamanhos, CRC, flags e offsets. UTF-8 flag pode ser 0 ou bit 11; demais flags zero. ZIP version needed <=20, writer 20; sem symlinks/diretórios/links. Sem prefixo, lacunas, sobreposição, sufixo ou entradas ocultas; primeiro local header offset 0, central directory após a última entrada, EOCD encerra o arquivo. CRC32 ZIP validado também, mas não substitui SHA-256. Cap do arquivo 1 GiB; soma rawLength <=8 GiB; até 2.000 registros por perfil, até 128 revisões por histórico; cap de 4.002 entradas (manifesto+perfil+2 por registro). Sem ZIP64 dentro desses limites.

Manifesto é a primeira entrada local e central, `manifest.afb`, kind 5 ou 6, codec 0, raw <=2 MiB. Manifesto é CBOR e segue `manifest.cddl`; inclui schema identificador próprio, schemaVersion=1, identificador de perfil (quando aplicável), lista `entries` na mesma ordem que as entradas ZIP após manifesto. Cada entrada: path, kind, id semântico, bytes (comprimento de AFB inteiro), rawBytes (rawLength), sha256 (64 hex minúsculos do AFB inteiro). Não há referência a si próprio. Hash do manifesto no próprio envelope. Campos completos do manifesto em CDDL. Nenhuma entrada fora da lista; ids e hashes conferidos após decodificação dos blocos.

#### 4.1. Nomes e ordem exatos

Perfil: `profile.afb` tipo 2 (id=profileId); depois para i de 0 até n-1, `records/IIIIII.afb` tipo 3 (id=recordId), `sessions/IIIIII.afb` tipo 1 (id=sessionId), I um decimal de seis dígitos com zeros à esquerda. Par correspondente à posição do registro na lista legada, NÃO à ordem musical. Metadado de registro contém exatamente os campos do legado exceto `session` (separada no bloco do mesmo índice). Reconstituir `record = {...recordHeader, session}` sem alterar dados; conferir `sessionHash`, IDs, `profileId`, revisão e vínculos. `recordId` único no perfil; sessionId pode repetir apenas com o mesmo stringId, como exige `migrateAndValidate`; não confundir revisões distintas da mesma aquisição com colisão de recordId. Não usar IDs do usuário como nomes. A lista manifesta `entries` contém tamanho e hashes de cada bloco, e não cópia de resultados. O manifesto não é índice confiável de validade acústica.

Histórico: `curves/IIIIII.afb` tipo 4 (id=versionId), ordem original de `versions`; sem perfil ou sessões. Conferir unicidade, parentesco, parentHash, integridade e manifesto de fontes exatamente como `verify` e `merge`. Não pressupor que importar curva restaura suas fontes acústicas ou autoriza aplicação. Ancestral deve estar presente no conjunto de revisões validado; importação como histórico isolado rejeita ancestral ausente. Merge explícito pode resolver ancestral existente na base local, após verificar a união. `.afc` com zero versões é permitido como arquivo vazio semanticamente, não há curva a aplicar.

Manifesto gravado primeiro exige prepass ou spool persistente dos blocos já preparados; não manter todo o ZIP em RAM. Exportador pode preparar/hash um bloco por vez e armazenar temporariamente em IndexedDB, depois emitir manifesto e ler spool incrementalmente. Recalcular/verificar digest ao escrever; abortar se geração mudou. Remover spool após sucesso/erro. Importador lê EOCD/central via slices, valida todos os limites, extrai apenas um bloco por vez. Uma pré-visualização não publica dados. Fallback Blob limitado (ver Segurança).

### 5. Determinismo e hashes

O formato NÃO exige representação CBOR canônica nem bytes comprimidos idênticos entre bibliotecas/níveis; aceita comprimentos definidos com cabeçalhos não mínimos de inteiros/comprimentos permitidos pela RFC. Writer deve produzir ordem estável para mesma entrada/configuração, sem promessa de igualdade byte a byte entre codecs. Os três hashes AFB cobrem bytes efetivamente emitidos; `sha256` do manifesto cobre AFB inteiro. A identidade semântica não depende de encoding. Preservar todos os hashes JCS antigos, inclusive snapshotHash/recordId. Reconstituir envelope JSON de perfil/history somente quando exportar para legado e recalcular JCS sobre payload na ordem original de arrays; perfil legado schemaVersion=1, curves=[]. Não armazenar envelope legado como segundo objeto gigante. Não confundir SHA do contêiner com identidade de sessão ou revisão.

Golden fixtures em `fixtures/` são exemplos de bytes, não autorização de uso musical. AFB de sessão real ou sintética preserva campos inteiros; arquivos de transporte isolado marcados como tais não são necessariamente aceitos pelos validadores acústicos. A CLI realiza verificações parciais de semântica; o aplicativo é a referência para aceitação e autorização de uso.

### 6. Normas

- CBOR: https://www.rfc-editor.org/rfc/rfc8949.html
- Typed arrays: https://www.rfc-editor.org/rfc/rfc8746.html
- CDDL: https://www.rfc-editor.org/rfc/rfc8610.html
- Zstandard: https://www.rfc-editor.org/rfc/rfc8878.html
- GZIP: https://www.rfc-editor.org/rfc/rfc1952.html
- JCS: https://www.rfc-editor.org/rfc/rfc8785.html
- ZIP: https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT


<a id="modelo"></a>
## 2. Modelo semântico e schemas

Referência do modelo de dados em conjunto com os capítulos [Formato](#formato), [Versionamento](#versionamento), [Segurança](#seguranca) e `schemas/`. O transporte é sem perdas; a semântica específica é definida pelos validadores e motores do aplicativo. O esquema de intercâmbio continua v1. Os mapas CDDL são estruturais e não substituem a validação semântica.

### 1. Modelo de dados e precisão

Um único item CBOR, sem trailing bytes. Mapas com chaves de texto UTF-8 válido e exclusivas (comparação por sequência Unicode, sem normalização); arrays ordenados de comprimento definido, mapas/strings de comprimento definido. `null` não significa campo ausente; não preencher defaults, reordenar arrays, arredondar, remover duplicatas de valores, descartar campos nem inferir valores acústicos. Evitar key interning, record structures, shared references, bundles de strings, tags de data e extensões de CBOR-X. O domínio é árvore JSON acíclica: boolean, null, string, número, array, object. Bytes soltos não permitidos nos objetos semânticos; somente conteúdo das tags Int16 explicitadas abaixo. Não há undefined, NaN, Infinity, pares de surrogate inválidos ou objetos executáveis. Limites na documentação de segurança.

- Inteiros CBOR (major 0/1), somente −9007199254740991..9007199254740991. Validar antes de converter para JS Number; não arredondar BigInt. Float64 binary64 CBOR (0xfb), finito; valores matematicamente integrais fora do domínio seguro também rejeitados. Float16 e float32 não fazem parte do contrato v1; sem nova quantização. Valor inteiro dentro do domínio pode ser representado como inteiro CBOR ou float64; não há diferença semântica no JS. Subnormais permitidos. Ordens/índices/contagens devem ser inteiros conforme validador de campo.
- **Zero com sinal:** +0 e −0 são preservados no transporte, −0 deve usar float64 `fb8000000000000000`. Writer deve verificar `Object.is(x,-0)` e emitir float64 explicitamente; se biblioteca não fizer isso, adaptar o encoder ou falhar sem gravar (nunca normalizar silenciosamente). Reader mantém sinal. JCS legado normaliza −0 para 0, sem mudança; SHA de bytes distingue. Exportador de diagnóstico JSON externo que pretenda reversibilidade deve emitir `-0` literal, não usar JSON.stringify cru para esse caso. As fixtures incluem casos sintéticos de −0. Não prometer suporte de toda entrada antiga que já perdeu o sinal numérico antes da codificação.
- Campo `spectrumGrid202.values`, exclusivamente sob objeto `spectrumGrid202` com validação de grade: array de inteiros −1600..0 (comprimento exatamente conforme versão/validador, até 4096), ou CBOR tag 73 (Int16 big-endian), 77 (Int16 little-endian), ambas com byte string de comprimento par entre 2 e 8192 bytes. Reconstituir array ordinário para JCS e consumidores legados, sem alterar valores, escala 0,1 dB ou ordem. Qualquer outra tag/byte string rejeitada, inclusive Int16 em outro caminho. Writer pode inicialmente usar só arrays convencionais; leitor suporta ambos. Não reduzir frequências ou B a float32 nem reinterpretar o nível como amplitude linear.

### 2. Sessão acústica

Raiz kind=1: `format: "afinador.acquisition-session"`, `schemaVersion: 1`. Objeto integral, sem wrapper adicional. CDDL define mapas principais e tipos, não substitui regras condicionais/transversais. Campos que existiam no legado e não são individualmente modelados por uma regra CDDL estreita são árvores `value` com validação semântica original obrigatória. **Nenhum campo é eliminado**. `docs/DICIONARIO_CAMPOS.csv` é um inventário auxiliar de caminhos e unidades observados em um corpus de 13 sessões; não é uma lista exaustiva nem um schema. Os mapas CDDL registram os campos permitidos e obrigatórios. Os predicados vigentes de SECURITY13 e dos demais validadores no `index.html` completam o contrato. Palavras “opcional” significam apenas que campo pode faltar na estrutura, não que condição semântica possa ser ignorada. Por exemplo acousticContext é exigido por validateSession quando se salvar perfil. Flags de elegibilidade não são calculadas pelo decodificador.

| Grupo/campo | Tipo, unidade e interpretação |
|---|---|
| sessionId, executionId, segmentId, keyId, pitchId, soundId, targetId, versionId | texto opaco; não converter para número nem derivar por nome de nota |
| schemaVersion, engineVersion, individualModelVersion, aggregationEngineVersion, validationEngineVersion | versão semântica/algoritmo; preservar exatamente |
| instrument, sourceCondition, acousticContext, analysisSettings15, collectionSettings15 | categoria/procedimento e configurações de origem; não assumir corda rígida, não substituir configurações atuais |
| musicalSnapshot, snapshotHash, binding, noteBindingAtCapture, musicRevision | snapshot musical, vínculos e revisão do contexto; ver §5 |
| createdAt, exportedAt, observedAt, confirmedAt | texto de data/hora legado, sem conversão de fuso ou regeneração |
| sampleRateHz, trackSettings (sampleRate), referenceA4Hz | Hz; trackSettings conservado sem inferir valor real calibrado |
| capturedSamples, windowSamples, selectedWindowSamples, usefulSamples, sampleStartIndex, workletFrameStart, startIndex, endIndex, zeroPaddingLength | contagens/índices de amostra, não ms; não trocar base de indexação |
| createdAt e startedAt vs startedMs/endedMs/pcmStartedMs | datas textuais vs timestamps numéricos do produtor; preservar distinção; tempos relativos com sufixo Ms em ms |
| executions, segments, revisions, aggregationRevisions, partialReviews | ordens, históricos, decisões e referências preservados; até 2000 execuções, sem truncar; validação de referencial original |
| result.partials | ordens e frequências (Hz), amplitudeDbRelative dBr, localSNRDb dB, differenceHz Hz, deviationCents e estabilidade em cents; status accepted/candidate/rejected; não confundir picos com parciais atribuídos |
| result.candidates, familyAnalysis.peaks, peakDiagnostics20 | picos Hz, amplitude dBr, SNR dB; rejeições e diagnósticos preservados |
| result.spectrum | pares [Hz, dB] do espectro individual; não alterar dB ou reamostrar |
| result.spectrumGrid202 | grade logarítmica, version e values; valores em 0,1 dB; posição/frequência derivada pelo algoritmo existente; não é DPX |
| fundamentalEstimateHz, firstPartialMeasuredHz, fundamental203, reference207, metrology205 | hipóteses e referências em Hz, status e comparações; não promover inferência a P1 medida. origin/referenceKind e curveEligible preservados |
| temporalEvidence, temporal207, stability208, windowAssessment205 | comparações temporais e drift; campos `*Cents` em cents; decayDb em dB; erros/score adimensionais ou específicos do motor; não substituir gates absolutos por relativos |
| inharmonicity, analysis20.attempts.physicalFit207, refit207 | B adimensional, FHz/modelFundamentalHz em Hz, parâmetros, incerteza, escolhas de ordens/resíduos e vetos. B null = não estimado/justificado; 0 não é null. `compatible_provisional` não é calibrado |
| assignment207, strongPeakDiagnostics208, coherence209 | atribuição, alternativas, verificações de ordens superiores; não descartar `usedToLiftVeto`, métricas e diagnósticos |
| aggregate, aggregationStatus, aggregationRevision, convergenceStatus, B | B consolidado, condições e histórico; nunca recalcular em transcodificação. status `consistent_provisional` exige verificações originais; curveEligible=false |
| reasonCodes, flags de qualidade, uncertainty, diagnostics, comparisons, parameters | dados do motor, preservar tipos e valores específicos; intervalo de sensibilidade não equivale a IC nem calibração |

Unidades explícitas nos nomes não autorizam interpretar qualquer parâmetro sem sufixo. Por exemplo scores/weights/losses/ratios são definidos por versões de motor, não métricas universais. Inventário complementar classifica as unidades explicitadas nos nomes, e marca os demais como sem unidade verificável no nome. A especificação de transporte não inventa unidade para um campo opaco; semântica completa de todos os diagnósticos internos é a do algoritmo versionado. Para reimplementar análise científica de um diagnóstico, consultar o código da versão correspondente; para ler e preservar os dados não é necessário executar esse código.

### 3. Perfil, metadados e registro separado

kind=2: mapa `profile` do legado (sem wrapper `afinador.acoustic-profile`). IDs, família, modelo acústico válido exigido por FAMILIAS6.validProfile (mesmo que opcional na lista estrutural de campos), subtype, nome, notas, datas, layout físico e auditEvents. As teclas em `instrumentLayout.keys` têm ordem física explícita; o identificador é par [keyId,octave] (pitchId é verificado); nunca ordenar pelo nome/cents. Até 1000 teclas. Mapeamento de corda pode estar ausente; `physicalKey` e `stringId` nulos são valores válidos. Layout não implica confirmação de nota. Nome de perfil e notas são texto, não HTML.

kind=3: `record` legado sem `session`: todos os 14 campos restantes obrigatórios, `recordSchemaVersion=1`. `sessionHash`, `baseSnapshotHash`, `recordId` são hex minúsculos SHA-256; `stringId` é a string JSON do array [keyId,octave,sourceCondition,stringLabel] ou null, conforme função makeRecord; não tratar como ID de nota. `curveEligible=false`. `discardedFromModeling` e `note` editáveis segundo regras antigas, sem mudar hash da sessão. `observationStatus` experimental/inconclusive é derivado no produtor e verificado na reconstrução, não recalculado para melhorar resultado. Vínculo entre kind 2,3,1 deve passar por `validProfile`, `validateSession`, `verifyRecord` e regras de colisão em `migrateAndValidate`. Header sozinho não prova que sessão foi validada. A reconstrução de perfil legado é `schema:"afinador.acoustic-profile", schemaVersion:1, profile, records, curves:[], integrity` (integrity sobre objeto sem integrity).

### 4. Curva e revisão

kind=4: objeto `afinador.tuning-curve-revision`, schemaVersion=1. Todos os campos de `revision` e `curve` preservados: `profileName`, `sourceManifest`, `versionId`, `curveId`, `versionNumber`, `parentVersionId`, `parentHash`, createdAt, reviewStatus, action, reason, curve, fundamentalAudit, changeFromParent, integrity. `curve` inclui `schema`, versão do algoritmo, status, curveEligible falso, physicalValidation pendente, profileId, baseSnapshotHash/baseSnapshot, physicalLayout, objective, corrections, intervalAudit, diagnostics, instrumentLayoutHash, compatibilityHash, identidade e data. `corrections`: frequencyHz e proposedFrequencyHz (Hz), deltaCents (¢), identidade, source/evidence/uncertainty/sensitivity preservados. Não converter correção teórica em resultado aprovado. `sourceManifest` máximo 512 entradas (recordId, sessionHash); unicidade e correspondência com fontes exatas. `reviewStatus=approved_experimental` só para preview e não constitui validação física. Executar SECURITY13.revision, A.validate, A.fundamental e verify; impor integridade/ancestralidade conforme merge. O legado exige ancestral presente na união com histórico local, parentHash igual à integridade do ancestral, curveId igual, versão crescente, função same(p.curve,v.curve) e diff reproduzido; histórico isolado deve conter os ancestrais. Raiz exige parentHash e changeFromParent nulos e versionNumber=1; não inventar ancestral nem recomputar hash; a leitura completa não autoriza reabrir/editar/aplicar sem fontes e procedimentos de verificação originais. Histórico reconstruído como `afinador.tuning-curve-history` v1, versions ordenado e integrity calculado.

### 5. Hashes semânticos e identidade (preservar literalmente)

JCS do legado = UTF-8 do JSON canônico: JSON.stringify de primitivos válidos (números ECMAScript binary64, zeros normalizados), chaves de objetos ordenadas lexicograficamente por unidades UTF-16 sem locale e sem normalização Unicode, arrays em ordem original, sem whitespace. Usar RFC 8785 e comparar com `jcs` da baseline; `json.dumps(sort_keys=True)` não é substituto (Unicode/float). `canonicalJSON` e `jcs` nesta baseline são equivalentes no domínio válido. SHA-256 minúsculo hex para hashes semânticos. Confrontar o SHA de cada snapshot e sessão reconstruída. Tipos CBOR Int16 convertidos para array antes do hash.

| Campo | Entrada do SHA-256/JCS |
|---|---|
| snapshotHash | musicalSnapshot original completo |
| sessionHash | sessão completa, não só execuções; não alterar exportedAt, flags, order etc depois de calcular |
| baseSnapshotHash | `semantic(musicalSnapshot)` (ou semantic(baseSnapshot) na curva), builder afinador-semantic-snapshot-3.0 |
| recordId | objeto `{sessionHash,baseSnapshotHash,stringId}` |
| instrumentLayoutHash (curva) | `physicalLayout` completo conforme verificador |
| compatibilityHash | `{baseSnapshotHash,instrumentLayoutHash}` |
| integrity.sha256 de revisão | revisão completa sem campo integrity |
| parentHash | hash de integridade do ancestral, não hash AFB |
| sourceManifest | referência a recordId/sessionHash, não a hash CBOR |
| integrity.sha256 envelope legado | objeto envelope sem integrity, incluindo ordem das listas |

`semantic` é definido nos validadores do aplicativo: frações reduzidas por MDC com denominador positivo, targets ordenados por keyId UTF-16 e octave numérica, somente keyId/pitchId/soundId/octave/frequency; definition íntegra; receita ordenada por index com frações cp/cs, closure e layout/referência normalizados conforme modo EDO ou não; builder fixo. Preservar a definição do hash enquanto o contrato semântico for o mesmo. A validação de binding confirmado exige targetId=`JSON.stringify([keyId,octave])`, correspondência de pitchId, soundId, frequencyHz e snapshotHash. IDs sem confirmação não ganham vinculação na importação.

### 6. Estruturas novas de acesso (não são formatos semânticos de intercâmbio)

Índice/projeção são descritos em [Arquitetura de armazenamento](#armazenamento): não são fonte de verdade; associação obrigatória a versão de registro, sessão/hash e política de validação. O perfil exportado não inclui caches. Não usar index/projection para aprovar curva só porque `curveEligible` aparece no resumo. `project(r)` continua contrato do otimizador legado. A extração de espectros, a caracterização empírica e a reprodução das fontes são responsabilidades dos respectivos validadores e motores. O índice e as projeções podem evoluir sem alterar os formatos AFB/ZIP: invalidar e reconstruir do bloco original.

### 7. Limites da CDDL e validação semântica

As regras CDDL explicitam envelope lógico, manif­estos, raízes e mapas principais; mapas profundamente internos usam `value` quando não há contrato CDDL individual exato (o validador original impõe limites e relações adicionais). CDDL não expressa hashes, vínculos, igualdade de frequências, unicidade de IDs, posição contextual de tag, algoritmo físico ou segurança de alocação. As listas exatas `fields()` extraídas e o código congelado completam o contrato semântico; reimplementações devem portar os predicados, não só validar CDDL. Campos desconhecidos nos mapas fechados são erro; dentro de árvores que original permite abertas, preservar e verificar árvore. Não aceitar arquivo futuro simplesmente porque um campo cabe em `value`. Cobertura de campos observados não prova cobertura de todos os domínios físicos ou valores possíveis. A equivalência integral dos validadores JS/Python não está demonstrada; a CLI não substitui a validação do aplicativo.

<a id="identidade-fisica"></a>
### 8. Identidade física e histórico de arquivamento

As estruturas abertas `session.revisions` e `profile.auditEvents` transportam eventos adicionais, sem alteração do envelope AFB nem dos campos dos mapas fechados. Devem ser preservadas integralmente, incluindo na transcodificação JSON.

**Identidade física (`AFBIdentityB`).** A avaliação usa a mediana das frequências `result.fundamentalEstimateHz` positivas das execuções elegíveis, incluídas e com resultado experimental. Um vínculo confirmado deve corresponder ao snapshot musical. Desvio absoluto acima de 45 cents exige confirmação explícita; ausência de evidência não equivale a confirmação. O evento `physical_identity_exception_confirmed` em `revisions` contém `type`, `at`, `sessionId`, `targetId`, `keyId`, `pitchId`, `octave`, `snapshotHash`, `musicRevision`, `acousticModelId`, `expectedHz`, `observedHz`, `deltaCents`, `method` (`median_raw_fundamental_estimate`) e `evidenceRows` (lista de `{id,hz,partials}`, com `partials` representando a lista serializada de ordens excluídas). A confirmação é validada contra a sessão, o contexto e as evidências; o último evento aplicável deve corresponder ao prefixo de evidências atuais e novas execuções e a mediana atual devem permanecer a até 10 cents da referência observada confirmada. Não fabricar eventos, nem interpretar a presença de um evento como autorização automática.

**Disposição e descarte (`AFBLayoutC`).** Eventos `physical_layout_reconfigured_23` em `auditEvents` registram `from`, `to`, `archived`, `hiddenKeys` e `knownSlots`, além de metadados do evento. O identificador de arquivamento é `JSON.stringify([sessionHash,stringLabel])`. Os elementos de `archived` contêm `id`, `physicalKey` e `userDiscarded`. Eventos `layout_archive_selection_23` registram `at`, `action`, `archiveId` e `userDiscarded`. Uma medição arquivada continua inelegível enquanto a tecla estiver fora do mapa; a escolha manual é preservada separadamente e respeitada na restauração. `hiddenKeys` preserva identidades físicas e `knownSlots` registra as posições conhecidas. Não remover esses metadados por parecerem redundantes.

A CLI Python incluída preserva essas árvores, mas seus predicados não implementam integralmente essas políticas. Em particular, sua derivação de `physicalKey` usa o vínculo confirmado e o mapa, sem a avaliação adicional de identidade física; pode aceitar ou rejeitar casos diferentemente do aplicativo. A validação completa de arquivos e da elegibilidade de curvas deve ocorrer no aplicativo.


<a id="seguranca"></a>
## 3. Segurança e limites

### 1. Limites normativos (MiB=2^20; KiB=2^10)

| Recurso | Limite 1.0 |
|---|---:|
| Cabeçalho AFB | 128 B |
| CBOR descomprimido por objeto | 32 MiB |
| Payload AFB | 34 MiB |
| Chunk descomprimido | 2 MiB |
| Chunk armazenado | 2 MiB + 64 KiB |
| Chunks | 16 |
| Janela Zstd | 2 MiB |
| Manifesto descomprimido | 2 MiB, STORE |
| ZIP completo | 1 GiB |
| Soma declarada rawLength por ZIP | 8 GiB |
| Registros por perfil / teclas layout | 2.000 / 1.000 |
| Versões por histórico / fontes por revisão | 128 / 512 |
| Entradas ZIP | 4.002 |
| Nós semânticos por objeto | 2.500.000 |
| Profundidade do nó raiz 0 | 60 |
| Chaves por mapa / elementos por array | 4.096 / 200.000 |
| Texto individual | 100.000 unidades UTF-16; máximo UTF-8 400.000 bytes antes de decodificar |
| Execuções por sessão / ordens por resultado | 2.000 / 256 |
| Grade Int16 | até 4.096 elementos (validador da versão pode exigir comprimento menor/exato) |

Os limites mais estritos do SECURITY13/validadores continuam aplicáveis. Limites de árvore por objeto, não por perfil inteiro — deliberadamente substitui o teto de 32 MiB do envelope JSON completo, não relaxa regras acústicas. Conferir a árvore reconstituída do registro inteiro, mesmo que header e sessão sejam separados. Na preflight CBOR, contar mapas, arrays, valores **e chaves** em orçamento de tokens separado (máximo 5.000.000 tokens; não ultrapassar 2.500.000 nós semânticos como no tree, incluindo cada elemento de Int16 após expansão). A profundidade semântica é medida sobre a árvore normalizada. Para valores grandes, não admitir com base em comprimento declarado até conferir bytes restantes e produto de contagens usando inteiros seguros. Erro claro; manter trabalho e fonte; não baixar limite físico para aceitar arquivo.

### 2. Ordem de validação (fail closed)

1. Identificar arquivo por conteúdo, tamanho real e limites; ZIP: EOCD/central/local, nomes fixos, offsets, sem traversal, entradas únicas, tipos, CRC e igualdade com manifesto; proibir ZIP64, links, criptografia, extras, descriptors, prefixos e trailers. Não extrair para filesystem com nomes do usuário. A carga de central directory deve ser limitada (máximo 2 MiB). Antes de expandir qualquer sessão, validar manifesto e soma de tamanhos com inteiros seguros.
2. AFB: versão/kind/codec/flags/reserved, header SHA, tamanho, tabela de chunks, payload SHA; rejeitar mismatch com manifesto. Validar um chunk antes de malloc: tamanho real, magic, frame size e janela Zstd, dicionário 0, exatamente um frame (verificar fim pelos block headers ou API equivalente); GZIP header sem campos opcionais, inflater bounded, CRC/ISIZE e fim exato. Não confiar em ISIZE ou content size isoladamente. Não usar decompressor que só verifica cap após alocar saída gigante; interromper ao ultrapassar rawChunkLength. Sem frames extras/skippable. Contabilizar chunks e saída efetiva; validar hash raw antes de aceitar objeto.
3. Preflight CBOR com cursor e limite antes de alocar coleções: recusar chaves duplicadas em texto decodificado, `__proto__`, `constructor`, `prototype`, `pcm`, `wav`, `rawAudio`, `audioBlob` em qualquer mapa; tipo de chave exclusivamente texto; validar Unicode, comprimentos, número seguro antes de conversão, float64 finito, tags só da grade. Rejeitar objeto trailing, indefinite, tags desconhecidas, tokens inválidos e arrays fora de limite. Usar objetos sem prototype na etapa não confiável; sem eval, dynamic import ou inserir texto como HTML. Bibliotecas podem converter duplicatas silenciosamente: preflight é obrigatório antes do CBOR-X, não só validação do resultado. Validar expansão Int16 e budgets totais. Não usar `int64AsNumber:true` até verificação de faixa.
4. CDDL e normalização; SECURITY13.tree + validadores específicos, regras de vínculos, hashes JCS, versão, compatibilidade, auditoria de B e revisões. Manifestos não são prova de validade física. Testar flags/snapshots/curvas e bloquear alteração de alvo por fonte inválida. Verificação criptográfica detecta corrupção mas atacante pode recalcular hashes; segurança semântica necessária.
5. Staging invisível; validar cada sessão/revisão uma vez por importação; publicação atômica por geração após verificar todos. Se erro/aborto/quota/conflito de geração, manter geração anterior e remover staging com journal; não retornar sucesso antes de oncomplete. Exclusão e edição invalidam fontes/curvas conforme os validadores vigentes. Não publicar só metadados antes das evidências.

### 3. Orçamentos de runtime (referências de engenharia, não medições de RAM)

| Componente | Limite inicial de engenharia |
|---|---|
| Memória linear Zstd WASM | 32 MiB máximo, inicial 16,125 MiB na versão testada; falhar se crescer além; confirmar build e liberação |
| Worker storage | 1 tarefa ativa; reciclagem por escopo de transferência, sem fila de buffers grandes |
| Descompressão de evidência | 1 objeto completo por vez em Worker; comparação explícita pode manter 2 sessões na UI, não abrir terceiro sem liberar |
| Cache de evidência descompactada descartável | até 8 MiB de peso lógico (bytes CBOR da sessão), no máximo 2 entradas; objeto acima do teto não cachear. Não é heap real. |
| Cache de projeções | repositório: projeções de até 8 MiB; cache de projeções na camada de acesso desabilitado; conjuntos transitórios tratados separadamente |
| Página de índice | até 100 itens, <=1 MiB serializado/página; cap de índice ativo 4 MiB lógico/página e cache, não materializar perfil inteiro por necessidade de listagem |
| Fallback Blob exportação | 128 MiB do ZIP final; estimar antes de alocar; se ultrapassar, utilizar streaming suportado ou lotes/sessão, nunca aumentar automaticamente |
| Timeout de tarefa de codec/preflight | 30 s por tarefa de codec, cancelamento por epoch/terminate; import/export grande progresso por bloco, não timeout único de 30s para todo instrumento |

Peso lógico não equivale a JS heap/RSS. Os 32 MiB de CBOR bruto podem exigir cópias e objetos adicionais; não prometer 32 MiB RAM total. Usar slices/Transferable, contabilizar buffers reais e WASM, não transferir DSP em uso, não deixar worker residente na afinação normal. Guardar sessão de trabalho não salva separada do cache: never evict trabalho sem decisão explícita; pode bloquear operação que exceda orçamento. Quota origem e margem livre devem ser medidas; falha exibe caminho de exportação alternativa; storage.persist quando disponível, sem substituir backup. O cap de 1 GiB não implica suporte de Blob de 1 GiB. Testar memória real e responsividade (Android/iOS e desktop); os orçamentos podem ser estreitados com evidência, não afrouxados silenciosamente no formato 1.0.

### 4. Pendências de produção e testes

Bloqueadores da promoção: pacote WASM exato e notices MIT/BSD, procedência e build auditável, uso da CSP `wasm-unsafe-eval` existente sem `unsafe-eval`, limites em todos os caminhos, Worker teardown e RAM (heap/external/linear/RSS), IndexedDB em origem válida, recuperação de quota, cancelamento, concorrência, mobile e comparação acústica. Categoria de testes: truncamentos em todos os limites, header/hash modificado, comprimentos inconsistentes, frames colados, janela/dicionário excessivo, decompressor bomb, UTF-8 inválido, duplicate/prototype poisoning, tags e floats fora do domínio, zip slip/zip bomb/entradas duplicadas/offets sobrepostos, manifest adulterado, hash semântico forjado, vínculo incorreto, geração alterada, fonte descartada, corte de energia/aba, erros de quota, lote >Blob, 52/104/208/300/1000 sessões. A suíte incluída cobre parte dos casos adversariais de transporte; não demonstra homologação integral. Não confundir fixture de transporte com validador de segurança completo.

O aplicativo destina-se ao uso em uma única aba. A CLI não implementa o staging IndexedDB, nem substitui os predicados atuais de identidade física e arquivamento.


<a id="armazenamento"></a>
## 4. Arquitetura de armazenamento

Acesso independente de UI/DSP. Base `afinador-acustico-binario-v1`, versão IndexedDB 1; não abre/escreve os bancos antigos. Chaves compostas arrays de strings/inteiros; nenhuma chave concatenada ambígua. Uma geração por perfil/histórico, identificada por UUID; revision counter seguro para concorrência. O ponteiro de geração publicada é fonte de verdade. Não persistir trabalho não confirmado como perfil publicado. Sessão evidência imutável por hash; não usar hash de AFB como sessionId. A tabela descreve a organização lógica dos stores; os detalhes de índices e APIs devem ser consultados em AFB21Repository no HTML.

| Store | KeyPath / chave | Conteúdo / índices |
|---|---|---|
| profiles | profileId | generation ativa, revision, sumário lista, tamanho; índice displayName |
| profileMeta | [profileId,generation] | metadado perfil validado (kind 2); layout sob demanda |
| sessionIndex | [profileId,generation,recordId] | resumo leve, header de record kind 3 ou referência, sessionId, aggregationRevision/null, hashes, byte sizes; índices [profileId,generation,keyId,octave] para vínculo confirmado, [profileId,generation,recordedAt,recordId] |
| evidence | [profileId,generation,recordId] | AFB kind 1, Blob/ArrayBuffer, sha256 binário; sem objeto descompactado |
| recordHeader | [profileId,generation,recordId] | AFB kind 3, hashes |
| projections | [profileId,generation,recordId,kind,policyVersion] | projeção, vínculo sessionHash/header hash, digest próprio; regenerável |
| curveHeads | historyId | ponteiro geração e revision; não significa aprovação |
| curveIndex | [historyId,generation,versionId] | lineage, versionNumber, parent hash, status, digest, metadados pequenos |
| curveBlocks | [historyId,generation,versionId] | AFB kind 4, digest |
| staging | jobId | journal, destino, geração, fase, contagem, tamanhos, hashes; estado prepared/validated/published/aborted |
| spool | [jobId,entryIndex] | AFB temporário do export; apagar pós operação |

Não usar getAll em evidence, recordHeader ou curveBlocks. IDB cursor paginado com limite; listagens não tocam nos blobs. Limitar índices por bytes e itens. Edição de nota e flag discarded exige recomputar header/digest/index e invalidar projeções/curvas afetadas, não recodificar evidência imutável. Edição de evidência/revisão altera sessionHash/recordId conforme legado; não reaproveitar aprovação. Após transação confirmada notificar os consumidores; BroadcastChannel sinaliza invalidação quando disponível. O uso previsto é em uma única aba. Cancelamento/época invalida fontes obsoletas; a abertura pendente pertence à sua própria época e não pode cancelar uma abertura posterior.

### API

Todas as operações assíncronas, com token generation/revision (snapshot de leitura), signal/epoch equivalente, erros tipados (`FORMAT`, `VERSION`, `LIMIT`, `INTEGRITY`, `SEMANTIC`, `CONFLICT`, `QUOTA`, `CANCELLED`, `UNAVAILABLE`). `listProfiles`, `getProfile`, `listSessions`, `getSessionIndex` retornam páginas/índices, sem evidência. `readSession(profileId,recordId,{generation,expectedSessionHash,signal})` retorna objeto validado; `readProjection(...,{kind,policyVersion,expectedSessionHash,expectedHeaderHash,...})` verifica binding e digest ou reconstrói de sessão validada; `verifySources(profileId,manifest,...)` iteração limitada por ID exato, não scan de todas as sessões. `commitSession(prepared,{expectedGeneration,expectedRevision,signal})`, `amendRecord`, `deleteRecord` com compare-and-set; `listCurveVersions`, `readCurveVersion(expectedHash)`, `stageImport`, `publishGeneration`, `abortStaging`, `exportBlocks` só confirmam após oncomplete. Os nomes representam operações lógicas; a API concreta é definida no HTML. Não expor IDB diretamente aos consumidores.

O índice inclui os resumos definidos pelo repositório no HTML; não substitui a evidência. Ausência/nulo preservados; não derivar valores novos salvo resumos explicitamente calculados e marcados. `project(r)` como projeção `curve-input` versão 1 deve ser igual à função original para registro verificado. Caches para síntese (S.extract e EMPIRICAL19) preservam filtros e metadados; se campo não puder ser projetado sem alterar comportamento, ler só evidência selecionada. Antes de reproduzir/aplicar/reabrir curva, verificar fontes completas por manifesto quando requerido pelo algoritmo vigente; não confiar no índice. Afinador ativo carrega somente artefato efetivo e metadados já autorizados. `pending`, sessão em aquisição/revisão e versões não salvas são trabalho, não cache descartável.

### Atomicidade

Preparar codec/hashes/validação fora da transação, transação curta de gravação de índice+header+blob+metadado+journal/revision. Sem await Worker/rede dentro de tx. Durante importação grande escrever blocos sob geração não publicada; conferir quota e bloqueios; verificar cada registro contra perfil e semântica, manifestos e conflitos, depois trocar ponteiro em transação curta somente se revision esperada coincide. Leitores capturam generation e abortam se alterada. Geração antiga preservada até publicação e limpeza segura; journal permite rollback/recolher órfãos após restart (não publicar automaticamente importação interrompida). Exclusão lógica e coleta física separadas. Não apagar dados de outras bases automaticamente. Staging/spool não são caches de evidência em heap; orçamento em disco e progresso explícito. Sem double write automático. Exportação streaming via File System Access quando suportada, fallback Blob cap 128 MiB, lotes separados caso necessário.

### Metadados e limites operacionais

A edição de descarte de uma medição arquivada atualiza o evento de decisão no perfil e mantém `discardedFromModeling` verdadeiro enquanto a tecla estiver ausente. Cabeçalho, metadados, índice e invalidação de projeções devem ser coerentes na transação. O repositório expõe páginas de até 100 itens e orçamento de 1 MiB por página; evidências são lidas sob demanda. A camada de acesso limita o cache de sessões a 2 entradas e 8 MiB de peso lógico; `projectionCacheBytes:0` nessa camada não elimina as projeções persistidas pelo repositório. Exportação Blob é limitada a 128 MiB; a escrita em arquivo, quando disponível, permite o limite do contêiner. A recuperação de operações interrompidas pressupõe uma única aba; não é suporte a edição simultânea multiaba. A homologação em IndexedDB nativo e em dispositivos móveis permanece necessária.


<a id="versionamento"></a>
## 5. Versionamento e evolução

Há três eixos independentes: (1) AFB major/minor 1.0; (2) schema CBOR semântico/manifesto (schemaVersion=1); (3) versões de motor acústico preservadas no conteúdo. O esquema do IndexedDB tem versão própria, nunca será chamado de versão de codec. AFB 1.0 só aceita major=1/minor=0/flags=0; desconhecido rejeitado com mensagem de versão e sem tentativa de heurística. Manifestos identificam seu schema; sessão e histórico usam schema legado. Não aceitar major/minor superior por default. Minor aditivo só pode ser lido quando explicitamente previsto e testado pelo leitor; major muda quando uma interpretação existente ou layout binário quebra. Novos campos críticos requerem versão/schema apropriados; campos desconhecidos em mapas fechados rejeitados. Não há campos invisíveis descartados.

| Mudança | Política |
|---|---|
| Atualização de biblioteca/nível de compressão dentro do perfil de frames aceito | Não altera formato; registra versão e testes de interoperabilidade |
| Codec/tag nova | novo minor explicitamente suportado, ou major conforme quebra; leitores 1.0 rejeitam |
| Novo diagnóstico acústico | versão de schema/motor conforme significado, preservar versões originais; não promover B |
| Índice ou projeção local | policyVersion nova, invalidar/reconstruir cache, formato de evidência intacto |
| Alteração de hashes ou interpretação de unidades | nunca silenciosa; novo schema/contrato com migração explícita |
| Sessão maior que limites v1 | não truncar; manter fonte e planejar particionamento lógico em versão posterior |

A aplicação não oferece garantia de abertura de formatos históricos. Os arquivos JSON de intercâmbio devem ser semanticamente válidos e aceitos pelos validadores vigentes; JSON v0 não é suportado. Preservar os arquivos de origem diante de falhas; não truncar nem alterar hashes para forçar importação. Os eventos de identidade física e arquivamento descritos no capítulo [Modelo semântico](#modelo) são parte das árvores de auditoria, não novos tipos de envelope. Formatos e validação do aplicativo podem evoluir independentemente da CLI.


<a id="python"></a>
## 6. Ferramentas Python

### Escopo

CLI Python independente para conversão científica de sessão (`.afs`), perfil (`.afp`) e histórico (`.afc`). Não precisa executar o HTML, JavaScript, npm ou WASM. Não acessa IndexedDB, microfone ou rede; não altera o aplicativo e não autoriza aplicar curvas. O contrato é este manual e os esquemas em `schemas/`. Ferramentas experimentais de intercâmbio. Preserve os arquivos originais. `validate` verifica envelope, árvore, regras estruturais, hashes e relações implementadas; **não substitui todos os predicados internos de SECURITY13 nem os procedimentos de autorização de curvas**. Um resultado `ok: true` não equivale a calibração, autenticação de origem, autorização física ou aprovação de importação no navegador.

### Instalação

- Extraia o pacote, mantendo `tools/`, `schemas/` e `fixtures/` no mesmo diretório pai. Não renomeie `inspect_file.py` para `inspect.py` (colisão com biblioteca padrão).
- Python 3.10 ou superior (testado apenas em 3.13.5, Linux x86_64). Não há módulos pip obrigatórios. `requirements.txt` é informativo.
- Para Zstandard, instale a biblioteca nativa `libzstd` da sua plataforma (Linux: pacote de runtime da distribuição, por exemplo `libzstd1` em sistemas Debian; Mac: biblioteca zstd do gerenciador de pacotes). O runtime precisa ser localizado por `ctypes.util.find_library('zstd')`. A versão testada é 1.5.7. Em Windows, recomendamos executar inicialmente em WSL; resolução de DLL nativa Windows não foi testada. STORE e GZIP não precisam da libzstd.
- Verifique a configuração de Zstandard: `python -c "import ctypes.util; print(ctypes.util.find_library('zstd'))"`. Se retornar `None`, o codec Zstandard falhará explicitamente; não existe fallback silencioso. Use `--codec gzip` apenas para escrever arquivos que deseja codificar com GZIP; ler arquivos Zstd ainda requer libzstd.
- Versões e procedência: [Licenças e procedência](#licencas). Não se inclui um binário de terceiros; a licença/cadeia de distribuição do libzstd do sistema é tratada pelo fornecedor. A dependência WASM do HTML permanece separada.

### Exemplos (a partir do diretório da entrega)

```sh
python tools/encode.py medicao.json --output medicao.afs
python tools/decode.py medicao.afs --output medicao-reconstruida.json
python tools/validate.py medicao.afs
python tools/inspect_file.py medicao.afs
python tools/encode.py medicao.json --output medicao-i16.afs --typed
python tools/encode.py medicao.json --output medicao-gzip.afs --codec gzip
python tools/encode.py instrumento.json --output instrumento.afp
python tools/inspect_file.py instrumento.afp
python tools/inspect_file.py instrumento.afp --deep
python tools/validate.py instrumento.afp
python tools/decode.py instrumento.afp --index 0 --output primeira-sessao.json
python tools/decode.py instrumento.afp --index 0 --record --output primeiro-registro.json
python tools/decode.py instrumento.afp --output instrumento-reconstruido.json
python tools/encode.py historico.json --output historico.afc
python tools/decode.py historico.afc --index 0 --output primeira-revisao.json
python tools/convert.py medicao.afs --output medicao-convertida.json
```

`--index` começa em zero e segue a posição original no manifesto, não a ordem das notas. Em perfil lê o metadado, cabeçalho e evidência correspondente. Em histórico lê a revisão indicada, sem validar sua genealogia inteira: use `validate` para percorrer o histórico isolado. `--record` devolve registro com a sessão, não o envelope inteiro do perfil. A listagem padrão do ZIP lê central/local, manifesto e cabeçalhos AFB, não verifica todos os CRCs/digests nem descomprime as sessões. `--deep` percorre e valida todos os blocos. O `.afs` individual é decodificado para inspeção. `convert` reconhece conteúdo e escolhe automaticamente JSON→binário ou binário→JSON. Codec 1 Zstandard nível 3 é padrão; `--codec store` permite teste sem compressão; `--codec gzip` é alternativa explícita. `--typed` usa tag 73 (big-endian) somente na grade quantizada; leitor reconhece 73/77. Tipos são reconstruídos como listas e mapas Python.

Use `--force` apenas para substituir explicitamente uma saída preexistente. A origem nunca é sobrescrita. Saída preparada em arquivo temporário no mesmo diretório e publicada por operação de filesystem ao final; falha mantém a saída anterior. Sem `--force`, publicação por hardlink (filesystem precisa suportar hardlinks; se não suportar, falha sem tocar no original). Não é garantia de persistência sob perda de energia; não há fsync ou journal de disco nesta CLI. Arquivos transport-only não são sessões válidas: para testes de envelope use `python tools/validate.py fixtures/transport-edge.afb --transport-only`. Nunca use essa opção para confiar em dados acústicos não validados.

### API para análise científica

```python
import sys
sys.path.insert(0, 'tools')
from archive import Archive
from cli import read_block

info, sessao = read_block('medicao.afs')
print(sessao.get('aggregate'))
with Archive('instrumento.afp') as ar:
    print(ar.manifest)
    for registro in ar.records():  # processa uma sessão por iteração
        sessao = registro['session']
        print(sessao['sessionId'], sessao.get('B'))
        # não acumule as sessões se quiser preservar o benefício de memória
```

`Archive.records(selected=N)` restringe o acesso a um registro; `Archive.revisions()` percorre revisões e valida ancestralidade/diff ao terminar o iterador. O consumidor não pode promover resultados antes do fim se requer validação integral. `Archive.validate()` percorre tudo. `codec.pack/unpack/cbor_encode/cbor_decode` são primitivas de transporte; não realizam autorização acústica. `semantics` verifica regras adicionais. Usar `read_block`, CLI e `Archive` para intercâmbio científico comum.

### Limites e decisões

AFB: 32 MiB CBOR, 34 MiB payload, chunks até 2 MiB, 16 chunks, janela Zstd até 2 MiB, saída DEFLATE limitada, 2.500.000 nós/5.000.000 tokens/60 níveis, texto e chaves conforme contrato. ZIP: 1 GiB, central 2 MiB, até 4.002 entradas, 2.000 registros ou 128 revisões, 8 GiB soma raw; caminhos fixos, sem extração ao filesystem por nome interno. Manifesto primeiro, CRC e SHA de cada bloco conferidos quando lido, sem frames anexados. Para escrever ZIP, os blocos são preparados em spool temporário no disco. Para decodificar ZIP completo para JSON, registros são escritos incrementalmente, hash JCS do wrapper calculado incrementalmente (números/estrutura preservados; formatação e bytes JSON podem mudar). A entrada JSON legada é limitada a 32 MiB, logo não há conversão JSON→AFB de um JSON monolítico arbitrariamente grande. Para perfis maiores, use leitura por sessão ou o exportador modular do aplicativo; um JSON grande reconstruído é para análise externa e pode ultrapassar o limite de importação legado.

Não confundir caps com pico RSS. Cada sessão decodificada, a árvore Python, cópias e strings de hash consomem memória adicional; durante validação/ligação ancestral pode haver duas revisões em RAM. O spool consome espaço em disco. A CLI não mede latência acústica. O limite de tempo do Worker JS não é reproduzido como timeout do processo Python: operações são limitadas em tamanho, CLI pode ser interrompida externamente; não há sandbox de processos. Em caso de encerramento abrupto pelo SO, arquivos temporários podem requerer limpeza. A suíte autônoma usa fixtures sintéticas; o teste de interoperabilidade opcional usa o HTML de confiança e um AFP fornecido pelo usuário.

### Testes reproduzíveis

```sh
python tests/test_codec.py
python tests/test_html_interop.py /caminho/index.html
python tests/test_html_interop.py /caminho/index.html --profile /caminho/instrumento.afp
```

O teste opcional requer Node.js moderno e um HTML local confiável do Afinador; executa os scripts de codec extraídos do HTML apenas para verificar transporte e equivalência de conteúdo. Não é teste de IndexedDB ou de interface.

**Limite semântico importante:** as ferramentas Python não implementam integralmente a política de confirmação física acima de 45 cents nem as decisões de arquivamento e descarte. Esses eventos são preservados como dados, mas a função `record()` pode divergir do validador do app ao derivar `physicalKey`. Não usar `validate` para autorizar curvas nem contornar rejeições do aplicativo. Consulte [Modelo semântico, seção 8](#identidade-fisica).


<a id="verificacao"></a>
## 7. Fixtures e verificação

### Arquivos de referência

Dados inteiramente sintéticos, sem medições de usuário. Exemplares de referência mantidos com seus hashes originais; usados por `tests/test_codec.py`. Não representam afinação aplicável. `session-*.afs` (STORE, Zstd e GZIP) contém sessão inconclusiva com resultado nulo. `profile.afp` contém essa sessão, cabeçalho e perfil. `history-empty.afc` é histórico vazio; `history-incomplete.afc` contém uma revisão draft/incomplete com delta=0 e nenhuma evidência física. Os JSONs expected são os objetos sintéticos reconstruídos, não versões de backup da medição do usuário. `transport-edge.afb` e `transport-multichunk.afb` testam apenas envelope/CBOR (não são sessões semanticamente válidas): incluem −0, subnormal, inteiro seguro máximo, UTF-8, Int16 e chunk boundary. SHA256SUMS registra hashes dos bytes exatos. Não exigir reprodução do mesmo fluxo Zstd entre versões de biblioteca; comparar hashes do exemplar entregue e equivalência do conteúdo.

### Evidências de interoperabilidade

Base consultada: `index.html`, SHA-256 `85cf47dfe7e216099f4a8a14363bb1eef9dc45c2974d78603eb5632f6500952b`.

- Conferência dos mapas estruturais: 53 listas de campos permitidos/obrigatórios do SECURITY13 coincidem com as listas usadas para gerar os CDDL; o cabeçalho de registro corresponde à projeção sem `session`. A lista do wrapper JSON de perfil permanece `schema schemaVersion profile records curves integrity`. Isso é comparação de listas, não prova de equivalência de tipos e predicados.
- `python tests/test_codec.py`: 18/18 testes aprovados, incluindo hashes, corrupção, limites, números e tags, compressão, perfis, histórico e escrita de saída.
- `python tools/validate.py CRAVO_SINTETICO_OITAVA_DO4_SI4_12_NOTAS.afp`: 12 registros validados no escopo parcial da CLI. O perfil do usuário não integra o ZIP.
- `python tests/test_html_interop.py index.html --profile CRAVO_SINTETICO_OITAVA_DO4_SI4_12_NOTAS.afp`: 39/39 blocos lidos, decodificados e regravados pelo codec JS extraído do HTML, com equivalência de conteúdo na leitura Python. Inclui 6 combinações escritas pelo Python (STORE/Zstd/GZIP × grade tipada ou não), 7 blocos de fixtures de perfil/histórico e 26 blocos do AFP sintético. O teste não executa a UI, a CSP ou o banco de dados do navegador.
- 12 hashes das fixtures conferidos.
- Ambiente: Python 3.13.5, Node 22.16.0, zlib 1.3.1, biblioteca de sistema libzstd.so.1.

A validação parcial da CLI não cobre integralmente as regras de identidade física e arquivamento; podem existir divergências de aceitação. Ver [Modelo semântico, seção 8](#identidade-fisica). A segurança, procedência de terceiros, homologação acústica, persistência nativa e interoperabilidade de todos os casos continuam fora do alcance desses testes.


<a id="licencas"></a>
## 8. Licenças e procedência

O aplicativo incorpora CBOR-X 1.6.6 no-eval, licença MIT incorporada no bloco `afbCodec214` do HTML.

Componente: `@bokuweb/zstd-wasm` 0.0.27, tarball de origem, SHA-256 `680a6ae81375a786c30671cf3824ff8c1d04657b5e540b4f92178897f2210344`. `package.json` declara MIT; README original `src/ZSTD-PACKAGE-README.md` declara glue MIT e núcleo Zstd BSD-3-Clause. O tarball não fornece os avisos completos do glue e núcleo nem identificação exata de revisão do núcleo. A procedência integral e os avisos exigidos desse componente ainda precisam ser confirmados antes da redistribuição pública. Antes de publicar, obter avisos exatos e revisão auditável (ou build reproduzido a partir de fontes oficiais), incluindo runtime Emscripten se aplicável, verificar vulnerabilidades e inserir avisos exigidos. Não inferir a versão do WASM a partir da libzstd instalada em Python.

Fonte: https://github.com/bokuweb/zstd-wasm ; https://github.com/facebook/zstd ; https://www.rfc-editor.org/rfc/rfc8878.html . A ausência de avisos completos é um gate aberto explícito. Não alegar revisão do binário de terceiros. O tarball original e o manifesto de build não acompanham este pacote. Conservar esses materiais separadamente, se disponíveis, para fechar a cadeia de procedência. Patches: seção de memória máximo 32768→512 páginas, inicial 258 preservado; glue `getHeapMax` 2147483648→33554432, remove export ES e comentário de source map para execução clássica; fornecimento de bytes explicitamente, sem fetch. Não há neste pacote evidência suficiente para fechar a auditoria de procedência do WASM.

GZIP utiliza API nativa do navegador, sem bibliotecas adicionais. SHA-256 incremental e preflight RFC1951 foram implementados no wrapper; testes com bibliotecas independentes não constituem auditoria criptográfica ou de segurança integral. Referências de formato: FIPS 180-4, RFC 1951/1952, RFC 8949, RFC 8746, RFC 8878.

### CLI Python

A implementação Python foi escrita para este projeto seguindo os contratos AFB 1.0 e verificações semânticas do aplicativo. Não inclui código de uma biblioteca CBOR de terceiros nem distribui binários nativos. O leitor de fixtures de referência serviu como referência; o novo leitor implementa preflight e limites próprios. Python: biblioteca padrão sob licença PSF (https://docs.python.org/3/license.html). zlib do Python: licença zlib (https://zlib.net/zlib_license.html). Zstandard 1.5.7: biblioteca compartilhada instalada no ambiente, originária de https://github.com/facebook/zstd; licenças BSD-3-Clause ou GPL-2 conforme aviso da distribuição copiado em `docs/NOTICE_LIBZSTD_SISTEMA.txt`. Nenhuma dessas bibliotecas é redistribuída neste ZIP. Versões testadas: Python 3.13.5, zlib 1.3.1, libzstd 1.5.7, Node v22.16.0 (somente teste). A instalação em outros SOs não foi validada. Os arquivos sintéticos herdados pertencem ao projeto. A procedência e os notices do binário Zstd WASM 0.0.27 dentro do HTML permanecem gate separado da publicação do Afinador; este pacote não resolve essa pendência.

A licença do código próprio e demais atribuições constam do README do projeto. O aviso de libzstd do sistema é preservado integralmente.
