# Afinador FFT com Círculo de Quintas Editável

[Acessar o afinador online](https://mv-pereira.github.io/Afinador/)

Afinador de instrumentos baseado em **FFT (Fast Fourier Transform)** com suporte a **temperamentos históricos e customizados**, incluindo edição via **frações de comas pitagórico e sintônico**.

---

## Visão Geral

Este projeto implementa um afinador em HTML/JavaScript que:

- Detecta frequência em tempo real via microfone
- Identifica nota musical com base em um **temperamento configurável**
- Mostra desvio em **cents**
- Permite ajustar **sensibilidade de captação**
- Permite selecionar modo de **desempenho** para diferentes aparelhos
- Permite editar o **círculo de quintas**
- Exibe análise visual:
  - Espectro FFT
  - Medidor de afinação
  - Círculo de quintas interativo
  - Tabela de qualidade de intervalos

---

## Funcionalidades

### Detecção de áudio
- Usa `Web Audio API`
- FFT para análise espectral
- Identificação do **pico dominante**
- Refinamento por interpolação parabólica
- Controle de **sensibilidade** para ajustar o limiar mínimo de detecção sonora

### Desempenho
- Modos selecionáveis:
  - **Econômico**: reduz a frequência de análise e redesenho do gráfico
  - **Normal**: equilíbrio entre resposta e uso de processamento
  - **Completo**: usa a resposta máxima permitida pelo aparelho
- Útil para adaptar o afinador a celulares antigos ou dispositivos mais lentos

### Sistema de temperamento
- Representação em **cents**
- Construção via:
  - Quintas sucessivas
  - Ajustes por comas

### Edição
- Ajuste de cada quinta via:
  - Frações de **coma pitagórico (c.p.)** (≈ 23.46 cents)
  - Frações de **coma sintônico (c.s.)** (≈ 21.51 cents)
- Acúmulo fracionário
- Quinta residual automática (fechamento do ciclo)

---

## Como usar

### 1. Ativar o microfone

Clique em:

Ativar microfone

Isso inicia:
- Captura de áudio
- FFT contínua
- Detecção de nota

---

### 2. Configurações

#### A4 (Referência)
Define a frequência do Lá:

Padrão: 440 Hz

#### Máx. gráfico
Limite superior do espectro FFT exibido.

#### Estabilidade
Controla suavização:
- Alto → mais estável
- Baixo → mais responsivo

#### Sensibilidade
Controla o volume mínimo necessário para o afinador detectar o som:

- Alto → detecta sons mais fracos
- Baixo → exige som mais forte e reduz interferência de ruídos

#### Desempenho
Define o modo de processamento do afinador:

- **Econômico** → menor uso de processamento, indicado para celulares antigos
- **Normal** → equilíbrio entre fluidez e resposta
- **Completo** → sem limite artificial de análise/desenho, como o funcionamento original

---

### 3. Temperamento

Selecione um preset:

- Pitagórico
- Igual
- Mesotônico (1/4, 1/6)
- Werckmeister II / III
- Kirnberger III
- Vallotti
- Young II
- Neidhardt
- Bach (Barnes / Lehman)

---

### 4. Ajuste manual

Cada quinta pode ser modificada via:

#### Coma pitagórico (c.p.)
Exemplo:
1/12

#### Coma sintônico (c.s.)
Exemplo:
1/4

Botões:
- `+` adiciona
- `−` subtrai
- `zerar` limpa ajuste

---

### 6. Enarmonia

Escolha o ponto de corte:

- Sol#  
- Lab  

---

## Funcionamento Interno

### Pipeline de áudio

1. Microfone → `MediaStream`
2. → `AnalyserNode`
3. → FFT (`frequencyBinCount`)
4. → Aplicação do limiar de sensibilidade
5. → Detecção de pico dominante
6. → Conversão para frequência
7. → Comparação com a tabela de notas do temperamento atual

---

### Detecção de nota

Para cada frequência detectada:

1. Percorre tabela MIDI (24–108)
2. Calcula erro em cents:

cents = 1200 * log2(freq / freqNota)

3. Seleciona menor erro

---

### Construção do temperamento

- Parte de Dó
- Soma quintas sucessivas:

C → G → D → A → ...

- Normaliza para classe de altura (mod 1200)

---

### Tabela de intervalos

Calcula desvios para:

- Quinta justa (3:2)
- Terça maior (5:4)
- Terça menor (6:5)
- Sexta maior (5:3)
- Sexta menor (8:5)

Coloração:
- Verde → próximo do puro
- Vermelho → maior erro

---

## Estrutura do Código

### Principais blocos:

- **Áudio / FFT**
- **Temperamento**
- **UI**
- **Cálculo musical**

---

## Limitações

- Pode detectar harmônicos em vez da fundamental
- Pode sofrer interferência de ruído ambiente, conforme a sensibilidade escolhida
- Requer navegador moderno com suporte à `Web Audio API`
- Latência e fluidez dependem do hardware e do modo de desempenho selecionado

---

## Possíveis melhorias

- Detecção por autocorrelação (YIN)
- Filtro de harmônicos
- Exportação/importação de temperamentos
- Modo instrumento específico
- Afinador polifônico

---

## Licença

Este projeto está licenciado sob a Licença MIT — veja o arquivo [LICENSE](![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)) para detalhes.
