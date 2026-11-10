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
