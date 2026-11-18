# Afinador — Oficina Pernambuco

**[Acessar o Afinador](https://mv-pereira.github.io/Afinador/)** · **[Guia de uso](GUIA_DE_USO.md)**

Aplicativo web de afinação musical, estudo de temperamentos e investigação acústica, desenvolvido para computadores e dispositivos móveis. Reúne detecção de altura em tempo real, edição de sistemas de afinação, análise de parciais e inarmonicidade, perfis instrumentais, cálculo experimental de curvas de afinação e síntese sonora.

O processamento é realizado localmente no navegador, sem servidor de análise, conta de usuário ou instalação obrigatória. A interface está em português do Brasil.

## Recursos

| Ferramenta | Funcionalidades |
| --- | --- |
| **Afinador** | Afinação automática ou por nota fixa, frequência em Hz, desvio em cents, quatro métodos de detecção, espectro FFT e zoom na nota-alvo. |
| **Parciais e inarmonicidade** | Captura individual ou multiataque, inspeção de picos e parciais, análise de séries harmônicas e componentes não harmônicos, estimativa experimental do coeficiente de inarmonicidade B para cordas compatíveis, avaliação de consistência e repetibilidade. |
| **Perfis instrumentais** | Organização de medições por instrumento, tecla e corda; consulta das evidências acústicas, comparação de sessões, armazenamento local e importação/exportação de registros. |
| **Curvas de afinação** | Construção experimental de curvas para piano acústico, objetivos de fidelidade ao temperamento ou coincidência acústica, ponderação intervalar, edição, auditoria e histórico de revisões. A aplicação efetiva das curvas ao afinador permanece bloqueada. |
| **Emissor** | Geração de notas conforme a referência musical, ondas periódicas, síntese aditiva harmônica e inarmônica, reconstrução espectral a partir de componentes medidos e espectros personalizados. |

As ferramentas compartilham a definição musical de referência, mas possuem domínios próprios de processamento e configurações. Os controles de visualização não reinicializam os detectores de altura. As preferências válidas são aplicadas imediatamente, podem ser salvas para futuras inicializações e restauradas aos padrões de fábrica por ferramenta, sem excluir os registros musicais ou acústicos.

## Temperamentos e representação musical

O catálogo integrado oferece 18 sistemas:

- **Pitagórico e igual (12-TET)**;
- **Mesotônicos:** 1/4, 1/5 e 1/6 de coma sintônico;
- **Temperamentos circulantes:** Kirnberger III, Werckmeister III e IV, Vallotti, Young II, Neidhardt — Kleine Stadt (1732) e Große Stadt (1724);
- **Reconstruções históricas:** Rameau (1726), d’Alembert (1752), Bach/Barnes (1979) e Bach/Lehman (2005);
- **Divisões iguais da oitava:** 13-EDO e 14-EDO.

Os sistemas históricos são representados por cadeias ou ciclos de quintas, com ajustes em frações de coma pitagórico e sintônico. O motor racional conserva as frações exatamente e verifica o fechamento dos ciclos. O cilindro acústico de quintas em 2,5D e a matriz de intervalos permitem examinar as relações resultantes.

A arquitetura distingue a grafia musical, a tecla física ou lógica, a coincidência acústica e o alvo de afinação. Assim, teclados históricos ampliados com teclas divididas não são confundidos com divisões iguais da oitava em 13 ou 14 graus. A frequência de referência é ajustável, com 415,3 Hz como padrão, e a apresentação contempla as notações científica e de Helmholtz.

A biblioteca pessoal permite guardar e compartilhar definições musicais em JSON. As fontes históricas e as qualificações das reconstruções estão incorporadas ao catálogo; uma atribuição histórica controversa não constitui comprovação de uma prática individual.

## Métodos de detecção de altura

| Método | Implementação |
| --- | --- |
| **YIN + FFT** | Método padrão. Estima a periodicidade temporal por diferença normalizada cumulativa (CMNDF), com validação harmônica e refinamento espectral adaptativo. |
| **pYIN** | Estimativa probabilística com múltiplas hipóteses de altura e acompanhamento temporal por Viterbi causal, incluindo tratamento de transições de oitava. |
| **SWIPE′** | Estimativa de altura por saliência de padrões espectrais, com múltiplas janelas de análise e kernel baseado em harmônicos de ordem 1 e prima. Adaptação causal para execução em tempo real. |
| **Pico** | Localização da componente espectral dominante; não garante que a frequência encontrada seja a fundamental. |

O espectro pode ser representado em escala logarítmica (padrão) ou linear. A busca de picos na ferramenta de parciais e a abrangência máxima dos gráficos respeitam o teto de 24 kHz e a frequência de Nyquist da captura. Os detectores de altura mantêm seus próprios limites operacionais; a faixa nominal do afinador é de 16 a 4.600 Hz. A redução de pontos para renderização preserva máximos espectrais, sem modificar os dados de análise.

## Arquitetura técnica

- HTML, CSS e JavaScript integrados em um único arquivo de distribuição (`index.html`), com interface responsiva e temas claro e escuro.
- Web Audio API para captura e emissão sonora; AudioWorklet para aquisição acústica; Web Workers para isolar os cálculos mais pesados da interface.
- PFFFT compilada para WebAssembly, com variantes SIMD128 e escalar, planos reutilizáveis e fallback nativo do navegador onde suportado. SWIPE′ requer o motor PFFFT/WASM.
- Motor de parciais independente do afinador convencional, com FFT radix-2 em JavaScript, janela Hann, interpolação de picos e aquisição multiataque.
- Modelo de corda rígida com ajuste robusto em cents, perda de Huber, consolidação de ataques e bootstrap por execução independente. Os parâmetros configuráveis e utilizados na análise são registrados nas sessões; análises personalizadas não são automaticamente habilitadas como fontes de curvas.
- Catálogo canônico de frequências, separado dos detectores acústicos; otimização de curvas por relações entre parciais, com restrições e âncora de referência.
- `localStorage` para preferências e biblioteca musical; IndexedDB para perfis instrumentais e histórico de curvas; WebCrypto/SHA-256 para verificações de integridade.

Não é necessário instalar dependências de frontend, executar um bundler ou baixar bibliotecas de uma CDN para utilizar o HTML distribuído.

## Compatibilidade e execução local

É necessário um navegador moderno com JavaScript habilitado. Os recursos de captura dependem de permissão de microfone e de contexto seguro (HTTPS ou `localhost`); funcionalidades adicionais dependem do suporte às APIs de áudio, Workers, WebAssembly, WebCrypto e armazenamento local.

Para desenvolvimento, na raiz do repositório:

```bash
git clone https://github.com/mv-pereira/Afinador.git
cd Afinador
python3 -m http.server 8000
```

A instância local fica disponível em `http://localhost:8000/`. Para acesso por outro dispositivo na rede, recomenda-se servir o aplicativo por HTTPS. O HTML é autocontido, mas abrir uma cópia por `file://` não garante acesso a todas as APIs em todos os navegadores. O funcionamento integral offline da página publicada também depende de sua disponibilidade local.

## Dados, privacidade e segurança

- O áudio e os cálculos permanecem no dispositivo; não há envio automático das medições a um serviço remoto.
- O microfone é ativado por ação explícita. O monitor de diagnóstico oferece captura limitada a 20 segundos e exportação local em ZIP, com `diagnostico.json` e WAV opcional. A gravação WAV pode conter sons do ambiente e conversas.
- Os arquivos JSON importáveis passam por validação estrutural em Worker, limites de tamanho e complexidade, rejeição de chaves perigosas e duplicadas, verificações específicas de formato, integridade e coerência dos dados aplicáveis.
- Uma Content Security Policy (CSP) restringe scripts não autorizados, conexões externas e outros recursos. As licenças e os avisos de terceiros estão incorporados ao HTML.

O SHA-256 verifica integridade em relação ao conteúdo esperado, não a identidade do remetente nem a autenticidade física de uma medição. As proteções reduzem riscos, mas não equivalem a uma certificação de segurança. Arquivos HTML executáveis devem ser obtidos de fontes confiáveis. Os dados locais podem ser perdidos se o armazenamento do navegador for limpo; as exportações permitem manter cópias independentes.

## Estado técnico e limitações

O Afinador é um projeto experimental. A qualidade da detecção depende do instrumento, do microfone, do ruído, da taxa de amostragem e do método escolhido. A detecção de altura destina-se principalmente a sons monofônicos; resultados inconclusivos são possíveis, especialmente em sinais com poucos parciais, componentes sobrepostos ou instabilidade.

A análise de inarmonicidade e a construção de curvas ainda não constituem instrumentos metrológicos homologados. As curvas possuem finalidade de estudo e pré-visualização; a aplicação real continua bloqueada e a extrapolação não é permitida. A reconstrução aditiva aproxima componentes espectrais, não reproduz integralmente o timbre, a fase e os transientes de uma gravação original.

As regressões computacionais abrangem o catálogo musical, os quatro detectores, a análise acústica, a síntese, os domínios de configuração e a importação segura. Os testes de segurança incluem 4.034 cenários de validação e ensaios de CSP; os testes de interface foram executados no Chromium, com parte do armazenamento, digest e aquisição simulados. A homologação física, a compatibilidade integral em dispositivos móveis e a auditoria independente de segurança permanecem pendentes.

## Repositório e contribuição

| Arquivo | Finalidade |
| --- | --- |
| [`index.html`](index.html) | Aplicativo autocontido. |
| [`README.md`](README.md) | Apresentação e documentação técnica geral. |
| [`GUIA_DE_USO.md`](GUIA_DE_USO.md) | Manual do usuário (em preparação). |
| [`Roadmap.md`](Roadmap.md) | Planejamento e requisitos técnicos do projeto. |
| [`LICENSE`](LICENSE) | Licença do projeto. |

Sugestões, relatos de problemas e contribuições são bem-vindos via [Issues](https://github.com/mv-pereira/Afinador/issues) e [Pull Requests](https://github.com/mv-pereira/Afinador/pulls). Para relatar problemas, informe o navegador, sistema operacional, ferramenta, detector e condições de medição relevantes; compartilhe diagnósticos somente após verificar que não contêm informações pessoais ou áudio que não deseja divulgar. Mudanças nos motores devem ser acompanhadas por testes de regressão; mudanças em scripts incorporados exigem manter os hashes da CSP coerentes com o conteúdo publicado.

## Créditos e referências

### Código de terceiros

| Componente | Autoria, origem e licença |
| --- | --- |
| **PFFFT — Pretty Fast FFT** | Julien Pommier (2013), baseada no FFTPACKv4 de Paul Swarztrauber (NCAR). Código adaptado para WebAssembly SIMD128/escalar e integrado ao Worker do Afinador. Licença FFTPACK/UCAR, permissiva, com avisos preservados em `licencaPFFFTEtapa2`. [Projeto original arquivado](https://github.com/source-archive/pffft) · [FFTPACK](https://www.netlib.org/fftpack/). |
| **SWIPE′** | Implementação C de Kyle Gorman (2009–2013), utilizada como base do porte causal em JavaScript, com integração à PFFFT/WASM. Licença MIT preservada em `licencaSWIPEGormanMIT`. [Código original](https://github.com/kylebgorman/swipe). |

### Fundamentos científicos

- Alain de Cheveigné e Hideki Kawahara (2002). *YIN, a fundamental frequency estimator for speech and music*. Journal of the Acoustical Society of America, 111(4), 1917–1930.
- Matthias Mauch e Simon Dixon (2014). *pYIN: A Fundamental Frequency Estimator Using Probabilistic Threshold Distributions*. ICASSP.
- Arturo Camacho (2007). *SWIPE: A Sawtooth Waveform Inspired Pitch Estimator for Speech and Music*. Tese de doutorado; e Arturo Camacho e John G. Harris (2008), artigo homônimo no Journal of the Acoustical Society of America.
- Harvey Fletcher (1964). *Normal Vibration Frequencies of a Stiff Piano String*. Journal of the Acoustical Society of America.
- Peter J. Huber (1964). *Robust Estimation of a Location Parameter*. Annals of Mathematical Statistics.
- Bradley Efron (1979). *Bootstrap Methods: Another Look at the Jackknife*. Annals of Statistics.

As referências científicas descrevem os métodos que fundamentam a implementação; não implicam que o Afinador reproduza integralmente os programas originais dos autores.

## Licença

O código próprio do projeto é disponibilizado sob a [licença MIT](LICENSE), conforme o arquivo de licença do repositório. Os componentes de terceiros continuam sujeitos às respectivas licenças e avisos de copyright, que devem ser preservados em redistribuições. A identidade visual da Oficina Pernambuco não é automaticamente abrangida pela licença de software.
