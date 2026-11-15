# Roadmap — Análise Acústica, Inarmonicidade e Afinação Personalizada

> **Documento-mestre de produto, experiência de usuário, arquitetura e validação**  
> **Edição ampliada:** 15 de novembro de 2026  
> **Destino de implementação:** `index.html` autocontido do projeto Afinador  
> **Estado:** especificação para desenvolvimento futuro; **não significa que as novas ferramentas já estejam implementadas**.  
> **Fonte primária:** `Roadmap.md` de 273 linhas enviado pelo responsável pelo projeto, complementado pelo `index.html` enviado na mesma conversa, pelas decisões acumuladas de projeto e pela pesquisa comparativa de ferramentas de afinação.  
> **Versão deste documento:** 2.0 (especificação ampliada; não é a versão do programa).

## Como usar este documento

Este arquivo deve ser **suficiente, por si só**, para recuperar a visão do projeto, as decisões de interface, a matemática, os fluxos de uso, as escolhas de arquitetura, os critérios de qualidade e o planejamento de implantação das futuras funções. Não é necessário ter acesso à conversa que originou o documento. Foi preservada a estrutura de **sete fases** do roadmap original; o texto original integral está no **Anexo A**, apenas para rastreabilidade.

### Convenções de decisão

- **[DEFINIDO]** — requisito ou intenção explicitamente estabelecido pelo responsável pelo projeto ou pelo roadmap original. Deve ser preservado.
- **[RECOMENDADO]** — proposta de implementação técnica/UX resultante da análise. É suficientemente específica para orientar o desenvolvimento, mas pode ser revista mediante testes.
- **[A VALIDAR]** — método, limiar, desempenho, parâmetro numérico ou decisão que exige experimentos antes de se tornar um padrão definitivo.
- **[FUTURO]** — funcionalidade prevista, sem autorização implícita para implementá-la na fase atual.
- **[EXISTENTE]** — comportamento identificado no `index.html` enviado. Não deve ser confundido com funcionalidade futura.

**Regra de interpretação:** uma proposta [RECOMENDADO] não pode revogar silenciosamente um requisito [DEFINIDO]. Uma referência a outro produto identifica uma ideia, um problema ou uma boa prática; não autoriza copiar aparência, ícones proprietários, códigos, textos ou algoritmos fechados.

---

# 1. Visão e princípios inegociáveis

## 1.1 Objetivo geral [DEFINIDO]

Evoluir o afinador cromático com temperamentos históricos para um sistema de **análise acústica e afinação individualizada por instrumento**, capaz de:

**Medir → Analisar → Caracterizar → Construir uma curva → Afinar.**

A experiência deve atender ao músico interessado em uma medição clara e ao usuário tecnicamente exigente que precisa inspecionar parciais, estimar inarmonicidade, avaliar uma curva e compreender as razões matemáticas de cada resultado.

## 1.2 Quatro conceitos que jamais devem ser confundidos [DEFINIDO]

1. **Temperamento musical:** conjunto de relações intervalares teóricas, calculadas a partir dos presets e dos ajustes do círculo de quintas.
2. **Afinação:** comparação do som produzido com uma referência de frequência.
3. **Inarmonicidade:** distribuição observada dos parciais reais de uma nota; depende do instrumento, da corda e das condições de medição.
4. **Curva instrumental:** correções por nota, calculadas ou escolhidas para um instrumento e um objetivo acústico específico.

O valor de inarmonicidade **não é**, isoladamente, um desvio de afinação, tampouco define a única curva ideal. Um coeficiente físico `B` não substitui um temperamento musical.

## 1.3 Regras de projeto

- **Preservar integralmente o afinador existente**: detectores, círculo de quintas, notações, presets, cálculos musicais, emissores e diagnóstico não serão reescritos para abrir espaço às ferramentas futuras. Novos módulos serão desenvolvidos em partes separadas, mesmo se o HTML continuar autocontido.
- **Informação progressiva**: mostrar o essencial primeiro e permitir aprofundamento por interação explícita. Nem interface opaca que oculta dados, nem painel visual poluído por dezenas de números.
- **Transparência matemática**: o usuário deve poder responder: *o que foi medido? por que foi aceito? como foi calculado? o que mudou?*
- **Confiabilidade acima de aparente precisão**: nenhuma estimativa definitiva quando o sinal, a atribuição de parciais ou o modelo são inadequados. Em vez de `0,00042` sem ressalvas, exibir `medição inconclusiva` quando necessário.
- **Resultados reproduzíveis**: com o mesmo conjunto de dados, parâmetros e versão de algoritmo, obter o mesmo resultado dentro de tolerâncias definidas; diferenciar variação do áudio real de não determinismo do software.
- **Aplicação reversível**: medições podem criar *prévia* de curva, mas não alteram automaticamente as frequências ativas do afinador nem reescrevem as quintas históricas.
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
- Temperamentos históricos, A4 de referência (**415,3 Hz** no padrão do arquivo enviado), círculo de quintas editável em comas, tabelas de relações/intervalos e emissor de notas conforme a afinação teórica ativa.
- Barra superior com **Ativar microfone**, **Configurações**, **Ajuda** e botão circular de tema imediatamente à direita de Ajuda.
- Temas **Claro — Marfim e carvão** (padrão, fundo `#EEECE7`) e **Escuro — Grafite monocromático** (`#101214` como fundo). O círculo do tema mostra a cor do **tema de destino**, não o tema atual.
- Configurações técnicas expansíveis de Geral, YIN + FFT, pYIN, SWIPE’ e Diagnóstico. Efeitos imediatos durante a sessão; persistência somente com **Salvar configurações**; **Restaurar padrões** não apaga A4, temperamento ou quintas.
- Ajuda rápida seguida de Ajuda avançada, recolhida por padrão.
- Monitor de diagnóstico opcional e compacto na ordem **Espectro FFT → Monitor (quando ativo) → Círculo de quintas**, com captura de **20 s**, JSON/ZIP e áudio WAV **opcional**. O WAV usa aquisição de amostras contínuas com AudioWorklet quando disponível; exportações locais.
- Processamento pesado em **Dedicated Worker**; FFT PFFFT via WebAssembly SIMD/escalar quando possível e fallback nativo onde suportado. SWIPE’ tem dependência própria do motor adequado.
- Barra inferior fixa de A4 e temperamento; tabelas e emissor ficam em seções expansíveis.

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
| Diagnóstico | **Oculto** por padrão; captura **20 s**; áudio WAV opt-in | Permanece entre FFT e círculo de quintas. |
| Tema | **Claro** (`#EEECE7`) padrão; escuro (`#101214`) | Alternância em botão circular, fora de Configurações. |
| Referência musical | **A4 415,3 Hz** e temperamento histórico selecionado no aplicativo | Referência teórica distinta do f1 acústico medido. |

**Regra de compatibilidade:** os parâmetros existentes são da detecção/visualização do Afinador. Os parâmetros do futuro Analisador de parciais serão mantidos separadamente, com nomes inequívocos e eventual perfil avançado próprio. Não reutilizar `pontosFFT` como se controlasse automaticamente a resolução física de todas as ferramentas.

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
5. **Desvio numérico pequeno, resultado sonoro ruim**: a curva precisa evidenciar os compromissos entre oitavas, duodécimas, quintas e outros intervalos. Zero cent em relação a uma curva não prova que ela seja adequada.
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
| **Afinador** | Já existe; padrão | Fase 5 (integração futura) | Visor atual, cents, FFT, diagnóstico, círculo de quintas, tabelas, emissor. |
| **Parciais e inarmonicidade** | Nova | Fases 1–2 | Captura de nota sustentada, espectro detalhado, parciais, confiança, modelo B e resíduos. |
| **Perfis instrumentais** | Nova | Fases 3 e 6 | Instrumentos, medições por nota/corda, histórico, comparação, importação/exportação. |
| **Curvas de afinação** | Nova | Fases 4–5 | Construção, critérios acústicos, edição e comparação de curvas, prévia e aplicação confirmada. |

**Fase 7 (validação)** é transversal e não requer uma tela pública. **Fase 6 (modelos específicos)** amplia os seletores e análises existentes, sem criar automaticamente outra área.

## 4.3 O que aparece em cada área

- **Afinador:** mantém integralmente o layout e os algoritmos; um futuro indicador `Correção instrumental: desligada/ativada` aparece somente quando existir curva aplicável e validada.
- **Parciais:** substitui o corpo de medição pelo fluxo de captura/inspeção de espectro. O círculo de quintas **não precisa ficar presente**, mas o temperamento base segue acessível por referência quando aplicável.
- **Perfis:** exibe seleção de instrumento, cobertura de notas, repetições, comparação de medições, e gerenciamento de arquivos locais.
- **Curvas:** exibe gráfico de correções por nota, curva anterior, proposta, intervalos afetados e estados `Rascunho / Prévia / Aplicada`.

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
| Parciais | `Medir`, `Congelar`, `Limpar`, `Salvar medição` | 4 contextuais |
| Perfis | `Novo`, `Salvar`, `Importar`, `Exportar`, `Comparar` | 5 contextuais |
| Curvas | `Gerar prévia`, `Editar`, `Comparar`, `Aplicar`, `Exportar` | 5 contextuais |
| Afinador futuro | `Correção instrumental` | 1 interruptor contextual |

Total estimado: **um novo botão permanentemente visível**; aproximadamente **14 ações contextuais**, mais um interruptor futuro. Além disso existirão seletores, menus e ações secundárias em painéis de detalhes; **não** há obrigação de mostrar 14 botões simultaneamente. Nomenclaturas e contagem são orientações de UX, ajustáveis nos testes de usabilidade.

---

# 5. Informação progressiva — política obrigatória de interface

Este princípio é uma das decisões centrais do projeto.

## 5.1 Camadas de apresentação

**Camada 0 — Orientação imediata**: nome da ferramenta, estado da captura, nota esperada, próxima ação simples. Não exibir um resultado impreciso como definitivo.

**Camada 1 — Resultado essencial (padrão)**: nota, frequência, quantidade de parciais confiáveis, status de qualidade, eventualmente B com ressalva. Mensagens como `Aguardando sustentação`, `Medindo`, `Pronto para revisar` ou `Dados insuficientes`.

**Camada 2 — Inspeção por toque**: abrir um parcial no espectro ou tabela. Mostrar frequência real/ideal, desvio, amplitude, janela de medição, estabilidade e status `aceito/candidato/rejeitado`.

**Camada 3 — Detalhes matemáticos**: fórmula, modelo, B, parâmetros, resíduos, pares de parciais e pesos do ajuste; indicação de pontos removidos, versões de algoritmos e critérios de confiança.

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

## 6.1 Missão [DEFINIDO]

Identificar os principais parciais de **uma nota sustentada**, medir suas frequências e amplitudes, compará-los com a série harmônica ideal, expressar desvios em cents, estimar sua confiabilidade e permitir inspeção direta da evidência espectral. A primeira fase **não precisa determinar um B conclusivo**, nem propor automaticamente curva instrumental.

**Critério original de conclusão:** identificar e medir parciais de notas isoladas com estabilidade e distinguir componentes reais de ruídos/interferências.

## 6.2 Tela inicial da ferramenta [RECOMENDADO]

```text
Parciais e inarmonicidade          [Ajuda contextual]
Instrumento: [Piano ▾]  Fonte: [Microfone / descrição disponível]
Nota: [Automática | Manual]  [Lá3 ▾]  Tipo: [Corda isolada ▾]

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
- Controles primários: **Medir**, **Congelar**, **Limpar**, **Salvar medição**. `Salvar` só quando o usuário validou uma sessão ou aceitou explicitamente uma medição marcada como problemática; não transformar `Limpar` em exclusão irreversível de dados já salvos.
- Opção **Repetir esta nota**; opção de excluir/recuperar um parcial da **candidatura ao ajuste** sem apagar a medição original.
- Opção `Nota automática / Seleção manual`, inclusive A4/temperamento em contexto apenas como referência musical, não como valor imposto ao f1 real medido.
- Indicação de microfone, sample rate real, processamento de captura (quando a API expõe), possíveis filtros de sistema e ausência de informações do hardware que o navegador não fornece.

## 6.4 Fluxo guiado e fluxo de inspeção

**Percurso guiado (padrão):**

1. Selecionar instrumento e condição `corda isolada / uníssono / nota completa`. Se a análise de B por corda for pretendida, recomendar isolar uma corda.
2. Selecionar nota manualmente ou permitir reconhecimento automático (com confirmação da identidade detectada).
3. Tocar `Medir`; informar que é necessária uma nota sustentada.
4. Detectar ataque e iniciar a janela estável, desprezando ou segregando o transiente inicial quando ele comprometer a análise.
5. Acumular janelas e mostrar progresso verdadeiro em segundos e quantidade de quadros úteis; pausa/repetição se necessário.
6. Congelar ou terminar automaticamente **somente quando critérios de qualidade comprovados forem atingidos**. Não declarar `Pronto` apenas porque venceu um temporizador.
7. Mostrar resumo dos parciais; marcar os rejeitados e as razões; permitir inspecionar antes de salvar.
8. Se o usuário aceitar, salvar no perfil ativo (Fase 3); antes disso, permitir exportação avulsa em JSON versionado.
9. Se nenhum parcial for confiável, oferecer `Repetir` e orientação específica, não uma medida vazia com aparência de sucesso.

**Inspeção avançada:** o usuário escolhe duração, número máximo de parciais, região frequencial, comportamento de seleção de pico, métodos de refinamento e limites de confiança **apenas quando tais parâmetros tiverem sido validados**. A configuração por padrão continua conservadora.

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
| `midiNote`, `scientificNote`, `helmholtzNote` | Identificação musical, sem substituir o dado acústico |
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
10. **Exportação auditável**: preservar picos candidatos, parciais aceitos e rejeitados, motivo de rejeição, parâmetros do método e estatísticas resumidas. Salvar FFT inteira somente de forma controlada se um modo de depuração futuro justificar; WAV é mais versátil para reprocessamento.

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
- Captura/nota: `midiNote` (identidade objetiva), notações científica/Helmholtz de apresentação, `stringIndex` ou grupo, tratamento de surdina, condição de medição.
- Distinguir pelo menos três tipos: **corda individual**, **grupo de cordas em uníssono**, **nota completa**; observações nesses tipos **não são intercambiáveis**.
- Versões de captação/analisador/modelo, fontes de áudio e informações de qualidade, para possibilitar auditoria após atualizações.
- Uma nota poderá ter **várias medições independentes**; não sobrescrever automaticamente a anterior.

## 8.4 Estrutura e semântica do histórico

1. Toda medição recebe ID e timestamp; o usuário pode editar observações sem reescrever o conteúdo acústico histórico.
2. Valores **medidos**, **inferidos pelo modelo**, **estimados por interpolação** e **alterados manualmente** devem usar campos/estados distintos.
3. Repetições da mesma nota podem produzir média/mediana robusta, mas cada medição permanece acessível e auditável.
4. O usuário pode marcar uma medição como `descartada da modelagem` sem apagá-la; exclusão física de dados exige confirmação.
5. Medições antigas com algoritmo anterior não são automaticamente reprocessadas; somente quando houver áudio local apropriado e consentimento.
6. A exportação preserva o histórico de alterações e informações suficientes para reconstruir B/curvas sem depender da interface.
7. Ao importar, verificar esquema, valores finitos, tamanho, relação dos IDs e possíveis colisões; não executar código contido no JSON.

## 8.5 Armazenamento local [RECOMENDADO]

- **IndexedDB** para perfis, medições, resultados intermediários e versões de curvas: adequado a conjuntos estruturados maiores que configurações simples.
- Manter o **`localStorage` atual exclusivamente para preferências técnicas pequenas**, respeitando o comportamento `Salvar configurações / Restaurar padrões`.
- Arquivos de áudio opcionais podem ter tamanho maior; oferecer política de retenção e armazenamento separada, limitar quota e informar claramente o espaço ocupado.
- Mudanças de versão do esquema exigem migrações explícitas e testes de ida/volta de exportação.
- Exportar/importar perfil em JSON versionado, com opção de arquivo compacto (ZIP) contendo áudio somente mediante escolha explícita do usuário.
- Dados não são enviados para servidores. Alertar que limpar dados do navegador ou trocar de aparelho pode apagar perfis não exportados.
- Em navegação privada, armazenamento restrito ou `file://`, detectar ausência de persistência e oferecer exportação, sem informar falsamente `Salvo`.
- Recuperação após falha e backup: gravações transacionais com commit atômico; impedir perfil parcialmente atualizado.

## 8.6 Interface comparativa

- Comparação **mesma nota, mesmo tipo de corda**: diferença em f1, B, amplitudes, estabilidade e qualidade entre duas datas.
- Se tipos diferirem, mostrar aviso `Corda isolada versus uníssono: comparação física limitada`.
- No mapa do piano, distinguir notas não medidas, medidas confiáveis, repetição recomendada e dados incompatíveis com o modelo.
- Ordenar por faixa, data, qualidade e notas críticas (por exemplo, perto da transição grave/tenor).
- Permitir abrir o espectro original a partir do ponto `B` do histórico.
- Mostrar quanto mudou e **por quê** (mais parciais, outra janela, mudança de microfone, nova versão do algoritmo, diferença real da corda).

## 8.7 Critérios de aceitação da Fase 3

- [ ] Criar, salvar, reabrir, renomear, duplicar, importar, exportar e excluir perfil com confirmação.
- [ ] Preservar todas as notas e repetições, sem alterar ordem dos parciais, valores e tipos de captura.
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

Construir curvas por nota com correção em cents relativamente a um **temperamento de referência explícito**, considerando medições de parciais, propriedades do instrumento e **critérios acústicos escolhidos** (por exemplo, compromissos entre oitavas e outros intervalos). Possibilitar comparação, interpolação com incerteza, ajustes manuais e aplicação opcional.

**Princípio absoluto:** `B` não determina sozinho uma curva ideal; não existe um único conjunto universal de correções para todo instrumento.

## 9.2 Tela de Curvas [RECOMENDADO]

```text
Curvas de afinação       Perfil: [Piano de estudo ▾]
Temperamento base: [Pitagórico ▾]  A4: [415,3 Hz]
Curva ativa: [Teórica (sem correção)]

[Gráfico: correção Δ_n em cents × nota MIDI]
    • linha teórica (0 em relação ao temperamento selecionado)
    • curva anterior aplicada (se houver)
    • prévia calculada, com intervalos de incerteza
    • pontos medidos / interpolados / editados pelo usuário

[Critérios acústicos ▾] [Pesos dos intervalos ▾]
[Gerar prévia] [Comparar] [Editar pontos] [Aplicar] [Exportar]
Estado: PRÉVIA — NÃO APLICADA

Nota selecionada: A4
Teórica: 415,300 Hz | Proposta: 415,300 Hz | Δ: 0,0 c
Informação: 6 parciais, 3 medições, incerteza em revisão

[Por que esta correção?] [Quais intervalos mudam?]
```

## 9.3 Três estados obrigatórios da curva

1. **Medindo**: novas medições entram no perfil; um cálculo experimental pode ocorrer em segundo plano, mas a **curva aplicada não muda**.
2. **Prévia**: o sistema apresenta uma nova curva com ID/versão e diff para a curva aplicada. Nenhum valor de referência do Afinador muda enquanto estiver em prévia.
3. **Aplicada**: após confirmação explícita, a curva é congelada em versão identificável e passa a poder ser usada pelo Afinador. Alterações posteriores geram nova prévia, nunca atualização silenciosa.

**[RECOMENDADO]** Acrescentar `Rascunho` para edições manuais ainda não resolvidas. Uma prévia válida pode ser descartada sem afetar a anterior. A qualquer instante: `Desativar correção` retorna às referências do temperamento base.

## 9.4 Camadas de informação no gráfico

- Eixo horizontal: nota MIDI, com nomes científicos/Helmholtz quando couber; para piano, A0–C8.
- Eixo vertical: **cents relativos ao temperamento base**, não necessariamente relativos ao igual temperamento. O rótulo deve nomear a referência usada.
- Linha de referência `0` = temperamento base; linha da curva aplicada = versão atual; linha de prévia = proposta.
- Pontos identificados por origem: `medidos`, `estimados por modelo`, `interpolados`, `manuais`, `sem dados`; incerteza quando validada.
- Tooltips/seleção mostram Hz teórico, Hz proposto, Δcents, origem do ajuste, critérios usados e versões.
- Permitir marcar quebra de escala ou mudança de material/categoria de corda em piano; suavização forte não deve apagar automaticamente uma irregularidade física repetível.
- Comparar duas curvas por diferenças por nota, RMS/mediana dessas diferenças, extremos e listas dos intervalos mais afetados; essas estatísticas não são critérios únicos de qualidade acústica.

## 9.5 Critérios acústicos e pesos

Exemplos de pares de parciais que podem aproximar frequências em intervalos:

| Relação entre notas | Parciais possíveis a comparar | Observação |
|---|---|---|
| Oitava | 2:1, 4:2, 6:3, 8:4, 10:5 | Os melhores compromissos dependem do registro e da intensidade de cada parcial. |
| Duodécima (oitava + quinta) | 3:1, 6:2, 9:3 | A comparação deve respeitar temperamento e instrumento. |
| Quinta | 3:2, 6:4 | Pode competir com pureza de oitavas. |
| Quarta | 4:3, 8:6 | Pode ser intencionalmente temperada. |
| Dupla oitava | 4:1, 8:2 | Pode afetar a região aguda/grave. |

Esses pares **não são uma receita obrigatória**; a implementação deve oferecer estilos objetivos e explicar quais relações cada estilo otimiza. Outras combinações e famílias podem ser acrescentadas após validação.

**O que visualizar ao tocar em um intervalo**:

- Notas e ordens de parciais em confronto, suas frequências previstas **antes e depois** da curva.
- Diferença em Hz/possível frequência de batimento `|f_a − f_b|`, com a ressalva de que batimento audível depende de amplitude e condições acústicas.
- Compromisso com outros intervalos: melhorar uma oitava pode piorar uma quinta; o painel deve deixar isso visível.
- Pesos numéricos de cada critério e justificativa do valor padrão (com versão do estilo).
- Região do instrumento em que o critério atua; possibilidade de pesos distintos por registro, quando tecnicamente fundamentada.

## 9.6 Modelo matemático de curva [RECOMENDADO]

O perfil fornece, para cada nota `m`, informações sobre parciais `p` e possíveis modelos. A curva define uma correção instrumental `Δ_m` em cents. A frequência-alvo nominal é

\[
f_m^{\mathrm{alvo}}=f_m^{\mathrm{temp}}\,2^{\Delta_m/1200}.
\]

Quando se analisa uma nota individual e se supõe que os parciais observados acompanhem aproximadamente um pequeno deslocamento global de afinação, uma frequência de parcial prevista sob correção pode ser modelada por

\[
f_{m,p}^{\mathrm{prevista}}(\Delta_m)\approx
  f_{m,p}^{\mathrm{perfil}}\,2^{\Delta_m/1200},
\]

**hipótese aproximada**, válida somente dentro de um intervalo físico de ajuste que precisará de validação; grandes mudanças de tensão podem alterar B e outras propriedades, exigindo nova medição.

Um critério de intervalo pode usar, quando o objetivo é coincidência de dois parciais, o resíduo

\[
r_{a,p,b,q}(\Delta)=1200\log_2\left(\frac{f_{a,p}^{\mathrm{prevista}}(\Delta_a)}{f_{b,q}^{\mathrm{prevista}}(\Delta_b)}\right)-t_{a,p,b,q},
\]

onde `t` é o **alvo intervalar explícito** em cents. Se se desejar coincidência de frequências, `t=0`; para critérios compatíveis com temperamentos desiguais, o alvo **não deve ser implicitamente zero** sem decisão fundamentada.

Exemplo de objetivo com critérios e suavidade:

\[
J(\Delta)=\sum_k w_k\,\rho(r_k(\Delta))
 +\lambda\sum_m(\Delta_{m+1}-\Delta_m)^2
 +\mu\sum_m(\Delta_{m+1}-2\Delta_m+\Delta_{m-1})^2,
\]

com `w_k` conforme qualidade e critério, `ρ` perda robusta e `λ, μ` penalizações explicitamente controladas. Esta é uma **família de objetivos ilustrativa**, não um algoritmo de produção já escolhido. Deve-se testar se cada termo preserva as irregularidades reais da escala.

**Âncora e calibração**: fixar uma nota e a frequência declarada ou impor uma condição equivalente, para evitar indeterminação por deslocamento global. Não mexer automaticamente em A4; se a âncora for outra nota, explicar a relação com A4 e o temperamento.

**Medições ausentes**: interpolar com identificação `interpolada`, incerteza por região e política para extrapolação. Se a região for insuficiente para sustentar correção, usar `Δ=0` ou bloquear aplicação segundo regra explícita e conservadora [A VALIDAR], nunca inventar B ou correção com falsa precisão.

## 9.7 Curva e temperamentos históricos

O mesmo conjunto de medições acústicas pode apoiar **mais de uma curva**, mas as correções `Δ_m` de uma curva são definidas relativamente a seu **temperamento base** e a um critério de intervalos. Ao trocar o temperamento após calcular a curva:

- não aplicar automaticamente os mesmos `Δ_m` como se significassem a mesma coisa;
- [RECOMENDADO] indicar incompatibilidade e oferecer `Recalcular prévia com este temperamento`, preservando a curva anterior;
- se for implementada uma função `Rebasear`, declarar matematicamente qual grandeza se preserva (frequências-alvo absolutas versus objetivos intervalares) e exigir confirmação;
- jamais alterar as frações de coma das quintas do temperamento anterior para “acomodar” a curva.

## 9.8 Edição manual e histórico

- O usuário pode ajustar Δ por nota, ancorar trechos, alterar pesos ou escolher estilo acústico. **Toda edição gera versão**.
- Exibir indicação `manual`, `calculado` ou `interpolado` para cada ponto.
- Permitir `Desfazer`, `Restaurar prévia`, comparar versão anterior e exportar sem aplicar.
- Não modificar medições originais ao editar curva. Medição é fato observado; curva é interpretação/decisão.
- Versões aplicadas deverão manter `curveId`, `baseTemperamentId`, A4, perfis de origem, algoritmo, pesos, correções, histórico de decisões e versões.
- Não sobrescrever uma curva aprovada ao abrir o mesmo perfil após novas medições.

## 9.9 Aceitação da Fase 4

- [ ] Gerar a mesma prévia ao repetir o cálculo com as mesmas entradas e parâmetros, dentro de tolerâncias numéricas documentadas.
- [ ] Curva exibe **pontos medidos, interpolados, manuais e incertos** de maneira distinta.
- [ ] Alterar pesos produz diff explicável e lista de intervalos afetados.
- [ ] Validar âncora e detecção de problemas de determinabilidade; não gerar curvas arbitrárias quando o sistema está subdeterminado.
- [ ] Tolerar dados ausentes e medições ruins sem inventar correções conclusivas.
- [ ] Comparar curvas de diferentes instrumentos e estilos com A4/temperamento explicitamente identificados.
- [ ] `Gerar prévia` nunca modifica a afinação ativa; `Aplicar` exige confirmação; `Desativar` volta às referências teóricas.
- [ ] Realizar testes acústicos e auditivos com instrumentos reais, incluindo comparações cegas quando factível; melhoria numérica não equivale automaticamente a melhoria musical.

---

# 10. Fase 5 — Integração entre temperamento e curva instrumental

**Prioridade: Alta | Complexidade: Muito alta.** Só liberar após Fase 4 validada.

## 10.1 Fórmula de integração [DEFINIDO]

\[
f_{\mathrm{final}}(n)=f_{\mathrm{temperamento}}(n)\cdot2^{\Delta_n/1200}
\]

`n` designa a nota MIDI, `f_temperamento(n)` a referência calculada pelo círculo de quintas e A4 vigentes, e `Δ_n` a correção instrumental em cents da curva **compatível com esse mesmo temperamento base**.

- Correção desligada → `Δ_n=0` **para todos os fins**: comparação, nota-alvo e emissor (se ele seguir a opção).
- Correção ligada → referência corrigida disponível para leitura da nota, modo Nota fixa e, **opcionalmente**, emissor de notas.
- O círculo de quintas preserva sempre os valores e presets históricos, sem absorver `Δ_n`.

## 10.2 Controle futuro no Afinador

Próximo ao medidor principal ou à referência da nota, mas **não** dentro do seletor YIN/pYIN/SWIPE’:

```text
Correção instrumental:  [ Desligada / Ativada ]
Curva: Piano de estudo — v3 (base: Pitagórico; A4 415,3 Hz)
Nota A3: teórica 207,650 Hz  | instrumental 207,900 Hz | Δ +2,1 c
[Comparar referências] [Abrir curva]
```

Números do exemplo fictícios.

O controle somente fica ativo quando existe curva **aplicada, compatível e válida**. Caso contrário, exibir `Nenhuma curva aplicada` ou `Curva incompatível com o temperamento atual`, com acesso à ferramenta Curvas.

## 10.3 Política operacional

1. **Desativação por padrão** em perfis novos [RECOMENDADO] até que o usuário escolha uma curva; iniciar captura normal sem alterar frequências teóricas.
2. A ativação exige confirmação informativa na primeira vez: qual perfil, versão, temperamento base e A4.
3. Trocar A4, temperamento ou quintas personalizadas enquanto a curva está ativa dispara verificação de compatibilidade; nunca reutilizar a curva silenciosamente com definição de base diferente.
4. O modo **Nota fixa** compara com frequência corrigida somente se a camada estiver ligada; informar também o valor teórico mediante acesso simples.
5. O emissor de notas possui opção `Seguir correção instrumental` desativada por padrão [RECOMENDADO], separada da emissão teórica já existente. O programa deve explicar claramente quando está gerando f_teórico ou f_final.
6. A4 de referência, temperamento histórico, perfis instrumentais e curva aplicada são entidades distintas; desligar a curva não restaura arbitrariamente A4 ou quintas.
7. O diagnóstico registra `curveApplied`, `curveId`, `curveVersion`, `baseTemperamentId`, `targetHzTheoretical`, `targetHzInstrumental`, `activeTargetHz`, `deltaCents`, sem alterar os logs dos algoritmos.
8. Na exportação das medições acústicas, não confundir `f1Medida` com `nota-alvo corrigida`; são grandezas diferentes.
9. Se a curva for excluída ou deixar de ser compatível, falhar de modo seguro: **desativar correção e informar**, sem manter frequência-alvo sem identificação.
10. Ativação/desativação durante microfone ativo não deve exigir parar o áudio nem recalcular uma nova amostra; apenas reprojetar a comparação com os mesmos dados acústicos quando adequado.

## 10.4 Critérios de aceitação da Fase 5

- [ ] Com `Δ=0`, resultados de referência idênticos aos do afinador original (dentro de erro de ponto flutuante).
- [ ] Alternância ligada/desligada muda apenas a referência-alvo, não a frequência acústica detectada.
- [ ] Modo Nota fixa e emissor respeitam independentemente as escolhas; compatibilidade é auditável.
- [ ] Nenhuma quinta histórica ou preset foi alterado por cálculos acústicos.
- [ ] Troca de temperamento e A4 invalida/bloqueia corretamente curva incompatível.
- [ ] Restauração de configurações técnicas não elimina perfis e curvas acústicas; eventual comando de restaurar curva deve ser separado e confirmado.
- [ ] Números em cents e Hz conferidos com exemplos matemáticos e testes de ida/volta.

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

### C. Integração

- Microfone inicia/para em todas as telas e há **uma única aquisição lógica**; alternar ferramenta não duplica buffers ou captura.
- Worker com ou sem SIMD; fallback funcional ou indisponibilidade explicada.
- Simultaneidade com áudio opcional: coleta de parciais não aciona gravação WAV sem consentimento.
- Mudar resolução FFT da tela principal não reinicia nem corrompe uma medição de parciais com janela própria.
- Perfis: IndexedDB, quota cheia, transações interrompidas, dados corrompidos, importação inválida ou tamanho excessivo.
- Exportações JSON/ZIP e WAV; reimportação reproduz os metadados, unidades e estados.
- Diagnóstico atual de 20 s conserva sua posição entre FFT e círculo, sem regressão.
- Ajuda, configurações e temas não interferem com a medição ou refazem cálculos indevidamente.

### D. Validação em instrumento real

- Repetir a mesma nota, mesma corda, diferentes dias, posições do microfone e dispositivos.
- Separar corda individual versus uníssono completo; avaliar efeitos de outras cordas simpáticas.
- Registrar comparações com equipamentos e técnicas de referência; informar qualidade e limites da referência.
- Avaliar a estabilidade da atribuição de ordem do parcial em agudos/graves.
- Repetir após afinação para verificar previsões e condições alteradas.
- Avaliar curvas por **intervalos auditivos reais** e, quando possível, comparações cegas/pareadas e registros independentes do mesmo instrumento.
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
3. Curvas são aplicadas sem confirmação ou modificam as quintas históricas.
4. Resultados não são reproduzíveis para o mesmo áudio/mesmo conjunto de parâmetros.
5. Não há tratamento de perfis corrompidos ou incompatíveis.
6. O desempenho/travamento em celular real não foi testado ou as limitações não foram comunicadas.
7. A implementação viola a privacidade do áudio ou ativa gravação sem consentimento.

---
# 13. Arquitetura técnica: módulos, áudio e integração

## 13.1 Divisão lógica em um HTML autocontido

O projeto atualmente reúne CSS, interface, scripts DSP e binários embutidos em `index.html`. A futura implementação pode manter um único HTML distribuível, mas deve **organizar os módulos por responsabilidades**, de modo que testes e revisões não exijam alterar simultaneamente as equações antigas.

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
│   ├── Critérios intervalares / pesos / otimização
│   ├── Estados Rascunho / Prévia / Aplicada
│   └── Versões / auditoria / compatibilidade
└── Camada de afinação composta [NOVO na Fase 5]
    ├── Frequências do temperamento original
    └── Correções instrumentais Δ_m opt-in
```

**[RECOMENDADO]** Usar Worker separado para análise mais pesada facilita isolamento de falhas, mas decisões reais de compartilhar ou não o Worker precisam de medições de memória e concorrência. **Não** manter FFT de alta resolução calculando continuamente enquanto o usuário está só no Afinador.

## 13.2 Aquisição compartilhada e sincronização

- Um único fluxo de microfone deve ser dono da permissão e do ciclo `iniciar/encerrar`. Cada ferramenta solicita dados conforme seu estado.
- O **AudioWorklet** é uma opção para capturar áudio contínuo de forma consistente; distinguir captura de PCM para análise da **gravação e retenção de WAV**. Captura temporária não implica consentimento para armazenar áudio longo.
- Incluir timestamps monotônicos de blocos, número de amostras e `sampleRate` efetivo; não juntar buffers sobrepostos do AnalyserNode como se fossem amostras contíguas.
- Usar **ring buffer limitado** para janelas de análise e transferência eficiente dos blocos; evitar alocação por amostra e serialização JSON por quadro DSP.
- Mensagens para Workers devem carregar `sessionId`, `generationId`, `frameId`, `mode`, `sourceId`, `sampleRateHz` e `capturedAtMs` conforme aplicável. Respostas de sessões antigas devem ser descartadas.
- Atribuir a cada resultado o hash/ID do conjunto de configuração que o produziu, para não aceitar quadro calculado com parâmetros anteriores após uma troca de ferramenta.
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
| `MEASUREMENT_STARTED` | Criar sessão imutável com IDs e parâmetros. |
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
- Limitar quantidade de perfis, tamanho de campos, número de parciais, duração máxima de uma sessão e tamanho de arquivos; rejeitar parâmetros numéricos inválidos.
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

**`AcousticMeasurement`** — evento de observação de uma nota/corda, com PCM opcional, candidatos, aceitos/rejeitados, dados temporais, parâmetros, f1 medida/inferida e status.

**`PartialObservation`** — um pico ou componente com ordem candidata, Hz real, amplitude relativa, estabilidade, confiança, status e proveniência de quadros.

**`InharmonicityEstimate`** — resultado opcional do ajuste: modelo, parâmetros F/B/f1, parciais usados, resíduos, incerteza, status e motivo.

**`TuningCurve`** — versão imutável de correções Δ por nota, referência musical, dados de origem, critérios/ponderações, resultado de otimização, estado e histórico.

**`CurveApplication`** — vínculo entre curva **compatível** e afinador, com confirmação, horário, versão e condição de ativação.

**`AuditEvent`** — evento que registra transições de estado e intervenções: quem/por que excluiu um parcial, marcou um outlier ou aplicou uma curva.

## 14.2 Esquema JSON de referência (exemplo fictício)

```json
{
  "schema": "afinador.acoustic-profile",
  "schemaVersion": 1,
  "exportedAt": "2026-11-15T15:00:00Z",
  "profile": {
    "profileId": "local-profile-001",
    "displayName": "Piano de estudo",
    "instrumentFamily": "piano",
    "noteRange": { "midiMin": 21, "midiMax": 108 },
    "acousticModelId": "stiff_string",
    "measurements": [
      {
        "measurementId": "measure-001",
        "midiNote": 57,
        "scientificNote": "A3",
        "captureMode": "single_string",
        "stringIndex": 1,
        "capturedAt": "2026-11-15T14:00:00Z",
        "sampleRateHz": 48000,
        "segmentStartMs": 290.0,
        "segmentEndMs": 1550.0,
        "fundamentalEstimateHz": 220.10,
        "firstPartialMeasuredHz": 220.10,
        "fundamentalSource": "measured_first_partial",
        "partialObservations": [
          {
            "partialId": "p1",
            "order": 1,
            "measuredHz": 220.10,
            "amplitudeDbRelative": -2.1,
            "frequencyStabilityCents": 0.4,
            "status": "accepted",
            "reasonCodes": [],
            "confidenceScore": null
          },
          {
            "partialId": "p2",
            "order": 2,
            "measuredHz": 440.43,
            "amplitudeDbRelative": -8.0,
            "frequencyStabilityCents": 0.7,
            "status": "accepted",
            "reasonCodes": [],
            "confidenceScore": null
          }
        ],
        "inharmonicity": {
          "modelId": "stiff_string",
          "status": "insufficient_data",
          "B": null,
          "F": null,
          "f1InferredHz": null,
          "usedPartialIds": [],
          "residualsCents": [],
          "uncertainty": null
        },
        "quality": {
          "status": "review_required",
          "notes": ["Exemplo com somente dois parciais"]
        },
        "algorithmInfo": {
          "analyzerVersion": "prototype-1",
          "windowSamples": 32768,
          "windowType": "blackman",
          "zeroPaddingLength": 0
        },
        "userNotes": "Exemplo fictício — não é uma medição real."
      }
    ]
  },
  "curves": [],
  "auditEvents": []
}
```

O exemplo utiliza `B: null` porque **dois parciais são insuficientes para uma estimativa robusta**, mesmo que matematicamente ajustem dois parâmetros. Não atribuir um número de confiança sem calibração; por isso `confidenceScore: null`.

`midiNote: 57` é A3 (MIDI padrão). `A4` é nota MIDI 69. Os rótulos de apresentação não substituem a identidade numérica. A faixa do piano ilustrada no esquema é A0 MIDI 21 a C8 MIDI 108.

## 14.3 Contrato de curva

```json
{
  "schema": "afinador.tuning-curve",
  "schemaVersion": 1,
  "curveId": "curve-001",
  "curveVersion": 1,
  "profileId": "local-profile-001",
  "status": "preview",
  "baseTemperamentId": "pitagorico",
  "baseTemperamentSnapshotHash": "hash-da-tabela-de-frequencias",
  "reference": { "midiNote": 69, "frequencyHz": 415.3 },
  "corrections": [
    { "midiNote": 57, "deltaCents": -0.5, "source": "computed" },
    { "midiNote": 69, "deltaCents": 0.0, "source": "anchor" },
    { "midiNote": 81, "deltaCents": 1.7, "source": "interpolated" }
  ],
  "objective": {
    "modelId": "weighted-partial-intervals",
    "version": "prototype-1",
    "intervalCriteria": [],
    "smoothness": null
  },
  "sourceMeasurementIds": ["measure-001"],
  "quality": { "status": "not_validated", "reasons": [] },
  "appliedAt": null
}
```

**Advertência**: os deltas, o hash e a lista de medições são *fictícios*. A curva ilustrativa não pode ser aplicada em produção; faltam critérios intervalares, validação e medições suficientes.

## 14.4 Regras formais para os esquemas

- Campo `schema` nomeia o formato; `schemaVersion` muda quando o contrato muda; `algorithmVersion` identifica mudança de método/constantes.
- Não usar `NaN`, `Infinity` ou strings ambíguas para ausências; usar `null` com `status/reasonCodes`.
- Valores com **unidades no nome** (`Hz`, `Cents`, `Ms`, `DbRelative`) e `midiNote` sem ambiguidade de notação.
- `B` não tem unidade; `F` e `f1` têm Hz. `fundamentalEstimateHz` pode diferir de `firstPartialMeasuredHz`.
- IDs internos do perfil/medição são distintos; não armazenar serial do instrumento como identificador técnico permanente por padrão.
- Preservar status `measured / inferred / interpolated / manually_edited` e distinguir “pico rejeitado” de “medição descartada da curva”.
- Proteger compatibilidade de curva não apenas pelo `baseTemperamentId` mas também por **snapshot/hash efetivo** da tabela ou das quintas, pois presets podem ter sido personalizados.
- Importações desconhecidas devem permanecer **não aplicadas**, jamais substituir curva ativa automaticamente.
- Não usar JSON de diagnóstico de 20 segundos como armazenamento primário do perfil; ele é um relatório de sessão, não a entidade histórica canônica.
- Arquivos exportados são cópias locais; salvar no `IndexedDB` e exportar ZIP/JSON são operações distintas, com feedback separado.
- Preparar esquema para reprocessamento posterior a partir de WAV associado por `audioAssetId`, mediante opt-in, sem exigir áudio gravado para todo perfil.
- Mudança de versões deve ter testes de migração sem perda de informações.

## 14.5 Auditoria acústica por nota — requisito transversal novo [RECOMENDADO]

Cada nota medida deve responder de maneira rastreável:

| Pergunta do usuário | Dados/visão |
|---|---|
| **O que foi medido?** | PCM opcional, segmento temporal, picos candidatos, Hz/amplitude/ordem, estado de cada parcial. |
| **Quanto confio?** | Estabilidade, SNR, número de repetições, incerteza, influência de cada pico e adequação do modelo. |
| **Como foi calculado?** | Fórmula B, parâmetros de ajuste, conjunto de parciais aceitos, perdas/pesos, versão e resíduos. |
| **O que mudou?** | Histórico da nota, evolução do B, curveVersion/delta e eventos de edição/aplicação. |

Fluxo de inspeção:

```text
Ponto da curva → nota → medição → lista de parciais → parcial específico
  → trecho de espectro → qualidade, janelas, resíduos, motivos
  → reavaliar/repetir/confirmar mantendo histórico
```

A cadeia de evidências é uma **característica central de qualidade**, não um painel experimental dispensável.

---

# 15. Integração com diagnóstico, ajuda e documentação

## 15.1 Diagnóstico existente [EXISTENTE]

O monitor atual é **opcional**, fica abaixo da FFT e acima do círculo de quintas, mostra parâmetros do algoritmo ativo e permite captura de **20 segundos** com contador, JSON/ZIP e WAV opcional (captura contínua por AudioWorklet quando suportada). O monitor atual registra metadados do navegador, áudio e desempenho dentro do limite imposto pelas APIs legítimas da plataforma.

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
7. Construção de curva, critérios intervalares, pesos e batimentos; por que não existe uma curva única.
8. Camadas de temperamento histórico e correção instrumental.
9. Perfis, versões, persistência, exportação e privacidade.
10. Limitações e plano de testes em celulares.

**Não substituir a ajuda atual** por documentação técnica longa. Seguir o padrão já existente: explicação pequena → expansão voluntária → aprofundamento contextual.

## 15.4 README, roadmap e nomenclatura

- Ao implementar cada fase, atualizar `README.md`, os capítulos da Ajuda e o roadmap **no mesmo conjunto de alterações**, separando `Disponível`, `Experimental` e `Planejado`.
- A interface usa **inarmonicidade** na nomenclatura em português; arquivos técnicos podem usar `inharmonicity` por compatibilidade de nomes internacionais, mas sem alternar grafias sem motivo no texto exibido.
- `Parcial` é a palavra preferida para componentes medidos; não usar `harmônico` como sinônimo universal para componentes desviados ou modos de sinos.
- `Temperamento` não é `curva`, `B` não é `cents de afinação`, `f1` não é necessariamente o pico dominante.
- Registrar créditos e licenças da implementação existente; não apagar avisos ao refatorar HTML.

---

# 16. Plano de implementação incremental e entregas

> A ordem das **Fases 1–7** é preservada. Há um **marco 0** transversal de infraestrutura/UX, recomendado para evitar mudanças invasivas posteriores.

| Marco | Entrega verificável | Pré-requisito / condição de avanço |
|---|---|---|
| **0 — Navegação e isolamento** | Menu Ferramentas, áreas isoladas, estados e testes de regressão, sem prometer análise ainda. | Afinador original inalterado e responsivo. |
| **1A — Extração de parciais** | Captura, FFT especializada, tabela de componentes e teste sintético. | Frequências/ordens corretamente recuperadas, rejeição clara. |
| **1B — Inspeção progressiva** | Zoom, gráfico de desvios, confiança individual, congelar, revisão. | Estados auditáveis e testes de celular. |
| **2A — Ajuste B** | Modelo físico, otimização robusta, resíduos e rejeição de casos inválidos. | Coeficientes sintéticos recuperáveis e repetibilidade. |
| **2B — Validação de B** | Ensaios de cordas reais, incerteza e calibragem dos critérios. | Sem B falso em dados insuficientes. |
| **3 — Perfis** | IndexedDB, histórico, 88 teclas, exportação/importação, compatibilidade. | Round-trip sem perda, migração testada. |
| **4A — Curvas em prévia** | Critérios de intervalo, otimização, comparação, incerteza, sem aplicação. | Reprodutibilidade e significados intervalares claros. |
| **4B — Curvas com histórico** | Edição, versões, diff, aprovação explícita. | Sem mudança silenciosa da referência. |
| **5 — Integração opt-in** | Curva aplicada opcionalmente ao Afinador/Nota fixa e emissor. | Frequências corretas, desligar restaura teoria, quintas preservadas. |
| **6 — Instrumentos adicionais** | Modelos adequados a famílias diversas. | Modelo B não imposto a fontes não cordofônicas. |
| **7 — Contínuo** | Testes matemáticos, comparação real, desempenho/privacidade/documentação. | Obrigatório a cada marco anterior. |

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
- Separar medida, interpretação via B, perfil instrumental, construção de curva e aplicação.
- Não copiar telas, códigos ou textos de aplicativos comerciais; aproveitar apenas lições gerais.
- Temperamentos históricos não serão adulterados pela curva instrumental; correções independentes e reversíveis.
- Atualizações de curva não devem mudar a afinação ativa silenciosamente.
- Analisador de parciais terá janelas temporais próprias, não herdadas indiscriminadamente da FFT visual.
- Testar **a cada marco de implementação**, com documentação das limitações dos aparelhos físicos.
- Preservar UI atual (temas, ajuda, círculo, diagnóstico e botão circular) quando a ferramenta Afinador estiver selecionada.

## 17.2 Recomendações suficientemente definidas para implementação

- Um botão `Ferramentas ▾`; três áreas novas dentro do HTML existente; sem nova barra inferior de navegação.
- Fluxo de medição por nota sustentada com `Medir`, `Congelar`, `Limpar`, `Salvar medição`.
- Camadas progressivas 0–4 e inspeção de evidências por parcial.
- Filtro de confiança separado em candidato, medição de Hz e adequação do modelo B.
- Estimativa de F e B robusta, inclusive quando o primeiro parcial está ausente.
- `IndexedDB` para perfis e histórico, JSON versionado para exportação, `localStorage` atual reservado a preferências técnicas.
- Curva por instrumento em estados **Medindo → Prévia → Aplicada**, com confirmação e versionamento.
- Diff e explicação dos efeitos intervalares (parciais e batimentos), em vez de gráfico de Railsback sozinho.
- Auditoria acústica por nota, rastreável de curva até pico espectral.
- Amostragem contínua com timestamps e consumidores de áudio isolados; Worker separado ou outra solução que preserve desempenho comprovado.

## 17.3 Pontos a validar antes de fixar padrões de produção

| Tema | Por que está aberto | Como decidir |
|---|---|---|
| Qual método final de refinamento de frequência por parcial? | FFT e interpolação podem não ser suficientes em todos os registros | Comparar métodos e precisão em dados sintéticos e reais |
| Duração mínima/máxima de sustentação | Dependente de grave/agudo e ruído | Medir erro/tempo por faixa e tipo instrumental |
| Limiares de SNR, estabilidade e confiança | Percentuais sem calibração produzem falsa certeza | Calibrar com conjunto independente e curvas de confiabilidade |
| Número mínimo de parciais para B | Depende de cobertura de ordens e ruído | Testar identificabilidade e influência dos pontos |
| Método robusto exato de ajuste B | Vários estimadores têm vantagens e falhas | Comparar robustez, erro e custo em cenários de contaminação |
| Restrições de B por família | Não há um único intervalo universal | Definir modelos físicos e faixas observadas com referências |
| Critérios de curva e pesos iniciais | Não existe uma afinação musical ideal única | Comparar compromissos acústicos e resultados auditivos |
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
| **Modelo incompatível** | Dados não bem descritos pelo modelo escolhido, mesmo que os picos sejam reais. |
| **Curva instrumental** | Correções Δ por nota relativamente a um temperamento musical definido. |
| **Railsback** | Perfil típico de extensão de afinação de piano, não fórmula universal a ser copiada. |
| **Batimento** | Modulação associada à interferência de frequências próximas; diferença em Hz é um indicador, não prova auditiva em qualquer condição. |
| **Parciais 2:1, 4:2 etc.** | Ordens de dois parciais de notas diferentes usadas em critérios intervalares. |
| **Temperamento base** | Frequências do círculo de quintas e A4 sem correção instrumental. |
| **Δₙ** | Correção instrumental por nota MIDI n, em cents. |
| **Medido** | Diretamente estimado de uma observação acústica. |
| **Inferido** | Estimado indiretamente pelo modelo, sem observação direta suficiente. |
| **Interpolado** | Estimado entre pontos medidos; exige representação de incerteza. |
| **Prévia** | Curva calculada ou editada que não modificou as referências ativas. |
| **Aplicada** | Curva validada e explicitamente escolhida como camada de correção. |
| **FFT points vs bins** | FFT de N pontos corresponde à análise de N amostras de entrada; `Δf=fs/N`. Uma FFT real com N amostras apresenta tipicamente N/2 bins positivos utilizáveis conforme a API. |
| **Zero-padding** | Acrescentar zeros para amostragem mais densa do espectro; não aumenta a informação física contida no sinal. |
| **PCM contínuo** | Sequência temporal correta de amostras, sem sobreposição arbitrária de blocos. |

---

# 19. Referências e fontes de evidência

## 19.1 Materiais do próprio projeto

1. **`Roadmap.md` original, 273 linhas**, enviado em 15/11/2026. Seus objetivos, sete fases, fórmulas e critérios originais estão reproduzidos integralmente no Anexo A.
2. **`index.html` enviado em 15/11/2026**, ~8.347 linhas: referência de interface e arquitetura atual, incluindo todas as seis mudanças prévias e os ajustes finais de tema e diagnóstico compacto. O número exato de linhas pode variar conforme normalização de finais de linha.
3. Discussões de produto consolidadas nesta especificação: botão `Ferramentas`, quatro áreas, informação progressiva, avaliação por parcial, ajuste B robusto, perfis, curvas, controles de aplicação e auditabilidade. O documento foi escrito para que essas decisões não dependam de novas consultas à conversa.

## 19.2 Manuais e documentação oficiais consultados

- **PianoMeter — Instructions & Support:** https://pianometer.com/support/  
  Coleta contínua de inarmonicidade, bloqueio de curva, gráfico espectral/zoom, parciais na visualização de afinação, estilos e pesos intervalares. Fonte para a análise de curvas dinâmicas e necessidade de estado aplicado.
- **PianoMeter — FAQ:** https://pianometer.com/faq/  
  Dificuldades de notas agudas, ruído de ataque, falsos batimentos e instabilidade de picos espectrais.
- **pianoscope — Manual:** https://www.pianoscope.app/manual4/html/index.en.html  
  Medição por tecla, visualização de inarmonicidade, valores discrepantes, repetição, ponderação de medidas, intervalos de afinador e apresentação de curvas.
- **TuneLab — Manual Android:** https://tunelab-world.com/TuneLabAndroidManual-3.0.pdf  
  Medição de inarmonicidade por notas isoladas, curvas, formas de comparação e escolha de parciais.
- **Verituner — Guia rápido:** https://www.veritune.com/VeritunerForAndroidQuickStartUserGuide.pdf  
  Estados, operações profissionais, análise múltipla e organização de funções técnicas.
- **CyberTuner — Guia de início:** https://mail.cybertuner.com/pub/reyburn/rct_demo/iRCT%20Getting%20Started%20Manual%20v7.8.x.pdf  
  Modos de troca automática, correção de altura, curva e controles especializados.
- **Pesquisa sobre otimização por entropia espectral:** https://www.sciencedirect.com/science/article/pii/S0003682X20300050  
  Demonstra diversidade de objetivos científicos e necessidade de avaliar reproducibilidade e preferência musical. Não utilizar como autorização para implementar algoritmo fechado.

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
- [ ] Insuficiência de evidência não gera valor definitivo.
- [ ] O usuário consegue inspecionar dados gradualmente, sem abrir um painel técnico inteiro para afinar uma nota.
- [ ] Não houve alteração silenciosa de A4, círculo de quintas, temperamento histórico ou configuração dos algoritmos atuais.
- [ ] A curva instrumental exige confirmação e pode ser desativada com retorno exato à referência teórica.
- [ ] Os perfis registram tipo de corda, data, origem, versões e qualidade.
- [ ] Dados acústicos e histórico têm esquema versionado, política de importação segura e exportação local.
- [ ] O diagnóstico atual de 20 segundos não foi confundido com o armazenamento histórico de perfis.
- [ ] O desempenho do afinador antigo não piora enquanto a nova ferramenta está inativa.
- [ ] Testes sintéticos, reais, matemáticos, de layout, persistência e privacidade estão documentados com limites claros.
- [ ] README/Ajuda/roadmap foram atualizados conjuntamente.

**Decisão orientadora final:** não queremos apenas um afinador que “acerta” uma frequência. Queremos um ambiente em que o usuário compreenda **o que foi realmente observado no instrumento, quão confiável é cada parcela da análise, por que determinada curva foi proposta e quais compromissos ela introduz** — preservando a facilidade de uso do afinador original.

---

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
