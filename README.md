# 🎵 Afinador FFT com Círculo de Quintas Editável

Afinador de instrumentos baseado em **FFT (Fast Fourier Transform)** com suporte a **temperamentos históricos e customizados**, incluindo edição detalhada via **frações de comas pitagórico e sintônico**.

---

## 📌 Visão Geral

Este projeto implementa um afinador em HTML/JavaScript que:

- Detecta frequência em tempo real via microfone
- Identifica nota musical com base em um **temperamento configurável**
- Mostra desvio em **cents**
- Permite editar o **círculo de quintas**
- Suporta diversos **temperamentos históricos**
- Exibe análise visual:
  - Espectro FFT
  - Medidor de afinação
  - Círculo de quintas interativo
  - Tabela de intervalos

---

## ⚙️ Funcionalidades

### 🎤 Detecção de áudio
- Usa `Web Audio API`
- FFT para análise espectral
- Identificação do **pico dominante**
- Refinamento por interpolação parabólica

### 🎼 Sistema de temperamento
- Representação em **cents**
- Construção via:
  - Quintas sucessivas
  - Ajustes por comas
- Suporte a:
  - Temperamento igual
  - Pitagórico
  - Mesotônico
  - Werckmeister
  - Kirnberger
  - Vallotti
  - Young
  - Neidhardt
  - Bach (Barnes / Lehman)

### 🔧 Edição avançada
- Ajuste de cada quinta via:
  - Frações de **coma pitagórico (c.p.)**
  - Frações de **coma sintônico (c.s.)**
- Acúmulo fracionário preciso
- Quinta residual automática (fechamento do ciclo)

### 📊 Visualizações
- Espectro FFT em tempo real
- Medidor de cents (±40)
- Círculo de quintas interativo
- Tabela de intervalos com erro relativo

---

## 🧠 Conceitos Importantes

### 🎯 Quinta justa
3:2 ≈ 701.955 cents

### 🎯 Comas
- Coma pitagórico ≈ 23.46 cents  
- Coma sintônico ≈ 21.51 cents  

### 🎯 Fechamento do círculo
O sistema garante:

12 quintas = 7 oitavas (8400 cents)

A diferença é absorvida como:
- **quinta residual (lobo)**

---

## 🚀 Como usar

### 1. Abrir o projeto
Basta abrir o arquivo `.html` no navegador.

> ⚠️ Necessário permitir acesso ao microfone.

---

### 2. Ativar o microfone

Clique em:

Ativar microfone

Isso inicia:
- Captura de áudio
- FFT contínua
- Detecção de nota

---

### 3. Configurações

#### 🎚️ A4 (Referência)
Define a frequência do Lá:

Padrão: 440 Hz

#### 📈 Máx. gráfico
Limite superior do espectro FFT exibido.

#### 🎛️ Estabilidade
Controla suavização:
- Alto → mais estável
- Baixo → mais responsivo

---

### 4. Temperamento

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

### 5. Ajuste manual

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

Isso altera:
- Nomeação das notas
- Posição da quinta residual

---

## 🔬 Funcionamento Interno

### 🎧 Pipeline de áudio

1. Microfone → `MediaStream`
2. → `AnalyserNode`
3. → FFT (`frequencyBinCount`)
4. → Detecção de pico
5. → Conversão para frequência

---

### 📐 Detecção de nota

Para cada frequência detectada:

1. Percorre tabela MIDI (24–108)
2. Calcula erro em cents:

cents = 1200 * log2(freq / freqNota)

3. Seleciona menor erro

---

### 🔄 Construção do temperamento

- Parte de Do = 0 cents
- Soma quintas sucessivas:

C → G → D → A → ...

- Normaliza para classe de altura (mod 1200)

---

### 📊 Tabela de intervalos

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

### 🎯 Medidor de cents

- Intervalo: ±40 cents
- Cor dinâmica:
  - Verde: afinado
  - Amarelo: leve desvio
  - Vermelho: fora

---

## 🧩 Estrutura do Código

### Principais blocos:

- **Áudio / FFT**
- **Temperamento**
- **UI**
- **Cálculo musical**

---

## ⚠️ Limitações

- Pode detectar harmônicos em vez da fundamental
- Sensível a ruído
- Requer navegador moderno
- Latência depende do hardware

---

## 💡 Possíveis melhorias

- Detecção por autocorrelação (YIN)
- Filtro de harmônicos
- Exportação/importação de temperamentos
- Modo instrumento específico
- Afinador polifônico

---

## 📜 Licença

Livre para uso e modificação.

---

## 👤 Autor

Projeto desenvolvido como ferramenta experimental de afinação e estudo de temperamentos musicais.
