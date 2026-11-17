# Roadmap — Análise Acústica, Inarmonicidade e Afinação Personalizada

> **Versão 3.0 — integração à arquitetura musical canônica do Afinador**  
> **Revisão e auditoria cruzada:** 17 de novembro de 2026  
> **Documento-mestre de produto, UX, arquitetura, matemática, dados, testes e implementação futura.**  
> **Base de implementação auditada:** `Etapa4_Limpeza_Validacao_Final_v1/index.html` (11.589 linhas; 707.224 bytes).  
> **SHA-256 da base:** `d898ea8e9c3c3c8442c273165338868e8de457396408447f0752b81a33bf53a8`  
> **Documento anterior:** `Roadmap_2_2.md`, SHA-256 `3f27eecc822598e2bf98848cee46e21152a793cc8dea7bab3128badfe17351c9`.  
> **Estado:** especificação para desenvolvimento **futuro**, não implementação concluída. O HTML de referência **não contém** ainda analisador multiparciais, ajuste B, perfis acústicos ou curvas instrumentais aplicáveis.  
> **Escopo da atualização 3.0:** abandonar integralmente MIDI/`pc` como identidade acústica ou índice de curva; integrar o grafo `keyId`/`pitchId`/`soundId`, catálogo canônico, ciclos históricos, EDOs, cilindro 2,5D, separação música/DSP e formatos atuais de diagnóstico/biblioteca. Preservar as decisões 2.2 sobre multiataque, modelo B, perfis, curvas, alvos assinados e fidelidade histórica.

## Como usar este documento

Este arquivo deve ser **suficiente, por si só**, para recuperar a visão do projeto, as decisões de interface, a matemática, os fluxos de uso, as escolhas de arquitetura, os critérios de qualidade e o planejamento de implantação das futuras funções. Não é necessário ter acesso à conversa que originou o documento. Foi preservada a estrutura de **sete fases** do roadmap original, com marco 0 transversal e subetapas de desenvolvimento. O texto original permanece no **Anexo A**, estritamente histórico e **não normativo quando conflita com a arquitetura 3.0**.

### Convenções de decisão

- **[DEFINIDO]** — requisito ou intenção explicitamente estabelecido pelo responsável pelo projeto ou pelo roadmap original. Deve ser preservado.
- **[RECOMENDADO]** — proposta de implementação técnica/UX resultante da análise. É suficientemente específica para orientar o desenvolvimento, mas pode ser revista mediante testes.
- **[A VALIDAR]** — método, limiar, desempenho, parâmetro numérico ou decisão que exige experimentos antes de se tornar um padrão definitivo.
- **[FUTURO]** — funcionalidade prevista, sem autorização implícita para implementá-la na fase atual.
- **[EXISTENTE]** — comportamento confirmado no HTML final da limpeza auditado em 17/11/2026. Não deve ser confundido com funcionalidade futura.

**Regra de interpretação:** uma proposta [RECOMENDADO] não pode revogar silenciosamente um requisito [DEFINIDO]. Uma referência a outro produto identifica uma ideia, um problema ou uma boa prática; não autoriza copiar aparência, ícones proprietários, códigos, textos ou algoritmos fechados.

---

# 1. Visão e princípios inegociáveis

## 1.1 Objetivo geral [DEFINIDO]

Evoluir o afinador cromático com temperamentos históricos para um sistema de **análise acústica e afinação individualizada por instrumento**, capaz de:

**Medir → Analisar → Caracterizar → Construir uma curva → Afinar.**

A experiência deve atender ao músico interessado em uma medição clara e ao usuário tecnicamente exigente que precisa inspecionar parciais, estimar inarmonicidade, avaliar uma curva e compreender as razões matemáticas de cada resultado.

## 1.2 Quatro conceitos que jamais devem ser confundidos [DEFINIDO]

1. **Temperamento musical:** conjunto de relações intervalares teóricas, calculadas a partir dos presets e dos ajustes do cilindro acústico de quintas.
2. **Afinação:** comparação do som produzido com uma referência de frequência.
3. **Inarmonicidade:** distribuição observada dos parciais reais de uma nota; depende do instrumento, da corda e das condições de medição.
4. **Curva instrumental:** correções por nota, calculadas ou escolhidas para um instrumento e um objetivo acústico específico.

**Distinção adicional da revisão 2.2 [DEFINIDO]:** uma quinta ou duodécima intencionalmente temperada **não tem, necessariamente, alvo de batimento zero**; selecionar um par de parciais (3:1, 6:2, 9:3 etc.) identifica **o que comparar**, não **qual relação musical impor**. Uma curva pode preservar intacta a *tabela de quintas* e ainda modificar os **intervalos efetivamente resultantes**; a diferença entre correções de notas adjacentes à comparação deve ser medida e comunicada.

O valor de inarmonicidade **não é**, isoladamente, um desvio de afinação, tampouco define a única curva ideal. Um coeficiente físico `B` não substitui um temperamento musical.

## 1.3 Regras de projeto

- **Preservar integralmente o afinador existente**: detectores, cilindro acústico de quintas, notações, presets, cálculos musicais, emissores e diagnóstico não serão reescritos para abrir espaço às ferramentas futuras. Novos módulos serão desenvolvidos em responsabilidades isoladas, mesmo com um único HTML autocontido.
- **Informação progressiva**: mostrar o essencial primeiro e permitir aprofundamento por interação explícita. Nem interface opaca que oculta dados, nem painel visual poluído por dezenas de números.
- **Transparência matemática**: o usuário deve poder responder: *o que foi medido? por que foi aceito? como foi calculado? o que mudou?*
- **Confiabilidade acima de aparente precisão**: nenhuma estimativa definitiva quando o sinal, a atribuição de parciais ou o modelo são inadequados. Em vez de `0,00042` sem ressalvas, exibir `medição inconclusiva` quando necessário.
- **Resultados reproduzíveis**: com o mesmo conjunto de dados, parâmetros e versão de algoritmo, obter o mesmo resultado dentro de tolerâncias definidas; diferenciar variação do áudio real de não determinismo do software.
- **Aquisição multiataque por nota [DEFINIDO]**: o usuário pode tocar a mesma nota quantas vezes quiser em uma sessão; cada ataque válido produz observação independente, revisável e preservada. O programa propõe o encerramento se houver convergência verificada, sem limitar o número de repetições nem tratar centenas de quadros sobrepostos como centenas de amostras independentes.
- **Aplicação reversível**: medições podem criar *prévia* de curva, mas não alteram automaticamente as frequências ativas do afinador nem reescrevem as quintas históricas.
- **Fidelidade histórica explícita [DEFINIDO / RECOMENDADO]**: separação entre (a) temperamento teórico por fundamentais, (b) *desafinação assinada* entre parciais do mesmo intervalo, (c) deslocamento causado por rigidez das cordas e (d) correção efetivamente proposta. O modo padrão recomendado para um temperamento desigual é **Fidelidade ao temperamento**; a opção **Otimização acústica** é escolha deliberada e comparável. Fidelidade pode significar restrições distintas: preservação estrita de intervalos fundamentais em uma região ou preservação do padrão de desvios acústicos de referência; nenhuma das duas será anunciada como equivalente à outra.
- **Arquitetura responsável com celulares**: cálculos intensivos em Worker, buffers limitados, atualização visual reduzida e regras claras para processos em andamento.
- **Privacidade local**: sem transmissão automática de áudio, perfis ou metadados; exportação sob comando do usuário. Não usar rastreamento invasivo ou identificadores persistentes de hardware.
- **Acessibilidade e consistência**: sem controles escondidos exclusivamente em gestos, informação não dependente só de cor, interfaces utilizáveis com toque, teclado e tecnologias assistivas.

## 1.4 O que NÃO integra este escopo inicial

- Substituir YIN + FFT/pYIN/SWIPE’/Pico por um novo detector geral.
- Corrigir automaticamente os temperamentos históricos com base em uma corda medida.
- Prometer identificação infalível de instrumentos, notas ou cordas em acordes complexos.
- Aplicar o modelo de corda rígida a sinos e sopros sem validação física.
- Construir uma curva de afinação *única* a partir de um valor isolado de `B`.
- Gravar áudio permanentemente ou enviá-lo a servidores.
- Introduzir sete telas para sete fases: **sete fases não correspondem a sete áreas de navegação**.

---

# 2. Estado de referência: o aplicativo atual

> Seção baseada no `index.html` fornecido com o roadmap; é uma fotografia da implementação na data acima. O implementador deve revalidar seus identificadores se trabalhar em versão posterior.

## 2.1 O que já está implementado [EXISTENTE]

- Aplicativo HTML autocontido para navegador, otimizado para celular, com captura do microfone mediante permissão.
- **YIN + FFT** com refinamento espectral adaptativo, **pYIN** com modelo probabilístico e Viterbi causal, **SWIPE’** em janelas espectrais próprias, e **Pico** como referência do componente dominante. Somente um dos quatro métodos opera como detector selecionado por análise normal.
- Seletor da FFT principal: **4.096, 8.192 (padrão), 16.384 e 32.768 pontos**. Pontos não são bins; a saída de análise real nessa implementação contém `N/2` bins úteis. A FFT visual principal e as janelas específicas de cada detector não são sinônimos.
- Leitura em nota e frequência; escala de cents; modulação de leitura **Bruta / Filtrada**; modos **Automático / Nota fixa**; seleção manual de nota-alvo.
- Notação científica e de Helmholtz com troca visual tocando no visor da nota.
- **18 presets internos**: 16 históricos (12 ciclos de quintas, quatro cadeias abertas, incluindo reconstruções identificadas) e 13-EDO/14-EDO. Referência histórica A4 **415,3 Hz** por padrão; EDO possui referência por **grau, oitava e `referenceHz` próprios**. Editor racional das quintas com c.p./c.s., tabelas de intervalos e gerador; **cilindro acústico 2,5D**, com lobo tracejado **direto entre os extremos** nas cadeias históricas pertinentes e órbitas EDO.
- Barra superior com **Ativar microfone**, **Configurações**, **Ajuda** e botão circular de tema imediatamente à direita de Ajuda.
- Temas **Claro — Marfim e carvão** (padrão, fundo `#EEECE7`) e **Escuro — Grafite monocromático** (`#101214` como fundo). O círculo do tema mostra a cor do **tema de destino**, não o tema atual.
- Configurações técnicas expansíveis de Geral, YIN + FFT, pYIN, SWIPE’ e Diagnóstico. Efeitos imediatos durante a sessão; persistência somente com **Salvar configurações**; **Restaurar padrões** não apaga A4, temperamento ou quintas.
- Ajuda rápida seguida de Ajuda avançada, recolhida por padrão.
- Monitor de diagnóstico opcional na ordem **Espectro FFT → Monitor (quando ativo) → Cilindro acústico 2,5D**, com captura de **20 s** e ZIP com JSON (`diagnosticSchemaVersion: 2`) e WAV **opt-in**. A captura PCM contínua via AudioWorklet é ativada para o WAV de diagnóstico, **não constitui automaticamente uma fonte contínua já disponível para a nova análise**.
- Processamento pesado em **Dedicated Worker**; FFT PFFFT via WebAssembly SIMD/escalar quando possível e fallback nativo onde suportado. SWIPE’ tem dependência própria do motor adequado.
- Barra inferior fixa de referência musical e temperamento; no modo histórico o campo é A4, no modo EDO é `referenceHz` do grau de referência. Tabelas e gerador permanecem em seções expansíveis.

## 2.2 Contratos que não podem ser quebrados

- O botão do algoritmo mantém o nome **YIN + FFT**; não haverá modo YIN puro nem seletor para desligar seu refinamento adaptativo.
- A janela temporal do YIN permanece gerenciada pelo algoritmo; não igualá-la automaticamente aos pontos de FFT selecionados pelo usuário.
- O pYIN e o SWIPE’ continuam matematicamente independentes do refinamento da FFT do YIN.
- Continuar usando a notação científica e Helmholtz, com a atual distinção entre texto principal e texto pequeno.
- O diagnóstico continua **desligado por padrão**, sem captura automática de WAV ou acesso oculto ao microfone.
- Alternar ferramenta não reinicializa A4, presets nem alterações de quintas; salvar configurações técnicas não equivale a salvar uma medição acústica.
- A alternância de tema não deve provocar perda da captura ativa ou invalidar o estado de áudio.
- O menu **Ferramentas** a ser criado é diferente de **Automático/Nota fixa** e de **YIN + FFT/pYIN/SWIPE’/Pico**.
- **Preservar atribuições e licenças embutidas no HTML**, especialmente PFFFT/FFTPACK e a licença MIT do SWIPE’ adaptado. Modularização não autoriza sua exclusão.

## 2.3 Testes conhecidos antes da expansão

Nos ciclos anteriores de desenvolvimento foram relatados testes de regressão sintética de **144 quadros FFT válidos**, com **142/144 leituras dentro de ±5 cents**; os dois quadros restantes diziam respeito ao caso de **55 Hz, 96 kHz e FFT de 4.096 pontos**, em que a leitura foi inconclusiva. Isso é **histórico de testes do projeto**, não uma garantia de precisão instrumental ou validação do novo analisador. Deve ser reexecutado a cada alteração de DSP e em hardware real.

## 2.4 Princípio de integração

O novo sistema deve ser um **consumidor opcional da infraestrutura de áudio e de resultados**; não uma modificação invasiva do caminho original. Estados e buffers separados garantem que uma medição de inarmonicidade não altere a interpretação normal do afinador.

## 2.5 Parâmetros técnicos atuais — não redefinir na expansão

Os controles abaixo foram confirmados no `index.html` de referência. Os futuros recursos **não devem alterar seus valores padrão** apenas por introduzir uma nova ferramenta:

| Componente | Valor atual ou opções | Papel |
|---|---|---|
| FFT principal | **8.192 pontos**; opções **4.096 / 8.192 / 16.384 / 32.768** | Visualização e refinamento FFT do YIN; não impõe a janela da análise de parciais. |
| Detector padrão | **YIN + FFT adaptativo** | Detector normal do Afinador, sem opção YIN puro. |
| Limiar YIN CMNDF | **0,17**; controle existente **0,05–0,26** | Aceitação do primeiro mínimo periódico. |
| Janela YIN | **Automática**, indicada na configuração como aproximadamente **65–185 ms** conforme frequência anterior | Não é a duração da FFT visual nem da futura medição B. |
| pYIN — limiares | **100**; controle **20–200**, passo 10 | Distribuição de hipóteses do detector probabilístico. |
| pYIN — distribuição Beta | **α=2, β=18**; campos editáveis nos limites do HTML | Modelo de probabilidade de limiares; não modificar para analisar B. |
| pYIN — confirmação de oitava | **2 quadros**; controle 1–5 | Comportamento temporal do Viterbi atual. |
| pYIN — peso contextual | **0,72**; controle 0–0,95 | Política de transição de oitava atual. |
| SWIPE’ — saliência | **0,20**; controle 0,05–0,50 | Aceitação de candidata SWIPE’; FFT própria. |
| Leitura temporal | **Bruta** por padrão; filtrada com **70%** ao selecionar o filtro | O filtro não altera o sinal físico capturado para futuros perfis. |
| Desempenho | **Automático** por padrão, ou Econômico | Não equivale ao estado de qualidade da medição acústica. |
| Diagnóstico | **Oculto** por padrão; captura **20 s**; áudio WAV opt-in; `diagnosticSchemaVersion:2` | Permanece entre FFT e cilindro acústico. |
| Tema | **Claro** (`#EEECE7`) padrão; escuro (`#101214`) | Alternância em botão circular, fora de Configurações. |
| Referência musical | **A4 415,3 Hz** por padrão histórico; EDO usa `referenceDegree`, `referenceOctave`, `referenceHz` próprios | Dois domínios de referência, ambos distintos de f1 observado. |

**Regra de compatibilidade:** os parâmetros existentes são da detecção/visualização do Afinador. Os parâmetros do futuro Analisador de parciais serão mantidos separadamente, com nomes inequívocos e eventual perfil avançado próprio. Não reutilizar `pontosFFT` como se controlasse automaticamente a resolução física de todas as ferramentas.

## 2.6 Arquitetura vigente — contrato obrigatório para TODO o desenvolvimento [EXISTENTE / DEFINIDO]

**Fonte de verdade, já implementada:** `CatalogoTemperamentos` (JSON interno versionado) + `MotorRacional` (frações de c.p./c.s.) + `ModeloIdentidadesHistoricas` ou `ModeloDivisaoIgual` geram `graph`; `CatalogoAlvosCanonicos.construir(graph)` valida/organiza alvos. Essas declarações estão no **script principal** do HTML; a expansão deve integrar-se ao mesmo escopo ou a uma interface interna explícita, sem duplicar funções musicais nem presumir que tais nomes já são APIs globais `window.*`. `estadoMusicalAtual` contém **somente** `{revision, temperament, graph, catalogoAlvos}`; não reintroduzir aliases de targets, tabelas MIDI/PC, caches paralelos de fechamento/lobo nem fontes musicais concorrentes.

Identidades e responsabilidade:

| Campo/API existente | Significado e restrição | Uso correto na expansão |
|---|---|---|
| `keyId` | Identidade da tecla física/lógica, única em uma disposição | Chave da medição/curva **com oitava**; preservar teclas enarmônicas |
| `pitchId` | Identidade da nota/grau; pode corresponder a múltiplas teclas | Associação musical; conferir ao importar/reativar |
| `soundId` | Agrupamento de alturas acusticamente coincidentes **no grafo vigente** | Exploração de coincidências; **não** substituir a identidade física persistida |
| `octave` | Registro inteiro associado ao alvo | Compor chave física `(keyId,octave)`; não assumir que nome de EDO é cromático |
| `targetId` | Identificador atual de alvo derivado de `[keyId,octave]` | Índice auxiliar; sempre vincular a snapshot do temperamento na persistência |
| `frequency` (Hz) | Alvo teórico já calculado | Única fonte para `f_temp`, via catálogo; não calcular de MIDI nem interpolar 12 classes |
| `CatalogoAlvosCanonicos.porTecla(cat,keyId,octave)` | Consulta de alvo físico | Preferencial para nota/curva ancorada em tecla |
| `CatalogoAlvosCanonicos.porNota(cat,pitchId,octave)` / `CatalogoAlvosCanonicos.porSom(cat,soundId,octave)` | Consultas de identidade e coincidência | Nunca arbitrar qual tecla o usuário tocou sem confirmação |
| `CatalogoAlvosCanonicos.listar(cat,politica)` | Registros `detector`, `fixo`, `geradorPadrao`, `geradorAmpliado` | Respeitar política real; nenhuma lista MIDI de 0..127 |
| `detectorEmOrdemDoGrafo` | Ordem estável de desempate da detecção | Preservar a regra existente ao sugerir nota acústica |

**Cadeias históricas:** `pitchId:'fifth:'+k` e `keyId:'keyboard:fifth:'+k`, com grafias enarmônicas independentes; configurações históricas de 12/13/14 teclas preservam as teclas-base. **Ciclos de 12 quintas** têm quinta compensatória e fechamento racional exato; **cadeias abertas** têm lobo representado por uma aresta **entre extremos**, não uma quinta normal de receita nem nó extrínseco no cilindro. As receitas incluem ajustes independentes c.p./c.s. e offsets por nota; preservar frações, não converter ida/volta por arredondamentos de cents. O editor de quinta e o cilindro são representações da **mesma receita/grafo**, não motores paralelos.

**EDO:** `pitchId:'degree:'+N+':'+j`, teclas `keyboard:degree:N:j` por padrão e possibilidade de várias `keyId` para um mesmo grau; `degree` é grau matemático, não classe cromática. O motor usa `divisionCount`, `fifthGeneratorSteps`, `referenceDegree`, `referenceOctave`, `referenceHz` e offsets de grau em c.p./c.s. **13-EDO** tem uma órbita de 13 (gerador 8), **14-EDO** duas órbitas de 7 (gerador 8). Não usar `octave` isoladamente para nomear automaticamente a nota EDO como Dó/Ré/Lá.

**Domínios de estado:** `estadoTemperamento.quintas`, `configuracaoIdentidades`, `configuracaoEDO`, `indiceQuintaCompensatoria`, `referenciaMusicalHz` e `estadoMusicalAtual` têm papéis diferentes. Em histórico o A4 está no domínio de 300–500 Hz; em EDO `referenceHz` do grau/oitava pode estar em 16–4600 Hz. Não tratar `referenceHz` EDO como A4 nem sobrescrever a referência histórica ao alternar. O grafo e o catálogo são validados **antes** da publicação atômica.

**Evolução separada de música e DSP:** `musicRevision` é incremento musical; `generationIdDSP` e `sessionIdDSP` controlam mudanças técnicas e descarte de quadros antigos. No HTML `ROLLBACK_INVALIDACAO_MUSICAL_DSP=false`. Troca de preset, A4, grau, layout ou offset **não** deve disparar `invalidarConfiguracaoDSP()` nem resetar pYIN/SWIPE'. Configurações técnicas, como FFT, continuam invalidando corretamente as respostas antigas. Uma futura `curveRevision`/revisão de aplicação de curva pertence ao **domínio de referência musical**, sem criar um novo `generationIdDSP` ou alterar dados capturados.

**Registros e oitavas:** detector/nota fixa históricos seguem o contrato convencional até Dó8; o gerador tem registro padrão Fá1–Fá7 e ampliado Dó0–Si9. EDOs têm políticas próprias. Os alvos ampliados são derivados do catálogo; o novo analisador precisa declarar faixa de medição física/limite de Nyquist **independentemente** da faixa de nomes ou do gerador. Não presumir 88 teclas ou 12 graus em todos os instrumentos.

## 2.7 Contratos atuais de arquivos e privacidade [EXISTENTE / DEFINIDO]

- `afinador-perfil-tecnico-v1` no `localStorage`: preferências técnicas e tema; salvar explicitamente, restaurar padrões não apaga dados acústicos.
- `afinador-biblioteca-musical-v1` / JSON `format:'afinador-tuning-v1'`, `schemaVersion:1`: biblioteca local de receitas e perfis musicais preexistente. **Não substituir nem migrar silenciosamente** para perfil acústico.
- `diagnosticSchemaVersion:2` no ZIP de diagnóstico de 20 s: usa `fixedTarget` canônico (`keyId`, `pitchId`, `soundId`, `octave`, `frequencyHz`), não `fixedTargetMidi`. Seu campo atual `referenceA4Hz` informa o **A4 histórico preservado**, e **não** identifica a referência EDO ativa; para futuro diagnóstico de EDO é necessário registrar explicitamente `referenceDegree`, `referenceOctave`, `referenceHz` com versão própria. A futura auditoria acústica tem formato **novo**; extensões incompatíveis do ZIP requerem nova versão e leitor anterior.
- Perfis acústicos e curvas são **futuros**: reservar schemas próprios `afinador.acoustic-profile` e `afinador.tuning-curve`, com versionamento independente. Não afirmar que existe migração de um perfil acústico MIDI já instalado — o JSON 2.2 era apenas **exemplo não implementado**.
- O diagnóstico AudioWorklet atual é **opt-in para WAV**, e não o caminho contínuo de PCM já pronto para o analisador. O desenho de aquisição compartilhada na seção 13 exige implementação e teste de exclusividade.

## 2.8 Regras de integração e bloqueio de arquitetura [DEFINIDO]

1. Toda medição com nota confirmada grava `(keyId,pitchId,octave)` e o **snapshot/hash** da base; `soundId` pode ser gravado como contexto do instante, não como chave permanente exclusiva. Medição acústica sem identificação confirmada permanece com `noteBindingStatus:'unresolved'` e frequências observadas, nunca recebe tecla por adivinhação.
2. Curva é função de `(snapshot,keyId,octave)→ΔCents`; duas teclas distintas que compartilham um som **podem ter Δ diferentes**, inclusive quando o som era igual antes de aplicar a curva. Declarar se a curva é por tecla ou grupo; não aplicar automaticamente um único Δ por `soundId`. **Coincidência teórica** (mesmo `soundId` no grafo-base) e **coincidência instrumental efetiva** (mesma `f_final` dentro da tolerância validada) passam a ser conceitos distintos; não modificar o `soundId` do grafo para representar a curva.
3. `f_temp` é **sempre** consultada em `CatalogoAlvosCanonicos.porTecla(snapshot.catalogoAlvos,keyId,octave).frequency`; qualquer frequência guardada em arquivo é testemunho para integridade, não segundo motor.
4. Uma curva ou perfil jamais modifica `graph`, `estadoTemperamento.quintas`, `configuracaoEDO`, A4/`referenceHz`, offsets ou cadastro de presets. Camada opt-in compõe referências **após** o motor canônico, sem publicar falsos soundIds ou alterar a identidade de teclas.
5. A compatibilidade depende de hash canônico de **receita, layout físico, referência, offsets e alvos efetivos por chave**, inclusive dados de definições pessoais; `musicRevision` isolado não é hash persistente.
6. Troca musical ou de layout que invalide uma curva ativa a **desativa de modo seguro** até revisão/reotimização explícita; não reativar por coincidência do nome do preset. Nenhuma mudança musical reinicia DSP.
7. Importação de perfil acústico/curva nunca cria grafo paralelo nem registra uma definição externa durante a **prévia**; a validação deve ser sem efeitos colaterais até confirmação e commit.
8. Os detectores atuais, a FFT visual, o diagnóstico, as licenças embutidas, a acessibilidade e a correção do lobo do cilindro são invariantes de regressão.

---

# 3. Pesquisa comparativa: aprendizados e diferenciais

Esta seção registra *o que motivou as decisões*, para não depender de discussões anteriores. As fontes públicas verificáveis estão na seção **Referências**. As avaliações de usabilidade abaixo são **análises de projeto**, não testes controlados de precisão entre fabricantes. Relatos de fóruns são anedóticos e não estabelecem a frequência de um defeito.

| Ferramenta | Recursos documentados | Lição de interface/problema a evitar | Resposta proposta neste projeto |
|---|---|---|---|
| **PianoMeter** | Coleta contínua de inarmonicidade; curva adaptativa; seleção automática de nota; estroboscópios por parcial; espectro, zoom e bloqueio de curva; pesos intervalares. | A atualização automática de curva pode não ser evidente para quem está afinando; alguns comandos de nota/visualização usam gestos. | Estados explícitos **Medindo / Prévia / Aplicada**, zoom visível, número do parcial junto ao marcador, explicação da atualização e botão de congelamento. |
| **pianoscope** | Medições por nota com indicação visual; repetição/aceitação de valores discrepantes; interpolação; detalhes de curva e de influência dos intervalos. | Um ponto discrepante pode refletir tanto erro de medição quanto característica real do instrumento; alternar visões por gesto não basta para toda a informação auditável. | Histórico de repetições, indicador de repetibilidade, acesso à evidência espectral de cada ponto e botão textual para as visualizações. |
| **TuneLab** | Espectro e fase; medidas de inarmonicidade; ajuste de curvas; procedimentos especiais de afinação. | Alta densidade de opções, seleção de parcial e procedimentos especializados exigem compreensão do fluxo. | Iniciar com um percurso guiado, permitir inspeção completa e nomear claramente o parcial ativo. |
| **Verituner** | Medição de múltiplos parciais, AutoNote, estilos e procedimentos técnicos. | A abundância de estados e controles pode tornar o aprendizado exigente. | Informações em camadas, estados visíveis e conteúdo técnico sob expansão explícita. |
| **Reyburn CyberTuner** | Estilos de extensão, modos de troca automática, correção de altura, recursos profissionais de afinação. | Modos especializados podem ser confundidos; o nome e o estado da ferramenta precisam permanecer identificáveis. | Diferenciar **Ferramenta**, **Modo da ferramenta**, **Algoritmo** e **Estado da curva**. |
| **Entropy Piano Tuner / pesquisa de entropia** | Exploração de critérios alternativos de otimização espectral. | Otimizar matematicamente não garante, por si só, preferência auditiva ou estabilidade; resultados exigem repetibilidade e comparação prática. | Objetivos explícitos, otimização determinística, comparação acústica e auditiva, sem afirmar uma curva universalmente ideal. |

### Exemplos concretos que orientam requisitos

1. **Nota muito aguda e ruído de ataque**: sinais agudos fracos podem ficar abaixo de ruído mecânico, e o espectro pode ter múltiplos picos próximos. Não presumir que o pico mais intenso seja o parcial certo; apresentar estabilidade por parcial, permitir seleção manual e restringir a análise à região pertinente.
2. **Uníssono não isolado**: duas ou três cordas próximas podem originar picos e batimentos que invalidam uma medição atribuída a uma única corda. O usuário deve escolher `corda isolada`, `uníssono` ou `nota completa`, com tratamento e avisos coerentes.
3. **Ponto de inarmonicidade muito diferente dos vizinhos**: exigir inspeção e repetição, mas **não suavizar nem descartar automaticamente** um ponto repetível sem registrar a decisão.
4. **Curva que se altera durante a análise**: cálculo em prévia é permitido, **aplicação silenciosa é proibida**.
5. **Desvio numérico pequeno, resultado sonoro ruim**: a curva precisa evidenciar os compromissos entre oitavas, duodécimas, quintas e outros intervalos. Zero cent em relação a uma curva não prova que ela seja adequada. **Adicional 2.2:** pureza de parciais 3:1/6:2/9:3 não equivale automaticamente a uma duodécima correta em temperamento desigual; comparar com alvo assinado histórico, não apenas zero.
6. **Informação demais ou de menos**: usar **informação progressiva**, preservando um caminho para a investigação matemática sem comprometer a medição rápida.
7. **Seleção de microfone não evidente**: quando a plataforma permitir, indicar fonte e parâmetros efetivamente em uso; incluir um teste simples do nível de entrada e nunca insinuar que um dispositivo específico está conectado sem evidência da API.
8. **Zoom espectral de difícil descoberta**: oferecer controle visível `Ampliar parcial`/`Zoom`, além de gestos opcionais.

### Diferencial a construir

> **Analisador de parciais excepcionalmente claro e confiável:** cada resultado numérico deve ter evidência consultável, qualidade mensurada, explicação reproduzível e histórico de decisões. A interface revela os detalhes **gradualmente**, sem competir com a tarefa musical.

Isso é um **objetivo de projeto**, não uma alegação antecipada de superioridade sobre programas comerciais. A qualidade só poderá ser declarada após testes comparativos reais.

---

# 4. Arquitetura de navegação e telas

## 4.1 Uma única entrada de navegação [DEFINIDO como direção aprovada]

**Adicionar um botão `Ferramentas ▾` junto a Microfone, Configurações e Ajuda**, preservando o botão circular de tema à direita de Ajuda.

Ordem proposta [RECOMENDADO]:

```text
[ Ativar microfone ] [ Ferramentas ▾ ] [ ⚙ Configurações ] [ ? Ajuda ] [ ● ]
                                                                ↑ tema de destino
```

Em larguras pequenas os controles poderão usar duas linhas, mas não poderão se sobrepor, truncar informação funcional ou criar rolagem horizontal. Não introduzir barra inferior de navegação concorrendo com a barra fixa de A4/temperamento.

**Nome deliberado:** `Ferramentas`, não `Modos`, para não confundir com `Automático / Nota fixa` e com os quatro algoritmos de detecção.

## 4.2 Quatro áreas de trabalho, apenas três novas

| Menu Ferramentas | Situação | Fases atendidas | Conteúdo |
|---|---|---|---|
| **Afinador** | Já existe; padrão | Fase 5 (integração futura) | Visor atual, cents, FFT, diagnóstico, cilindro acústico de quintas, tabelas, emissor. |
| **Parciais e inarmonicidade** | Nova | Fases 1–2 | Captura de nota sustentada, espectro detalhado, parciais, confiança, modelo B e resíduos. |
| **Perfis instrumentais** | Nova | Fases 3 e 6 | Instrumentos, medições por nota/corda, histórico, comparação, importação/exportação. |
| **Curvas de afinação** | Nova | Fases 4–5 | Construção, objetivos de fidelidade histórica ou otimização acústica, alvos assinados por intervalo, edição/comparação de curvas, prévia e aplicação confirmada. |

**Fase 7 (validação)** é transversal e não requer uma tela pública. **Fase 6 (modelos específicos)** amplia os seletores e análises existentes, sem criar automaticamente outra área.

## 4.3 O que aparece em cada área

- **Afinador:** mantém integralmente o layout e os algoritmos; um futuro indicador `Correção instrumental: desligada/ativada` aparece somente quando existir curva aplicável e validada.
- **Parciais:** substitui o corpo de medição pelo fluxo de captura/inspeção de espectro. O cilindro acústico de quintas **não precisa ficar presente**, mas o temperamento base segue acessível por referência quando aplicável.
- **Perfis:** exibe seleção de instrumento, cobertura de notas, sessões multiataque, execuções individuais, estimativa consolidada, comparação histórica, e gerenciamento de arquivos locais.
- **Curvas:** exibe gráfico de correções por nota, curva anterior, proposta, **modo de prioridade acústico-histórica**, intervalos afetados e estados `Rascunho / Prévia / Aplicada`. Para cada intervalo, distinguir desvio em fundamentais, diferença entre parciais e batimentos previstos.

A barra inferior fixa atual pode tornar-se **contextual** [RECOMENDADO], sem perder acesso a A4 e temperamento: no Afinador permanece como hoje; em Parciais pode destacar `instrumento / nota`; em Perfis `instrumento / perfil`; em Curvas `temperamento base / curva`. Não mudar A4 ou o temperamento de maneira implícita ao alternar de área.

## 4.4 Estados de navegação e segurança

1. Inicialização: abrir sempre **Afinador** com a mesma configuração musical anterior; não ativar áudio sem toque/permissão.
2. Selecionar outra ferramenta: conservar os ajustes musicais e o tema. Não salvar automaticamente medições parciais.
3. Se uma captura estiver ocorrendo: [RECOMENDADO] pedir confirmação antes de descartar a sessão, com opções **Continuar / Concluir e salvar / Descartar**; se tecnicamente seguro, permitir pausar e retomar, preservando timestamps.
4. A troca de área não pode deixar um Worker pesado ativo sem motivo nem causar dupla aquisição concorrente do microfone.
5. Ao voltar ao Afinador, recuperar a interface e os estados anteriores, exceto medições já confirmadas como encerradas.
6. Recursos de fases não implementadas não devem aparecer como botões acionáveis; se necessário apresentá-los em Ajuda avançada como `Planejado`, sem simular funcionalidade.
7. A escolha da ferramenta só será persistida entre visitas se houver decisão explícita de produto futura [A VALIDAR]; o padrão seguro é abrir no Afinador.
8. Tecla Esc, navegação do navegador, leitores de tela e foco devem funcionar. Modais/menus devem devolver foco ao botão que os abriu.

## 4.5 Inventário estimado de novos controles

| Área | Controles principais | Quantidade indicativa |
|---|---|---:|
| Barra superior | `Ferramentas ▾` | **1** permanente |
| Menu | `Afinador`, `Parciais`, `Perfis`, `Curvas` | 4 opções, dentro do mesmo menu |
| Parciais | `Medir`, `Congelar`, `Limpar`, `Salvar medição` | 4 contextuais; `Medir novamente` e `Finalizar e revisar` são ações de sessão exibidas por estado, não permanentes |
| Perfis | `Novo`, `Salvar`, `Importar`, `Exportar`, `Comparar` | 5 contextuais |
| Curvas | `Gerar prévia`, `Editar`, `Comparar`, `Aplicar`, `Exportar`; seletor `Prioridade` entre fidelidade e otimização | 5 ações contextuais + 1 seletor de objetivo |
| Afinador futuro | `Correção instrumental` | 1 interruptor contextual |

Total estimado: **um novo botão permanentemente visível**; aproximadamente **14 ações contextuais principais** (e até duas ações de sessão apresentadas conforme o estado), mais um interruptor futuro. Além disso existirão seletores, menus e ações secundárias em painéis de detalhes; **não** há obrigação de mostrar 14 botões simultaneamente. Nomenclaturas e contagem são orientações de UX, ajustáveis nos testes de usabilidade.

---

# 5. Informação progressiva — política obrigatória de interface

Este princípio é uma das decisões centrais do projeto.

## 5.1 Camadas de apresentação

**Camada 0 — Orientação imediata**: nome da ferramenta, estado da captura, nota esperada, próxima ação simples. Não exibir um resultado impreciso como definitivo.

**Camada 1 — Resultado essencial (padrão)**: nota, frequência, quantidade de parciais confiáveis, **execuções aceitas/tentadas e indicação de convergência**, status de qualidade, eventualmente B com ressalva. Na tela Curvas, o modo `Fidelidade ao temperamento` / `Otimização acústica` e o estado `prévia/aplicada` são essenciais e **não ficam escondidos**. Mensagens como `Aguardando sustentação`, `Medindo`, `Pronto para revisar` ou `Dados insuficientes`.

**Camada 2 — Inspeção por toque**: abrir **cada execução do mesmo som** ou um parcial no espectro/tabela, comparar resultados entre ataques e visualizar quais tentativas foram rejeitadas. Mostrar frequência real/ideal, desvio, amplitude, janela de medição, estabilidade e status `aceito/candidato/rejeitado`.

**Camada 3 — Detalhes matemáticos**: fórmula, modelo, **B por execução e B consolidado, dispersão entre execuções, ajuste conjunto com escala própria por ataque**, parâmetros, resíduos, pares de parciais e pesos do ajuste; indicação de pontos removidos, versões de algoritmos e critérios de confiança. Em Curvas, detalhar `I_T`, `I_final`, `t_T^harm`, `s`, `t`, `r`, `Δ_b−Δ_a` e batimento previsto em Hz, sempre com unidades e convenção de sinais.

**Camada 4 — Auditoria/depuração**: medições originais, decisões de exclusão, métricas por janela, latências, razão das alterações, identificação da fonte de áudio, exportação estruturada e eventual WAV por consentimento. Pode compartilhar apresentação com o Monitor de diagnóstico existente, mas o registro acústico duradouro pertence ao perfil.

## 5.2 Regras de apresentação

- Cada informação visível deve ter um significado imediato; valores como `B`, `RMS`, `resíduo` e `parcial 5` terão explicação contextual acessível.
- Botões visíveis para ações críticas; gestos de zoom, deslizamento e toque longo são **atalhos opcionais**, nunca o único acesso.
- `Confiança do parcial` e `Qualidade do modelo B` **não são a mesma métrica**. Exibi-las separadamente.
- Um resultado `Não confiável` não deve ser escondido nem convertido em `0`. Mostrar razão e ação útil: `aproxime o microfone`, `sustente mais tempo`, `isole uma corda`, `repita a medida`.
- Usar números com unidades: Hz, cents, segundos/milissegundos, dB relativos, coeficiente B **adimensional**.
- Diferenciar visualmente **medido**, **previsto**, **interpolado**, **rejeitado** e **aplicado** por legenda, traço, formas e texto; não apenas cor.
- Permitir `Ver por que?` e `Ver dados` em resultado, ponto do gráfico e curva.
- Exibir *estado de atualização*: `curva aplicada v3`, `prévia atualizada`, `2 novas medições não aplicadas`.
- Uma sessão multiataque mostrará `2 execuções válidas; ainda sem convergência` ou `3 execuções consistentes; você pode finalizar ou continuar`. A mensagem `convergência` requer critérios quantitativos validados, não apenas o número de ataques.
- **Não esconder resultados individuais atrás do B consolidado**: o usuário deve poder inspecionar ou excluir uma tentativa do ajuste e perceber como muda a estimativa. Não mostrar dispersão falsamente pequena por contar quadros correlacionados como replicações.
- O status deve continuar verdadeiro após trocar ferramenta, tema, orientação ou tamanho da janela do navegador.
- Help rápida: como medir e interpretar o resultado. Help avançada: métodos de estimativa, limitações, física, confiança, privacidade e troubleshooting. Não apresentar todas as fórmulas no primeiro contato.

## 5.3 Acessibilidade, tema e comportamento móvel

- Preservar temas **Marfim e carvão** / **Grafite monocromático**, tokens CSS, escolha salva somente via fluxo existente; todas as novas telas seguem os mesmos temas e o círculo de alternância não é duplicado.
- Contraste adequado, foco visível, `aria-live` moderado (sem anunciar dezenas de alterações de parciais por segundo), teclado e botões de toque apropriados.
- Zoom de gráfico acessível por controles de `+ / − / Restaurar`, arrastar e seleção de faixa; pinça opcional; eixos sempre rotulados.
- Tabelas largas têm rolagem horizontal **apenas dentro da tabela**, cabeçalhos identificáveis e visualização por cartões em 320–390 px.
- Dados críticos nunca desaparecem só porque uma tela é estreita. Podem migrar para uma seção expandida.
- Painéis e menus evitam competir com a barra fixa, incluindo a área segura inferior de iPhone (`safe-area`).
- A animação não deve transmitir dados acústicos falsos; mostrar valor aceito em cada atualização real ou estado de processamento.

---
# 6. Fase 1 — Analisador de parciais e inarmonicidade

**Prioridade: Alta | Complexidade: Média–Alta | Primeira funcionalidade acústica nova.**

**Requisito adicionado na revisão 2.1 [DEFINIDO]:** a aquisição é **multiataque por nota**. A sessão permanece aberta para repetições voluntárias; cada ataque com sustentação utilizável é processado e registrado separadamente. O sistema nunca transforma repetição em média aritmética automática de frequências sem examinar qualidade, repetibilidade e ajuste físico. A explicação e os estados de sessão estão nas seções 6.4.1–6.4.5.

## 6.1 Missão [DEFINIDO]

Identificar os principais parciais de **uma nota sustentada**, medir suas frequências e amplitudes, compará-los com a série harmônica ideal, expressar desvios em cents, estimar sua confiabilidade e permitir inspeção direta da evidência espectral. A primeira fase **não precisa determinar um B conclusivo**, nem propor automaticamente curva instrumental.

**Critério original de conclusão:** identificar e medir parciais de notas isoladas com estabilidade e distinguir componentes reais de ruídos/interferências.

## 6.2 Tela inicial da ferramenta [RECOMENDADO]

```text
Parciais e inarmonicidade          [Ajuda contextual]
Instrumento: [Piano ▾]  Fonte: [Microfone / descrição disponível]
Nota: [Automática | Manual]  [Tecla: Lá3 / keyId ▾]  Tipo: [Corda isolada ▾]

[  Medir  ] [ Congelar ] [ Limpar ] [ Salvar medição ]
Status: Aguardando nota sustentada · entrada mono · 48.000 Hz

NOTA IDENTIFICADA       PARCIAIS CONFIÁVEIS      QUALIDADE
Lá3 · 220,1 Hz          6 / 8 candidatos        Boa

[ FFT detalhada — picos reais, posições teóricas, zoom visível ]
[ Gráfico desvio em cents × ordem dos parciais ]
[ Lista resumida dos parciais ]
    1  220,10 Hz    0,0 c    confiável   [Detalhes]
    2  440,43 Hz   +0,9 c    confiável   [Detalhes]
    3  661,2  Hz   +2,6 c    candidato   [Detalhes]
    ...
[ Ver metodologia e resíduos ] (somente quando Fase 2 disponível)
```

**Todos os números acima são exemplos de organização, não testes reais.**

## 6.3 Componentes obrigatórios

- Cabeçalho com fonte de áudio efetivamente selecionada, nota ativa, modo de seleção e tipo de captação da corda.
- Estado da análise: `Parado`, `Aguardando sinal`, `Ataque`, `Sustentando`, `Processando`, `Pronto para revisão`, `Inconclusivo`, `Erro de áudio`.
- Resumo essencial: nota/f1 estimada; quantidade de parciais candidatos, aceitos e rejeitados; tempo efetivo de análise; indicação de qualidade (calculada de modo justificável).
- **FFT detalhada** com eixo de frequência (Hz, opção escala log), amplitude (dB relativo), cursores, zoom por parcial e posições previstas. O gráfico **não é** mera reprodução com zoom do canvas FFT atual; pode usar janelas temporais próprias.
- **Gráfico de desvio por parcial**: eixo X = número do parcial, Y = `1200 log2(f_medido/(n·f1))`, em cents; marcar pontos medidos e, posteriormente, curva calculada por B.
- **Tabela de parciais**: ordem `n`, frequência real `Hz`, frequência harmônica ideal `Hz`, diferença `Hz`, desvio `cents`, amplitude relativa `dB`, estabilidade `cents`, confiança, estado e motivo da decisão.
- Detalhes acessíveis ao tocar em parcial, com mini-espectro e a janela de tempo associada.
- Controles primários: **Medir**, **Congelar**, **Limpar**, **Salvar medição**; ações contextuais **Medir novamente** (rearmar nova execução) e **Finalizar e revisar** (fechar a coleta, sem aplicar uma curva). `Congelar` interrompe atualização da execução em inspeção, **não** rejeita outras execuções nem encerra automaticamente toda a sessão. `Limpar` só remove rascunhos da sessão corrente mediante confirmação; dados salvos não são excluídos sem confirmação específica. `Salvar` exige revisão e confirmação quando houver ressalvas.
- Opção **Repetir esta nota** livremente, sem número máximo rígido de ataques; comparação entre execuções aceitas/rejeitadas e opção de excluir/restaurar tentativa **apenas do consolidado**, sem apagar o registro acústico. Excluir/recuperar um parcial da candidatura ao ajuste também preserva o original.
- Opção `Nota automática / Seleção manual`, inclusive A4/temperamento em contexto apenas como referência musical, não como valor imposto ao f1 real medido.
- Indicação de microfone, sample rate real, processamento de captura (quando a API expõe), possíveis filtros de sistema e ausência de informações do hardware que o navegador não fornece.

## 6.4 Fluxo guiado e fluxo de inspeção

**Percurso guiado (padrão):**

1. Selecionar instrumento e condição `corda isolada / uníssono / nota completa`. Se a análise de B por corda for pretendida, recomendar isolar uma corda.
2. Selecionar nota manualmente ou permitir reconhecimento automático (com confirmação da identidade detectada).
3. Tocar `Medir`; informar que é necessária uma nota sustentada.
4. Detectar ataque e iniciar a janela estável, desprezando ou segregando o transiente inicial quando ele comprometer a análise.
5. Acumular janelas e mostrar progresso verdadeiro em segundos e quantidade de quadros úteis; pausa/repetição se necessário.
6. **Finalizar a execução individual** após sustentação útil/soltura da nota; atualizar a lista de ataques e rearmar a detecção, sem encerrar a sessão. Um ataque inválido é registrado com motivo e pode ser repetido. Não declarar `Pronto` apenas porque venceu um temporizador.
7. Após cada execução, mostrar parciais, B individual (quando já suportado), qualidade, **quantas execuções válidas** existem e evolução da estimativa agregada. Indicar `convergência ainda não demonstrada` ou sugerir `Você pode finalizar ou continuar`, sem fechar compulsoriamente.
8. **Finalizar e revisar** encerra a sessão voluntariamente; congelar o resumo, permitir inspecionar/excluir/restaurar execuções do ajuste e registrar decisões. **Salvar medição** só após revisão, no perfil ativo (Fase 3); antes disso permitir exportação avulsa em JSON versionado.
9. Se nenhum parcial ou nenhuma execução for confiável, oferecer `Repetir` e orientação específica; nunca criar uma média ou B com aparência de sucesso.

**Inspeção avançada:** o usuário escolhe duração, número máximo de parciais, região frequencial, comportamento de seleção de pico, métodos de refinamento e limites de confiança **apenas quando tais parâmetros tiverem sido validados**. A configuração por padrão continua conservadora.

### 6.4.1 Aquisição multiataque por nota [DEFINIDO / RECOMENDADO]

**Conceito:** uma `AcquisitionSession` agrupa `N ≥ 1` **execuções/ataques** da *mesma nota, fonte, corda/grupo e contexto de captura*. Uma `AcousticMeasurement` é a observação de **uma execução** (não cada quadro FFT). O vínculo musical é `(keyId,pitchId,octave)` **apenas após confirmação**; antes disso manter hipóteses acústicas e `noteBindingStatus=unresolved`, sem inventar a tecla quando duas teclas coincidem. Os quadros espectrais da sustentação são observações temporais *correlacionadas* dentro dessa execução. Os parciais e a estimativa de frequência podem variar dentro de um ataque; o coeficiente B final da nota será opcional e calculado posteriormente (Fase 2).

- Ao tocar **Medir**, iniciar sessão `armed` e escutar **transitoriamente** a nota, sem escrever WAV ou histórico persistente por padrão. Permitir ataques sucessivos até o usuário escolher **Finalizar e revisar**, **Pausar** ou **Cancelar/Descartar**. Não fixar limite de **quantidade** de ataques; impor **limites físicos de memória, duração da aquisição contínua, quota e número de quadros armazenados** com políticas de descarte de buffers temporários já resumidos. Ao atingir um limite seguro, **pausar explicitamente** e oferecer salvar/exportar/revisar, nunca descartar observações silenciosamente.
- Cada execução válida gera `executionId`, ordem e horário da execução, identificação de nota/corda, segmento PCM e janelas efetivamente analisadas, detecções de picos, parciais com estados, qualidade do sinal, resultado provisório, razões de aceitação ou rejeição e versão do método. **Tentativas descartadas por ruído ou truncamento também são contabilizadas**, não fingir que nunca aconteceram.
- **Identidade acústica fixa por sessão:** no modo `Nota automática`, A primeira **tecla musical** plausível precisa ser confirmada por `(keyId,octave)` quando existir ambiguidade, não apenas pelo `soundId`/Hz; ataques incompatíveis com a nota esperada não devem ser agregados, mesmo quando o detector os confunde com a oitava vizinha. Mudança de corda, instrumento, modo `corda isolada/uníssono/nota completa`, microfone ou sample rate encerra ou separa a sessão; nunca misturar resultados sob mesma identidade por conveniência.
- A duração de uma execução depende da qualidade do decaimento e da nota, não de cronômetro fixo. Distinguir `ataque`, `trecho sustentado útil` e `soltura/silêncio`. Alguns instrumentos têm sustain curto: aceitar uma medida somente se houver informação temporal suficiente para a resolução exigida; caso contrário sugerir nova tentativa.
- **Separar repetição verdadeira de quadros:** janelas FFT sobrepostas dentro de uma execução ajudam a localizar parciais, mas não contam como novas execuções na dispersão entre ataques. Identificar o número efetivo de blocos independentes ao estimar incerteza temporal, sem inflar significância.
- A cada toque aceito, oferecer visualização individual, comparação com os demais e um consolidado **provisório**. Não trocar a curva de afinação aplicada nem salvar automaticamente os resultados em perfil.

### 6.4.2 Máquina de estados da aquisição [RECOMENDADO]

```text
INATIVA → [Medir] → AGUARDANDO_ATAQUE
AGUARDANDO_ATAQUE → [onset plausível] → CAPTURANDO_ATAQUE
CAPTURANDO_ATAQUE → [transiente superado] → SUSTENTACAO_UTIL
SUSTENTACAO_UTIL → [soltura / fim útil] → PROCESSANDO_EXECUCAO
PROCESSANDO_EXECUCAO → [resultado com status, válido ou não] → AGUARDANDO_ATAQUE
AGUARDANDO_ATAQUE → [Finalizar e revisar] → REVISAO_DA_SESSAO
REVISAO_DA_SESSAO → [Medir novamente] → AGUARDANDO_ATAQUE
REVISAO_DA_SESSAO → [Salvar, confirmado] → SALVA
qualquer estado de coleta → [Pausar] → PAUSADA → [Retomar] → AGUARDANDO_ATAQUE
qualquer estado → [troca de identidade/áudio/interrupção] → PAUSADA/INCONCLUSA
qualquer estado não salvo → [Descartar, confirmado] → INATIVA
```

- Detectar **novo ataque** por mudança de energia/envelope e evidência de onset, com histerese, separação temporal mínima e retorno a estado de repouso. Uma única nota longa, vibrato, batimento, reverberação ou parciais que aparecem/desaparecem **não** podem criar dezenas de ataques falsos.
- Se um novo ataque ocorrer com a cauda anterior ainda audível, registrar `overlap_detected` e não combinar até demonstrar separabilidade física; oferecer repetir depois de cessar o som. Em notas rápidas, ataques muito próximos podem exigir modo manual.
- **Modo automático** é o padrão; **modo manual** permite `Iniciar execução / Encerrar execução` ou `Repetir esta nota` caso onset falhe. Os dois modos registram `triggerMode=automatic|manual` e a mesma evidência de sinal; não tratar um clique como prova de nota válida.
- Confirmar o fim de uma execução após critério físico de decaimento/soltura ou fechamento manual, com *timeouts* seguros configuráveis [A VALIDAR]. Distinguir `não detectado`, `rejeitado` e `processado, mas insuficiente`.
- Em análise contínua, rearmar apenas quando a execução anterior estiver resolvida; o Worker pode processar a execução anterior enquanto novas amostras são captadas, **desde que filas e buffers tenham limite estrito** e nunca haja fusão de sessões ou resultados atrasados.
- Se o usuário mudar de ferramenta, negar permissão ou interromper áudio, preservar o rascunho recuperável ou oferecer exportação; não chamar uma tentativa truncada de aceita.

### 6.4.3 Interface e informação progressiva da sessão [RECOMENDADO]

**Camada 0:** `Aguardando nota`, `Ataque 3: analisando`, `Aguardando próximo toque`, `Captura pausada`, sempre com instrumento/nota e fonte confirmados.

**Camada 1 (padrão):** `3 execuções válidas de 4 tentativas`; **B consolidado provisório** apenas quando Fase 2 estiver validada; indicador textual `Ainda não convergiu / Resultados consistentes / Modelo incompatível`; ações **Medir novamente** e **Finalizar e revisar**. Recomendação de 3 ataques é somente orientação inicial, não critério matemático ou bloqueio.

**Camada 2 (sob demanda):** cartões ou lista por execução `1ª, 2ª, 3ª...`, cada uma com duração útil, parciais aceitos, B individual (quando estimável), qualidade, motivo de rejeição, e opção `Incluir / Excluir do consolidado` com possibilidade de restauração. Comparar frequências de parciais equivalentes, não apenas B.

**Camada 3:** evolução do B consolidado **após cada execução** com faixa de dispersão/incerteza quando validada, influência de cada ataque e detalhamento dos resíduos. O gráfico deve preservar pontos individuais e indicar qual ajuste foi recalculado. Exibir métricas dimensionais e métodos; nunca mostrar uma porcentagem de confiança fabricada.

**Camada 4:** auditoria de cada ataque (trecho temporal, janelas, configurações, candidatos, excluídos, versões, razões), exportação local e WAV opcional **somente mediante consentimento explícito**. `Finalizar` não salva no perfil nem aplica curva; `Salvar` exige confirmação/commit verificável.

No celular, o resumo e as duas ações principais ficam visíveis; a lista de execuções e o gráfico de convergência permanecem recolhidos por padrão. Nenhum indicador deve piscar ou mudar de posição sem leitura nova. Sempre mostrar ao menos um motivo prático se uma repetição não for aceita.

### 6.4.4 Quantas execuções medir? [DEFINIDO / A VALIDAR]

- **Sem máximo fixo de toques** [DEFINIDO]. Após **uma** execução válida, só cabe resultado preliminar; com **duas**, pode começar a comparação; com **três**, o sistema **pode começar a verificar critérios de convergência**, sem afirmar que está conclusivo. Quatro ou mais são opcionais conforme qualidade do áudio e consistência do modelo. Esses números são **orientações de UX**, não thresholds científicos ou regras de aprovação.
- **Nunca encerrar a sessão automaticamente só porque chegaram 3 ataques.** Se houver dados suficientes, mostrar: `3 execuções consistentes. Você pode finalizar ou continuar medindo.` O usuário mantém o controle, inclusive se decidir parar sem convergência: o resultado fica inconclusivo e pode ser salvo/assinalado com ressalva, sem promover B a medição robusta.
- A convergência deve observar simultaneamente: estimabilidade de B/identificação das ordens, cobertura dos parciais, qualidade por execução, dispersão entre execuções, estabilidade do consolidado a nova observação (*leave-one-execution-out*), intervalo de incerteza quando calculável e adequação do modelo. **NÃO usar só número de ataques, variação pequena dos valores arredondados nem contagem de quadros FFT.**
- Distinguir `convergiu numericamente` de `precisão física demonstrada`. Repetir um mesmo viés de microfone, posição, harmônico mal atribuído ou uníssono não isolado pode produzir resultados altamente repetíveis e **incorretos**. Se o modelo não ajusta bem os parciais, manter `modelo incompatível` apesar da baixa dispersão de B.
- [A VALIDAR] Derivar limites de dispersão de B (absolutos e relativos, perto de B≈0), largura de intervalo, influência, tempo de sustentação e número/ordens de parciais por faixa/instrumento a partir de sinais sintéticos e dados físicos independentes. Faltando validação, mostrar **números e ressalvas**, não um selo `Alta confiança` automático.

### 6.4.5 Regras de intervenção, custos e memória [RECOMENDADO]

- Oferecer `Pausar`, `Retomar`, `Repetir` e `Finalizar e revisar` sem perder a identificação da nota; não reabrir captação se o microfone foi desconectado sem consentimento.
- Exclusão **lógica** do consolidado (`includedInAggregate=false`, motivo, instante, intervenção de usuário/algoritmo) é reversível; manter observações intactas. Reintroduzir um ataque deve recalcular o consolidado e suas métricas com o mesmo conjunto versionado de dados.
- Conservação de dados: durante a sessão, PCM fica em ring buffer controlado e resumos por execução ficam em memória; nunca guardar cópia infinita de cada janela. A ausência de WAV impede reconstruir forma de onda depois, mas não impede auditoria de picos e métricas já extraídas. Retenção persistente de PCM/WAV exige opt-in explícito.
- A operação `Limpar` somente remove rascunho não persistido depois de confirmação; exclusão de sessão salva ou histórico antigo é outra ação e tem trilha própria. O usuário deve poder exportar o rascunho quando a quota de persistência falhar.
- Uma atualização de detector, parâmetros, fonte de áudio ou modelo não altera retroativamente ataques já aceitos: criar revisão de análise explicitamente identificada ou exigir nova medição; nunca mesclar resultados incompatíveis como se fossem homogêneos.


## 6.5 Separar FFT visual e FFT de medição [DEFINIDO]

- A FFT principal atualmente usa seleção 4.096–32.768 pontos, com 8.192 padrão.
- A **medição de parciais deve possuir janelas temporais próprias** e, conforme necessidade acústica, diferentes comprimentos para graves e agudos.
- A duração física de `N` amostras é `T=N/fs`; a distância entre bins é `Δf=fs/N`. Mais pontos **não garantem precisão em cents**, resolução de dois tons próximos ou melhor estimativa de parcial.
- Zero-padding pode melhorar a interpolação numérica da localização de picos, mas **não aumenta a duração da amostra nem a resolução física efetiva**. Não usar somente zeros para afirmar que foram capturadas 65.536 amostras reais.
- Frequências próximas, falsos batimentos, vazamento espectral e janela de análise devem ser tratados explicitamente.
- O analisador deve registrar `windowType`, `windowSamples`, `effectiveDurationMs`, `zeroPaddingLength`, `sampleRateHz` e identificadores de segmento.
- Janelas progressivamente maiores podem aumentar a qualidade nos graves ao custo de tempo; otimizar essa escolha por faixa, não impor um único tamanho a todas as notas.

## 6.6 Modelo de dados da medição (nível funcional)

| Campo | Unidade / observação |
|---|---|
| `keyId`, `pitchId`, `octave`, `soundIdAtCapture`, `targetId`, `baseSnapshotHash`, `scientificNote`, `helmholtzNote` | Vínculo canônico confirmado e rótulos de apresentação; `soundId` é contextual; uma medição sem nota identificável conserva vínculo `null` |
| `fundamentalEstimateHz`, `firstPartialMeasuredHz` | Distintos; o primeiro parcial pode estar ausente |
| `partialOrder` (`n`) | Inteiro positivo; nunca inferir ordem apenas pela posição do pico em amplitude |
| `measuredHz`, `idealHarmonicHz` | f(n) real e `n·f1`; se f1 estimado, registrar sua origem |
| `deviationCents` | `1200·log₂(measuredHz/idealHarmonicHz)` |
| `amplitudeDbRelative` | dB referenciado à medida; não confundir com SPL calibrado |
| `frequencyStabilityCents` | Dispersão temporal; especificar estimador |
| `candidateConfidence` | Qualidade da atribuição do parcial; método versionado |
| `status`, `reasonCodes` | `accepted`, `candidate`, `rejected`, `unavailable` etc. |
| `sourceFrameIds`, `timeStartMs`, `timeEndMs` | Proveniência temporal para auditoria |
| `captureMode`, `microphoneInfo` | Metadados com proteção de privacidade |
| `sessionId`, `executionId`, `executionIndex`, `triggerMode` | Vínculo do ataque com a sessão, ordem de captura e origem do disparo |
| `executionStatus`, `includedInAggregate`, `reasonCodes` | Estado de cada ataque e elegibilidade para consolidação sem excluir o original |
| `onsetAtMs`, `sustainStartMs`, `sustainEndMs`, `releaseAtMs` | Tempos monotônicos ou relativos ao início da sessão; ausências como `null` com motivo |
| `usefulDurationMs`, `effectiveTemporalBlocks` | Tempo realmente útil e estimativa documentada de independência temporal, não contagem bruta de quadros FFT |
| `sessionConvergenceStatus`, `aggregationRevision` | Estado provisório da sessão e revisão do consolidado que preserva as execuções usadas |

## 6.7 Algoritmo espectral proposto [RECOMENDADO]

**Pipeline físico e computacional:**

1. **Aquisição de áudio contínuo**: consolidar PCM sem lacunas e com timestamps monotônicos. A aquisição da análise será separada da gravação opcional WAV. Se AudioWorklet estiver indisponível, usar somente um fallback cuja continuidade temporal possa ser demonstrada; se não houver, desabilitar de maneira explicada a medição de B, sem falsificar os dados.
2. **Verificação do sinal**: RMS, clipping, saturação, perda de amostras, ruído, variação grosseira de altura e mudanças de fonte. Registrar configurações solicitadas e as realmente aplicadas por `MediaStreamTrack.getSettings()` quando disponíveis. Não assumir processamento de áudio desativado sem conferir.
3. **Identificação de nota/fundamental candidata**: usar o detector ativo ou uma estimativa auxiliar, mas **não tomar a frequência de YIN como verdade absoluta** em uma corda inarmônica. Considerar a possibilidade de f1 ausente e testar hipóteses de ordem de parcial.
4. **Seleção de segmento estável**: evitar transiente de ataque e mudanças grandes da nota. Permitir capturar diferentes momentos do decaimento para medir estabilidade.
5. **Análise multijanela**: usar FFT com janela apropriada, interpolação local de pico e, quando necessário, métodos de ajuste senoidal/estimação de fase validados. Não atribuir precisão superior à demonstrada pelo teste.
6. **Busca de candidatos**: identificar máximos locais sobre um piso espectral estimado; verificar isolamento, amplitude, largura de pico, relação sinal/ruído, estabilidade e possíveis picos duplicados.
7. **Atribuição do número de parcial**: associar candidatos a ordens `n` de forma global ou iterativa, minimizando inconsistências; evitar usar ingenuamente `f_pico/f1` arredondado se a inarmonicidade já desloca o pico ou f1 é incerto.
8. **Verificação temporal**: confirmar persistência de cada componente através de quadros independentes. O programa deve distinguir um parcial que some naturalmente de um falso candidato.
9. **Ponderação/seleção**: combinar qualidade de pico, estabilidade temporal, consistência de modelo e detecção de mistura de cordas; registrar critérios utilizados e suas versões.
10. **Exportação auditável**: preservar picos candidatos, parciais aceitos e rejeitados, motivo de rejeição, **execução/sessionId, índices e estado de inclusão no consolidado**, parâmetros do método e estatísticas resumidas. Salvar FFT inteira somente de forma controlada se um modo de depuração futuro justificar; WAV é mais versátil para reprocessamento.

### Condições de rejeição ou incerteza

- Pico só presente no ataque ou em um quadro isolado.
- Risco de aliasing, frequência acima de Nyquist ou mais próxima da borda que a largura de resolução permite.
- Clipping, interrupção da aquisição, dropouts e forte variação de altura.
- Fundamental ou ordem do parcial ambígua; dois modelos com ajuste semelhante.
- Uníssono com componentes sobrepostos, batimentos e impossibilidade de atribuir o pico a uma corda única.
- Sinal insuficiente no agudo ou grave; ruído acústico/elétrico predominante.
- Espectro compatível com múltiplas notas ou ressonâncias em vez de um único conjunto de parciais.

## 6.8 Métricas de qualidade: não inventar percentuais

O rótulo `Boa`, `Moderada` ou `Insuficiente` exige calibração sobre conjuntos independentes de sinais. [A VALIDAR] Definir score contínuo a partir de SNR local, estabilidade, consistência de ordem, evidência temporal e número de picos sustentados. Se o score for exibido como **probabilidade percentual**, ela deve ser calibrada empiricamente; até lá, preferir métricas dimensionais e categorias com critérios documentados.

**Três avaliações distintas:** (1) qualidade do candidato/ordem, (2) confiabilidade da frequência individual, (3) compatibilidade de todos os parciais com um modelo físico — somente a terceira permite avaliar o B da Fase 2.

## 6.9 Aceitação da Fase 1

- [ ] Recuperar as frequências e ordens dos parciais de tons sintéticos harmônicos e inarmônicos, inclusive com f1 fraca ou ausente, nos limites de tolerância definidos antes do teste.
- [ ] Um parcial contaminado/rejeitado aparece com estado e explicação; a exclusão não apaga a amostra original.
- [ ] Identificar notas manualmente sem interferência de troca automática de oitava.
- [ ] Registrar e exportar Hz, amplitude, cents, janela e confiança de cada parcial.
- [ ] Diferenciar notas sustentadas, ataques e silêncio; nunca converter silêncio em medida confiável.
- [ ] Preservar o resultado após abrir/fechar detalhes, mudar tema e orientação.
- [ ] Regressão completa no afinador existente e ausência de cálculo extra quando a ferramenta não estiver ativa.
- [ ] Demonstração com instrumento real incluindo repetibilidade e inspeção de erro.
- [ ] Detectar vários ataques de uma mesma nota como execuções independentes, sem disparos extras por vibrato, reverberação ou um único sustain; permitir disparo manual alternativo.
- [ ] Permitir repetições indefinidas em número lógico, com memória física limitada e pausa avisada; preservar registros aceitos mesmo quando buffers temporários forem liberados.
- [ ] Encerrar/continuar a sessão por escolha do usuário; a mensagem de convergência é uma sugestão calibrada, não um fechamento automático nem promessa baseada em 3 ataques.

---

# 7. Fase 2 — Coeficiente de inarmonicidade B

**Prioridade: Alta | Complexidade: Alta.** Habilitar após ter um analisador de parciais validado.

## 7.1 Modelo físico do roadmap [DEFINIDO]

Para cordas rígidas adequadamente representadas pelo modelo:

\[
f_n = n f_1 \sqrt{\frac{1+B n^2}{1+B}}
\]

Onde `n` é a ordem do parcial, `f_n` sua frequência, `f_1` a frequência do **primeiro parcial físico** (não necessariamente o pico mais intenso) e `B` um coeficiente **adimensional**. Para `B=0`, `f_n=n·f_1`, a série ideal harmônica. `B≥0` é o domínio físico usual do modelo de rigidez adotado; um ajuste numérico negativo não autoriza concluir `B físico negativo`.

Diferença em cents contra a série harmônica:

\[
\delta_n = 1200\log_2\!\left(\frac{f_n}{n f_1}\right)
\]

Desvio previsto pelo modelo:

\[
\delta_n(B) = 600\log_2\!\left(\frac{1+B n^2}{1+B}\right).
\]

**Observação crucial:** se o primeiro parcial não estiver visível, não substituir `f1` pelo primeiro pico disponível. Uma forma para estimação conjunta é escrever

\[
f_n=nF\sqrt{1+B n^2},\qquad f_1=F\sqrt{1+B},
\]

ajustando simultaneamente `F` e `B` a vários parciais com ordens atribuídas. `F` é um parâmetro auxiliar de escala, **não** a frequência do primeiro parcial. Uma estimativa de f1 com parcial ausente deve ser marcada como **inferida pelo modelo**.

## 7.2 O que a interface deve mostrar

- **B estimado** e indicação clara do modelo físico em uso (`Corda rígida`).
- Quantidade e **ordens** de parciais efetivamente usados no ajuste, não apenas total de picos detectados.
- **Gráfico medido × previsto** e **resíduo por parcial** (Hz/cents).
- Desvio médio/mediano robusto, dispersão temporal do ajuste, pontos influentes e pontos rejeitados.
- Incerteza estimada de B com método explicitado (por exemplo, replicações temporais, bootstrap por janelas/blocos com dependência considerada ou propagação do erro de frequência). Não usar um intervalo de confiança fictício de ±valor fixo.
- Estado do modelo: `compatível`, `ajuste fraco`, `dados insuficientes`, `modelo incompatível`, `atribuição ambígua`.
- Explicação resumida de impacto: `parciais mais altos estão acima de n·f1`; **não** concluir automaticamente qual nota se deve afinar mais aguda.
- Botão `Por que este B?` que revela os parciais, pesos, resíduos e as escolhas do ajuste.

## 7.3 Ajuste numérico robusto [RECOMENDADO]

1. Validar que há **ordens múltiplas e suficientemente afastadas** para identificar dois parâmetros (`F` e `B`); dois pontos matematicamente suficientes não são uma estimativa fisicamente robusta.
2. Ajustar no domínio logarítmico/frequência relativa, com resíduos em cents (para evitar que os agudos dominem apenas pela magnitude de Hz).
3. Usar perdas robustas como Huber/Tukey ou comparação de modelos, combinadas a pesos de qualidade por parcial, sem confundir o robust loss com autorização para apagar dados.
4. Registrar a função objetivo, limites, inicialização, critério de convergência, tolerância numérica, solução e versão.
5. Comparar o ajuste com `B=0`, verificar se a melhoria é distinguível do ruído e se a estimativa é estável ao retirar um parcial (análise de influência).
6. Se várias soluções tiverem ajustes semelhantes ou a variância for elevada, declarar **B inconclusivo**, não escolher silenciosamente um número.
7. Evitar extrapolação não comprovada para parciais nunca observados; marcar como *previsão*, não medida.
8. Atribuição de ordens e ajuste B devem ser reavaliados conjuntamente se a distribuição espectral contradisser as hipóteses iniciais.
9. Não usar parâmetros de um único fabricante como intervalo universal de B. Limites e prioridades devem ser validados por família instrumental [A VALIDAR].

Exemplo **conceitual** de função objetivo (não fixa o método final):

\[
\min_{F>0,\,B\ge0}\sum_{n\in\mathcal A}
  w_n\,\rho\!\left(1200\log_2\frac{f_n^{\mathrm{medido}}}{nF\sqrt{1+B n^2}}\right),
\]

onde `𝒜` é o conjunto de parciais aceitos, `w_n` descreve qualidade e `ρ` é uma função de perda robusta. As restrições e a validação de convergência devem impedir resultados fisicamente absurdos.

## 7.4 Repetições e outliers: não confundir três casos

| Situação | Interpretação | Ação |
|---|---|---|
| Resultado incoerente e **instável** em capturas repetidas | Possível ruído, erro de atribuição, transiente ou mistura | Repetir e investigar; não aplicar à curva |
| Resultado discrepante da tendência, mas **repetível** e com bons parciais | Pode ser característica real da escala do instrumento | Preservar como medição; comparação com interpolação, sem exclusão automática |
| Parciais repetíveis, mas ajuste de B ruim | O **modelo de corda rígida** pode ser inadequado | Registrar parciais; classificar B como não aplicável/inconclusivo |

O procedimento de aceitar/rejeitar um outlier deve registrar **autor, instante, motivo e valor original**, permitir reversão e conservar o histórico.

### 7.4.1 Agregação robusta entre execuções [RECOMENDADO; validar estatística]

**Não adotar como estimador principal a média aritmética cega das frequências ou dos valores B.** Existem três níveis de informação: (i) vários quadros **correlacionados** dentro de uma execução, (ii) execuções **independentes** da mesma nota/corda, (iii) notas diferentes do instrumento, usadas somente posteriormente para perfil e curva. Misturar esses níveis produz certeza artificial.

Primeiro, estimar por ataque `j` as frequências dos parciais e a qualidade espectral; quando identificável, calcular também `B_j` (estimativa individual) e seu estado. Para o consolidado, preferir ajuste robusto **conjunto** a todos os parciais aceitos das execuções incluídas, com **um coeficiente B comum** e **uma escala de frequência por execução**:

\[
f_{j,n}=n f_{1,j}\sqrt{\frac{1+B n^2}{1+B}}=n F_j\sqrt{1+B n^2},\qquad F_j=\frac{f_{1,j}}{\sqrt{1+B}}.
\]

Aqui `j` é a execução e `n` a ordem do parcial. `F_j` e `f1,j` podem variar ligeiramente entre ataques; `B` é compartilhado **somente se** identidade de corda, período de tempo e modelo físico justificarem essa hipótese. Uma fonte com variação sistemática relevante de B entre toques pode exigir resultados separados, nunca um único B forçado.

Uma função objetivo de referência, não fixando o algoritmo final, é:

\[
\min_{B\ge0,\;F_j>0}\sum_{j\in\mathcal J}\alpha_j
  \sum_{n\in\mathcal P_j} w_{j,n}\,\rho\!\left(
  1200\log_2\frac{f^{\mathrm{medido}}_{j,n}}{nF_j\sqrt{1+Bn^2}}
  \right),
\]

em que `𝒥` contém execuções aceitas e incluídas, `𝒫_j` contém as ordens identificadas, `w_j,n` pondera qualidade do parcial **normalizada dentro da execução** e `α_j` controla a contribuição de cada ataque (por padrão evitando que uma execução com muitas janelas ou picos domine todas as outras). `ρ` é uma perda robusta validada. Sem parciais/ordens suficientes para separar `F_j` de `B`, o estado é `insufficient_data`.

**Comparadores e diagnósticos obrigatórios:** estimativas `B_j` quando válidas; mediana/mediana ponderada como referência robusta de comparação; dispersão entre ataques por método documentado (por exemplo, MAD com correção apropriada); retirada de uma execução de cada vez (*leave-one-execution-out*); sensibilidade à retirada de cada parcial; resíduos em cents; cobertura de ordens; adequação do modelo. Mostrar a diferença entre consolidado e cada execução, não apenas um valor final.

**Incerteza:** não usar bootstrap de quadros sobrepostos como se fossem observações independentes. Usar a **execução como unidade de reamostragem** (*bootstrap por clusters/ataques*) apenas quando o número independente de execuções permitir estimativa estável; com poucos ataques, rotular intervalo como **não estimável** ou provisório. Reamostragem temporal em blocos pode estimar erro interno de cada execução, mas não substitui variabilidade entre ataques. Viés sistemático compartilhado deve ser avaliado separadamente; três ataques iguais não demonstram acurácia absoluta.

**Revisão versionada:** depois de cada ataque válido, atualizar o consolidado em memória com novo `aggregationRevision`, lista de `includedExecutionIds`, método/versão, pesos e motivos. `Finalizar` congela a revisão de coleta; `Salvar` persiste a revisão explicitamente aceita. A inclusão/exclusão reversível de qualquer ataque exige recomputação e nova revisão, nunca edição do resultado anterior sem trilha.

### 7.4.2 Convergência, repetibilidade e parada sugerida [DEFINIDO / A VALIDAR]

A interface não pode apresentar convergência apenas porque `N ≥ 3`. Exigir, em conjunto, evidência suficiente por execução, B identificável, ordens bem distribuídas, resíduos aceitáveis, dispersão entre ataques e influência de um ataque adicional/retirado pequenas **em unidades adequadas**, além de consistência física. Como `B` pode ser muito próximo de zero, não usar apenas erro relativo para julgar estabilidade. Parâmetros exatos são **[A VALIDAR]** com dados independentes por família/nota.

Estados recomendados: `preliminary` (uma observação útil), `collecting` (repetições em curso), `repeatability_unverified`, `consistent_provisional` (repetibilidade observada, sem certeza física demonstrada), `converged_validated` (somente após calibragem), `insufficient_data` e `model_mismatch`. **Convergência estatística não significa adequação do modelo**: um B altamente repetível pode ser fisicamente inválido quando os resíduos são grandes ou as cordas misturadas.

A sessão **nunca se encerra automaticamente** ao atingir convergência; mostrar sugestão opcional de finalizar ou continuar. Se o usuário finalizar sem dados suficientes, registrar `inconclusive` e permitir salvar com ressalva, sem alterar curvas. Medições repetidas em dias, posições de microfone ou contextos diferentes são **sessões distintas**; não agregá-las automaticamente ao mesmo B de sessão. Podem ser comparadas posteriormente no perfil.


## 7.5 Fatores que limitam B

- Número e distribuição de parciais; fundamental ausente; ruído; amplitude relativa; duração e decaimento; modulação de frequência.
- Duas ou três cordas tocando juntas; picos batendo entre si; acoplamento, ressonâncias de caixa/tampo e modos múltiplos.
- Instrumentos não bem descritos pelo modelo; por exemplo, sinos de modos não harmônicos.
- Mudanças grandes de tensão entre medição e afinação; não presumir constância exata do perfil sem avaliação.
- Erros de amostragem/latência, tratamentos do microfone, aliasing, limite da janela e quantização numérica.

## 7.6 Critérios de aceitação da Fase 2

- [ ] Recuperar B conhecido em sinais sintéticos com diversos `B`, notas, intensidades e parciais ausentes; definir **tolerâncias absolutas e relativas por faixa** com base em precisão física demonstrada, não apenas por desejo.
- [ ] `B=0` permanece compatível com harmônicos ideais; níveis baixos não produzem valores positivos artificialmente significativos.
- [ ] Em sinais insuficientes ou incompatíveis com corda rígida, devolver `inconclusivo`/`não aplicável` e explicação.
- [ ] Testar erros de ordem de parcial e sensibilidade a um parcial espúrio.
- [ ] Repetições de um mesmo áudio/mesma configuração produzem resultados estáveis.
- [ ] Repetições com cordas reais permitem avaliar dispersão, deriva e influência da posição do microfone.
- [ ] Dados brutos preservados ao rejeitar picos; qualquer ajuste manual reflete-se no relatório de auditoria.

---
# 8. Fase 3 — Perfis acústicos individuais

**Prioridade: Alta | Complexidade: Média–Alta.** Depende de um registro confiável de parciais e, para instrumentos de cordas rígidas, de B validado.

## 8.1 Propósito [DEFINIDO]

Armazenar características de **instrumentos individuais** com histórico de medições por nota, sem misturar observações de várias cordas, instrumentos ou ocasiões. Permitir comparar uma medição atual com anteriores e exportar/importar o perfil completo.

## 8.2 Tela de Perfis [RECOMENDADO]

```text
Perfis instrumentais
[Instrumento: Piano de estudo ▾] [Novo perfil] [Importar]
Família: piano | extensão: A0–C8 | 32 de 88 teclas medidas

[Mapa de notas/teclas: medidas | pendentes | inconclusivas]

Nota selecionada: A3 [Medir novamente]
Última medição: 2026-11-15 · qualidade boa
B: 0,00038 (modelo corda rígida) | 7 parciais aceitos

[Ver medição] [Comparar histórico] [Exportar perfil]

Histórico
15/11 — corda isolada 1 — confiável
12/11 — corda isolada 1 — moderado
10/11 — uníssono completo — não equivalente à medição isolada
```

Exemplos exclusivamente ilustrativos.

## 8.3 Identidade de um perfil

- `profileId` gerado localmente, sem identificadores persistentes do aparelho; `displayName` fornecido pelo usuário.
- `instrumentFamily`, `instrumentSubtype`, faixa e mapeamento musical. Para piano, suportar **88 notas (A0–C8)**, com extensão configurável quando justificável.
- Campos opcionais de identificação **escolhidos pelo usuário**, como fabricante/modelo, localização física genérica, observações e data; não coletar automaticamente nomes pessoais ou números de série.
- Captura/nota: `(keyId,pitchId,octave)` e `baseSnapshotHash` quando a tecla estiver confirmada; `targetId` e `soundIdAtCapture` como metadados, não como chave de substituição; notações científica/Helmholtz **somente quando cabíveis** (graus EDO conservam seu rótulo de grau), `stringIndex`/grupo e condição de medição.
- Distinguir pelo menos três tipos: **corda individual**, **grupo de cordas em uníssono**, **nota completa**; observações nesses tipos **não são intercambiáveis**.
- Versões de captação/analisador/modelo, fontes de áudio e informações de qualidade, para possibilitar auditoria após atualizações.
- Uma nota poderá ter **várias medições independentes**; não sobrescrever automaticamente a anterior.

## 8.4 Estrutura e semântica do histórico

1. Toda medição recebe ID e timestamp; o usuário pode editar observações sem reescrever o conteúdo acústico histórico.
2. Valores **medidos**, **inferidos pelo modelo**, **estimados por interpolação** e **alterados manualmente** devem usar campos/estados distintos.
3. Cada **execução/ataque** é uma `AcousticMeasurement` individual; a `AcquisitionSession` agrupa execuções da mesma nota e contexto. Várias execuções podem produzir **consolidação robusta versionada**, mas cada medição permanece acessível e auditável. **Média de B ou Hz não substitui o ajuste conjunto** quando este for identificável e validado.
4. O usuário pode marcar uma medição como `descartada da modelagem` sem apagá-la; exclusão física de dados exige confirmação.
5. Medições antigas com algoritmo anterior não são automaticamente reprocessadas; somente quando houver áudio local apropriado e consentimento.
6. A exportação preserva o histórico de alterações, **sessionIds, executionIds, conjuntos de ataques incluídos/excluídos, parâmetros de consolidação, revisões e estado de convergência**, suficientes para reconstruir B/curvas sem depender da interface.
7. Ao importar, verificar esquema, valores finitos, tamanho, relação dos IDs e possíveis colisões; não executar código contido no JSON.

## 8.5 Armazenamento local [RECOMENDADO]

- **IndexedDB** para perfis, medições, resultados intermediários e versões de curvas: adequado a conjuntos estruturados maiores que configurações simples.
- **Preservar** as duas utilizações atuais de `localStorage`: `afinador-perfil-tecnico-v1` (preferências pequenas) e `afinador-biblioteca-musical-v1` (biblioteca musical atual), respeitando os respectivos fluxos. **Novos perfis acústicos** vão para IndexedDB; não transferir automaticamente a biblioteca musical nem apagar perfis musicais ao restaurar preferências.
- Arquivos de áudio opcionais podem ter tamanho maior; oferecer política de retenção e armazenamento separada, limitar quota e informar claramente o espaço ocupado.
- Mudanças de versão do esquema exigem migrações explícitas e testes de ida/volta de exportação.
- Exportar/importar perfil em JSON versionado, com opção de arquivo compacto (ZIP) contendo áudio somente mediante escolha explícita do usuário.
- Dados não são enviados para servidores. Alertar que limpar dados do navegador ou trocar de aparelho pode apagar perfis não exportados.
- Em navegação privada, armazenamento restrito ou `file://`, detectar ausência de persistência e oferecer exportação, sem informar falsamente `Salvo`.
- Recuperação após falha e backup: gravações transacionais com commit atômico; impedir perfil parcialmente atualizado.

## 8.6 Interface comparativa

- Comparação **mesma nota, mesmo tipo de corda**: diferença em f1, B, amplitudes, estabilidade e qualidade entre duas datas. Mostrar separadamente variabilidade **entre ataques da mesma sessão** e **entre sessões diferentes**, sem fundi-las automaticamente.
- Se tipos diferirem, mostrar aviso `Corda isolada versus uníssono: comparação física limitada`.
- No mapa do piano, distinguir notas não medidas, medidas confiáveis, repetição recomendada e dados incompatíveis com o modelo.
- Ordenar por faixa, data, qualidade e notas críticas (por exemplo, perto da transição grave/tenor).
- Permitir abrir o espectro original a partir do ponto `B` do histórico.
- Mostrar quanto mudou e **por quê** (mais parciais, outra janela, mudança de microfone, nova versão do algoritmo, diferença real da corda).

## 8.7 Critérios de aceitação da Fase 3

- [ ] Criar, salvar, reabrir, renomear, duplicar, importar, exportar e excluir perfil com confirmação.
- [ ] Preservar todas as notas, **sessões e execuções**, incluindo tentativas rejeitadas e revisões de inclusão, sem alterar ordem dos parciais, valores e tipos de captura.
- [ ] Testar 88 notas por piano e múltiplos perfis sem queda ou travamento relevante.
- [ ] Passar em round-trip `exportar → importar → comparar hashes/valores` com equivalência de dados.
- [ ] Validar migração de pelo menos uma versão anterior simulada do schema.
- [ ] Distinguir dados incompletos, incompatíveis e resultados interpolados.
- [ ] Sem internet, manter todos os recursos locais já existentes; sem IndexedDB, falhar de modo claro e oferecer exportação.
- [ ] Não interferir nos temperamentos, A4 ou configuração dos algoritmos do afinador.

---

# 9. Fase 4 — Curvas de afinação personalizadas

**Prioridade: Alta | Complexidade: Muito alta.** Só iniciar após validar a aquisição dos parciais e os perfis. Os controles podem ser prototipados antes, mas não indicar curvas matematicamente definitivas sem validação.

## 9.1 Objetivo [DEFINIDO]

Construir curvas por nota com correção em cents relativamente a um **temperamento de referência explícito**, considerando medições de parciais, propriedades do instrumento e **critérios acústicos escolhidos** (por exemplo, compromissos entre oitavas e outros intervalos). Possibilitar comparação, interpolação com incerteza, ajustes manuais e aplicação opcional. **Para temperamentos desiguais, nunca converter automaticamente a escolha de parciais comparados em obrigação de batimento zero**; distinguir alvos musicais e acústicos conforme a seção 9.7.

**Princípio absoluto:** `B` não determina sozinho uma curva ideal; não existe um único conjunto universal de correções para todo instrumento.

## 9.2 Tela de Curvas [RECOMENDADO]

```text
Curvas de afinação       Perfil: [Piano de estudo ▾]
Temperamento base: [Pitagórico ▾]  A4: [415,3 Hz]
Curva ativa: [Teórica (sem correção)]

[Gráfico: correção Δ(keyId,oitava) em cents × tecla do instrumento]
    • linha teórica (0 em relação ao temperamento selecionado)
    • curva anterior aplicada (se houver)
    • prévia calculada, com intervalos de incerteza
    • pontos medidos / interpolados / editados pelo usuário

Prioridade: [Fidelidade ao temperamento ▾]  (padrão para desigual)
             [Otimização acústica]            (opção explícita)
[Critérios acústicos ▾] [Pesos e restrições ▾]
[Gerar prévia] [Comparar] [Editar pontos] [Aplicar] [Exportar]
Estado: PRÉVIA — NÃO APLICADA

Nota selecionada: A4
Teórica: 415,300 Hz | Proposta: 415,300 Hz | Δ: 0,0 c
Informação: 6 parciais, 3 medições, incerteza em revisão

Intervalo selecionado: [A3–E5 / duodécima ▾]
[Desvio teórico / Desvio dos parciais / Batimento previsto]
[Por que esta correção?] [Quais intervalos mudam?]
```

## 9.3 Três estados obrigatórios da curva

1. **Medindo**: novas medições entram no perfil; um cálculo experimental pode ocorrer em segundo plano, mas a **curva aplicada não muda**.
2. **Prévia**: o sistema apresenta uma nova curva com ID/versão e diff para a curva aplicada. Nenhum valor de referência do Afinador muda enquanto estiver em prévia.
3. **Aplicada**: após confirmação explícita, a curva é congelada em versão identificável e passa a poder ser usada pelo Afinador. Alterações posteriores geram nova prévia, nunca atualização silenciosa.

**[RECOMENDADO]** Acrescentar `Rascunho` para edições manuais ainda não resolvidas. Uma prévia válida pode ser descartada sem afetar a anterior. A qualquer instante: `Desativar correção` retorna às referências do temperamento base.

## 9.4 Camadas de informação no gráfico

- Eixo horizontal: **ordem física das teclas do instrumento**, identificadas por `(keyId,octave)`; rótulos científicos/Helmholtz quando disponíveis e graus EDO quando aplicáveis; piano típico A0–C8. Duas teclas enarmônicas nunca podem ser fundidas no mesmo ponto por terem frequência igual.
- Eixo vertical: **cents relativos ao temperamento base**, não necessariamente relativos ao igual temperamento. O rótulo deve nomear a referência usada. Em comparação adicional com temperamento igual, mostrar **um segundo conjunto de dados/escala explicitamente rotulado**, nunca trocar silenciosamente a referência.
- Linha de referência `0` = temperamento base; linha da curva aplicada = versão atual; linha de prévia = proposta.
- Pontos identificados por origem: `medidos`, `estimados por modelo`, `interpolados`, `manuais`, `sem dados`; incerteza quando validada.
- Tooltips/seleção mostram Hz teórico, Hz proposto, Δcents, origem do ajuste, critérios usados e versões.
- Permitir marcar quebra de escala ou mudança de material/categoria de corda em piano; suavização forte não deve apagar automaticamente uma irregularidade física repetível.
- Comparar duas curvas por diferenças por nota, RMS/mediana dessas diferenças, extremos e listas dos intervalos mais afetados; essas estatísticas não são critérios únicos de qualidade acústica.
- Em temperamentos desiguais, oferecer inspeção por par de notas: `intervalo por fundamentais previsto no temperamento`, `intervalo por fundamentais com curva`, `mudança Δ_superior−Δ_inferior`, `desvio assinado entre parciais ideal harmônico`, `desvio assinado previsto com B` e `diferença de frequências em Hz`; não chamar todos esses valores simplesmente de "desvio da duodécima".

**Interpretação de abscissa:** a ordem horizontal da curva vem do mapa físico do perfil. A correção deve ser aplicada por `(keyId,octave)`; `soundId` é equivalência observada na base, não permissão para fundir teclas. Em 13/14 históricos e EDO personalizado, nunca ordenar por frequência como se isso representasse automaticamente vizinhança física.

## 9.5 Critérios acústicos e pesos

Exemplos de pares de parciais que podem aproximar frequências em intervalos:

| Relação entre notas | Parciais possíveis a comparar | Observação |
|---|---|---|
| Oitava | 2:1, 4:2, 6:3, 8:4, 10:5 | Os melhores compromissos dependem do registro e da intensidade de cada parcial. |
| Duodécima (oitava + quinta) | 3:1, 6:2, 9:3 | **Parcial da nota inferior : parcial da superior**, nesta ordem. Em temperamento desigual, a diferença teórica assinada entre esses parciais normalmente **não é zero**; obedecer aos alvos e modos da seção 9.7. |
| Quinta | 3:2, 6:4 | Pode competir com pureza de oitavas. |
| Quarta | 4:3, 8:6 | Pode ser intencionalmente temperada. |
| Dupla oitava | 4:1, 8:2 | Pode afetar a região aguda/grave. |

Esses pares **não são uma receita obrigatória**; a implementação deve oferecer estilos objetivos e explicar quais relações cada estilo otimiza. Outras combinações e famílias podem ser acrescentadas após validação. **Selecionar `3:1` não significa solicitar pureza 3:1**: o alvo pode ser `t=0` (coincidência acústica) **ou um desvio assinado de referência** derivado do temperamento; a opção deve ser explícita, versionada e auditável.

**O que visualizar ao tocar em um intervalo**:

- Notas e ordens de parciais em confronto, suas frequências previstas **antes e depois** da curva.
- **Diferença assinada em cents** entre os parciais e diferença em Hz/possível frequência de batimento `|f_a − f_b|`; mostrar o **sinal** do desvio em cents e a magnitude em Hz separadamente. Batimento audível depende de amplitude e condições acústicas, e diferença em Hz não prova batimento audível.
- Compromisso com outros intervalos: melhorar uma oitava pode piorar uma quinta; o painel deve deixar isso visível.
- Pesos numéricos de cada critério e justificativa do valor padrão (com versão do estilo).
- Região do instrumento em que o critério atua; possibilidade de pesos distintos por registro, quando tecnicamente fundamentada.

## 9.6 Modelo matemático de curva e previsão de parciais [RECOMENDADO; revisado 3.0]

**Grandezas independentes e unidades obrigatórias:** seja `x=(keyId,octave)` um **alvo físico** válido no catálogo canônico do snapshot `T`, `p≥1` a ordem do parcial e `Δ_x` a correção instrumental proposta em cents. `T` é um snapshot imutável de preset/receita e frações, layout, referência histórica A4 **ou referência EDO por grau**, offsets e alvos efetivos. `f_x^temp(T)` é a frequência fundamental teórica, **consultada no catálogo**, não uma função de MIDI. O alvo nominal da frequência fundamental é

\[
f_x^{\mathrm{alvo}}(\Delta_x)=f_x^{\mathrm{temp}}(T)\,2^{\Delta_x/1200}.
\]

A medição acústica de uma execução pode trazer `f_{x,1}^{observado}` **desafinado em relação a esse alvo**. É incorreto prever a nota-alvo simplesmente multiplicando `f_{x,p}^{observado}` por `2^{Δ_x/1200}`: isso deixaria a desafinação original embutida na curva. A nova regra é separar a **forma espectral** da **escala absoluta de afinação**:

- Para corda rígida com `B_x` validado, definir `g_{x,p} = p sqrt((1+B_x p²)/(1+B_x))`, com `g_{x,1}=1`. Então `f_{x,p}^{previsto}(Δ_x)=f_x^alvo(Δ_x) g_{x,p}`.
- Quando não se aplica B mas existe série empírica confiável, definir `g_{x,p}=f_{x,p}^{medido}/f_{x,1}^{referência acústica}` **dentro da mesma execução/estimativa consolidada** e com normalização/qualidade documentadas. Se o primeiro parcial estiver ausente, um estimador inferido e validado poderá suprir a escala; não usar cegamente o primeiro pico.
- Se não existir `g` defensável para o parcial, marcar o critério como **não avaliável**, sem interpolar razões fictícias. Para instrumentos de modos não harmônicos, usar um modelo próprio e a semântica de modo modal, não impor `p` harmônico.
- A aproximação de que `g` permanece constante durante a pequena correção de afinação é **[A VALIDAR]**; grandes mudanças de tensão podem exigir nova captura de B e da estrutura espectral.

Para notas `a` (inferior) e `b` (superior), e respectivos parciais `p` e `q`, o desvio acústico **assinado** entre as frequências previstas é

\[
s_{a,p;b,q}(\Delta)=1200\log_2\!\left(\frac{f_{a,p}^{\mathrm{previsto}}(\Delta_a)}{f_{b,q}^{\mathrm{previsto}}(\Delta_b)}\right).
\]

`+` significa que o parcial da nota **inferior** tem frequência maior que o da nota **superior**; `−` significa menor. **Não confundir** `s` com `I_{a,b}` (intervalo entre fundamentais), com `Δ_b−Δ_a` (correção diferencial da curva), nem com `|f_{a,p}−f_{b,q}|` (diferença em Hz). O resíduo de um critério é

\[
r_{a,p;b,q}(\Delta)=s_{a,p;b,q}(\Delta)-t_{a,p;b,q},
\]

em que **`t` é o alvo explícito, assinado em cents**, definido por política e snapshot do temperamento. `t=0` significa coincidência física de parciais; **não** é a regra automática de duodécimas ou quintas em temperamento desigual. A seção 9.7 define dois estilos, um alvo histórico derivado e as restrições musicais necessárias.

Uma família **ilustrativa**, não algoritmo fechado, de objetivos é

\[
J(\Delta)=\sum_k w_k\,\rho\!\left(s_k(\Delta)-t_k\right)
 +\lambda\sum_{(a,b)\in E_{\mathrm{adj}}}\omega_{ab}(\Delta_b-\Delta_a)^2
 +\mu\sum_{(a,b,c)\in P_3}\omega_{abc}(\Delta_c-2\Delta_b+\Delta_a)^2
 +J_{\mathrm{fidelidade}}(\Delta),
\]

com `w_k` ligados à confiabilidade e ao estilo escolhido; `ρ` robusta; `E_adj` e `P₃` são pares e trios de teclas **na ordem física explícita do instrumento, NÃO na sequência de quintas, frequência ou semitons MIDI**; `ω` pondera adjacências, e `λ`, `μ` controlam suavidade, além de `J_fidelidade`/restrições de 9.7. Os componentes devem ser **normalizados por escala e unidades** antes de ponderar; o tamanho da tabela de pares não pode dominar o objetivo apenas por quantidade. Pesos, limiares, restrições e perdas ainda requerem validação.

**Âncora e identificabilidade:** fixar uma nota de referência ou condição equivalente. A âncora deve ser informada; ela não precisa necessariamente coincidir com A4, mas não altera implicitamente o A4 armazenado. O conjunto de intervalos e vínculos precisa ser conectado à âncora ou usar uma regra expressa para componentes desconexos, sob pena de múltiplas soluções equivalentes.

**Ausências e extrapolação:** dados sem parciais válidos ou sem modelo adequado não produzem correções automáticas confiáveis. Pontos interpolados/extrapolados devem trazer fonte, status e incerteza; pode-se adotar `Δ=0` ou bloquear a aplicação conforme política conservadora documentada [A VALIDAR], sem criar falsos valores de B.

## 9.7 Temperamentos desiguais, duodécimas e preservação da identidade histórica [DEFINIDO / RECOMENDADO — revisão 2.2]

### 9.7.1 Problema: comparar parciais não é decidir sua pureza

O par `3:1` de uma duodécima significa comparar **terceiro parcial da nota inferior** com **primeiro parcial da nota superior**. Analogamente, `6:2` e `9:3` descrevem outros pares de ordens que se aproximariam em um intervalo de razão 3:1 **entre fundamentais harmônicas ideais**. A relação de fundamentais da **duodécima pura** é `3:1 ≈ 1901,955 cents`, mas um intervalo de 19 semitons no temperamento igual vale **1900 cents**. Um temperamento histórico pode prever outro valor, determinado pelas quintas/oitavas no preset (inclusive edição pelo editor racional de quintas).

Assim, exigir `s=0` em todas as duodécimas pode involuntariamente **retemperar o instrumento**. Uma afinação historicamente desigual e uma coincidência acústica exata não são objetivos equivalentes. O mesmo vale para quintas `3:2`, quartas `4:3` e outros intervalos temperados. 

**Regra vinculante:** a escolha do **par** de parciais é uma decisão de observação; a escolha do **alvo** é outra decisão de otimização, exposta ao usuário e registrada no perfil da curva.

### 9.7.2 Grandezas matemáticas: referência nominal, desvio acústico e curva

Com `a<b` em altura, definir o intervalo **teórico entre fundamentais** do temperamento `T`:

\[
I_T(a,b)=1200\log_2\left(\frac{f_b^{\mathrm{temp}}(T)}{f_a^{\mathrm{temp}}(T)}\right).
\]

A diferença assinada entre **parciais harmônicos ideais**, na ausência de inarmonicidade e **antes de qualquer correção**, é

\[
t_T^{\mathrm{harm}}(a,p;b,q)
 =1200\log_2\left(\frac{p}{q}\right)-I_T(a,b).
\]

Esse valor pode ser **diferente de zero e ter sinal musicalmente intencional**. Com a curva aplicada, o intervalo efetivo entre fundamentais torna-se

\[
I_{\mathrm{final}}(a,b)=I_T(a,b)+(\Delta_b-\Delta_a),
\]

logo **a tabela do temperamento não ser editada não significa que a relação entre fundamentais permaneceu igual**. A interface deve exibir `Δ_b−Δ_a` como "mudança de intervalo em relação ao temperamento".

A diferença acústica prevista com o modelo de parciais de 9.6 obedece à identidade

\[
s_{a,p;b,q}(\Delta)
 =t_T^{\mathrm{harm}}(a,p;b,q)
 +1200\log_2\left(\frac{g_{a,p}/p}{g_{b,q}/q}\right)
 +(\Delta_a-\Delta_b).
\]

Esta equação explicita **três fontes** que não devem ser misturadas: `t_T^harm` (característica do temperamento), `1200 log₂((g_a,p/p)/(g_b,q/q))` (contribuição da forma espectral/inarmonicidade) e `Δ_a−Δ_b` (decisão de extensão da curva). Se `g_{x,p}=p` e `Δ=0`, o desvio acústico coincide exatamente com o valor harmônico teórico do temperamento, **não necessariamente com zero**.

**Exemplo calculável e apenas ilustrativo:** A3–E5, intervalo de 19 semitons, em um temperamento **hipotético** cuja quinta Lá–Mi tem **697 cents** e oitava teórica 1200 cents: `I_T=1897 c`, enquanto `1200 log₂(3)=1901,955 c`. Logo `t_T^harm(3:1)≈+4,955 c` (terceiro parcial de A3 acima do primeiro de E5). Impor coincidência 3:1 (`s=0`) com cordas ideais já exigiria `Δ_E5−Δ_A3≈+4,955 c`, modificando esse intervalo fundamental **sem qualquer inarmonicidade**. Esse 697 c **não é atribuído a nenhum preset específico** do programa; é apenas um exemplo aritmético. No temperamento igual, o alvo harmônico de 3:1 é ≈`+1,955 c`.

### 9.7.3 Três significados possíveis de "preservar o temperamento"

Distinguir explicitamente, na matemática, na UX e nos testes:

1. **Preservação da fonte teórica — invariável em ambos os modos:** os presets, o cilindro acústico de quintas, A4 e `f_temp` não são modificados pela curva. A composição `f_final=f_temp·2^(Δ/1200)` é separada e reversível. Isso **sozinho não garante preservação de intervalos**.
2. **Preservação estrita de determinados intervalos entre fundamentais:** exigir `I_final≈I_T` para pares selecionados, isto é, `Δ_b−Δ_a≈0`, com restrições duras ou tolerâncias. É apropriado, por exemplo, proteger uma região central ou relações críticas, mas **preservar estritamente todos os intervalos conectados com uma âncora fixa força Δ=0** e torna impossível uma curva de extensão não trivial.
3. **Preservação do padrão acústico de temperamento, compensando a rigidez:** usar como alvo o desvio assinado `t_T^harm` de um par de parciais. Assim, `s(Δ)≈t_T^harm` para as relações selecionadas, em vez de forçar coincidência. Isso pode demandar `Δ_b−Δ_a≠0`, portanto **não preserva literalmente todos os intervalos entre fundamentais**. É um critério acústico contextual, não uma prova automática de reprodução histórica perfeita.

O nome público "Fidelidade ao temperamento" designará uma **política híbrida transparente**: fonte histórica imutável, proteção explícita dos intervalos fundamentais relevantes e preservação ponderada dos alvos assinados em parciais. A interface deverá identificar a importância e a tolerância de cada subobjetivo; quando incompatíveis, apresentar o compromisso obtido, não afirmar que ambos foram plenamente satisfeitos.

### 9.7.4 Dois modos de prioridade no construtor de curvas

| Modo | Alvos de intervalo | Proteção da estrutura histórica | Quando usar |
|---|---|---|---|
| **Fidelidade ao temperamento** — padrão [RECOMENDADO] para temperamentos desiguais | Critérios de parciais usam inicialmente `t_T^harm` (com sinal); apenas intervalos fisicamente elegíveis. | Restrições explícitas sobre `Δ_b−Δ_a` para pares/região central relevantes, mais desvios e tolerâncias por registro [A VALIDAR]. | Ao estudar ou afinar mantendo a coloração intencional do temperamento; não equivale a "parciais totalmente sem batimentos". |
| **Otimização acústica** — escolha explícita | Pode priorizar `t=0` para pares escolhidos, **ou** metas de batimentos assinados/não nulos e critérios intervalares próprios. | Presets continuam intocados; o usuário define quanto aceitar de alteração intervalar. Devem aparecer advertências se o deslocamento apagar traços do temperamento. | Experimentos controlados de compromisso de oitavas, duodécimas, quintas, estilos ou preferências instrumentais. |

Em ambos os modos, `t` deve estar **por critério e não escondido em um "estilo" opaco**. O operador pode inspecionar os pesos, mas uma visualização simples deve traduzir o resultado: "duodécima A3–E5: referência do temperamento +4,955 c entre parciais; previsão com a curva +4,6 c; diferença do objetivo −0,355 c" (apenas exemplo). Não exibir todos os termos na tela inicial.

**Se o temperamento for igual:** ainda existem diferenças entre a duodécima temperada (1900 c) e a pura (~1901,955 c). O modo selecionado, e não o rótulo "igual", deve determinar se `t` será 0 ou o desvio teórico harmônico. Sem inarmonicidade, o modo de fidelidade com âncora e proteção adequadas deveria produzir `Δ≈0`; o modo acústico poderá produzir correções adicionais como compromisso deliberado.

### 9.7.5 Objetivo e restrições de otimização [RECOMENDADO; pesos A VALIDAR]

Cada critério `k` precisa declarar: `lowerTarget:{keyId,pitchId,octave}`, `upperTarget:{keyId,pitchId,octave}`, `baseSnapshotHash`, `partialLower`, `partialUpper`, `temperamentIntervalCents`, `referencePartialDetuningCents`, `targetDetuningCents` **assinado**, `targetPolicy`, `weight`, `confidence`, `register`, `reason` e `modelVersion`. Os alvos devem existir no catálogo do mesmo snapshot; dois `keyId` distintos jamais são colapsados por `soundId`. O modelo/curva de origem deve ser versionado e vinculado ao snapshot efetivo de A4/temperamento/quintas.

Os termos objetivos são separados, por exemplo:

- `J_parciais`: mede `ρ(s_k(Δ)−t_k)` **com desvio assinado** e pesos adequados para cada família de intervalo.
- `J_fundamentais`: mede `ρ(Δ_b−Δ_a)` ou impõe `|Δ_b−Δ_a|≤ε_{a,b}` para relações históricas protegidas. O `ε` é dependente da região, **[A VALIDAR]**; não fixar um valor universal como 1 cent sem ensaio.
- `J_regularidade`: limita saltos artificiais entre notas, mas permite irregularidades reais em pontos repetíveis e mudanças de escala do piano.
- `J_ancora`: fixa referência absoluta/nota âncora, sem alterar A4 implicitamente.
- `J_manual`: respeita travas e deslocamentos escolhidos pelo usuário, registrando conflitos de restrições.

O motor deve detectar e relatar restrições **incompatíveis, redundantes ou subdeterminadas**. Em vez de apresentar falsa precisão, mostrar, por exemplo, "não é possível cumprir simultaneamente a preservação estrita desta quinta e a coincidência exata desta duodécima". **Nenhum modo garante batimentos nulos em todos os intervalos.**

O objetivo de uma possível **igualdade de velocidades de batimento** entre intervalos diferentes usa diferenças **assinadas de frequência em Hz**, avaliadas com hipóteses explícitas; não substituir esse objetivo automaticamente por `s=0` ou por desvio em cents. A percepção do batimento também depende de amplitude, acoplamento, decaimento e composição do som. A Fase 4 terá de validar empiricamente quais critérios musicais são adequados.

### 9.7.6 Camadas progressivas na interface [RECOMENDADO]

1. **Essencial:** selo de prioridade selecionada (`Fidelidade ao temperamento` ou `Otimização acústica`), curva em prévia/aplicada e alerta resumido `Oitavas estendidas; temperamento base preservado como referência`.
2. **Comparação por intervalo:** selecionar `A3–E5 / duodécima / 3:1`; apresentar `fundamentais: referência 1897 c → proposta 1899 c (mudança +2 c)` e `parciais: alvo +4,955 c → previsão +... c`. Valores não fundamentados por medição devem aparecer como `—`, não números inventados.
3. **Justificativa:** `por que esta meta?`, relação 3:1/6:2/9:3, B e qualidade dos parciais, pesos, concessões a oitavas/quintas, lista de notas alteradas e causas da diferença.
4. **Auditoria:** snapshot de temperamento, A4, valores de `g_{x,p}`, alvos `t`, resíduos, restrições ativas, versão do algoritmo, medições por execução, relatório de consistência e histórico de confirmação.

Mostrar **três grandezas sempre diferenciáveis** na comparação: (a) relação entre fundamentais em cents, (b) desvio assinado entre parciais em cents e (c) diferença absoluta entre frequências de parciais em Hz. Acrescentar magnitude/sinal e acessibilidade textual; nunca usar uma única cor ou um simples `0` sem legenda de referência. `Informação progressiva` não autoriza esconder que o modo selecionado altera o objetivo da curva.

Se o usuário tentar aplicar uma prévia do modo acústico com mudanças importantes na estrutura do temperamento, exigir confirmação específica com **resumo de impacto verificável**. Não fixar o limiar de alerta antes da validação; mostrar o diff sempre que houver alteração efetiva.

### 9.7.7 Sequência técnica de cálculo e auditoria

1. Capturar `T` (preset/definição externa, `tuningKind`, frações efetivas, `layoutId`/teclas físicas, A4 histórico **ou** `referenceDegree`/`referenceOctave`/`referenceHz` EDO, offsets, alvos canônicos por `(keyId,octave)` e hash determinístico) **antes de calcular**; congelar a versão da curva e as medições por `measurementId`/`sessionId`. Não gerar uma tabela cromática MIDI paralela.
2. Validar a chave `(keyId,octave)` contra `CatalogoAlvosCanonicos.porTecla()` do snapshot, conferir `pitchId`, contexto de corda/uníssono, modelo físico, estimativas de `B`/`g`, qualidade e cobertura por registro; rejeitar casos com identidade musical ambígua ou sem predição defensável.
3. Construir `I_T(a,b)` e `t_T^harm` **a partir das frequências efetivas do instrumento no temperamento**, não de uma quinta fixa de 700 cents nem de pressuposto universal `3:1` puro.
4. Para cada relação, escolher `targetPolicy`, calcular `targetDetuningCents` e documentar sua origem (temperamento harmônico, coincidência, valor manual ou modelo alternativo). Calcular `s_k(Δ)` e `r_k(Δ)`. Normalizar escalas/pesos e registrar equações.
5. Montar a função objetivo com ancoragem, regularidade e proteção histórica, testar conectividade/identificabilidade e detectar incompatibilidades; em caso de falha retornar `invalid/inconclusive`, não uma curva aparentemente pronta.
6. Calcular **somente prévia** com parâmetros e versão identificáveis; antes de oferecer `Aplicar`, produzir relatório de `I_T`, `I_final`, `Δ_b−Δ_a`, `s(Δ)`, `t`, `r`, diferença entre parciais em Hz e incerteza; mostrar onde faltam dados.
7. O usuário pode inspecionar/editar, comparar os dois modos usando **mesmas medições/snapshot** e aplicar explicitamente uma versão. O motor nunca reescreve `T`, notas observadas ou uma curva anteriormente aplicada.
8. Ao mudar A4, quintas ou temperamento, invalidar compatibilidade da curva calculada; oferecer **recalcular prévia** com novo snapshot. A função eventual `Rebasear` deve oferecer explicitamente manter frequências absolutas ou redefinir critérios musicais; não reutilizar Δ automaticamente.

### 9.7.8 Como calcular e testar a compensação de inarmonicidade sem retemperar em silêncio

Um caso útil para testar o significado do modo **Fidelidade** é um único par de notas cuja referência histórica é `t_T^harm` e cujas funções de parcial `g` são confiáveis. A condição `s(Δ)=t_T^harm` implica

\[
\Delta_b-\Delta_a=1200\log_2\!\left(\frac{g_{a,p}/p}{g_{b,q}/q}\right).
\]

Portanto, com parciais perfeitamente harmônicos (`g=p` e `g=q`), o modo de fidelidade acústica produz `Δ_b−Δ_a=0` para esse par **mesmo se o intervalo histórico não for puro**. Se houver inarmonicidade, a correção diferencial compensa a alteração relativa dos parciais, mas **o intervalo de fundamentais efetivo muda na quantidade exibida**. Uma restrição estrita de `Δ_b−Δ_a≈0` pode entrar em conflito; o otimizador deve informar essa tensão e fornecer um compromisso verificável. Essa identidade é um **caso analítico unitário**, não uma receita suficiente para otimizar um instrumento inteiro.

No modo de **coincidência acústica** (`t=0`), mesmo quando `g=p` e `g=q` o ajuste desejado pode ser `Δ_b−Δ_a=t_T^harm` (com a convenção de sinal de 9.6); isto é, pode **mudar o temperamento intencionalmente**. Não chamar tal decisão de "compensação pura de inarmonicidade".

### 9.7.9 Compatibilidade ao alternar temperamentos e evidência histórica

As medições acústicas podem alimentar mais de uma curva, mas os `Δ_x` são **interpretados relativamente a `T`** e associados a cada `(keyId,octave)` e ao alvo `targetPolicy`. Uma curva calculada para um temperamento não é automaticamente transferível para outro. As opções seguras são:

- **Recalcular prévia:** usar as mesmas medições compatíveis com um novo snapshot de temperamento/A4/quintas e novos `t_T^harm`, produzindo nova versão. Não importar pesos de modo antigo sem verificar a semântica.
- **Rebasear frequências absolutas:** se uma operação explícita futura for solicitada, `Δ_x^{novo}=1200 log₂(f_x^{alvo,antigo}/f_x^{temp,novo})`, para **o mesmo `(keyId,octave)` mapeado e validado nos dois snapshots**. A **frequência absoluta** permanece, mas a fidelidade aos intervalos do novo temperamento **não** está garantida. Exigir confirmação e marcar como `rebase_absolute`, sem aceitar isso como recálculo acústico.
- **Reotimizar musicalmente:** manter dados acústicos e estilo histórico, mas gerar novo conjunto de alvos e resolver outra curva. É diferente de rebasear.

Ao citar precedentes, distinguir fatos de capacidade documentada de matemática interna não pública: **TuneLab** apresenta campos separados para desvio de temperamento e desvio da curva; **PianoMeter** e **pianoscope** documentam temperamentos desiguais e estilos de extensão; o procedimento **EBVT de Bill Bremmer (2001)** é exemplo prático de temperamento desigual com oitava estendida; **Dixon, Mauch e Tidhar (2012)** estudam conjuntamente inarmonicidade e classificação de temperamentos em cravos. **Nenhuma dessas fontes prova que um produto implemente exatamente a política de alvos `t_T^harm` aqui recomendada**; ela é uma proposta matemática deste roadmap a validar musicalmente.

### 9.7.10 Critérios de aceitação específicos de temperamentos desiguais

- [ ] Para cada par, ordens e nota inferior/superior têm convenção consistente; `t_T^harm` reproduz diferenças exatas para 3:1, 6:2 e 9:3 no regime harmônico.
- [ ] `B=0`, `Δ=0`: `s=t_T^harm` para todo temperamento/intervalo elegível; nenhuma correção espúria é atribuída à rigidez.
- [ ] Duodécima de 1900 cents → alvo 3:1 `+1,955 c`; duodécima hipotética de 1897 cents → `+4,955 c`; trocar entre modelos não altera o temperamento base.
- [ ] `t=0` com parciais ideais pode alterar `I_final` deliberadamente; a interface apresenta `Δ_b−Δ_a` e não rotula o resultado como fidelidade histórica.
- [ ] Se todos os intervalos protegidos forem estritos e conectarem todas as notas a uma âncora, o sistema reconhece `Δ=0` como única solução para eles e não promete extensão adicional.
- [ ] Restrições incompatíveis retornam diagnóstico compreensível e não produzem prévia aplicável automaticamente.
- [ ] Previsões de parciais são ancoradas em `f_temp·2^(Δ/1200)` e razões acústicas `g`, **não** na afinação observada de uma corda desafinada.
- [ ] Gráficos/textos distinguem cents relativos ao temperamento, desvio parcial assinado e batimento em Hz; modo de prioridade e mudança de intervalo sempre visíveis.
- [ ] Recalcular com um temperamento diferente produz snapshot/targets atualizados; rebase absoluto não se passa por preservação musical.
- [ ] Comparar os dois modos com os mesmos dados acústicos; documentar seus compromissos em oitavas, duodécimas, quintas e regiões do teclado.

## 9.8 Edição manual e histórico

- O usuário pode ajustar Δ por nota, ancorar trechos, alterar pesos ou escolher estilo acústico. **Toda edição gera versão**.
- Exibir indicação `manual`, `calculado` ou `interpolado` para cada ponto.
- Permitir `Desfazer`, `Restaurar prévia`, comparar versão anterior e exportar sem aplicar.
- Não modificar medições originais ao editar curva. Medição é fato observado; curva é interpretação/decisão.
- Versões aplicadas deverão manter `curveId`, `baseTemperamentId`, A4, **snapshot/hash efetivo do temperamento**, `priorityMode`, `targetPolicy`/`targetDetuningCents` de cada relação, proteção de intervalos fundamentais, perfis de origem, algoritmo, pesos, correções, resíduos e histórico de decisões.
- Não sobrescrever uma curva aprovada ao abrir o mesmo perfil após novas medições.

## 9.9 Aceitação da Fase 4

- [ ] Gerar a mesma prévia ao repetir o cálculo com as mesmas entradas e parâmetros, dentro de tolerâncias numéricas documentadas.
- [ ] Curva exibe **pontos medidos, interpolados, manuais e incertos** de maneira distinta.
- [ ] Alterar pesos ou alternar `Fidelidade ao temperamento`/`Otimização acústica` produz diff explicável de frequências, mudanças de intervalos por fundamentais e desvios assinados entre parciais.
- [ ] Validar âncora e detecção de problemas de determinabilidade; não gerar curvas arbitrárias quando o sistema está subdeterminado.
- [ ] Tolerar dados ausentes e medições ruins sem inventar correções conclusivas.
- [ ] Comparar curvas de diferentes instrumentos e estilos com A4/temperamento explicitamente identificados; **não comparar Δ diretamente entre snapshots diferentes sem normalizar as referências**.
- [ ] `Gerar prévia` nunca modifica a afinação ativa; `Aplicar` exige confirmação; `Desativar` volta às referências teóricas.
- [ ] Realizar testes acústicos e auditivos com instrumentos reais, incluindo comparações cegas quando factível; melhoria numérica não equivale automaticamente a melhoria musical.

---

# 10. Fase 5 — Integração entre temperamento e curva instrumental

**Prioridade: Alta | Complexidade: Muito alta.** Só liberar após Fase 4 validada.

## 10.1 Fórmula de integração [DEFINIDO]

\[
f_{\mathrm{final}}(x;T,C)=f_{\mathrm{temperamento}}(x;T)\cdot2^{\Delta_x(C)/1200},\quad x=(keyId,octave)
\]

`x` é a tecla física com oitava; `f_temperamento(x;T)` vem de `CatalogoAlvosCanonicos.porTecla()` no snapshot `T`, histórico **ou EDO**; `Δ_x(C)` é a correção em cents da curva `C` **compatível com este snapshot**. O cilindro é visualização do grafo e **não** motor de frequência. A fórmula não faz indexação MIDI e não altera o motor canônico.

- Correção desligada → `Δ_x=0` **para todos os fins**: comparação, nota-alvo e emissor (se ele seguir a opção).
- Correção ligada → referência corrigida disponível para modo **Automático**, modo **Nota fixa** e, **opcionalmente**, gerador. A detecção acústica continua estimando Hz sem temperamento; a associação de **alvo mais próximo** passa a comparar as frequências `f_final` por `(keyId,octave)`, conservando a ordem estável dos alvos do grafo para desempate e a política de registro. A **ambiguidade efetiva** deve ser recalculada das frequências corrigidas, não lida diretamente de `porSom()`/`soundId` teóricos: dois alvos de um mesmo `soundId` podem separar-se após Δ, e dois `soundId` diferentes podem coincidir. Mostrar separadamente ambas as coincidências quando necessário. Essa comparação é uma **camada reversível de interpretação**, nunca sobrescrita de `CatalogoAlvosCanonicos`.
- O cilindro acústico de quintas preserva sempre os valores e presets históricos, sem absorver `Δ_x`. **Mas** os intervalos realmente emitidos entre notas podem mudar: `I_final(a,b)=I_T(a,b)+(Δ_b−Δ_a)`. O painel de comparação deve tornar esse efeito explícito mesmo quando a tabela de quintas não muda.
- O registro da curva deve declarar `priorityMode`, critérios acústicos, alvos assinados por parcial, restrições de fidelidade, `(keyId,octave)` de cada nó, snapshot canônico de referência e relatório intervalar. `Fidelidade ao temperamento` não significa "todas as fundamentais continuam em intervalos exatamente iguais" se houver extensão; mostrar limites/compromissos.

## 10.2 Controle futuro no Afinador

Próximo ao medidor principal ou à referência da nota, mas **não** dentro do seletor YIN/pYIN/SWIPE’:

```text
Correção instrumental:  [ Desligada / Ativada ]
Curva: Piano de estudo — v3 (base: Pitagórico; A4 415,3 Hz)
Prioridade: Fidelidade ao temperamento; restrições consultáveis
Nota A3: teórica 207,650 Hz | instrumental 207,900 Hz | Δ +2,1 c
[Comparar referências] [Ver intervalos afetados] [Abrir curva]
```

Números do exemplo fictícios.

O controle somente fica ativo quando existe curva **aplicada, compatível e válida**. Caso contrário, exibir `Nenhuma curva aplicada` ou `Curva incompatível com o temperamento atual`, com acesso à ferramenta Curvas.

## 10.3 Política operacional

1. **Desativação por padrão** em perfis novos [RECOMENDADO] até que o usuário escolha uma curva; iniciar captura normal sem alterar frequências teóricas.
2. A ativação exige confirmação informativa na primeira vez: qual perfil, versão, temperamento base e A4.
3. Trocar A4, temperamento ou quintas personalizadas enquanto a curva está ativa dispara verificação de compatibilidade; nunca reutilizar a curva silenciosamente com definição de base diferente.
4. O modo **Nota fixa** compara com frequência corrigida somente se a camada estiver ligada; o **Automático** também deve resolver o alvo corrigido mais próximo, conservando o critério de desempate e sem inferir a tecla apenas de Hz quando houver coincidências. Informar o valor teórico mediante acesso simples e conservar o resultado físico medido ao alternar a curva.
5. O emissor de notas possui opção `Seguir correção instrumental` desativada por padrão [RECOMENDADO], separada da emissão teórica já existente. O programa deve explicar claramente quando está gerando f_teórico ou f_final.
6. A4 de referência, temperamento histórico, perfis instrumentais e curva aplicada são entidades distintas; desligar a curva não restaura arbitrariamente A4 ou quintas.
7. O relatório de curva e a futura extensão versionada do diagnóstico registram `curveApplied`, `curveId`, `curveVersion`, `baseSnapshotHash`, `(keyId,pitchId,octave)`, `targetHzTheoretical`, `targetHzInstrumental`, `activeTargetHz`, `deltaCents`, sem modificar os logs dos algoritmos nem o formato `diagnosticSchemaVersion:2` existente de modo incompatível.
8. Na exportação das medições acústicas, não confundir `f1Medida` com `nota-alvo corrigida`; são grandezas diferentes. **O cálculo dos parciais-alvo deve partir da nova frequência nominal e de razões espectrais `g`, jamais da frequência medida desafinada.**
9. Se a curva for excluída ou deixar de ser compatível, falhar de modo seguro: **desativar correção e informar**, sem manter frequência-alvo sem identificação.
10. Ativação/desativação durante microfone ativo não deve exigir parar o áudio nem recalcular uma nova amostra; apenas reprojetar a comparação com os mesmos dados acústicos quando adequado.

## 10.4 Critérios de aceitação da Fase 5

- [ ] Com `Δ=0`, resultados de referência idênticos aos do afinador original (dentro de erro de ponto flutuante).
- [ ] Alternância ligada/desligada muda apenas a referência-alvo, não a frequência acústica detectada.
- [ ] Modo Nota fixa e emissor respeitam independentemente as escolhas; compatibilidade é auditável.
- [ ] Nenhuma quinta histórica ou preset foi alterado por cálculos acústicos; **mudanças reais de intervalos causadas por `Δ_b−Δ_a` foram quantificadas e identificadas, sem alegar falsamente preservação literal**.
- [ ] Troca de temperamento e A4 invalida/bloqueia corretamente curva incompatível.
- [ ] Restauração de configurações técnicas não elimina perfis e curvas acústicas; eventual comando de restaurar curva deve ser separado e confirmado.
- [ ] Números em cents e Hz conferidos com exemplos matemáticos e testes de ida/volta, incluindo duodécimas 3:1/6:2/9:3 sob temperamentos iguais e desiguais.

---

# 11. Fase 6 — Modelos por família de instrumento

**Prioridade: Média | Complexidade: Alta–Muito alta.** Expandir após ter o fluxo genérico de parciais estável.

| Família | Primeira interpretação física | Cuidados especiais |
|---|---|---|
| Piano | Cordas rígidas; B por corda; afin. estendida por tecla; curvas de Railsback como família de referência | 88 teclas; mudança de escala; uníssonos; múltiplas cordas; ruído de ataque; treble sem parcial estável. |
| Cravo | Parciais e possíveis desvios por corda; compatibilidade com temperamentos históricos | Construção e excitação diferem do piano; não assumir mesmo critério de estiramento. |
| Violão | Parciais e possível rigidez das cordas | Influência de trastes, posição, pressão, capo, acoplamento da caixa; medir por corda/casa quando relevante. |
| Guitarra | Medição por corda, casa e região | Amplificação, distorção e processamento podem criar componentes adicionais. |
| Sopros | Série de harmônicos ou modos de ressonância adequados à família | Não aplicar B de corda rígida sem validação; relações podem variar com dedilhado, coluna de ar, embocadura. |
| Sinos e percussão | Frequências dos modos vibratórios **não necessariamente harmônicos** | Não numerar automaticamente como harmônicos de f1; modelo modal próprio, não estimar B de corda. |

**[RECOMENDADO]** O perfil define um `acousticModelId` (`stiff_string`, `harmonic_series`, `modal_nonharmonic`, `exploratory`) e a disponibilidade das métricas, sem retirar a visualização genérica de picos de outras famílias.

Quando `B` não for fisicamente apropriado, a tela continua útil como **Analisador de parciais/modos**, mostrando os picos e relações sem fingir que se obteve coeficiente de rigidez de corda. Se o usuário escolher `Modelo exploratório`, a interface exige confirmação de caráter não validado.

**Critérios de aceitação:** testes com instrumentos reais de pelo menos dois tipos, identificação correta de modelo aplicável/não aplicável, metadados suficientes para comparar técnicas equivalentes, nenhuma aplicação silenciosa de curva de piano a instrumentos de outro modelo.

---

# 12. Fase 7 — Validação acústica e aperfeiçoamento (contínua)

## 12.1 Política [DEFINIDO]

**Testar a cada mudança**, como prática já estabelecida para o projeto. Não aprovar implementação por sintaxe apenas. Resultados de instrumento sintético são importantes, mas **não substituem** testes com instrumento e microfone reais.

## 12.2 Pirâmide de testes

### A. Unitários matemáticos

- Hz ↔ cents: `c=1200·log₂(f/fref)` e `f=fref·2^(c/1200)`, incluindo frequências próximas e extremos válidos.
- Modelo B: `B=0 → f_n=n f1`; validar inversões algébricas, estimativa conjunta de F/B e estabilidade numérica.
- Rejeitar NaN, infinito, B abaixo do domínio físico aceito, frequências ≤0, ordenações inválidas, divisão por zero.
- Propriedade de reconstrução: a partir de `F,B` conhecidos, obter parciais previstos; ajustar com ruído controlado; avaliar erro de B e de f1 separadamente.
- Curvas: `Δ=0` equivale ao temperamento original; `f_final/f_base=2^(Δ/1200)`; inversão e arredondamento estáveis.
- **Temperamentos desiguais (9.7):** testar `I_T`, `I_final`, `t_T^harm`, `s(Δ)` e diferença `Δ_b−Δ_a` com convenção de sinal; pares 3:1, 6:2, 9:3, 2:1, 3:2; desvio 3:1 de +1,955 c no igual e +4,955 c no exemplo hipotético com `I_T=1897 c`.
- **Modelo B e alvo:** com `B=0`, a política de fidelidade não produz extensão espúria; com `B>0`, a identidade de compensação de 9.7.8 deve ser recuperada para par isolado sem restrições conflitantes. Alterar o pitch de uma execução observada **sem alterar `g`** não pode alterar os parciais-alvo propostos.
- **Incompatibilidades:** restrições estritas conectadas a uma âncora não admitem extensão não trivial; identificar sistema desconexo, superdeterminado/incompatível, invalidade de snapshot e alteração de pesos sem versão.
- Isolamento entre A4, temperamento histórico e Δ_n.

### B. DSP sintético

- Harmônicos ideais e inarmônicos com B de referência e diferentes intensidades por parcial.
- f1 ausente/fraca, segundo/terceiro parciais dominantes, múltiplas ordens não consecutivas.
- Dois tons e acorde; interferência elétrica 50/60 Hz; ruído branco/rosa; transiente de ataque; reverberação; silêncio e clipping.
- Frequências com parciais próximos, aliasing, bordas do espectro e janelas insuficientes.
- Duas/ três cordas em uníssono com diferenças pequenas de frequência e fases distintas.
- Vibrato, glissando, variação de pitch, decaimento realista e durações curtas.
- Amostragens 44,1/48/96 kHz (e outras suportadas), dispositivos simulados com buffers irregulares, perda de blocos e sample-rate real diferente do solicitado.
- Determinismo: o mesmo PCM/parametrização/versão deve produzir os mesmos IDs de candidatos, estimativas e curvas dentro das tolerâncias.
- **Multiataque**: 1, 2, 3 e ≥4 ataques com pausas; ataque ausente, onset duplo por ressonância, ataque muito próximo da cauda anterior, nota sustentada sem repetição, silêncio, batimentos, vibrato, notas equivocadas, mudança de fonte, buffers perdidos.
- **Convergência**: B sintético constante com escala F_j ligeiramente variável; B_j contaminado em um ataque; erro sistemático repetido; incompatibilidade do modelo; mesma nota repetida com diferentes intensidades. Garantir que três execuções ruins não gerem aprovação.
- **Estatística**: comparar ajuste conjunto e mediana robusta; validar peso por execução e não por número de quadros; bootstrap por ataques somente com número de execuções suficiente; `NaN`/CI fictícios jamais exibidos.

### C. Integração

- Microfone inicia/para em todas as telas e há **uma única aquisição lógica**; alternar ferramenta não duplica buffers ou captura.
- Worker com ou sem SIMD; fallback funcional ou indisponibilidade explicada.
- Simultaneidade com áudio opcional: coleta de parciais não aciona gravação WAV sem consentimento.
- Mudar resolução FFT da tela principal não reinicia nem corrompe uma medição de parciais com janela própria.
- Perfis: IndexedDB, quota cheia, transações interrompidas, dados corrompidos, importação inválida ou tamanho excessivo.
- Exportações JSON/ZIP e WAV; reimportação reproduz os metadados, unidades e estados. **Round-trip de sessão multiataque:** mesma lista de execuções, motivos de exclusão, revisão de agregação, ordenação, parâmetros e resultado consolidado.
- Diagnóstico atual de 20 s conserva sua posição entre FFT e cilindro, sem regressão.
- Ajuda, configurações e temas não interferem com a medição ou refazem cálculos indevidamente.

### D. Validação em instrumento real

- **Dentro da mesma sessão**, repetir uma mesma nota/corda 1, 2, 3 e mais vezes, com intensidades e separações variadas; observar quando a dispersão estabiliza, quando o detector falha e se o estado de convergência é justificável.
- Repetir a mesma nota, mesma corda, diferentes dias, posições do microfone e dispositivos (**sessões distintas**).
- Separar corda individual versus uníssono completo; avaliar efeitos de outras cordas simpáticas.
- Registrar comparações com equipamentos e técnicas de referência; informar qualidade e limites da referência.
- Avaliar a estabilidade da atribuição de ordem do parcial em agudos/graves.
- Repetir após afinação para verificar previsões e condições alteradas.
- Avaliar curvas por **intervalos auditivos reais** e, quando possível, comparações cegas/pareadas e registros independentes do mesmo instrumento.
- Comparar **os dois modos** de 9.7 usando o mesmo piano/cravo, mesma sessão acústica e temperamentos iguais e desiguais: além de parciais, medir se os intervalos fundamentais, desvios assinados e batimentos previstos foram documentados corretamente e se a coloração/compromisso histórico é percebido conforme a escolha.
- Não atribuir melhora ao algoritmo por um teste em um único piano; registrar tamanho e composição da amostra.

### E. Layout e acessibilidade

- Larguras mínimas: 320, 360, 390, 412, 768 px; desktop largo; retrato e paisagem.
- Temas claro/escuro com contraste adequado; zoom 200%; fontes ampliadas; leitor de tela; teclado; gesto opcional sempre com alternativa visível.
- Ações de medir/salvar/aplicar não são tão pequenas a ponto de dificultar toque; compactação visual não equivale a reduzir indiscriminadamente o alvo tátil.
- Sem rolagem horizontal geral, elementos sobrepostos ou perda de estado da captura.
- Menus de Ferramentas, Configurações e Ajuda ficam legíveis acima da barra inferior fixa.

### F. Desempenho, energia e memória

- Medir CPU/tempo por quadro, p50/p95/p99, memória de buffers, taxa de atualizações, quedas, latência e bateria/temperatura em aparelho representativo.
- Monitor e gráfico com frequência de atualização deliberadamente menor que a taxa de DSP quando necessário; isso não deve perder dados da aquisição para calcular B.
- Definir orçamento de memória para análise e WAV; encerrar seguramente e avisar se alcançado.
- Em modo **Afinador**, a instrumentação acústica futura não pode impor custo permanente significativo. Comparar versão original, ferramenta inativa, ferramenta ativa e gravação opcional.
- Verificar resposta ao sair/voltar do plano de fundo, bloqueio de tela, perda de permissão, desconexão do microfone e mudança de sample rate.

### 12.2.1 Testes obrigatórios da arquitetura canônica [DEFINIDO para v3.0]

Cada ID deve existir como caso automatizado reproduzível com parâmetros, resultado esperado, evidência e marcação `pass/fail/pending_hardware`. Nomes de chaves e valores devem ser comparados com o **HTML congelado**, sem recodificar a lógica de MIDI em fixtures.

| ID | Teste e condição de aceitação |
|---|---|
| INH-ARCH-001 | Histórico 12 teclas: `keyId/pitchId/soundId/octave` consultados por `porTecla()` devolvem exatamente o alvo congelado. |
| INH-ARCH-002 | Histórico 13 teclas com Ré♯/Mi♭ divididos: duas chaves distintas; nenhum colapso por nome, cents ou índice MIDI. |
| INH-ARCH-003 | Histórico 14 teclas com Ré♯/Mi♭ e Sol♯/Lá♭: quatro identidades independentes, inclusive quando alguma frequência coincide. |
| INH-ARCH-004 | Um mesmo `soundId` com duas teclas: medição ambígua solicita confirmação; perfis e curvas preservam dois `keyId`. |
| INH-ARCH-005 | 13-EDO: graus, gerador 8, uma órbita; curva e perfil não inventam notações cromáticas. |
| INH-ARCH-006 | 14-EDO: gerador 8, duas órbitas de 7; correção em um grau não afeta o outro por alias. |
| INH-ARCH-007 | EDO com `keyboardKeys` duplicando um grau: duas teclas físicas persistem com identidades distintas sem duplicar grau matemático. |
| INH-ARCH-008 | 18 presets de fábrica (12 ciclos, quatro cadeias, dois EDOs) inalterados e importação de definição pessoal validada antes de commit. |
| INH-ARCH-009 | Frações c.p./c.s. historicamente fechadas preservam fechamento ΣCP=−1, ΣCS=0; cadeias abertas não inserem lobo na receita. |
| INH-ARCH-010 | Cilindro 2,5D: aresta de lobo diretamente entre as coordenadas dos extremos, sem vértice externo; ciclos fechados sem lobo artificial. |
| INH-ARCH-011 | A4 histórico preservado ao entrar/sair de EDO; referência EDO por grau/oitava/Hz não sobrescreve A4. |
| INH-ARCH-012 | Trocar apenas música/curva altera `musicRevision`/revisão de curva e **não** `generationIdDSP`, `sessionIdDSP` nem reinicia pYIN/SWIPE'. |
| INH-ARCH-013 | Trocar FFT/técnica invalida geração DSP e descarta respostas atrasadas; aquisição acústica tem IDs próprios. |
| INH-ARCH-014 | Prévia de importação ou curva inválida não publica estado musical, não registra catálogo e não modifica alvos ativos. |
| INH-ARCH-015 | Desativar `Δ` devolve **bit a bit/tolerância de ponto flutuante documentada** os alvos teóricos; não muda nota detectada nem áudio capturado. |
| INH-ARCH-016 | Alterar fração, layout, referência ou offset muda hash do snapshot; curva prévia/aplicada é revalidada ou bloqueada. |
| INH-ARCH-017 | Alterar somente tema, abertura de detalhes ou foco não modifica medição/curva; mudar FFT visual pode atualizar a geração DSP **existente**, mas não modifica o PCM já adquirido nem os parâmetros próprios da análise de parciais. |
| INH-ARCH-018 | Round-trip de perfil/curva por tecla/oitava preserva identidades e frequências observadas; rejeita campo `midiNote` como identidade canônica no novo schema acústico (`schemaVersion:1`, definido no roadmap v3.0). |
| INH-ARCH-019 | `afinador-tuning-v1` e biblioteca atual funcionam sem migração; novo `afinador.acoustic-profile` não sobrescreve sua chave no localStorage. |
| INH-ARCH-020 | Diagnóstico original `diagnosticSchemaVersion:2` permanece legível; novos relatórios acústicos têm schema distinto e exportação somente solicitada. |
| INH-ARCH-021 | Respeitar registros `detector/fixo/geradorPadrao/geradorAmpliado`; comparar detector histórico até Dó8, gerador Fá1–Fá7, ampliado até Si9 e políticas EDO próprias. |
| INH-ARCH-022 | A ordem física de regularização da curva é explícita no perfil; duas teclas enarmônicas vizinhas não são fundidas nem interpoladas por 12 semitons. |
| INH-ARCH-023 | Mesmo PCM reprocessado com outros temperamentos altera **somente interpretação**, não candidatos acústicos/estimativa B; vínculos antigos ficam versionados. |
| INH-ARCH-024 | `soundId` alterado por novo temperamento não redireciona perfil/curva: `(keyId,octave)` e hash determinam compatibilidade. |
| INH-ARCH-025 | Analisador desligado não cria Worker extra, FFT própria contínua, captura WAV, buffers adicionais permanentes ou consumo DSP significativo. |
| INH-ARCH-026 | Worker acústico atrasado após troca de nota/corda/ferramenta é descartado; não reaparece execução incompleta nem valor B indevido. |
| INH-ARCH-027 | Detector automático com curva ativa escolhe alvo por `f_final` em registro admissível; retorno para curva desligada recupera a escolha canônica/ordem de desempate sem reset DSP. |
| INH-ARCH-028 | Alterar `Δ_x` enquanto uma frequência já foi medida reinterpreta imediatamente Hz/cents quando a leitura ainda é válida, sem criar quadro DSP nem reviver leituras após silêncio. |
| INH-ARCH-029 | Curva separa duas teclas com o mesmo `soundId` ou iguala dois `soundId` distintos: a ambiguidade acústica **efetiva** é recalculada em Hz/cents com tolerância explícita, preservando a coincidência teórica imutável. |

**Provas matemáticas obrigatórias:** além das fórmulas de 9.7, comparar para cada par de teclas elegível `I_T`, `t_T^harm`, `s(Δ)`, `I_final`, `Δ_b−Δ_a`, diferenças em Hz; com `B=0` e `Δ=0` exigir `s=t_T^harm`. Testar também duas teclas coincidentes com `Δ_a≠Δ_b`: há dois alvos instrumentais distintos **sem mudar o grafo teórico**; o usuário deve conhecer a consequência.

**Testes de stress independentes:** aquisição multiataque com silêncio/vibrato/overlap, lote de 100 trocas de preset e 100 de método sem resets musicais, quadros atrasados de Worker, quota, gravação WAV opt-in, suspensão e retorno. Esses novos testes **acrescentam-se**, não substituem, às suítes YIN/pYIN/SWIPE'/FFT, ao cilindro e à biblioteca já existentes.

## 12.3 Métricas e limiares [A VALIDAR]

Não aprovar métricas apenas porque um número ilustrativo parece satisfatório. Antes de cada implementação definir **com antecedência**: faixa de frequências, níveis de SNR, duração, parcial elegível, limite de erro, erro máximo de B (absoluto e relativo), taxa de rejeição correta, sensibilidade a picos falsos, estabilidade entre repetições, consumo e latência. O conjunto de validação final deve ser distinto do usado para ajustar limiares.

Critérios de validação estatística:

- Reportar **erro mediano, p95 e pior caso**, não apenas média.
- Reportar **falso positivo de parcial/B** e **taxa de dados inconclusivos**; um sistema que sempre responde “insuficiente” não satisfaz qualidade.
- Comparar com testes anteriores de regressão e parâmetros idênticos quando possível.
- Não extrapolar erro medido em ondas senoidais para instrumentos reais.
- Documentar limitações e instrumentos/taxas não validados no README e na Ajuda avançada.

## 12.4 Condição de bloqueio de publicação

**Não publicar como ferramenta de afinação personalizada confiável** se:

1. Atribuição de parciais falha sistematicamente em casos comuns sem avisos.
2. A interface apresenta B definitivo quando o ajuste é indeterminado.
3. Curvas são aplicadas sem confirmação, modificam as quintas históricas ou **alteram silenciosamente intervalos característicos de um temperamento sob alegação enganosa de fidelidade histórica**.
4. Resultados não são reproduzíveis para o mesmo áudio/mesmo conjunto de parâmetros.
5. Não há tratamento de perfis corrompidos ou incompatíveis.
6. O desempenho/travamento em celular real não foi testado ou as limitações não foram comunicadas.
7. A implementação viola a privacidade do áudio ou ativa gravação sem consentimento.

---
# 13. Arquitetura técnica: módulos, áudio e integração

## 13.1 Divisão lógica em um HTML autocontido

O projeto auditado reúne CSS, interface, scripts DSP/licenças e binários embutidos em `index.html`, com o motor canônico já integrado. A futura implementação pode manter um único HTML distribuível, mas deve **organizar os módulos por responsabilidades**, de modo que testes e revisões não exijam alterar simultaneamente as equações antigas.

```text
INDEX.HTML (interface autocontida)
├── Navegação Ferramentas / temas / ajuda progressiva
├── Afinador existente (referência teórica + medição DSP)
│   ├── YIN + FFT / pYIN / SWIPE' / Pico
│   ├── FFT visual e Nota fixa
│   └── Diagnóstico existente (20 s; WAV opcional)
├── Captura de áudio compartilhada (gerenciamento único do microfone)
│   ├── Blocos PCM com timestamp e sample rate real
│   └── Distribuição seletiva aos consumidores ativos
├── Worker DSP existente (não reescrever)
├── Worker de análise de parciais [NOVO]
│   ├── Seleção de janelas / extração espectral
│   ├── Identificação de componentes / ordens
│   ├── Qualidade por parcial / estabilidade
│   └── Modelo B robusto (Fase 2)
├── Gerenciador de perfis [NOVO]
│   ├── IndexedDB / migrações / transações
│   └── JSON versionado / importação / exportação
├── Motor de curvas [NOVO]
│   ├── Snapshot histórico / alvos assinados / critérios intervalares
│   ├── Fidelidade ao temperamento × Otimização acústica
│   ├── Pesos / restrições / otimização / relatório de intervalos
│   ├── Estados Rascunho / Prévia / Aplicada
│   └── Versões / auditoria / compatibilidade
└── Camada de afinação composta [NOVO na Fase 5]
    ├── Frequências do temperamento original
    └── Correções instrumentais Δ_x opt-in
```

**Contrato de integração com o HTML atual:** o motor musical já existe em `ModeloIdentidadesHistoricas`/`ModeloDivisaoIgual` → `CatalogoAlvosCanonicos` → `estadoMusicalAtual`. Novos perfis e curvas **consomem** essas APIs e jamais instalam uma tabela por número MIDI, `byPc` ou `targetsByMidi`. `soundId` serve para detecção de coincidências no snapshot, não para igualar decisões de correção de duas teclas. O futuro Worker acústico não é o atual Worker DSP nem o AudioWorklet opt-in do diagnóstico.

**[RECOMENDADO]** Usar Worker separado para análise mais pesada facilita isolamento de falhas, mas decisões reais de compartilhar ou não o Worker precisam de medições de memória e concorrência. **Não** manter FFT de alta resolução calculando continuamente enquanto o usuário está só no Afinador.

### 13.1.1 Coordenação de sessões multiataque [RECOMENDADO]

- **`AcquisitionSessionController`** coordena a máquina de estados de 6.4.2, com nota/corda/fonte imutáveis até revisão/encerramento. Não confundir `sessionIdDSP` do afinador (ciclo de Worker) com `acquisitionSessionId` do histórico acústico: IDs separados.
- **`AttackSegmenter`** avalia onset, decaimento, silêncio e sobreposição; não produz nota ou B por si só. Envia `attackDetected`/`sustainSegmentReady` associados a `executionId` e `captureGeneration` para evitar resposta obsoleta.
- **`PartialMeasurementEngine`** consome somente o trecho útil, devolve parciais e qualidade por execução. **`SessionAggregator`** recebe observações finalizadas, aplica política de inclusão e (na Fase 2) ajusta B conjunto; a camada UI consome snapshots imutáveis da revisão.
- **Coleta contínua de PCM temporário não é gravação histórica**. Ring buffer tem limite verificável e descarte seguro dos segmentos temporários já processados; metadados de ataques permanecem até salvar/descartar ou quota segura. Sessões sem memória suficiente pausam com explicação, não produzem resultados silenciosamente truncados.
- **`sessionRevision` e `aggregationRevision`** evitam que um resultado antigo sobrescreva revisões posteriores; a versão de algoritmo/params deve acompanhar cada execução e impedir mistura incompatível. Se o usuário voltar do modo Perfis, a sessão recupera identidade e estado sem trocar de corda automaticamente.


## 13.2 Aquisição compartilhada e sincronização

- Um único fluxo de microfone deve ser dono da permissão e do ciclo `iniciar/encerrar`. Cada ferramenta solicita dados conforme seu estado.
- O **AudioWorklet** é uma opção para capturar áudio contínuo de forma consistente; distinguir captura de PCM para análise da **gravação e retenção de WAV**. Captura temporária não implica consentimento para armazenar áudio longo.
- Incluir timestamps monotônicos de blocos, número de amostras e `sampleRate` efetivo; não juntar buffers sobrepostos do AnalyserNode como se fossem amostras contíguas.
- Usar **ring buffer limitado** para janelas de análise e transferência eficiente dos blocos; evitar alocação por amostra e serialização JSON por quadro DSP.
- Mensagens para Workers acústicos devem carregar `acquisitionSessionId`, `executionId`, `captureGeneration`, `analysisConfigRevision`, `frameId`/`segmentId`, `sourceId`, `sampleRateHz` e `capturedAtMs`; resultados musicais incluam `baseSnapshotHash`/`musicRevisionAtCapture` quando houver associação musical. **Não** reinterpretar `generationIdDSP`/`sessionIdDSP` do Worker do afinador como sessão acústica; respostas obsoletas de qualquer domínio são descartadas.
- Vincular cada resultado ao ID/hash da configuração de captação/análise usada. Mudanças apenas musicais atualizam `musicRevision`, mas **não** invalidam nem reiniciam o processamento DSP; reavaliam o vínculo com nota/curva. Mudanças técnicas seguem `generationIdDSP` e cancelam resultados de geração incorreta. Troca de ferramenta/nota durante aquisição cria revisão/cancelamento **do analisador**, não reset técnico indiscriminado de pYIN/SWIPE'.
- Um caminho de fallback só é aceito se preservar a propriedade física exigida pelo algoritmo; queda de capacidade pode desabilitar cálculo de B e deixar o afinador tradicional funcionando.
- A escolha de FFT de 4.096–32.768 pontos do afinador **não limita artificialmente** janelas internas do analisador de parciais, nem deve modificar as janelas nativas de SWIPE’.
- Marcar aquisições com origem/microfone quando a API oferecer dados válidos; nunca prometer modelo de chip, driver ou latência real de hardware que não estejam acessíveis.

## 13.3 Eventos e transições de estado

| Evento | Reação obrigatória |
|---|---|
| `MIC_PERMISSION_GRANTED` | Iniciar captura apenas para ferramenta solicitante; informar settings efetivos. |
| `MIC_PERMISSION_DENIED` | Mostrar razão do navegador quando disponível e caminho de retomada; não travar outras áreas. |
| `TOOL_SELECTED` | Desativar consumidores desnecessários; preservar preferências musicais; tratar medição inacabada. |
| `NOTE_SELECTED` | Invalidar somente os candidatos da análise atual e confirmar nova identidade. |
| `MEASUREMENT_STARTED` | Criar `AcquisitionSession` com nota, corda, origem, modelo e parâmetros; alterações de contexto exigem outra sessão. |
| `ATTACK_DETECTED` | Criar `executionId`, anotar onset e bloquear duplo disparo no mesmo sustain. |
| `EXECUTION_SEGMENT_READY` | Enviar trecho útil ao analisador; registrar qualidade e duração, sem contar quadros correlacionados como ataques. |
| `EXECUTION_ACCEPTED` / `EXECUTION_REJECTED` | Preservar observação e razões; apenas ataques aceitos participam do consolidado por padrão. |
| `SESSION_AGGREGATE_UPDATED` | Criar revisão imutável com ataques incluídos, valores e status de convergência; não modificar curvas aplicadas. |
| `SESSION_PAUSED` / `SESSION_RESUMED` | Preservar rascunho, rearmar apenas após confirmação e continuidade física de captura. |
| `SESSION_REVIEW_REQUESTED` | Encerrar coleta voluntariamente e congelar revisão; deixar ataques individualmente inspecionáveis. |
| `STABLE_SEGMENT_READY` | Executar extração espectral e avaliação dos parciais. |
| `MEASUREMENT_FROZEN` | Fixar resultado para inspeção sem modificá-lo por áudio subsequente. |
| `MEASUREMENT_SAVED` | Transação persistida e feedback de êxito; nunca sinalizar sucesso antes de confirmar escrita. |
| `B_ESTIMATED` | Atualizar somente modelo da medição, não a curva aplicada. |
| `CURVE_PREVIEW_READY` | Criar versão de prévia e diff; não afetar afinador. |
| `CURVE_APPLY_REQUESTED` | Conferir compatibilidade, mostrar consequências e exigir confirmação. |
| `CURVE_APPLIED` | Atualizar referências-alvo com identificador de versão, preservando dados teóricos. |
| `CURVE_DISABLED` | Voltar a f_temperamento, sem descartar perfis ou curvas. |
| `STORAGE_FAILURE` | Alertar, permitir exportar dados em memória, impedir falsa confirmação. |
| `AUDIO_INTERRUPTED` | Invalidar segmento incompleto e não converter silêncio/dropout em medida. |

## 13.4 Segurança de implementação

- Dados provenientes de `JSON` importado, nomes de perfis e comentários devem ser tratados como texto sem interpretação de HTML/JS; usar `textContent`, não `innerHTML` com valores do usuário.
- Limitar quantidade de perfis, tamanho de campos/arquivos, número de parciais e **memória/duração do fluxo contínuo**, com pausa e aviso; **não impor um teto arbitrário de execuções válidas** nem apagar histórico aceito. Rejeitar parâmetros numéricos inválidos.
- Não avaliar/`eval` código vindo de perfis ou supostas “fórmulas personalizadas”.
- Não criar `blob:`/AudioWorklet indefinidamente sem liberar recursos; encerrar Worker e stream por ferramenta quando não necessários.
- Se o usuário retirar permissão ou fechar, esvaziar buffers temporários conforme política; persistência de dados só após ação explícita.
- Auditoria deve evitar serializar amostras brutas de áudio em cada quadro do JSON; o WAV pode ser exportado separadamente quando autorizado.
- Interface e processamento não podem se autoconfirmar (`Salvo`, `Aplicado`) antes da conclusão da transação/cálculo.

---

# 14. Contratos de dados e formatos versionados

> Os exemplos abaixo definem **a semântica recomendada**, não impõem nomes de classes internas. Campos ilustrativos são estruturados para que a equipe implemente e teste sem depender da conversa.

## 14.1 Entidades fundamentais

**`InstrumentProfile`** — identifica instrumento e família, extensão, modelo escolhido e histórico; não contém diretamente uma única medição definitiva.

**`AcousticMeasurement`** — observação de **uma execução/ataque** de nota/corda, com PCM opcional, candidatos, aceitos/rejeitados, dados temporais, parâmetros, f1 medida/inferida e status. Não usar um registro por quadro FFT.

**`AcquisitionSession`** — conjunto de execuções da **mesma nota e contexto**, com `sessionId`, identidade congelada, modo de disparo, ordem/IDs dos ataques, contagens de tentativas/aceitas, estado da sessão e `SessionAggregate` versionado.

**`SessionAggregate`** — resultado combinado/provisório por sessão, com `aggregationRevision`, `includedExecutionIds`, `excludedExecutionIds`, política de pesos, estimativa B conjunta quando elegível, dispersão entre ataques, estabilidade e estado de convergência. Nunca substitui as execuções individuais.

**`PartialObservation`** — um pico ou componente com ordem candidata, Hz real, amplitude relativa, estabilidade, confiança, status e proveniência de quadros.

**`InharmonicityEstimate`** — resultado opcional do ajuste: modelo, parâmetros F/B/f1, parciais usados, resíduos, incerteza, status e motivo.

**`TuningCurve`** — versão imutável de correções Δ por nota, referência musical, **`priorityMode`/alvos assinados dos parciais, restrições de fidelidade em fundamentais, snapshot histórico**, dados de origem, critérios/ponderações, resultado de otimização, estado e histórico.

**`CurveApplication`** — vínculo entre curva **compatível** e afinador, com confirmação, horário, versão, condição de ativação, resumo do modo de prioridade e registro de mudanças intervalares aceitas.

**`AuditEvent`** — evento que registra transições de estado e intervenções: quem/por que excluiu um parcial, marcou um outlier ou aplicou uma curva.

## 14.2 Esquema JSON canônico de perfil acústico (EXEMPLO FICTÍCIO, NÃO INSTALADO)

**Formato proposto** `schema:'afinador.acoustic-profile'`, `schemaVersion:1`: é um novo contrato, **não** o `afinador-tuning-v1` da biblioteca musical e **não** um upgrade do diagnóstico v2. A escolha `schemaVersion:1` é válida porque esse perfil acústico ainda não foi implementado. IDs são ilustrativos; o `baseSnapshotHash` será calculado por canonicalização formal na implementação. Na demonstração, A3 pertence à quinta `k=3` da disposição histórica, **não** à posição MIDI 57.

```json
{
  "schema": "afinador.acoustic-profile",
  "schemaVersion": 1,
  "profile": {
    "profileId": "instrumento-exemplo",
    "displayName": "Instrumento histórico de estudo — exemplo fictício",
    "instrumentFamily": "harpsichord",
    "instrumentLayout": {
      "layoutId": "12-standard",
      "physicalKeysPerOctave": 12,
      "keyOrderSource": "canonical_graph",
      "range": {
        "first": {"keyId": "keyboard:fifth:3", "octave": 3},
        "last": {"keyId": "keyboard:fifth:3", "octave": 4}
      }
    },
    "acousticModelId": "stiff_string",
    "measurements": [
      {
        "measurementId": "measurement-001",
        "sessionId": "session-001",
        "executionId": "execution-001",
        "executionIndex": 1,
        "capturedAt": "2026-11-17T12:00:00Z",
        "noteBindingStatus": "confirmed",
        "noteBinding": {
          "keyId": "keyboard:fifth:3",
          "pitchId": "fifth:3",
          "soundIdAtCapture": "sound:fifth:3",
          "octave": 3,
          "scientificLabelAtCapture": "A3",
          "baseSnapshotHash": "EXEMPLO-NAO-E-UM-HASH-VALIDO"
        },
        "captureContext": {
          "captureMode": "single_string",
          "stringIndex": 1,
          "sampleRateHz": 48000,
          "sourceContextId": "microphone-session-local",
          "triggerMode": "automatic"
        },
        "onsetAtMs": 100,
        "sustainStartMs": 290,
        "sustainEndMs": 1550,
        "releaseAtMs": 1620,
        "usefulDurationMs": 1260,
        "effectiveTemporalBlocks": null,
        "fundamentalEstimateHz": 207.7,
        "fundamentalSource": "measured_first_partial",
        "firstPartialMeasuredHz": 207.7,
        "partialObservations": [
          {
            "partialId": "partial-1", "order": 1,
            "measuredHz": 207.7, "amplitudeDbRelative": -2.1,
            "frequencyStabilityCents": 0.4,
            "status": "accepted", "reasonCodes": [],
            "confidenceScore": null
          },
          {
            "partialId": "partial-2", "order": 2,
            "measuredHz": 415.9, "amplitudeDbRelative": -8.0,
            "frequencyStabilityCents": 0.7,
            "status": "accepted", "reasonCodes": [],
            "confidenceScore": null
          }
        ],
        "inharmonicity": {
          "modelId": "stiff_string",
          "status": "insufficient_data",
          "B": null, "F": null, "f1InferredHz": null,
          "usedPartialIds": [], "residualsCents": [],
          "uncertainty": null
        },
        "executionStatus": "accepted_for_partial_review",
        "includedInAggregate": true,
        "reasonCodes": []
      }
    ],
    "acquisitionSessions": [
      {
        "sessionId": "session-001",
        "noteBindingStatus": "confirmed",
        "noteBinding": {
          "keyId": "keyboard:fifth:3",
          "pitchId": "fifth:3",
          "octave": 3,
          "baseSnapshotHash": "EXEMPLO-NAO-E-UM-HASH-VALIDO"
        },
        "sourceContextId": "microphone-session-local",
        "captureMode": "single_string",
        "stringIndex": 1,
        "status": "review",
        "executionIds": ["execution-001"],
        "attemptCount": 1,
        "acceptedExecutionCount": 1,
        "aggregationRevision": 1,
        "aggregate": {
          "status": "insufficient_data",
          "modelId": "stiff_string", "B": null,
          "includedExecutionIds": ["execution-001"],
          "excludedExecutionIds": [],
          "perExecutionB": {"execution-001": null},
          "perExecutionScaleHz": {},
          "convergenceStatus": "preliminary",
          "aggregationMethodId": "joint_robust_stiff_string_proposed",
          "aggregationMethodVersion": "proposal-1",
          "uncertainty": null,
          "reasonCodes": ["single_execution", "insufficient_partial_orders"]
        },
        "revisions": [
          {
            "aggregationRevision": 1,
            "includedExecutionIds": ["execution-001"],
            "status": "insufficient_data"
          }
        ]
      }
    ]
  },
  "curves": [],
  "auditEvents": []
}
```

**Regras do exemplo:** o primeiro parcial foi observado e registrado separadamente da estimativa de fundamental; duas ordens e um ataque não autorizam B robusto. `soundIdAtCapture` foi armazenado para auditoria e **não** serve sozinho como chave permanente. Os rótulos em texto são apresentação. A referência teórica do A3 depende do temperamento real no snapshot; a medição `207,7 Hz` é **um valor observado fictício**, não a frequência-alvo imposta ao perfil. A faixa ilustrativa de duas notas não pretende descrever um cravo inteiro.

### Exemplo mínimo de revisão após três execuções (somente para entendimento)

```json
{
  "sessionId": "session-demo-003",
  "noteBinding": {"keyId":"keyboard:fifth:3", "pitchId":"fifth:3", "octave":3},
  "aggregationRevision": 3,
  "executionIds": ["exec-01", "exec-02", "exec-03"],
  "individualEstimates": [
    {"executionId":"exec-01", "B":0.00038, "status":"provisional"},
    {"executionId":"exec-02", "B":0.00040, "status":"provisional"},
    {"executionId":"exec-03", "B":0.00039, "status":"provisional"}
  ],
  "aggregate": {
    "B":null,
    "method":"pending_validated_joint_fit",
    "convergenceStatus":"repeatability_unverified",
    "includedExecutionIds":["exec-01","exec-02","exec-03"],
    "uncertainty":null
  }
}
```

Três ataques consistentes são observações independentes, não autorização para uma média cega. Os B individuais e IDs são fictícios; os parciais necessários ao ajuste conjunto não foram fornecidos, portanto o B consolidado permanece `null`.

## 14.3 Esquema proposto de curva por tecla canônica

```json
{
  "schema": "afinador.tuning-curve",
  "schemaVersion": 1,
  "curveId": "curve-001",
  "curveVersion": 1,
  "profileId": "instrumento-exemplo",
  "status": "preview",
  "baseSnapshot": {
    "temperamentId": "pythagorean",
    "tuningKind": "fifths-chain",
    "layoutId": "12-standard",
    "reference": {"kind": "historical-a4", "frequencyHz": 415.3},
    "source": "CatalogoAlvosCanonicos",
    "snapshotHash": "EXEMPLO-NAO-E-UM-HASH-VALIDO"
  },
  "corrections": [
    {
      "keyId": "keyboard:fifth:3", "pitchId": "fifth:3",
      "octave": 3, "deltaCents": -0.5, "source": "computed"
    },
    {
      "keyId": "keyboard:fifth:3", "pitchId": "fifth:3",
      "octave": 4, "deltaCents": 0.0, "source": "anchor"
    },
    {
      "keyId": "keyboard:fifth:3", "pitchId": "fifth:3",
      "octave": 5, "deltaCents": 1.7, "source": "interpolated"
    }
  ],
  "objective": {
    "modelId": "weighted-partial-intervals",
    "version": "prototype-3.0-unvalidated",
    "priorityMode": "temperament_fidelity",
    "targetPolicyDefault": "harmonic_temperament_signed",
    "partialRatioModel": "stiff_string_or_validated_empirical",
    "intervalCriteria": [],
    "fundamentalIntervalConstraints": [],
    "adjacencyPolicy": "physical_keyboard_order",
    "anchorPolicy": {
      "keyId": "keyboard:fifth:3", "pitchId": "fifth:3",
      "octave": 4, "deltaCents": 0.0
    }
  },
  "intervalAudit": {
    "status": "not_computed",
    "pairs": [],
    "requiredFieldsPerPair": [
      "lowerTarget", "upperTarget", "baseSnapshotHash",
      "partialLower", "partialUpper",
      "temperamentIntervalCents", "referencePartialDetuningCents",
      "targetDetuningCents", "predictedPartialDetuningCents",
      "fundamentalIntervalShiftCents", "predictedPartialDifferenceHz",
      "targetPolicy", "qualityStatus"
    ]
  },
  "sourceMeasurementIds": ["measurement-001"],
  "quality": {"status":"not_validated", "reasons":["no_interval_evidence"]},
  "appliedAt": null
}
```

**Advertência:** valores de correções, hash e medições são fictícios. Uma curva sem critérios avaliados, sem restrições validadas e com `status:'preview'` **não é aplicável**. `baseSnapshot` real também precisa serializar ou referenciar de forma verificável o **conteúdo efetivo de frações, configuração física/EDO e alvos**, não apenas os campos resumidos deste exemplo. Na implementação, `lowerTarget`/`upperTarget` contêm `(keyId,pitchId,octave)`; `targetDetuningCents` é assinado; a política de curva preserva a decisão de **uma correção por tecla física**, e não colapsa teclas por `soundId`.

## 14.4 Regras formais para os esquemas

- Campo `schema` nomeia o formato; `schemaVersion` muda quando o contrato muda; `algorithmVersion` identifica mudança de método/constantes.
- Não usar `NaN`, `Infinity` ou strings ambíguas para ausências; usar `null` com `status/reasonCodes`.
- Valores com **unidades no nome** (`Hz`, `Cents`, `Ms`, `DbRelative`) e vínculo musical `(keyId,pitchId,octave)` confirmado e verificável contra o snapshot; `soundIdAtCapture` é contextual. **Não adicionar `midiNote`, `pc`, `lowerMidi` ou `upperMidi` como índice primário.**
- `B` não tem unidade; `F` e `f1` têm Hz. `fundamentalEstimateHz` pode diferir de `firstPartialMeasuredHz`.
- IDs internos do perfil/medição são distintos; **sessionId, executionId e measurementId são identificadores diferentes** (o measurementId pode ter vínculo 1:1 com execução). Integridade referencial e ordem de `executionIds` são obrigatórias; não armazenar serial do instrumento como identificador técnico permanente por padrão.
- Preservar status `measured / inferred / interpolated / manually_edited` e distinguir “pico rejeitado” de “medição descartada da curva”.
- Proteger compatibilidade de curva não apenas pelo `baseTemperamentId` mas também por **snapshot/hash efetivo** da tabela ou das quintas, pois presets podem ter sido personalizados. O hash de snapshot deve usar canonicalização documentada, com unidades, representação racional exata dos ajustes, teclas físicas, alvos e referência **histórica A4 ou EDO por grau/oitava/Hz** definidas; não usar hashes textuais sensíveis a formatos locais inconsistentes.
- Em curvas, exigir `priorityMode`, `targetPolicyDefault` e, por relação, `targetDetuningCents` **assinado**; registrar distinção entre `temperamentIntervalCents`, `fundamentalIntervalShiftCents` e `predictedPartialDetuningCents` para impedir que dados de batimento sejam confundidos com cents entre fundamentais. Na migração, campos ausentes devem ser declarados `unknown/not_computed`, nunca presumidos como `t=0`.
- Uma medição acústica anterior à afinação não deve se transformar em alvo absoluto por multiplicação ingênua: preservar `f1` observado e razões espectrais `g` separadamente; o alvo é sempre reconstruído a partir de `f_temp` e `Δ` no snapshot ativo.
- Importações desconhecidas devem permanecer **não aplicadas**, jamais substituir curva ativa automaticamente.
- Não usar JSON de diagnóstico de 20 segundos como armazenamento primário do perfil; ele é um relatório de sessão, não a entidade histórica canônica.
- Arquivos exportados são cópias locais; salvar no `IndexedDB` e exportar ZIP/JSON são operações distintas, com feedback separado.
- Preparar esquema para reprocessamento posterior a partir de WAV associado por `audioAssetId`, mediante opt-in, sem exigir áudio gravado para todo perfil.
- Mudança de versões deve ter testes de migração sem perda de informações.
- Um importador futuro de dados acústicos legados pode reconhecer medições avulsas, mas **não pode inventar sessões, identidade física de tecla, repetições ou B consolidado**. A evolução do esquema a ser implementado precisa de versão e política de migração registradas; o exemplo `schemaVersion:1` é proposta não implantada, por isso integra sessão desde o primeiro contrato previsto.

### 14.4.1 Canonicalização e compatibilidade de snapshot [DEFINIDO para v3.0]

Implementar canonicalização **determinística e testada** antes de assinar qualquer curva. Campos mínimos: `schemaVersion`, família `tuningKind`, ID e conteúdo da definição-base (inclusive definições pessoais), frações racionalizadas de cada quinta/offset (numerador/denominador normalizados, **não** floats locais), `indiceQuintaCompensatoria`, `layoutId`, `baseLayoutId`, `extensionFifths`, `extraPitchOffsets`, `keyboardKeys`/mapa de graus quando EDO, referência discriminada (`historicalA4Hz` **ou** tripla EDO), e tabela **ordenada por `(keyId,octave)`** de `pitchId`, `frequencyHz` em representação numérica canônica, `targetId` e política de registros relevante. Hash criptográfico sobre serialização canônica com UTF-8, ordem fixa e versão de canonicalização.

O conteúdo da `CatalogoTemperamentos` / definição pessoal é parte da assinatura; comparar só ID e `musicRevision` é **insuficiente**. Registrar a tolerância **somente** na comparação de floats durante testes, nunca substituir hash por arredondamento sem política definida. A compatibilidade de um instrumento/acoustic profile pode abranger medições com snapshots diferentes, mas cada **curva aplicada** se vincula a um único snapshot e a um conjunto explícito de teclas. Uma importação que não consegue provar a correspondência entre `keyId` de origem e destino é `unresolved`, não aplicada.

**Separar quatro revisões:** `musicRevision` (já existe), `generationIdDSP` (já existe), `acquisitionSessionId`/`captureGeneration` (novos e independentes, para dados acústicos), `curveVersion`/`curveApplicationRevision` (novos). Não acrescentar outra tabela musical ou nova função de cálculo de frequência paralela ao catálogo.

## 14.5 Auditoria acústica por nota — requisito transversal novo [RECOMENDADO]

Cada nota medida deve responder de maneira rastreável:

| Pergunta do usuário | Dados/visão |
|---|---|
| **O que foi medido?** | PCM opcional, segmento temporal, picos candidatos, Hz/amplitude/ordem, estado de cada parcial. |
| **Quanto confio?** | Estabilidade dentro de cada execução, dispersão **entre ataques independentes**, SNR, contagens de tentativas/aceitas, incerteza, influência de cada pico/execução e adequação do modelo. |
| **Como foi calculado?** | Fórmula B, parâmetros de ajuste, conjunto de parciais aceitos, perdas/pesos, versão e resíduos; no caso de curva, `I_T`, `t_T^harm`, `g`, `priorityMode`, alvo assinado, restrições e desvios resultantes. |
| **O que mudou?** | Histórico da nota, evolução do B, curveVersion/delta e eventos de edição/aplicação. |

Fluxo de inspeção:

```text
Ponto da curva → nota → sessão → execução/ataque → lista de parciais → parcial específico
  → trecho de espectro → qualidade, janelas, resíduos, motivos
  → reavaliar/repetir/confirmar mantendo histórico
```

A cadeia de evidências é uma **característica central de qualidade**, não um painel experimental dispensável.

---

# 15. Integração com diagnóstico, ajuda e documentação

## 15.1 Diagnóstico existente [EXISTENTE]

O monitor atual é **opcional**, fica abaixo da FFT e acima do cilindro acústico de quintas, mostra parâmetros do algoritmo ativo e permite captura de **20 segundos** com contador, JSON/ZIP e WAV opcional (captura contínua por AudioWorklet quando suportada). O monitor atual registra metadados do navegador, áudio e desempenho dentro do limite imposto pelas APIs legítimas da plataforma.

## 15.2 Extensão futura para o analisador [RECOMENDADO]

- O usuário pode solicitar um **relatório de auditoria acústica** a partir de uma medição ou curva; ele não deve iniciar automaticamente uma gravação de 20 segundos do monitor original.
- Novo diagnóstico pode incluir frequências de todos os parciais, IDs de quadros, rejeições, tempo de cálculo de B, mudança de critérios e métricas de erro; armazenar informações suficientes para reprocessamento analítico.
- Audio WAV é **opcional** e deve ser claramente rotulado. O WAV pode captar conversas ao redor e não pode ser enviado automaticamente; antes de exportar, informar sua presença.
- Evitar FFT completa por quadro quando já existe áudio preservado e será possível recalcular FFT sob outras janelas; se houver motivo para exportar um espectro congelado, gravar janela/tipo/versão e não alegar equivalência com PCM.
- O diagnóstico jamais deverá produzir amostras extras de YIN/pYIN/SWIPE’ apenas por estar aberto.
- Dados de navegador/sistema/hardware: coletar apenas o legitimamente exposto por APIs padrão, com campos opcionais e sem rastreamento.
- Limitar arquivo/tamanho de memória, apresentar o consumo e encerrar captura com segurança se o limite for atingido.

## 15.3 Ajuda rápida e avançada

A **Ajuda rápida** do Afinador permanece introdutória. Ao selecionar Ferramentas > Parciais, a ajuda contextual explica **o que é um parcial**, **como sustentar e isolar a nota**, **como repetir uma medida** e **por que um resultado pode ser inconclusivo**.

A **Ajuda avançada** deve acrescentar capítulos progressivos:

1. Física dos parciais e série harmônica ideal.
2. FFT, tamanho da janela, interpolação, resolução real e limites de zero-padding.
3. Como a ferramenta separa picos, parciais, interferências e ordens.
4. Modelo B, hipótese de corda rígida, ajustes robustos e resíduos.
5. Diferença entre medido, inferido, interpolado e corrigido.
6. Medições por corda, uníssono, nota completa; cuidados especiais de piano/cravo e outros instrumentos.
7. Construção de curva, critérios intervalares, pesos e batimentos; por que não existe uma curva única; **duodécimas 3:1/6:2/9:3, temperamentos desiguais, alvos assinados e modos de fidelidade/otimização**, com advertência contra pureza indiscriminada.
8. Camadas de temperamento histórico e correção instrumental.
9. Perfis, versões, persistência, exportação e privacidade.
10. Limitações e plano de testes em celulares.

**Não substituir a ajuda atual** por documentação técnica longa. Seguir o padrão já existente: explicação pequena → expansão voluntária → aprofundamento contextual.

## 15.4 README, roadmap e nomenclatura

- Ao implementar cada fase, atualizar `README.md`, os capítulos da Ajuda e o roadmap **no mesmo conjunto de alterações**, separando `Disponível`, `Experimental` e `Planejado`.
- A interface usa **inarmonicidade** na nomenclatura em português; arquivos técnicos podem usar `inharmonicity` por compatibilidade de nomes internacionais, mas sem alternar grafias sem motivo no texto exibido.
- `Parcial` é a palavra preferida para componentes medidos; não usar `harmônico` como sinônimo universal para componentes desviados ou modos de sinos.
- `Temperamento` não é `curva`, `B` não é `cents de afinação`, `f1` não é necessariamente o pico dominante; `soundId` não é chave persistente exclusiva; `parcial selecionado` não é `alvo de batimento zero`; `t_T^harm` não é `I_T`; `f1 observada` não é automaticamente `f1 alvo`.
- Registrar créditos e licenças da implementação existente; não apagar avisos ao refatorar HTML.

---

# 16. Plano de implementação incremental e entregas

> A ordem das **Fases 1–7** é preservada. Há um **marco 0** transversal de infraestrutura/UX, recomendado para evitar mudanças invasivas posteriores.

| Marco | Entrega verificável | Pré-requisito / condição de avanço |
|---|---|---|
| **0 — Congelamento canônico e navegação** | Baseline SHA do HTML, 18 presets, 12/13/14, EDO, registros, cilindro/lobo, transições musicais/DSP; Ferramentas e áreas isoladas **sem** habilitar análise fictícia. | Assinaturas de alvos/identidades e no-reset DSP preservadas; `f_temp` somente via catálogo. |
| **1A — Extração de parciais** | Captura, FFT especializada, tabela de componentes e teste sintético. | Frequências/ordens corretamente recuperadas, rejeição clara. |
| **1B — Inspeção progressiva** | Zoom, gráfico de desvios, confiança individual, congelar, revisão. | Estados auditáveis e testes de celular. |
| **1C — Aquisição multiataque** | Detectar/rearmar ataques, registrar execuções independentes, permitir repetição livre, mostrar estados e revisões sem calcular B conclusivo. | Onset robusto a batimentos/vibrato, sem falsa contagem, limitação de memória e validação real. |
| **2A — Ajuste B** | Modelo físico, otimização robusta, resíduos e rejeição de casos inválidos. | Coeficientes sintéticos recuperáveis e repetibilidade. |
| **2B — Agregação e convergência** | Ajuste conjunto robusto por execução com `F_j` próprio, estabilidade entre ataques, exclusão reversível, sugestão de parada sem bloqueio. | Não confundir quadros e ataques; detectar erros sistemáticos e modelos ruins. |
| **2C — Validação de B** | Ensaios de cordas reais, incerteza e calibragem dos critérios de convergência e parada sugerida. | Sem B falso em dados insuficientes; estudos de repetibilidade entre ataques. |
| **3 — Perfis canônicos** | IndexedDB, histórico por `(keyId,octave)` (piano 88 teclas quando cabível), vínculos musicais com snapshot, exportação/importação, compatibilidade com biblioteca atual. | Round-trip sem perda, colisões key/pitch e transições histórico↔EDO testadas; **não** migrar biblioteca musical silenciosamente. |
| **4A — Curvas por tecla em prévia** | Critérios entre **alvos canônicos por tecla/oitava**, objetivos explícitos `Fidelidade ao temperamento` e `Otimização acústica`, `t_T^harm`, otimização, comparação, incerteza, sem aplicação. | Casos analíticos iguais/desiguais/EDO e 3:1/6:2/9:3; testes de enarmonia, coincidência sonora e restrições incompatíveis. |
| **4B — Curvas com histórico** | Edição, versões, diff, relatório de mudança de intervalos fundamentais e de desvios parciais, aprovação explícita. | Sem mudança silenciosa da referência ou de significado histórico. |
| **5 — Integração opt-in canônica** | Correção por `(keyId,octave)` aplicada opcionalmente à nota fixa/automática e gerador, sem alterar grafo ou DSP; compatibilidade por hash. | `Δ=0` equivalente; mudança musical não reseta DSP; desligar restaura alvo exato; quintas/EDO/lobo preservados. |
| **6 — Instrumentos adicionais** | Modelos adequados a famílias diversas. | Modelo B não imposto a fontes não cordofônicas. |
| **7 — Contínuo** | Testes matemáticos, comparação real, desempenho/privacidade/documentação. | Obrigatório a cada marco anterior. |

### Gates específicos para compatibilidade com a nova arquitetura

**Gate 0:** validar fonte HTML por SHA e APIs canônicas, registrar os 18 presets, referências históricas/EDO, layouts 12/13/14, diagnóstico v2 e grafo do cilindro; rejeitar qualquer projeto que necessite reintroduzir `midiNote` ou `pc` como identidade.

**Gate 1:** caracterização acústica sem publicar curvas e sem capturar audio quando não solicitado; preservar noteBinding incerto, qualidade individual, multiataque e PCM correto.

**Gate 2:** ajuste B não reinterpreta a frequência-alvo teórica como observação; resultados B e graus físicos permanecem separados de identidades por tecla.

**Gate 3:** perfis IndexedDB têm chave de instrumento/tecla/oitava/sessão/corda, exportação round-trip, snapshot/hash; biblioteca musical `afinador-tuning-v1` e preferências continuam intocadas.

**Gate 4:** curvas por tecla, ordem física explícita, alvos assinados e snapshots completos; casos de duas teclas coincidentes, EDO e incompatibilidade musical obrigatórios.

**Gate 5:** integração opcional preserva `CatalogoAlvosCanonicos`, `musicRevision`/`generationIdDSP`; nenhum reset musical de pYIN/SWIPE'. Frequências teóricas intactas com correção desligada.

**Gate 6/7:** instrumentação/performance e homologação real; só declarar pronto após testes de microfone e browsers móveis, nunca apenas pelo Chromium sintético.

### Fluxo obrigatório para cada alteração

1. Registrar a especificação mínima e um conjunto de testes **antes** de editar.
2. Alterar apenas o módulo/fase aprovada e manter backup da versão anterior.
3. Rodar unitários, dados sintéticos, integração e regressão dos detectores e temperamentos atuais.
4. Testar nos dois temas, em múltiplas larguras de tela, com áudio ativo/inativo.
5. Quando envolver captura ou otimização acústica, validar em HTTPS/dispositivo real e classificar como pendente quando isso não for possível.
6. Documentar resultados, limitações e condições de falha; **não declarar completude total** se a parte física não foi validada.
7. Atualizar README/Ajuda/Roadmap e entregar `index.html` e arquivos da fase.
8. Somente então iniciar o marco seguinte.

### Indicadores para avaliar a UX (além de DSP)

- Tempo para iniciar e concluir uma medição, sem consultar manual.
- Capacidade do usuário de repetir ataques sem tocar em botões a cada nota e de entender por que uma execução foi aceita/rejeitada; taxa de disparos duplos/falsos e de ataques perdidos.
- Se a indicação de `pode finalizar` corresponde à convergência efetiva, sem induzir o usuário a encerrar cedo ou repetir indefinidamente por insegurança.
- Capacidade de explicar por que uma frequência/B foi rejeitada.
- Tempo e número de toques necessários para chegar ao dado de um parcial específico.
- Capacidade do usuário de apontar **qual curva está aplicada** e se ela mudou.
- Taxa de erros de seleção de nota, perfil e corda; recuperação de ações acidentais.
- Desempenho de tarefas em celular de 320–390 px, com e sem ampliação de texto.

---

# 17. Decisões, recomendações e pontos pendentes

## 17.1 Decisões fixadas (não reabrir sem solicitação explícita)

- Manter o projeto como **afinador histórico com possibilidade futura de análise acústica**, não transformá-lo em afinador exclusivo de piano.
- Quatro ferramentas em total: **Afinador**, **Parciais e inarmonicidade**, **Perfis instrumentais**, **Curvas de afinação**; uma entrada superior `Ferramentas` é a direção de navegação preferida.
- Informação **progressiva** e um **analisador de parciais excepcionalmente claro e confiável** são princípios centrais.
- Parciais com qualidade individual, status de aceitação e dados detalhados consultáveis.
- **Aquisição multiataque:** tocar uma mesma nota quantas vezes desejar; observações independentes preservadas; convergência é recomendação informativa, jamais encerramento compulsório por contagem de ataques.
- Separar medida, interpretação via B, perfil instrumental, construção de curva e aplicação.
- Não equiparar pares de parciais 3:1, 6:2, 9:3 a alvos universais de pureza. A finalidade histórica de cada relação é identificada via snapshot de temperamento; as mudanças da curva nos intervalos fundamentais devem ser transparentes, mesmo sem modificar as quintas.
- Não copiar telas, códigos ou textos de aplicativos comerciais; aproveitar apenas lições gerais.
- Temperamentos históricos e EDOs não serão adulterados pela curva instrumental; correções **por tecla/oitava** independentes e reversíveis, inclusive enarmonias e teclas coincidentes.
- Atualizações de curva não devem mudar a afinação ativa silenciosamente.
- Analisador de parciais terá janelas temporais próprias, não herdadas indiscriminadamente da FFT visual.
- Testar **a cada marco de implementação**, com documentação das limitações dos aparelhos físicos.
- Preservar UI atual (temas, ajuda, cilindro, diagnóstico e botão circular) quando a ferramenta Afinador estiver selecionada.

## 17.2 Recomendações suficientemente definidas para implementação

- Um botão `Ferramentas ▾`; três áreas novas dentro do HTML existente; sem nova barra inferior de navegação; **preservar cilindro acústico 2,5D e identidade de cada tecla no Afinador**.
- Fluxo multiataque por nota sustentada com `Medir`, `Congelar`, `Limpar`, `Salvar medição`, e ações por estado `Medir novamente`/`Finalizar e revisar`.
- Detecção de ataque automática por padrão e alternativa manual; separar ataques reais de janelas FFT e evitar contagem dupla.
- Ajuste conjunto `F_j` por execução e `B` compartilhado somente quando houver justificativa física; exibir B_j, dispersão, resíduos e influência, preservando dados individuais.
- Sessões e revisões de agregação versionadas; decisão de incluir/excluir ataque é auditável e reversível.
- Camadas progressivas 0–4 e inspeção de evidências por parcial.
- Filtro de confiança separado em candidato, medição de Hz e adequação do modelo B.
- Estimativa de F e B robusta, inclusive quando o primeiro parcial está ausente.
- `IndexedDB` para os **novos** perfis acústicos e histórico, JSON versionado para exportação; preservar `localStorage` **técnico e biblioteca musical** atuais sem migração automática.
- Curva por instrumento em estados **Medindo → Prévia → Aplicada**, com confirmação e versionamento.
- Diff e explicação dos efeitos intervalares (parciais e batimentos), em vez de gráfico de Railsback sozinho.
- Auditoria acústica por nota, rastreável de curva até pico espectral.
- Dois modos explícitos de objetivo em Curvas: `Fidelidade ao temperamento` (recomendado para desiguais, com proteção de fundamentais e alvo assinado relativo ao temperamento) e `Otimização acústica` (objetivos escolhidos deliberadamente). Ambos são validações futuras, não resultados garantidos.
- Amostragem contínua com timestamps e consumidores de áudio isolados; Worker separado ou outra solução que preserve desempenho comprovado.

## 17.3 Pontos a validar antes de fixar padrões de produção

| Tema | Por que está aberto | Como decidir |
|---|---|---|
| Qual método final de refinamento de frequência por parcial? | FFT e interpolação podem não ser suficientes em todos os registros | Comparar métodos e precisão em dados sintéticos e reais |
| Duração mínima/máxima de sustentação | Dependente de grave/agudo e ruído; ataques repetidos não podem gerar espera fixa injustificada | Medir erro/tempo por faixa e tipo instrumental |
| Detector de ataque e rearme automático | Vibrato, batimentos, ruído e notas sobrepostas geram disparos falsos | Comparar onset e encerramento com anotação manual; testar instrumentos e acústicas distintos |
| Limiares de convergência entre ataques | Número de execuções não define confiança; B≈0 torna erro relativo instável | Calibrar dispersão absoluta/relativa, influência e resíduos em validação independente |
| Política de pesos por execução | Muitas janelas ou muitos parciais podem fazer um ataque dominar o ajuste | Comparar ponderação hierárquica, sensibilidade a outliers e bootstrap por clusters |
| Limiares de SNR, estabilidade e confiança | Percentuais sem calibração produzem falsa certeza | Calibrar com conjunto independente e curvas de confiabilidade |
| Número mínimo de parciais para B | Depende de cobertura de ordens e ruído | Testar identificabilidade e influência dos pontos |
| Método robusto exato de ajuste B | Vários estimadores têm vantagens e falhas | Comparar robustez, erro e custo em cenários de contaminação |
| Restrições de B por família | Não há um único intervalo universal | Definir modelos físicos e faixas observadas com referências |
| Critérios de curva e pesos iniciais | Não existe uma afinação musical ideal única | Comparar compromissos acústicos e resultados auditivos; distinguir alvo assinado histórico de coincidência física |
| Prioridade histórica vs acústica: pesos/limites | Fidelidade estrita em todas as notas é incompatível com extensão não trivial | Definir regiões e relações protegidas, tolerâncias e avisos por instrumento/temperamento; validar com músicos e afinadores |
| Interpretação dos batimentos previstos | Desvio em cents pode não prever audibilidade ou estética | Testar previsão em Hz, componentes reais, registro, amplitude, decaimento e comparações auditivas |
| Suavização/interpolação de curvas | Pode ocultar irregularidade verdadeira | Comparar previsão com notas retidas e quebra de escala |
| Curva perante troca de temperamento | Δ base-específico; rebasing é ambíguo | Definir política explícita e validar propriedades matemáticas |
| Persistência do modo Ferramentas | Preferência de UX não decidida | Teste de usabilidade; padrão conservador é Afinador |
| Navegação da barra fixa em outras telas | Pode ficar visualmente densa | Prototipar com 320–390 px e teste de foco/teclado |
| Exportar áudio junto a perfis | Quota e privacidade | Opt-in e testes de armazenamento em dispositivo real |
| Compatibilidade AudioWorklet iOS/Android | Diferentes versões/plataformas | Teste HTTPS e microfone físico, fallback seguro |
| Uso de `f1` estimada versus física | Pode haver primeiro parcial ausente | Inspeção de consistência e cálculo conjunto F/B |
| Aplicação opcional da curva no emissor | Pode induzir confusão de referência | Desativada por padrão e rotulada inequivocamente |

Nenhum ponto pendente autoriza preencher um valor silenciosamente. O implementador deve registrar sua decisão, método de validação e critérios de aceitação no changelog e no arquivo de teste.

---

# 18. Glossário essencial

| Termo | Definição operacional |
|---|---|
| **Parcial** | Componente espectral observado, de ordem identificada quando a evidência permite. |
| **Harmônico ideal** | Frequência `n·f1` em uma série perfeitamente harmônica. |
| **Inarmonicidade** | Desvio real dos parciais em relação à série harmônica ideal. |
| **Coeficiente B** | Parâmetro adimensional de modelo de corda rígida, não um desvio em cents. |
| **Fundamental / f1** | Primeiro parcial físico do modelo; pode ser fraco ou ausente no espectro. |
| **F auxiliar** | Parâmetro de escala da expressão `f_n=n F sqrt(1+B n²)`. |
| **Ordem do parcial** | Índice n do componente dentro da série de uma fonte. |
| **Atribuição de ordem** | Hipótese de qual componente corresponde a n=1,2,3 etc.; sujeita a erro. |
| **Resíduo** | Diferença entre valor medido e previsto por um modelo após ajuste. |
| **Confiança do parcial** | Qualidade da identificação de um componente; deve ser calibrada e não equivale à confiança de B. |
| **Repetibilidade** | Proximidade entre resultados obtidos sob condições semelhantes. |
| **Execução/ataque** | Uma nova excitação da nota/corda, tratada como observação acústica própria. Não é sinônimo de quadro FFT. |
| **Sessão de aquisição** | Conjunto voluntariamente aberto de execuções da mesma nota/corda/fonte/contexto, finalizado ou pausado pelo usuário. |
| **Convergência** | Consistência progressiva dos resultados após novos ataques, desde que o modelo se ajuste e os critérios tenham sido validados; não prova acurácia absoluta. |
| **Agregação conjunta** | Ajuste matemático que usa parciais de diferentes ataques, mantendo variação de escala f1/F por execução e parâmetro B comum quando apropriado. |
| **Modelo incompatível** | Dados não bem descritos pelo modelo escolhido, mesmo que os picos sejam reais. |
| **Curva instrumental** | Correções Δ por nota relativamente a um temperamento musical definido. |
| **Railsback** | Perfil típico de extensão de afinação de piano, não fórmula universal a ser copiada. |
| **Batimento** | Modulação associada à interferência de frequências próximas; diferença em Hz é um indicador, não prova auditiva em qualquer condição. |
| **Parciais 2:1, 4:2 etc.** | Ordens de dois parciais de notas diferentes usadas em critérios intervalares. |
| **Temperamento base** | Frequências canônicas do grafo histórico (A4) **ou EDO** (grau/oitava/Hz), sem correção instrumental. O cilindro é visualização, não calculadora. |
| **Δₓ**, com `x=(keyId,octave)` | Correção instrumental em cents **por tecla física e registro**; não por índice MIDI, grafia ou `soundId`. |
| **Medido** | Diretamente estimado de uma observação acústica. |
| **Inferido** | Estimado indiretamente pelo modelo, sem observação direta suficiente. |
| **Interpolado** | Estimado entre pontos medidos; exige representação de incerteza. |
| **Prévia** | Curva calculada ou editada que não modificou as referências ativas. |
| **Aplicada** | Curva validada e explicitamente escolhida como camada de correção. |
| **FFT points vs bins** | FFT de N pontos corresponde à análise de N amostras de entrada; `Δf=fs/N`. Uma FFT real com N amostras apresenta tipicamente N/2 bins positivos utilizáveis conforme a API. |
| **Zero-padding** | Acrescentar zeros para amostragem mais densa do espectro; não aumenta a informação física contida no sinal. |
| **PCM contínuo** | Sequência temporal correta de amostras, sem sobreposição arbitrária de blocos. |

---

## 18.1 Termos de temperamento e otimização acrescentados na revisão 2.2

- **`I_T(a,b)` — intervalo teórico fundamental:** diferença em cents entre as frequências **fundamentais** de `b` e `a` previstas pelo temperamento do snapshot, sem curva.
- **`t_T^harm(a,p;b,q)` — desvio harmônico histórico assinado:** comparação, em cents, entre `p·f_temp(a)` e `q·f_temp(b)`; **não** é um parâmetro de inarmonicidade.
- **`g_{x,p}` — fator espectral relativo:** relação entre a frequência prevista do parcial `p` e a fundamental-alvo da mesma nota. Pode vir de B validado ou de medição empírica apropriada; `g_{x,1}=1` e para série ideal `g_{x,p}=p`.
- **`s_{a,p;b,q}(Δ)` — desvio acústico assinado:** diferença em cents entre as frequências **de dois parciais previstos**; positivo se o da nota inferior for mais agudo. Não equivale ao intervalo em fundamentais.
- **`targetPolicy` — política do alvo:** `harmonic_temperament_signed`, `acoustic_coincidence_zero`, `manual_signed`, ou outro identificador versionado. Deve determinar o valor de `t`, não a mera escolha do par de parciais.
- **`priorityMode` — modo de prioridade:** `temperament_fidelity` ou `acoustic_optimization`; cada um determina quais restrições musicais/objetivos acústicos são usados. Nenhum modo modifica presets.
- **`Δ_b−Δ_a` — mudança efetiva de intervalo:** diferença entre correções instrumentais das notas superior e inferior; igual a `I_final−I_T`, mesmo com tabela teórica imutável.
- **Rebasear curva:** transformar correções por `(keyId,octave)` de uma base para outra **somente para teclas mapeadas explicitamente**, mantendo frequências absolutas, sem afirmar preservação da assinatura musical; distinto de reotimizar. Mudança de layout que elimina tecla bloqueia rebase automático.
- **`keyId` / `pitchId` / `soundId`:** tecla física / identidade musical / coincidência acústica no snapshot; `soundId` não substitui as duas primeiras.
- **`targetId`:** índice canônico atual da dupla `[keyId,octave]`, sempre acompanhado de snapshot/hash em arquivos externos.
- **`musicRevision` / `generationIdDSP`:** revisões de interpretação musical / geração do processamento técnico; jamais uni-las.
- **Referência EDO:** `referenceDegree`, `referenceOctave`, `referenceHz`; não é sinônimo de A4.

---

# 19. Referências e fontes de evidência

## 19.1 Materiais do próprio projeto

1. **`Roadmap.md` original, 273 linhas**, enviado em 15/11/2026. Seus objetivos, sete fases, fórmulas e critérios originais estão reproduzidos integralmente no Anexo A.
2. **`Etapa4_Limpeza_Validacao_Final_v1/index.html`**, auditado em 17/11/2026, 11.589 linhas / 707.224 bytes / SHA-256 registrado no cabeçalho: fonte de verdade para a arquitetura atual; inclui 18 presets, modelos históricos e EDO, catálogo de alvos canônicos, cilindro 2,5D, diagnóstico v2 e a separação música/DSP. O HTML de 15/11/2026 (~8.347 linhas) permanece **fonte histórica anterior**, não referência de integração vigente. A presente revisão **não alterou** nenhum dos dois HTMLs.
3. Discussões de produto consolidadas nesta especificação: botão `Ferramentas`, quatro áreas, informação progressiva, avaliação por parcial, ajuste B robusto, perfis, curvas, controles de aplicação e auditabilidade. **Revisão 2.1:** repetição livre de ataques da mesma nota, identificação automática/manual, ajuste conjunto robusto, comparação/convergência, preservação de execuções e encerramento por decisão do usuário. **Revisão 2.2:** temperamentos desiguais, duodécimas, alvos assinados por parciais, modos de fidelidade e otimização, mudanças de intervalos fundamentais, modelo físico ancorado no alvo e integridade da auditoria. O documento foi escrito para que essas decisões não dependam de novas consultas à conversa.

## 19.2 Manuais e documentação oficiais consultados

- **PianoMeter — Instructions & Support:** https://pianometer.com/support/  
  Coleta contínua de inarmonicidade, bloqueio de curva, gráfico espectral/zoom, parciais na visualização de afinação, estilos e pesos intervalares. Fonte para a análise de curvas dinâmicas e necessidade de estado aplicado e de distinguir atualizações contínuas de execuções independentes.
- **PianoMeter — FAQ:** https://pianometer.com/faq/  
  Dificuldades de notas agudas, ruído de ataque, falsos batimentos e instabilidade de picos espectrais.
- **pianoscope — Manual:** https://www.pianoscope.app/manual4/html/index.en.html  
  Medição por tecla, visualização de inarmonicidade, valores discrepantes, repetição da nota, ponderação de medidas, intervalos de afinador e apresentação de curvas.
- **TuneLab — Manual Android:** https://tunelab-world.com/TuneLabAndroidManual-3.0.pdf  
  Medição de inarmonicidade por notas isoladas, comando de repetição/média de medidas (Save,+), curvas, formas de comparação e escolha de parciais; referência para a proposta multiataque, **sem copiar seu algoritmo de agregação**.
- **Verituner — Guia rápido:** https://www.veritune.com/VeritunerForAndroidQuickStartUserGuide.pdf  
  Estados, operações profissionais, análise múltipla e organização de funções técnicas.
- **CyberTuner — Guia de início:** https://mail.cybertuner.com/pub/reyburn/rct_demo/iRCT%20Getting%20Started%20Manual%20v7.8.x.pdf  
  Modos de troca automática, correção de altura, curva e controles especializados.
- **Pesquisa sobre otimização por entropia espectral:** https://www.sciencedirect.com/science/article/pii/S0003682X20300050  
  Demonstra diversidade de objetivos científicos e necessidade de avaliar reproducibilidade e preferência musical. Não utilizar como autorização para implementar algoritmo fechado.

### 19.2.1 Precedentes documentados específicos de temperamentos desiguais (revisão 2.2)

- **TuneLab — manual Android v3.0 (setembro de 2024):** https://tunelab-world.com/TuneLabAndroidManual-3.0.pdf  
  Apresenta separadamente `Tuning Curve Offset` e `Temperament Offset` para temperamentos desiguais, além dos parciais usados na afinação. Isso documenta a coexistência de duas camadas, **não** prova que seus critérios internos adotem `t_T^harm`.
- **PianoMeter — documentação oficial:** https://pianometer.com/support/  
  Seções *Unequal Temperaments* e *Tuning Style (Interval Weights)* documentam temperamentos desiguais, estilos intervalares e pares de duodécimas 3:1/9:3. A implementação interna de preservação musical não é presumida.
- **pianoscope — manual oficial:** https://pianoscope.app/manual4/website/en/tuning-documents/temperament/index.html  
  Documenta seleção de temperamentos históricos/desiguais; manual de curvas: https://www.pianoscope.app/manual4/html/index.en.html. Não atribuir a ele o método matemático proposto neste documento sem prova.
- **Bill Bremmer, "New Bearing Plan for EBVT" (3 de junho de 2001):** https://www.moypiano.com/ptg/pianotech.php/2001-June/086958.html  
  Plano prático de temperamento desigual com oitava A3–A4 estendida do tipo 6:3. **A própria postagem ressalta que o plano não detalha como compensar a inarmonicidade**; não apresentá-la como implementação formal de metas assinadas para todas as duodécimas.
- **Simon Dixon, Matthias Mauch e Dan Tidhar, JASA 131(1), 878–887 (2012), DOI 10.1121/1.3651238:** https://pubmed.ncbi.nlm.nih.gov/22280710/  
  Pesquisa conjunta sobre estimativa de inarmonicidade e classificação de temperamentos a partir de gravações de cravo, evidência de que as grandezas interagem mas precisam ser identificadas separadamente. Não a confundir com estudo de otimização de curvas para piano.

**Limite de evidência:** os dois modos de prioridade, a política de alvo harmônico histórico `t_T^harm` e o objetivo com proteção explícita dos intervalos fundamentais são **especificações propostas para o Afinador**, ainda [A VALIDAR]; referências demonstram o problema e recursos relacionados, **não** uma comparação experimental de qualidade ou equivalência de algoritmos.

## 19.3 Relatos de comunidade (evidência qualitativa, não estatística)

- Discussão comparando PianoMeter e pianoscope, com comentários sobre intuitividade, zoom, clareza da interface e confirmação de microfone externo: https://www.reddit.com/r/pianotech/comments/1umnx0i/beginner_piano_tuner_pianoscope_or_pianometer_plus/
- Discussão sobre pianoscope, outliers e afinação auditivamente insatisfatória apesar de valores pequenos de cents: https://www.reddit.com/r/pianotech/comments/1pnoews/pianoscope_tuning_purity/
- Discussão sobre expectativas de mudança da curva PianoMeter durante coleta: https://www.reddit.com/r/pianotech/comments/1qtb5qm/question_for_those_who_use_piano_meter_on_style/

**Limitação**: comentários de usuários ilustram dificuldades possíveis, mas são amostras de conveniência; não se deve afirmar que representam a maioria dos usuários nem estabelecer precisão relativa dos softwares apenas por relatos.

## 19.4 Uso ético das referências

As referências servem para identificar demandas de interface, problemas de medição e critérios acústicos conhecidos. Não copiar obras visuais, telas, conteúdos protegidos, nomenclaturas proprietárias exclusivas, código comercial ou dados de terceiros. Implementar os métodos públicos e suas adaptações respeitando licenças, atribuição e documentação técnica.

---

# 20. Checklist executivo de completude do roadmap

Antes de iniciar uma fase, confirmar:

- [ ] Os **requisitos originais** estão preservados e as decisões posteriores estão marcadas.
- [ ] A ferramenta corrente e o estado da curva são identificados sem ambiguidades.
- [ ] Cada número exibido pode ser rastreado à medição ou à equação que o gerou.
- [ ] Os ataques de uma mesma sessão são preservados individualmente, com origem, status, parciais, versões e possibilidade de revisar inclusão/exclusão sem apagar evidência.
- [ ] O número de execuções é livre; um limite de memória é tratado com pausa e aviso explícito, sem perder registro aceito.
- [ ] A convergência não decorre apenas de três ataques, nem de número de quadros FFT, nem de um B aparentemente constante mas com ajuste físico ruim.
- [ ] Insuficiência de evidência não gera valor definitivo.
- [ ] O usuário consegue inspecionar dados gradualmente, sem abrir um painel técnico inteiro para afinar uma nota.
- [ ] Não houve alteração silenciosa de A4, cilindro acústico de quintas, temperamento histórico ou configuração dos algoritmos atuais.
- [ ] A curva instrumental exige confirmação e pode ser desativada com retorno exato à referência teórica.
- [ ] Para temperamentos desiguais, a duodécima 3:1/6:2/9:3 tem **alvo assinado próprio**, sem pureza zero presumida; o modo acústico é escolha deliberada.
- [ ] O gráfico mostra separadamente intervalo entre fundamentais, diferença assinada de parciais e magnitude em Hz, bem como `Δ_b−Δ_a` em comparação com o preset, sem alegar fidelidade literal quando há mudança.
- [ ] A previsão usa `f_temp·2^(Δ/1200)` e razões espectrais `g`; não herda por engano o desafino original da medição.
- [ ] O snapshot/hash de A4, quintas e tabela é imutável por curva; troca de temperamento bloqueia reutilização silenciosa de Δ e exige recálculo explícito.
- [ ] Os perfis registram tipo de corda, data, origem, versões e qualidade.
- [ ] Dados acústicos e histórico têm esquema versionado, política de importação segura e exportação local.
- [ ] O diagnóstico atual de 20 segundos não foi confundido com o armazenamento histórico de perfis.
- [ ] O desempenho do afinador antigo não piora enquanto a nova ferramenta está inativa.
- [ ] Testes sintéticos, reais, matemáticos, de layout, persistência e privacidade estão documentados com limites claros.
- [ ] README/Ajuda/roadmap foram atualizados conjuntamente.

**Decisão orientadora final (revisão 2.2):** não queremos apenas um afinador que “acerta” uma frequência. Queremos um ambiente em que o usuário compreenda **o que foi realmente observado no instrumento, quão confiável é cada parcela da análise, por que determinada curva foi proposta e quais compromissos ela introduz**. Ao trabalhar com duodécimas e outros intervalos, o objetivo não é impor pureza acústica universal, mas permitir **conservar, negociar ou alterar deliberadamente** o padrão de um temperamento histórico, sempre com as consequências matemáticas expostas e a referência musical original preservada e reversível.

---

---

# 21. Auditoria pré-entrega da revisão 3.0 — resultado documental

Esta auditoria é de **consistência entre especificação 2.2 e HTML atual**, não é validação de execução das funcionalidades futuras. O HTML foi somente lido; **não foi alterado**.

| Verificação | Constatação no HTML | Correção na revisão 3.0 |
|---|---|---|
| Fonte musical única | `CatalogoTemperamentos` + modelos + `CatalogoAlvosCanonicos`; `estadoMusicalAtual` mínimo | Curvas/medidas consomem `porTecla`, não tabelas paralelas |
| MIDI legado | Ausente dos caminhos operacionais do modelo musical | Removidos campos MIDI de requisitos, fórmulas e JSON prospectivos |
| Identidades | `keyId`, `pitchId`, `soundId`, `octave`, `targetId` | Duas teclas enarmônicas podem ter Δ independentes |
| Layout histórico | 12/13/14 teclas, offsets, quinta compensatória e lobo | Cobertura expressa, sem confundir ciclo fechado com cadeia aberta |
| EDO | 13/14-EDO, referência por grau/oitava/Hz, órbitas | Contratos sem A4 obrigatório e sem nomes cromáticos inventados |
| Cilindro | SVG 2,5D, lobo direto, não círculo bidimensional antigo | Seções UI/documentação atualizadas |
| Transições musicais/DSP | `musicRevision` separado de `generationIdDSP`, rollback flag desativado | Ativação de curva não reinicia pYIN/SWIPE'; geração técnica segue distinta |
| FFT/PCM | FFT visual e Worker existentes; AudioWorklet PCM do diagnóstico WAV opt-in | Futuro analisador precisa criar captura contínua compartilhada, não alegar que já está pronta |
| Perfil técnico | `afinador-perfil-tecnico-v1` no localStorage | Preservado |
| Biblioteca musical | `afinador-biblioteca-musical-v1`, JSON `afinador-tuning-v1` | Preservada e separada dos futuros perfis acústicos IndexedDB |
| Diagnóstico | ZIP de 20 s, `diagnosticSchemaVersion:2` e `fixedTarget` | Preservado; nova auditoria acústica versionada separadamente |
| Alvos intervalares | 2.2 já distingue `t_T^harm`, `s`, `I_final`, `Δ_b−Δ_a` | Matemática preservada, índices migrados para alvos por tecla |
| Curva e suavidade | 2.2 usava vizinhança implícita de `m+1` MIDI | Substituída pela **ordem física explícita** em perfil/layout |
| Exemplos JSON | 2.2 continha `midiNote`, `lowerMidi`, faixas MIDI | Exemplos completos por teclas e versões de esquema **ainda não implementado** |
| Auditabilidade | Sessões/execuções multiataque e dados originais | Inalterados; vinculados a snapshot e política de confirmação de nota |
| Testes | 2.2 não exercitava identidade não cromática end-to-end | 29 casos `INH-ARCH-*` e gates por fase adicionados |

**Critério de aceite do roadmap 3.0:** nenhum fluxo normativo usa MIDI como identidade; nenhuma curva toma `soundId` como chave única; nenhum modo de afinador é reescrito; todas as dependências futuras são marcadas como futuras; as equações de inarmonicidade/histórico são preservadas; a separação de estado musical, DSP e curva é explícita; os exemplos JSON são válidos e consistentes. As limitações físicas permanecem pendentes até implementação.

**Documentação preservada:** o Anexo A a seguir contém o roadmap anterior original, **não uma instrução de implementação contemporânea**. Suas referências históricas a MIDI devem ser lidas como legado e não prevalecem sobre as seções 2, 9, 10, 12, 13 e 14 desta revisão.

# Anexo A — Roadmap original recebido (preservado integralmente)

> Anexo para comparação histórica. A especificação ampliada acima orienta a implementação; em caso de conflito, os requisitos originais explicitamente preservados e as regras **[DEFINIDO]** prevalecem sobre recomendações, e questões não decididas devem ser validadas, não preenchidas silenciosamente.

## Roadmap — Análise Acústica e Afinação Personalizada

O desenvolvimento futuro do afinador poderá incluir ferramentas de análise acústica destinadas a investigar a relação entre **temperamento musical, inarmonicidade, propriedades físicas dos instrumentos e afinação percebida**.

O objetivo de longo prazo é permitir a construção de **perfis acústicos e curvas de afinação personalizadas para instrumentos individuais**, considerando seus parciais reais, sem comprometer o funcionamento dos temperamentos históricos existentes.

As funcionalidades serão desenvolvidas progressivamente, com validação matemática, análise de sinais sintéticos e testes com instrumentos reais.

### Fase 1 — Analisador de parciais e inarmonicidade

**Prioridade: Alta | Complexidade: Média–Alta**

Implementar um módulo independente para analisar a composição espectral de notas sustentadas.

**Funcionalidades previstas:**

- Identificação automática dos principais parciais presentes no som.
- Medição individual da frequência e intensidade de cada parcial.
- Comparação com a série harmônica ideal.
- Cálculo dos desvios dos parciais em cents.
- Identificação de padrões de inarmonicidade.
- Visualização simultânea dos parciais teóricos e medidos.
- Indicador de confiança para cada parcial identificado.
- Possibilidade de selecionar manualmente uma nota para análise.

**Parâmetros de medição:**

| Parâmetro | Descrição |
|---|---|
| Frequência fundamental | Estimativa da frequência do primeiro parcial |
| Ordem do parcial | Identificação de cada componente: 1º, 2º, 3º etc. |
| Frequência medida | Frequência real do parcial, em Hz |
| Frequência ideal | Múltiplo inteiro da fundamental |
| Desvio | Diferença entre a frequência medida e a ideal, em cents |
| Amplitude | Intensidade relativa de cada componente |
| Confiança | Qualidade da identificação espectral |
| Duração da análise | Intervalo utilizado para estimar as frequências |

A análise deverá utilizar janelas temporais independentes da FFT empregada na visualização em tempo real, permitindo maior resolução espectral quando necessário.

**Critério de conclusão:** identificar e medir parciais de notas isoladas com estabilidade e distinguir componentes reais de ruídos ou interferências.

---

### Fase 2 — Estimativa do coeficiente de inarmonicidade

**Prioridade: Alta | Complexidade: Alta**

Implementar a estimação do coeficiente de inarmonicidade \(B\) para instrumentos cujos parciais possam ser adequadamente descritos pelo modelo físico de cordas rígidas.

O modelo utilizado será:

\[
f_n=nf_1\sqrt{\frac{1+Bn^2}{1+B}}
\]

Onde:

- \(f_n\): frequência do parcial de ordem \(n\);
- \(f_1\): frequência do primeiro parcial;
- \(B\): coeficiente de inarmonicidade.

**Funcionalidades previstas:**

- Estimativa automática do coeficiente \(B\).
- Ajuste matemático do modelo aos parciais medidos.
- Análise do erro residual do ajuste.
- Identificação de parciais discrepantes.
- Estimativa da confiabilidade do coeficiente.
- Comparação da distribuição medida com a curva teórica calculada.
- Armazenamento dos resultados por nota e por instrumento.

**Parâmetros adicionais:**

| Parâmetro | Descrição |
|---|---|
| Coeficiente B | Inarmonicidade estimada |
| Parciais utilizados | Quantidade e ordens dos componentes considerados |
| Resíduo do ajuste | Diferença entre frequências previstas e medidas |
| Qualidade do modelo | Grau de compatibilidade entre os dados e o modelo físico |
| Incerteza | Estimativa da confiabilidade de B |
| Estabilidade temporal | Variação das medições durante a sustentação da nota |

A estimativa deverá utilizar métodos de ajuste robustos, evitando que componentes espúrios comprometam os resultados.

**Critério de conclusão:** recuperar coeficientes conhecidos em sinais sintéticos e demonstrar repetibilidade em medições de cordas reais.

---

### Fase 3 — Perfis acústicos individuais

**Prioridade: Alta | Complexidade: Média–Alta**

Criar um sistema para registrar características acústicas de instrumentos específicos.

Cada instrumento poderá possuir um perfil independente, contendo as medições de suas notas.

**Funcionalidades previstas:**

- Criação e identificação de perfis por instrumento.
- Registro individual das notas analisadas.
- Armazenamento dos coeficientes de inarmonicidade.
- Histórico das medições.
- Comparação entre medições anteriores e atuais.
- Exportação e importação de perfis.
- Registro das condições e da qualidade das medições.

**Dados previstos por nota:**

| Campo | Informação |
|---|---|
| Nota | Identificação científica e oitava |
| Frequência | Frequência fundamental medida |
| Parciais | Frequências e intensidades identificadas |
| Coeficiente B | Inarmonicidade estimada, quando aplicável |
| Confiança | Qualidade da medição |
| Data | Momento da análise |
| Observações | Informações adicionais sobre a medição |

Para instrumentos como o piano, o sistema poderá armazenar informações para as 88 teclas.

Os perfis deverão distinguir medições individuais de cordas, grupos de cordas em uníssono e notas completas do instrumento.

**Critério de conclusão:** salvar, recuperar e comparar perfis sem perda de informações, mantendo compatibilidade com futuras versões do aplicativo.

---

### Fase 4 — Construção de curvas de afinação personalizadas

**Prioridade: Alta | Complexidade: Muito alta**

Desenvolver um sistema capaz de propor curvas de afinação com base nas características acústicas medidas de cada instrumento.

O objetivo principal será investigar e, quando aplicável, compensar os efeitos da inarmonicidade na afinação de intervalos.

**Funcionalidades previstas:**

- Construção de curvas de afinação por nota e oitava.
- Representação dos desvios em cents em relação ao temperamento de referência.
- Comparação com curvas de afinação teóricas.
- Análise da extensão das oitavas.
- Visualização de tendências semelhantes à curva de Railsback.
- Ajustes manuais de pontos da curva.
- Interpolação entre notas medidas, com indicação de incerteza.
- Comparação entre curvas de diferentes instrumentos.
- Aplicação opcional da curva personalizada ao afinador.

**Parâmetros da curva:**

| Parâmetro | Descrição |
|---|---|
| Temperamento base | Sistema musical utilizado como referência |
| Nota de referência | Nota utilizada para ancorar a afinação |
| Frequência de referência | Frequência associada à nota de ancoragem |
| Desvio por nota | Correção individual em cents |
| Inarmonicidade | Coeficiente B medido para cada corda |
| Critério acústico | Relações entre parciais utilizadas na otimização |
| Peso dos parciais | Importância atribuída aos componentes analisados |
| Suavidade | Controle da regularidade da curva |
| Confiança | Qualidade das medições que fundamentam cada correção |

**Princípio fundamental:** o coeficiente de inarmonicidade não determina sozinho uma curva de afinação ideal.

A construção da curva deverá considerar critérios acústicos definidos, como a coincidência ou a redução dos batimentos entre determinados pares de parciais de notas diferentes.

Também deverá ser possível comparar diferentes critérios e preservar ajustes realizados manualmente pelo usuário.

**Critério de conclusão:** gerar curvas reproduzíveis a partir de dados medidos e demonstrar sua utilidade por meio de comparações acústicas e auditivas com instrumentos reais.

---

### Fase 5 — Integração entre temperamentos históricos e curvas instrumentais

**Prioridade: Alta | Complexidade: Muito alta**

Implementar um sistema de afinação em camadas.

A frequência final de referência será determinada por dois elementos independentes:

1. **Temperamento musical:** define as relações entre as classes de notas por meio do círculo de quintas.
2. **Correção instrumental:** acrescenta ajustes individuais em cents, considerando características acústicas do instrumento.

A relação poderá ser representada por:

\[
f_{\text{final}}(n)=f_{\text{temperamento}}(n)\cdot2^{\Delta_n/1200}
\]

Onde \(\Delta_n\) corresponde à correção instrumental da nota MIDI \(n\), em cents.

**Funcionalidades previstas:**

- Aplicação de curvas personalizadas a diferentes temperamentos.
- Preservação dos ajustes originais do círculo de quintas.
- Ativação e desativação independente das correções instrumentais.
- Comparação entre afinação teórica e instrumental.
- Visualização dos desvios introduzidos pela curva.
- Utilização das novas frequências no modo Nota fixa.
- Aplicação opcional das correções ao emissor de notas.
- Preservação das frequências teóricas quando a correção estiver desativada.

A implementação deverá preservar a distinção entre **temperamento, inarmonicidade e afinação estendida**.

**Critério de conclusão:** permitir alternar entre referências teóricas e personalizadas sem modificar permanentemente o temperamento original.

---

### Fase 6 — Modelos acústicos específicos por instrumento

**Prioridade: Média | Complexidade: Alta–Muito alta**

Ampliar o sistema para considerar as características físicas de diferentes famílias de instrumentos.

**Possíveis perfis:**

| Instrumento | Análise prevista |
|---|---|
| Piano | Inarmonicidade de cordas, afinação estendida e curva individual por tecla |
| Cravo | Análise de parciais, inarmonicidade e relações com temperamentos históricos |
| Violão | Análise espectral e inarmonicidade das cordas |
| Guitarra | Análise por corda, posição e região de frequência |
| Instrumentos de sopro | Análise de parciais e características das ressonâncias |
| Sinos e percussão | Análise de modos parciais potencialmente não harmônicos |

O coeficiente \(B\) será utilizado apenas quando o modelo de corda rígida for fisicamente adequado.

Para outros instrumentos, deverão ser considerados modelos específicos, evitando aplicar indiscriminadamente uma mesma descrição matemática.

---

### Fase 7 — Validação acústica e aperfeiçoamento

**Prioridade: Contínua**

Todas as etapas deverão ser acompanhadas por testes matemáticos, computacionais e acústicos.

**Testes previstos:**

- Sinais sintéticos com coeficientes de inarmonicidade conhecidos.
- Fundamentais ausentes ou pouco intensas.
- Harmônicos predominantes.
- Ruído ambiente e interferência elétrica.
- Cordas com diferentes graus de rigidez.
- Notas graves e agudas.
- Sons com vibrato ou variações de frequência.
- Decaimento natural de cordas.
- Múltiplas cordas produzindo a mesma nota.
- Comparação de medições com instrumentos e equipamentos de referência.
- Testes de desempenho em computadores e dispositivos móveis.

As medições deverão apresentar indicadores de confiança e, quando possível, estimativas de incerteza.

O sistema não deverá gerar correções automáticas quando os dados acústicos forem insuficientes ou incompatíveis com o modelo utilizado.

---

### Objetivo de longo prazo

Desenvolver um sistema capaz de:

**Medir → Analisar → Caracterizar → Construir uma curva → Afinar**

Dessa forma, o programa poderá evoluir de um afinador cromático com temperamentos históricos para uma ferramenta de **análise acústica e afinação personalizada**, capaz de relacionar modelos matemáticos de temperamento às propriedades físicas de instrumentos individuais.

O princípio central será preservar a independência entre:

- **Temperamento:** organização teórica das relações intervalares.
- **Afinação:** comparação entre frequências produzidas e referências.
- **Inarmonicidade:** distribuição real dos parciais do instrumento.
- **Curva instrumental:** conjunto de correções de afinação escolhido ou calculado para um instrumento específico.

A implementação dessas ferramentas deverá ocorrer de forma modular, sem comprometer o funcionamento atual do afinador FFT + YIN.
