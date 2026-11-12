# Afinador FFT + YIN/pYIN com Círculo de Quintas Editável

**[Acessar o afinador online](https://mv-pereira.github.io/Afinador/)**

## Como usar em poucos passos

1. **Ative o microfone** e permita o acesso quando solicitado pelo navegador. Toque preferencialmente **uma nota por vez**.
2. **Escolha o temperamento** no rodapé. O padrão é **Sistema Pitagórico**, com **Lá de referência (A4) = 415,3 Hz**, ajustável entre 300 e 500 Hz.
3. **Escolha o modo de afinação:**
   - **Automático (padrão):** identifica a nota mais próxima no temperamento selecionado e mostra seu desvio.
   - **Nota fixa:** escolha a nota-alvo pelos botões **<** e **>**. O desvio será calculado em relação a essa nota, mesmo que o som esteja mais próximo de outra.
4. **Escolha a detecção:** mantenha **Fundamental + YIN** para a afinação usual. O **pYIN Experimental** permite comparar outra abordagem de detecção; **Pico** acompanha o componente mais intenso do espectro, que pode ser um harmônico.
5. **Para ouvir uma referência**, use o **Emissor de notas — temperamento atual**. Se estiver captando áudio simultaneamente, prefira fones de ouvido.

> **Dica:** leitura instável pode resultar de ruído, ataque muito curto, harmônicos predominantes ou sinal fraco. Sustente a nota e afaste outras fontes sonoras antes de alterar o algoritmo.

---

## Visão geral

**Afinador de instrumentos no navegador, com modos Automático e Nota fixa, temperamentos históricos, detecção YIN/pYIN e edição de quintas por frações de coma.**

O projeto utiliza **HTML, CSS e JavaScript**, com captação pela **Web Audio API**. A análise do sinal é executada em um **Dedicated Web Worker**. A FFT é usada para exibir o espectro e, no caminho YIN, verificar a coerência espectral da frequência estimada.

Além da afinação, permite estudar a distribuição dos temperamentos, modificar quintas do círculo e emitir notas de referência nas frequências correspondentes.

**Recursos principais:**

- Afinação **Automática** ou por **Nota fixa** (C0 a C8).
- Modo **Fundamental** com escolha entre **YIN (padrão)** e **pYIN Experimental**; modo **Pico** independente.
- Frequência medida, identificação da nota, desvio em **cents** e diagnóstico da detecção.
- Espectro **FFT de 8192 pontos**, medidor de cents e marcadores de frequência medida e nota-alvo.
- **13 presets** de temperamento com ajustes individuais das quintas.
- Círculo de quintas editável e tabelas de comas e desvios de intervalos.
- Emissor de notas com notação científica e de Helmholtz, volume, oitava e forma de onda.
- **Leitura Bruta (padrão)** ou **Filtrada**, além de desempenho **Automático (padrão)** ou **Econômico**.
- Arquivo HTML único e autocontido, sem dependências externas de execução.

## Modos de afinação

### Automático — padrão

O afinador procura a nota mais próxima da frequência captada na tabela do **temperamento atual**. A referência acompanha a nota identificada, e o desvio é mostrado em cents.

### Nota fixa

O seletor começa em **Dó4 (C4)** e permite navegar de **C0 a C8** por semitons:

- **<** desce um semitom; **>** sobe um semitom.
- A frequência-alvo acompanha o **A4**, o preset e os ajustes manuais das quintas.
- O desvio é calculado **sempre em relação à nota-alvo**, mesmo quando a nota captada é outra.
- Durante o silêncio, a nota-alvo continua indicada, mas não é inventada uma medição.

**No gráfico FFT:**

- **Verde tracejado:** frequência da nota-alvo.
- **Vermelho:** frequência estimada do áudio.
- **Zoom na nota-alvo (±100 cents):** amplia apenas a **visualização**, sem acrescentar resolução à FFT.

O medidor usa uma escala visual de **−40 a +40 cents**. Se o desvio exceder essa faixa, o valor numérico continua representando o desvio calculado, mesmo quando o ponteiro chega à extremidade.

## Detecção de frequência: YIN, pYIN e Pico

O controle **Pico / Fundamental** define a família de detecção. Em **Fundamental**, o músico pode escolher **YIN** ou **pYIN**; em **Pico**, essa escolha fica inativa, sem apagar a seleção anterior.

| Detecção | Como funciona | Uso recomendado |
|---|---|---|
| **Fundamental + YIN (padrão)** | Estima a periodicidade do sinal e verifica a coerência dos harmônicos por FFT. | Afinação monofônica geral, inclusive graves e mudanças rápidas de nota. |
| **Fundamental + pYIN Experimental** | Obtém candidatas de frequência com probabilidades e aplica acompanhamento temporal por **Viterbi causal**. | Comparação experimental em notas sustentadas; não há vantagem global comprovada sobre o YIN deste projeto. |
| **Pico** | Seleciona o componente espectral de maior intensidade. | Investigar o pico dominante; ele nem sempre corresponde à fundamental musical. |

O **YIN** utiliza janelas adaptativas para equilibrar estabilidade nos graves e resposta nos agudos:

| Frequência de referência para a janela | Duração |
|---|---:|
| ≥ 220 Hz | 65 ms |
| 110 a menos de 220 Hz | 90 ms |
| 55 a menos de 110 Hz | 135 ms |
| Abaixo de 55 Hz | 185 ms |
| Sem frequência anterior disponível | 135 ms |

Uma memória de até **300 ms** pode conservar temporariamente a última frequência válida **somente para selecionar a janela YIN** durante perdas breves de confiança. Essa memória **não é apresentada como medição** e é limpa no silêncio, ao desligar o microfone ou ao trocar de método.

O **pYIN** implementado é uma adaptação probabilística **causal, para tempo real**. Ele combina candidatas acústicas com estados vozeados/não vozeados e decodificação Viterbi. Não deve ser interpretado como uma reprodução bit a bit de um pYIN offline. Mesmo na **Leitura Bruta**, o pYIN conserva sua inferência temporal interna.

> **Limitação importante:** em comparações laboratoriais com sinais sintéticos, o pYIN experimental apresentou erros de oitava e latência maiores em alguns cenários. Em especial, **não foi comprovada melhoria na identificação do FF do cravo**. Por isso, o YIN permanece como padrão.

## Como interpretar a afinação

O desvio utiliza **cents**, uma unidade logarítmica:

```text
cents = 1200 × log2(frequência_medida / frequência_de_referência)
```

- **0 cent:** frequência medida igual à referência.
- **Negativo:** som mais grave que a referência.
- **Positivo:** som mais agudo que a referência.
- **100 cents:** um semitom no temperamento igual; **1200 cents:** uma oitava.

A frequência de referência depende do **temperamento escolhido**. Duas configurações diferentes podem atribuir desvios distintos à mesma frequência captada.

## Temperamentos e círculo de quintas

O projeto inclui **13 presets**:

1. Sistema Pitagórico.
2. Temperamento Igual (−1/12 do coma pitagórico por quinta).
3. Mesotônico de 1/4 de coma sintônico.
4. Mesotônico de 1/6 de coma sintônico.
5. Kirnberger III.
6. Werckmeister II.
7. Werckmeister III.
8. Vallotti.
9. Young II.
10. Neidhardt — Kleine Stadt.
11. Neidhardt — Große Stadt.
12. Bach / Barnes.
13. Bach / Lehman.

O **círculo de quintas** mostra a distribuição do temperamento. Na **Tabela de ajuste de comas**, é possível alterar cada quinta por frações de:

- **Coma pitagórico (c.p.):** aproximadamente **23,460 cents**.
- **Coma sintônico (c.s.):** aproximadamente **21,506 cents**.

Os ajustes são acumulados; a quinta residual reflete o fechamento do círculo. **Zerar ajustes** restaura a configuração do preset. A opção de enarmonia permite escolher a grafia **Sol# / Lab** no ponto de corte.

A **Tabela de intervalos — Desvios** apresenta diferenças em relação a intervalos puros de referência: quinta justa (3:2), terça maior (5:4), terça menor (6:5), sexta maior (5:3) e sexta menor (8:5).

## Emissor de notas

O **Emissor de notas — temperamento atual** produz uma referência sonora independente da captação do microfone.

- Escolha a nota por **notação científica** e **notação de Helmholtz**, ou navegue por semitons.
- A extensão padrão é de **F1 (FF) a F7**; **Ampliar extensão** libera **C0 a B9**.
- Selecione a forma de onda: **senoidal**, **triangular**, **quadrada** ou **dente de serra**.
- Ajuste o volume; o valor emitido acompanha mudanças de **A4**, temperamento e quintas.

**Atenção:** use fones ao emitir e captar som simultaneamente, para evitar que o microfone identifique o próprio emissor. O sintetizador não reproduz a inarmonicidade de cordas reais.

## Configurações

| Controle | Função |
|---|---|
| **Lá de referência (A4)** | Base da afinação; padrão **415,3 Hz**, ajustável de **300 a 500 Hz**. |
| **Temperamento** | Seleciona um dos 13 presets. |
| **Pico / Fundamental** | Escolhe entre pico dominante e identificação de frequência fundamental. |
| **Algoritmo: YIN / pYIN** | Seleciona o detector em Fundamental; pYIN é **Experimental**. |
| **Leitura acústica: Bruta** | Apresenta as estimativas sem filtragem visual temporal adicional. |
| **Leitura acústica: Filtrada** | Aplica suavização opcional, com intensidade ajustável e possível atraso de resposta. |
| **Desempenho: Automático** | Adapta o intervalo entre análises à capacidade de processamento. |
| **Desempenho: Econômico** | Limita o agendamento a até **18 solicitações de análise por segundo**. |
| **Máx. gráfico (Hz)** | Define o limite superior da visualização FFT; padrão **2000 Hz**. |
| **Enarmonia** | Alterna a grafia Sol# / Lab. |
| **Zoom na nota-alvo** | Amplia visualmente a região de ±100 cents em torno da nota escolhida. |

## Funcionamento técnico

**Caminho básico do áudio:**

```text
Microfone → Web Audio API
            ├── AnalyserNode (FFT, 8192 pontos)
            │     └── Espectro e dados para validação
            └── AnalyserNode (amostras no tempo)
                         ↓
                 Dedicated Web Worker
                   ├── Pico dominante
                   ├── YIN + verificação FFT
                   └── pYIN + Viterbi causal
                         ↓
              Frequência / estado / quadro
                         ↓
              Nota, cents e marcador FFT
```

Um único caminho de detecção é executado por análise; o Worker controla a identificação de sessão e quadro para descartar respostas obsoletas. Leituras inconclusivas ou silenciosas **não são promovidas a medições confiáveis**.

A matemática musical, o desenho do espectro e a seleção de temperamento são independentes das otimizações internas de desempenho. A FFT exibida mantém **8192 pontos**, fornecidos pelo `AnalyserNode` do navegador.

A faixa nominal de busca do **YIN** é de **16 a 4600 Hz**; a detecção efetiva também depende da amostragem, da janela e da qualidade do sinal. O programa pode informar quando a nota-alvo está fora da faixa nominal.

O núcleo DSP, o pYIN e o Worker são implementados em **JavaScript puro**. A versão autocontida incorpora seu código ao próprio HTML; não requer bibliotecas acústicas externas nem WASM.

## Requisitos e execução

- Navegador moderno com **Web Audio API**, **Web Workers** e acesso ao microfone.
- Permissão do usuário para a captura.
- Para a publicação online, **HTTPS**; o projeto utiliza **GitHub Pages**.

O aplicativo pode ser distribuído como **um único HTML autocontido**, sem CDN ou carregamento remoto de bibliotecas. Seu código pode funcionar sem internet, mas a disponibilidade do **microfone e de Workers ao abrir via `file://` varia entre navegadores**. Para testar a captura de maneira mais previsível, use um contexto seguro (`https://` ou `localhost`, conforme o navegador).

A versão modular, usada também para desenvolvimento e testes, mantém os módulos de DSP e Worker em arquivos separados.

## Testes e limitações conhecidas

- **Uma nota por vez:** acordes e instrumentos sobrepostos podem produzir ambiguidades.
- **Ruído, harmônicos e fundamental fraca:** podem causar rejeição da leitura ou erro de oitava.
- **pYIN Experimental:** pode ter maior latência e erros de oitava; não foi demonstrada superioridade global em relação ao YIN otimizado.
- **Graves e agudos extremos:** a precisão depende do microfone, da taxa de amostragem, do instrumento e do ambiente.
- **Inarmonicidade:** o sistema não compensa desvios dos parciais de cordas reais.
- **Zoom FFT:** altera a visualização, não a resolução espectral.
- **Tempo real:** latência e consumo dependem do navegador e do dispositivo; o modo Econômico reduz a cadência de solicitações.

Foram realizados **testes automatizados com sinais sintéticos**, comparações quadro a quadro e ensaios em navegador/Worker. As otimizações de JavaScript preservaram as saídas acústicas nos conjuntos avaliados, mas **não garantem melhora de desempenho em todos os aparelhos**.

**Permanecem pendentes a validação com instrumentos e microfones físicos, testes prolongados em Android e a verificação completa da distribuição modular no navegador.** Resultados laboratoriais não substituem essas verificações.

## Possíveis desenvolvimentos

- Calibração e avaliação independente do pYIN em gravações reais de cravo.
- Redução dos erros de oitava do pYIN e estudo de suas transições temporais.
- Exportação e importação de temperamentos personalizados.
- Perfis de afinação por instrumento.
- Registro de medições e análise de estabilidade.
- Tratamento opcional de inarmonicidade para instrumentos que necessitem disso.

## Licença

Distribuído sob a **Licença MIT**. Consulte o arquivo [LICENSE](LICENSE) para os termos completos.
