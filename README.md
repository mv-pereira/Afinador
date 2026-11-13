# Afinador — FFT, YIN, pYIN e SWIPE' com Círculo de Quintas Editável

**[Acessar o afinador online](https://mv-pereira.github.io/Afinador/)**

Afinador de instrumentos musicais executado no navegador, com **temperamentos históricos**, edição do **círculo de quintas por frações de coma**, visualização do espectro e emissão de notas de referência. A detecção de frequência utiliza **YIN, pYIN, SWIPE' ou Pico**, com processamento local em um *Web Worker* e FFT **PFFFT em WebAssembly**.

> **Importante:** este README descreve a versão atualizada do `index.html`. Para que o endereço do GitHub Pages apresente todas as funcionalidades descritas aqui, publique também o HTML correspondente no repositório.

## Como usar em poucos passos

1. Abra o afinador e pressione **Ativar microfone**. Autorize a captação quando o navegador solicitar. Toque, de preferência, **uma nota por vez**.
2. Escolha o **temperamento** na barra inferior. O padrão é **Sistema Pitagórico**, com **Lá4 (A4) = 415,3 Hz**. A referência pode ser ajustada entre **300 e 500 Hz**.
3. Selecione o modo de afinação:
   - **Automático (padrão):** identifica a nota mais próxima de acordo com o temperamento atual e mostra o desvio.
   - **Nota fixa:** escolha a nota-alvo com os botões **<** e **>**. O desvio será calculado em relação a essa nota, mesmo que outra esteja mais próxima do som captado.
4. Escolha o método de detecção. **YIN é o padrão**; pYIN e SWIPE' são alternativas para comparar diferentes formas de estimar a fundamental. O modo **Pico** identifica o componente de maior intensidade da FFT.
5. Observe a **frequência medida**, o **nome da nota** e o **desvio em cents**. Desvio negativo significa som mais grave que a referência; positivo, mais agudo.
6. Para ouvir a afinação de referência, abra **Emissor de notas — temperamento atual**. Se o microfone estiver ativo ao mesmo tempo, prefira **fones de ouvido**.

**Dica:** se a leitura oscilar, sustente a nota, reduza ruídos próximos e experimente outro detector. Ataques curtos, harmônicos fortes e sinais sobrepostos podem dificultar a estimação.

---

## Visão geral

O Afinador combina ferramentas de **afinação monofônica** e de **estudo de temperamentos** em um único arquivo HTML, com CSS, JavaScript e os binários WebAssembly incorporados.

**Recursos principais:**

- Afinação **Automática** ou por **Nota fixa**, com seleção de C0 a C8.
- Quatro métodos de detecção: **YIN, pYIN, SWIPE' e Pico**.
- FFT de **8192 pontos** para o espectro principal e análise multijanela para o SWIPE'.
- Frequência estimada, nota musical, desvio numérico e medidor em **cents**.
- **Notação científica e de Helmholtz simultâneas** no visor da nota, com alternância por toque.
- **13 presets** de temperamento e edição individual das quintas por frações de coma.
- Círculo de quintas, tabela de comas e tabela de desvios de intervalos.
- Emissor de notas com volume, oitava, forma de onda e as duas notações.
- Leitura acústica **Bruta** ou **Filtrada**; desempenho **Automático** ou **Econômico**.
- Execução **local**, sem envio do áudio a servidores para processamento.

## Modos de afinação

### Automático — padrão

O programa procura a nota mais próxima da frequência medida na tabela de frequências do **temperamento selecionado**. A frequência de referência e o desvio em cents acompanham a nota reconhecida.

### Nota fixa

O seletor começa em **Dó4 (C4)** e percorre de **C0 a C8**, em passos de semitom:

- **<** desce um semitom; **>** sobe um semitom.
- A nota-alvo acompanha as alterações no A4, no preset e nos ajustes individuais das quintas.
- O desvio é calculado em relação à **nota-alvo**, independentemente da nota mais próxima do som.
- Durante o silêncio, a nota-alvo permanece indicada, mas não é apresentada uma medição inexistente.

No gráfico de FFT, a **linha verde tracejada** marca a nota-alvo e a **linha vermelha** indica a frequência detectada. O **zoom de ±100 cents** amplia somente a visualização; não aumenta a resolução real da análise.

O medidor apresenta uma escala de **−40 a +40 cents**. Caso o desvio exceda essa escala, o ponteiro pode permanecer na extremidade, enquanto o valor numérico continua informando o desvio calculado.

## Métodos de detecção de frequência

O controle **Pico / Fundamental** alterna entre a observação do componente espectral dominante e a estimação da frequência fundamental. No modo Fundamental, é possível escolher **YIN**, **pYIN** ou **SWIPE'**.

| Método | Como funciona | Em que pode ser mais útil |
|---|---|---|
| **YIN (padrão)** | Examina a periodicidade da onda no domínio do tempo e usa informações da FFT para verificar a coerência harmônica. | Afinação monofônica geral, ataques e mudanças de nota; pode reconhecer uma fundamental mais fraca que seus harmônicos. |
| **pYIN** | Distribui probabilidades entre candidatas de frequência e acompanha sua evolução por um **Viterbi causal**. | Notas sustentadas e leituras que se beneficiam de continuidade temporal. Mudanças bruscas podem exigir mais tempo de resposta. |
| **SWIPE'** | Avalia a saliência da fundamental pela estrutura de **harmônicos primos**, usando várias janelas FFT e uma escala perceptual ERB. | Timbres ricos em harmônicos e casos em que a fundamental não é a componente espectral mais intensa. Exige mais processamento. |
| **Pico** | Localiza o pico de maior intensidade do espectro. | Análise do componente dominante, inspeção de harmônicos e comparação com detectores de fundamental. **Não garante que o pico seja a nota musical.** |

Nenhum método é superior em todas as situações. O aplicativo é voltado principalmente a **uma nota por vez**; sinais polifônicos podem produzir leituras ambíguas.

### Particularidades dos algoritmos

- **YIN:** emprega janelas temporais adaptativas, mais longas para notas graves e mais curtas para notas agudas. O espectro PFFFT ajuda a avaliar a coerência dos harmônicos.
- **pYIN:** utiliza candidatas probabilísticas, estados vozeados/não vozeados e um Viterbi executado em tempo real. Sua política temporal foi ajustada para permitir mudanças de oitava com evidência acústica forte e consistente, reduzindo o caso de retenção identificado como **PYIN-001**. Não é uma reprodução bit a bit de implementações pYIN offline.
- **SWIPE':** é uma adaptação causal da implementação de referência de Kyle Gorman, baseada no método de Arturo Camacho. Utiliza FFT multijanela PFFFT no Worker. **Pode apresentar desvios maiores de precisão nos extremos graves e agudos**, que ainda exigem validação com instrumentos reais.
- **Pico:** pode apresentar uma leitura de ruído ou de um harmônico como frequência, pois não possui um modelo próprio de confiança da fundamental.

O controle adaptativo antigo de **sensibilidade/ruído** foi removido: os detectores recebem sinais fracos e aplicam seus próprios critérios. Permanece apenas um **piso RMS fixo de 0,00001** para reconhecer sinais praticamente nulos e limpar a leitura no silêncio.

## Visor da nota: científica e Helmholtz

Durante a afinação, o nome da nota é também um **botão** com duas representações simultâneas:

- **Inicialmente:** a notação científica aparece **grande**, e a notação de Helmholtz aparece **pequena no canto inferior direito**.
- **Primeiro toque:** a notação de Helmholtz assume a posição principal e a científica passa para o canto inferior direito.
- **Segundo toque:** restaura a disposição inicial.

Exemplos: **Lá4 ↔ a'**, **Dó4 ↔ c'**, **Fá1 ↔ FF**, **Fá2 ↔ F** e **Fá3 ↔ f**.

A troca altera **apenas a apresentação**, sem modificar a frequência detectada, o desvio em cents, a nota-alvo ou o processamento acústico.

## Como interpretar o desvio em cents

O desvio é calculado pela relação entre a frequência medida e a frequência de referência:

```text
cents = 1200 × log2(frequência_medida / frequência_de_referência)
```

- **0 cent:** frequência medida igual à referência.
- **Valor negativo:** som abaixo da referência (mais grave).
- **Valor positivo:** som acima da referência (mais agudo).
- **100 cents:** um semitom no temperamento igual; **1200 cents:** uma oitava.

A referência vem do **temperamento atual**. Assim, a mesma frequência pode produzir desvios diferentes quando se muda de preset ou se ajusta uma quinta.

## Temperamentos e círculo de quintas

O aplicativo oferece **13 presets**:

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

No **círculo de quintas**, é possível visualizar o sistema selecionado. A **Tabela de ajuste de comas** permite modificar cada quinta por frações de:

- **Coma pitagórico (c.p.):** aproximadamente **23,460 cents**.
- **Coma sintônico (c.s.):** aproximadamente **21,506 cents**.

Os ajustes são acumulados e a **quinta residual** representa o fechamento do círculo. **Zerar ajustes** restaura o preset selecionado. O controle de enarmonia permite escolher a grafia **Sol# / Lab** no ponto de corte.

A **Tabela de intervalos — Desvios** compara os intervalos resultantes com referências puras: **quinta justa (3:2), terça maior (5:4), terça menor (6:5), sexta maior (5:3) e sexta menor (8:5)**.

## Emissor de notas

O **Emissor de notas — temperamento atual** gera uma referência sonora sem depender da captação do microfone.

- Permite selecionar notas por **notação científica e de Helmholtz** ou navegar por semitons.
- A extensão inicial vai de **F1 (FF)** a **F7**; **Ampliar extensão** libera de **C0 a B9**.
- Oferece ondas **senoidal, triangular, quadrada e dente de serra**.
- Permite ajustar o volume e interromper a emissão.
- A frequência emitida acompanha alterações no **A4**, no **temperamento** e nos ajustes das quintas.

**Atenção:** se usar o emissor e o microfone simultaneamente, prefira **fones de ouvido** para evitar realimentação. O emissor produz formas de onda eletrônicas, não uma simulação da inarmonicidade de cordas reais.

## Configurações

| Controle | Função |
|---|---|
| **Lá de referência (A4)** | Padrão **415,3 Hz**; ajustável entre **300 e 500 Hz**. |
| **Temperamento** | Seleciona um dos 13 presets de afinação. |
| **Pico / Fundamental** | Alterna entre pico espectral e detecção da fundamental. |
| **Algoritmo YIN / pYIN / SWIPE'** | Escolhe o detector da fundamental; YIN é o padrão. |
| **Leitura acústica: Bruta** | Apresenta o resultado sem filtragem temporal visual adicional. |
| **Leitura acústica: Filtrada** | Aplica suavização opcional, ajustável, com possível atraso de resposta. |
| **Desempenho: Automático** | Ajusta a cadência de análise à capacidade observada do dispositivo. |
| **Desempenho: Econômico** | Limita a cadência de solicitações para reduzir o consumo de processamento. |
| **Máx. gráfico (Hz)** | Define o limite superior de exibição da FFT; padrão **2000 Hz**. |
| **Zoom na nota-alvo** | Amplia visualmente a região de ±100 cents da nota-alvo. |
| **Enarmonia** | Seleciona a grafia Sol# ou Lab no ponto de corte. |
| **Visor da nota** | Alterna, por toque, qual notação aparece em destaque. |

Não há mais controle de sensibilidade adaptativa nem botão de diagnóstico de 20 segundos nesta versão.

## Funcionamento técnico

O processamento de áudio é realizado localmente, usando **Web Audio API**, **Dedicated Web Worker** e **WebAssembly**:

```text
Microfone → Web Audio API → amostras temporais
                               │
                               ▼
                       Dedicated Web Worker
                         │
                         ├── PFFFT WASM SIMD128
                         │       └── FFT principal (8192 pontos)
                         │           ├── Espectro para o gráfico
                         │           ├── Validação harmônica do YIN
                         │           └── Pico dominante
                         │
                         ├── YIN (periodicidade + espectro)
                         ├── pYIN (candidatas + Viterbi causal)
                         ├── SWIPE' (FFT multijanela PFFFT)
                         └── Pico
                               │
                               ▼
                    Frequência / estado / quadro
                               │
                               ▼
             Temperamento → nota, cents e marcadores
```

O motor PFFFT dispõe de **SIMD128** e **fallback escalar**. Quando o WASM não está disponível, há **fallback nativo** para YIN, pYIN e Pico; o **SWIPE' exige o PFFFT WASM** e não é substituído silenciosamente por outro algoritmo.

O Worker utiliza identificadores de sessão, geração e quadro para impedir a apresentação de resultados antigos. A FFT do gráfico e os detectores consomem dados correspondentes ao mesmo quadro processado.

O YIN tem faixa **nominal de busca de aproximadamente 16 a 4600 Hz**; a precisão real depende da janela, da taxa de amostragem, do instrumento e do microfone. As análises multijanela e o motor FFT oferecem uma base para estudos futuros de parciais e **inarmonicidade**, mas o Afinador **ainda não realiza compensação automática de inarmonicidade**.

## Requisitos e execução

- Navegador atualizado com suporte à **Web Audio API**, **Web Workers** e **WebAssembly**.
- Permissão de acesso ao **microfone**.
- Para execução na web, um **contexto seguro (HTTPS)**. O GitHub Pages oferece HTTPS.
- Em dispositivos que permitam abrir um HTML localmente, a disponibilidade do microfone pode variar conforme as restrições de segurança do navegador (`file://`).

O arquivo `index.html` é **autocontido**: contém interface, Worker e binários WASM incorporados, sem precisar baixar bibliotecas de processamento durante a execução. Uma conexão com a internet não é necessária **para os cálculos acústicos**; o acesso pelo GitHub Pages, naturalmente, requer carregar a página.

## Testes e limitações conhecidas

Foram realizados testes automatizados em navegador Chromium, Worker e sinais sintéticos, incluindo comparação entre o PFFFT e a FFT anterior, cenários de ruído e harmônicos, mudanças de oitava e regressões dos quatro modos. **Esses testes não equivalem à homologação em microfones físicos de celulares Android ou iPhone.**

Limitações importantes:

- **Monofonia:** acordes e fontes simultâneas podem produzir notas ambíguas.
- **Erros de oitava:** continuam possíveis em alguns timbres e transições; a correção PYIN-001 reduz um caso de retenção temporal, mas não elimina todas as ambiguidades.
- **SWIPE':** exige mais processamento e pode apresentar desvios de precisão nas regiões mais graves e mais agudas.
- **Pico:** o maior componente espectral pode ser ruído ou um harmônico.
- **Silêncio e sinais fracos:** cada detector tem seus critérios; o piso RMS mínimo não substitui uma avaliação da qualidade musical do som.
- **Inarmonicidade:** não há modelo de compensação para parciais deslocados de cordas reais.
- **FFT e zoom:** ampliar a representação do espectro não aumenta sua resolução física.
- **Latência e consumo:** dependem do navegador, dispositivo, método escolhido e taxa de amostragem.

## Possíveis desenvolvimentos

- Validação sistemática em instrumentos e microfones físicos, sobretudo Android e iOS.
- Medição de precisão, latência e consumo por detector em condições reais.
- Análise de parciais e **inarmonicidade**, aproveitando os espectros do PFFFT.
- Exportação e importação de temperamentos personalizados.
- Perfis de afinação por instrumento.
- Registro opcional de medidas e análise de estabilidade.

## Créditos e licenças

O código próprio do projeto está distribuído sob a **[Licença MIT](LICENSE)**, conforme o repositório.

O aplicativo também incorpora ou adapta trabalhos de terceiros, cujas atribuições e condições devem ser preservadas nas redistribuições:

- **PFFFT (Pretty Fast FFT):** Julien Pommier (2013), com base no **FFTPACK** de Paul Swarztrauber / **NCAR–UCAR**. Utilizado sob os termos de licença FFTPACK/UCAR indicados no código-fonte. O porte para o Afinador acrescenta **WASM SIMD128 e escalar, macros SIMD adaptadas, wrapper C, janelas configuráveis, planos reutilizáveis, tratamento de DC/Nyquist e integração ao Worker**.
- **SWIPE':** método de **Arturo Camacho**, implementado em C por **Kyle Gorman** (copyright 2009–2013, **MIT**). Adaptado ao processamento causal em JavaScript e à FFT PFFFT multijanela, substituindo as dependências de FFTW e leitura de arquivo. Consulte a [implementação de referência de Gorman](https://github.com/kylebgorman/swipe).
- **YIN e pYIN:** métodos associados aos trabalhos de **Alain de Cheveigné e Hideki Kawahara** (YIN) e **Matthias Mauch e Simon Dixon** (pYIN). O módulo pYIN do Afinador é uma **implementação própria em JavaScript**, baseada nas formulações publicadas e na documentação técnica, e não incorpora o porte GPL do código C++ de referência.

Os avisos legais associados ao PFFFT e ao SWIPE' estão mantidos no HTML distribuído. A licença MIT do repositório **não substitui as obrigações específicas** das partes de terceiros.
