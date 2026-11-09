# Afinador FFT + YIN com Círculo de Quintas Editável

**[Acessar o afinador online](https://mv-pereira.github.io/Afinador/)**

## Como usar em poucos passos

1. **Abra o afinador** pelo link acima e clique em **Ativar microfone**. Autorize o uso do microfone quando o navegador solicitar.
2. **Escolha o temperamento** no campo **Preset** e, se desejar, altere o **Lá de referência (A4)**. A configuração inicial é **Pitagórico**, com **A4 = 440 Hz**.
3. **Escolha como afinar:**
   - **Automático (padrão):** toque uma nota isolada. O programa identifica a nota mais próxima e exibe o desvio em cents.
   - **Nota fixa:** ative o seletor à direita de “Automático”, escolha a nota-alvo com **<** e **>** (começa em **Dó4 / C4**) e toque o instrumento. O desvio será calculado **sempre em relação à nota escolhida**.
4. **Acompanhe o medidor:** valor **negativo** indica som mais grave que a referência; valor **positivo**, mais agudo; valor próximo de **0 cent**, afinação próxima da nota-alvo.
5. **Para ouvir uma referência**, abra **Emissor de notas — temperamento atual**, selecione uma nota e clique em **Emitir nota**. Use fones de ouvido se o microfone estiver ligado.

> **Dica:** para a maioria dos instrumentos tocando **uma nota por vez**, mantenha a detecção em **Fundamental (YIN + FFT)**. O modo **Pico** é útil para observar o componente mais intenso, mas ele pode ser um harmônico.

---

## Visão geral

**Afinador de instrumentos no navegador, com afinação automática ou por nota fixa, temperamentos históricos e edição de quintas por frações de coma.**

Este projeto é uma aplicação **HTML, CSS e JavaScript**, executada diretamente no navegador. A captação usa a **Web Audio API** e combina análise espectral por **FFT** com estimação da frequência fundamental por **YIN**.

Além de afinar instrumentos, o programa permite **experimentar e comparar temperamentos**, modificar as quintas do círculo por frações de coma e gerar sons nas frequências calculadas pelo sistema selecionado.

**Recursos principais:**

- Afinação **automática** ou por **nota fixa** (C0 a C8).
- Detecção por **Fundamental (YIN + FFT)** ou **Pico dominante** — seletor independente do modo de afinação.
- Frequência medida, nota de referência, desvio em **cents** e indicador de **confiança** da detecção.
- **Espectro FFT**, medidor de cents e marcadores de frequência medida e de frequência-alvo.
- **13 presets** de temperamento, com ajustes individuais das quintas.
- Círculo de quintas editável e tabelas de **comas** e **desvios de intervalos**.
- Emissor de notas com escolha de nota, oitava, volume e forma de onda.
- Controles de sensibilidade, estabilidade, desempenho e frequência máxima do gráfico.

## Modos de afinação

### Automático — padrão

O afinador mede a frequência do som, busca a nota mais próxima na **tabela do temperamento atual** e calcula a distância em cents até ela. A referência muda automaticamente quando a nota detectada muda.

### Nota fixa

Ao ativar **Nota fixa**, aparece um seletor que começa em **Dó4 (C4)**:

- **<** desce um semitom; **>** sobe um semitom.
- A seleção vai de **C0 a C8**; os botões são desativados nos limites.
- A frequência-alvo acompanha alterações no **A4**, no **preset** e nos **ajustes manuais do círculo de quintas**.
- O desvio é calculado exclusivamente contra a **nota-alvo**, mesmo quando o som está mais próximo de outra nota.
- A nota-alvo e sua frequência continuam visíveis durante o silêncio; a medição e o desvio ficam em branco quando não há leitura confiável.

**No gráfico FFT:**

- **Linha verde tracejada:** frequência da nota-alvo.
- **Linha vermelha:** frequência estimada do som captado.
- **Ampliar região da nota no FFT (±100 cents):** zoom **visual** em torno do alvo. Ele não aumenta a resolução real da FFT.
- Se a nota-alvo estiver acima do máximo configurado do gráfico, a escala é ampliada visualmente para incluí-la.

O medidor mostra uma escala de **−40 a +40 cents**, mas **o valor numérico não é limitado** a essa faixa no modo fixo. Em desvios maiores, o ponteiro permanece na extremidade e o número continua mostrando o erro real.

## Detecção de frequência: FFT e YIN

O seletor **Pico / Fundamental**, situado no painel do espectro, determina **como a frequência é estimada**. Ele funciona nos dois modos de afinação.

| Detecção | Como funciona | Quando usar |
|---|---|---|
| **Fundamental (padrão)** | Usa **YIN** para estimar a periodicidade do sinal e a **FFT** para verificar a coerência dos harmônicos. | Afinação de notas isoladas, especialmente quando um harmônico é mais forte que a fundamental. |
| **Pico** | Seleciona o componente de maior intensidade do espectro, com refinamento do pico. | Inspeção espectral e situações em que interessa acompanhar o componente dominante. |

O detector de fundamental usa **janelas temporais adaptativas**, com análises mais longas para frequências graves e mais curtas para frequências agudas. A FFT usada na **visualização permanece com 8192 pontos**. A análise inclui verificação de consistência entre harmônicos, avaliação de confiança e descarte de leituras inconclusivas.

> O sistema foi desenvolvido para **sons monofônicos** (uma nota por vez). Nem YIN nem FFT garantem a recuperação da fundamental em todos os timbres, ambientes ou combinações de notas.

## Como interpretar a afinação

O desvio é medido em **cents**, unidade logarítmica. O cálculo é:

```text
cents = 1200 × log2(frequência_medida / frequência_de_referência)
```

- **0 cent:** frequência medida igual à referência.
- **Cents negativos:** som abaixo da referência (mais grave).
- **Cents positivos:** som acima da referência (mais agudo).
- **100 cents:** um semitom no temperamento igual; **1200 cents:** uma oitava.

A frequência de referência vem do **temperamento selecionado**, e não obrigatoriamente do temperamento igual. Assim, uma mesma frequência captada pode apresentar desvios diferentes em presets diferentes.

## Temperamentos e círculo de quintas

O projeto inclui os seguintes **13 presets**:

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

O **círculo de quintas** exibe a distribuição resultante. Para personalizá-la, abra **Tabela de ajuste de comas** e altere cada quinta por frações de:

- **Coma pitagórico (c.p.):** aproximadamente **23,460 cents**.
- **Coma sintônico (c.s.):** aproximadamente **21,506 cents**.

Os ajustes são acumulados; a **quinta residual** resulta do fechamento do círculo. O botão **Zerar ajustes** restaura a configuração base do preset selecionado. A opção de enarmonia permite escolher a nomenclatura **Sol# / Lab** no ponto de corte.

A **Tabela de intervalos — Desvios** apresenta as diferenças em relação a intervalos puros de referência: quinta justa (**3:2**), terça maior (**5:4**), terça menor (**6:5**), sexta maior (**5:3**) e sexta menor (**8:5**).

## Emissor de notas

Abra o painel **Emissor de notas — temperamento atual** para gerar uma nota de referência, independentemente de o microfone estar ligado.

- Selecione uma nota na lista, com **notação científica** e **notação de Helmholtz**.
- Use **◀ Semitom** e **Semitom ▶** para navegar, **Emitir nota** para reproduzir e **Parar som** para interromper.
- A extensão padrão vai de **F1 a F7**; a opção **Ampliar extensão** permite **C0 a B9**.
- Ajuste o volume e escolha onda **senoidal**, **triangular**, **quadrada** ou **dente de serra**.
- Alterações no **A4**, no temperamento, nos ajustes das quintas ou na nota escolhida atualizam a frequência emitida.

**Atenção:** se usar emissão e captação simultaneamente, prefira **fones de ouvido** para evitar que o próprio som gerado seja identificado pelo microfone. O emissor não modela a **inarmonicidade** de cordas reais.

## Configurações

| Controle | Função |
|---|---|
| **Lá de referência (A4)** | Define o Lá4 usado na construção das frequências. Padrão: **440 Hz**; campo de **300 a 500 Hz**. |
| **Máx. gráfico (Hz)** | Ajusta o limite superior da visualização FFT. Padrão: **2000 Hz**. Não é o limite geral do detector. |
| **Estabilidade** | Suaviza a leitura em cents dentro da mesma nota. **0%** desativa a suavização; valores maiores estabilizam mais, com resposta menos imediata. |
| **Sensibilidade** | Define o limiar mínimo de intensidade: valores maiores detectam sons mais fracos; valores menores exigem som mais forte. |
| **Desempenho** | **Econômico**, **Normal** ou **Completo**, com frequências crescentes de análise e atualização visual. |
| **Pico / Fundamental** | Alterna o algoritmo de detecção, independentemente de **Automático / Nota fixa**. |
| **Enarmonia** | Alterna a grafia **Sol#** / **Lab** conforme o ponto de corte escolhido. |

## Funcionamento técnico

**Caminho básico do áudio:**

```text
Microfone → MediaStream → Web Audio API
                         ├── AnalyserNode (FFT, 8192 pontos)
                         │     ├── Exibição do espectro
                         │     └── Verificação espectral de harmônicos
                         └── AnalyserNode (amostras no tempo)
                               └── YIN com janela adaptativa
                                       ↓
                              Frequência estimada + confiança
                                       ↓
               Modo Automático: nota mais próxima no temperamento
               Modo Nota fixa:  nota-alvo escolhida pelo usuário
                                       ↓
                              Desvio em cents + medidor
```

A análise considera o nível do sinal para evitar leituras no silêncio. A suavização da frequência é feita em **escala logarítmica**, evitando médias artificiais entre notas muito diferentes; mudanças grandes ou a perda do sinal reiniciam a leitura. No modo Fundamental, uma detecção sem confiança suficiente pode ser apresentada como **inconclusiva**, sem atribuir uma nota.

A faixa nominal de busca do detector YIN é **16 a 4600 Hz**. O programa sinaliza quando a nota fixa selecionada fica fora dessa faixa, algo possível nos extremos de oitava com valores de A4 diferentes de 440 Hz.

## Requisitos e execução

- Navegador moderno com suporte a **Web Audio API** e acesso ao microfone.
- Permissão de microfone concedida pelo usuário.
- Para uso online, conexão **HTTPS** (o link do projeto utiliza GitHub Pages).

O afinador é um **único arquivo HTML**, com CSS e JavaScript incorporados, **sem bibliotecas externas**. Para executar localmente, abra o arquivo no navegador; a permissão de microfone pode variar conforme o navegador e o contexto de segurança. Em hospedagem web, use HTTPS.

## Limitações conhecidas

- **Uma nota por vez:** acordes e sons complexos sobrepostos podem causar ambiguidade.
- **Harmônicos e ruídos:** o detector híbrido reduz erros de oitava, mas não os elimina em todos os casos; interferências podem resultar em leitura inconclusiva.
- **Região muito grave ou muito aguda:** a captação depende da resposta do microfone e do dispositivo; a faixa nominal do algoritmo não garante a precisão física em toda a extensão.
- **Inarmonicidade:** cordas reais, especialmente cordas rígidas de piano, podem ter parciais não exatamente harmônicos; o programa não compensa esse fenômeno.
- **Zoom do FFT:** apenas amplia a exibição; não acrescenta resolução espectral.
- **Latência e desempenho:** dependem do navegador, do hardware, da taxa de amostragem e do modo selecionado.

O sistema passou por testes automatizados de cálculos e interface com **sinais sintéticos**, mas esses testes **não substituem uma calibração ou validação com instrumentos e microfones físicos**.

## Possíveis desenvolvimentos

- Exportação e importação de temperamentos personalizados.
- Perfis de afinação por instrumento.
- Registro de medições e análise de estabilidade ao longo do tempo.
- Tratamento específico de inarmonicidade para instrumentos que necessitem disso.
- Estudos de detecção polifônica como recurso separado do afinador monofônico.

## Licença

Distribuído sob a **Licença MIT**. Consulte o arquivo [LICENSE](LICENSE) para os termos completos.
