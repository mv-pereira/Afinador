# Afinador — Oficina Pernambuco

**[Acessar o Afinador](https://mv-pereira.github.io/Afinador/)** · **[Guia de uso completo](GUIA_DE_USO.md)**

![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue) ![Plataforma Web](https://img.shields.io/badge/plataforma-web-506A60) ![Estado experimental](https://img.shields.io/badge/estado-experimental-lightgrey)

Aplicativo web de afinação musical, estudo de temperamentos e investigação acústica, com especial atenção ao piano, ao fortepiano e ao cravo. Reúne detecção de altura em tempo real, representação e edição de sistemas de afinação, análise espectral, caracterização de instrumentos, cálculo experimental de curvas de afinação e síntese sonora.

Desenvolvido para computadores e dispositivos móveis, com interface em português do Brasil. O processamento ocorre localmente no navegador, sem necessidade de conta, servidor de análise ou instalação de aplicativo.

**Estado do projeto:** desenvolvimento experimental — Etapa 18. A análise física de inarmonicidade e a otimização instrumental ainda não foram homologadas. A aplicação de curvas está disponível em caráter experimental, sob condições explícitas de verificação e confirmação.

## Objetivos

- Oferecer uma ferramenta de afinação que não se limite ao temperamento igual de doze divisões.
- Preservar a identidade musical e física das teclas em sistemas históricos, inclusive instrumentos com teclas divididas.
- Permitir investigar a relação entre a referência musical teórica e as propriedades acústicas efetivamente observadas em um instrumento.
- Documentar as medições, hipóteses, critérios de qualidade e revisões, distinguindo observações experimentais de conclusões físicas comprovadas.
- Manter o processamento de áudio independente da rede e a interface adequada ao uso em dispositivos móveis.

## Ferramentas

| Ferramenta | Finalidade e recursos |
| --- | --- |
| **Afinador** | Detecção de altura, afinação automática e por nota fixa, frequência em Hz, desvio em cents, espectro FFT em escala linear ou logarítmica, zoom espectral e representação dos temperamentos. |
| **Parciais e inarmonicidade** | Capturas individuais e multiataque, inspeção de picos e parciais, comparação de execuções, ajuste experimental de inarmonicidade e avaliação de repetibilidade. |
| **Perfis instrumentais** | Organização das medições por instrumento, tecla e corda; mapa físico, histórico, comparação de sessões, armazenamento e backups JSON. |
| **Curvas de afinação** | Otimização experimental para piano, fortepiano e cravo; análise de relações intervalares, edição de restrições, auditoria, histórico de versões e aplicação reversível de correções instrumentais. |
| **Emissor de notas** | Geração de referências sonoras, formas de onda periódicas, séries inarmônicas, reconstrução aditiva de espectros medidos e síntese de componentes personalizados. |

As ferramentas compartilham o contexto musical, mas possuem motores e configurações próprios. A interface adota informação progressiva: resultados essenciais permanecem acessíveis, enquanto evidências, parâmetros avançados e explicações detalhadas são apresentados sob demanda. O [guia de uso](GUIA_DE_USO.md) documenta os procedimentos, os controles, seus valores de referência e a interpretação dos resultados.

## Temperamentos e representação musical

O catálogo integrado contempla 18 sistemas, entre temperamentos históricos, reconstruções e divisões iguais da oitava:

| Grupo | Sistemas |
| --- | --- |
| Sistemas de referência | Pitagórico; Igual (12-TET) |
| Mesotônicos | 1/4, 1/5 e 1/6 de coma sintônico |
| Temperamentos circulantes | Kirnberger III; Werckmeister III e IV; Vallotti; Young II; Neidhardt — Kleine Stadt (1732) e Große Stadt (1724) |
| Reconstruções e hipóteses | Rameau (1726); d’Alembert (1752); Bach/Barnes (1979); Bach/Lehman (2005) |
| Divisões iguais alternativas | 13-EDO e 14-EDO |

O motor musical utiliza frações racionais independentes de coma pitagórico e sintônico, com verificação do fechamento dos ciclos de quintas. O **cilindro acústico de quintas**, em perspectiva 2,5D, e a matriz de intervalos representam a estrutura do temperamento, sem confundi-la com a resposta física do instrumento.

O catálogo distingue identidade de tecla, grafia enarmônica e coincidência de frequência. Teclados históricos de 12, 13 ou 14 teclas por oitava são tratados separadamente dos EDOs de 13 e 14 graus. Nos EDOs, a representação considera o gerador, suas órbitas e os ajustes individuais dos graus.

A referência musical é ajustável; o estado de fábrica utiliza o sistema Pitagórico com Lá4 = 415,3 Hz. A interface contempla notações científica e de Helmholtz, e a biblioteca pessoal conserva receitas musicais e referências em JSON. As fontes e ressalvas históricas dos presets são apresentadas no próprio aplicativo: reconstruções e atribuições controversas não são tratadas como práticas históricas inequivocamente comprovadas.

## Detecção de altura e processamento espectral

| Método | Princípio |
| --- | --- |
| YIN + FFT | Estimativa temporal de periodicidade por função de diferença cumulativa normalizada (CMNDF), com validação harmônica e refinamento espectral. |
| pYIN | Avaliação probabilística de candidatos e acompanhamento temporal por Viterbi causal, incluindo tratamento de transições de oitava. |
| SWIPE′ | Estimativa de saliência em múltiplas janelas espectrais, com kernels associados à fundamental e aos harmônicos de ordem prima. |
| Pico | Identificação da componente espectral predominante, que não necessariamente corresponde à fundamental. |

A faixa nominal de detecção de altura é de 16–4.600 Hz. A representação espectral e a busca de picos acústicos respeitam o limite de 24 kHz e a frequência de Nyquist. O espaçamento entre bins da FFT não equivale à precisão final de um estimador de frequência.

O detector opera principalmente sobre sons monofônicos. Acompanhamento temporal, histerese e filtragem da apresentação são tratados separadamente da edição da referência musical e da análise acústica instrumental.

## Análise acústica e inarmonicidade

A ferramenta de Parciais e inarmonicidade separa a família do instrumento da hipótese acústica empregada para interpretar as observações. Piano, Fortepiano e Cravo possuem políticas próprias; a categoria Outro permite investigar fontes distintas sem pressupor automaticamente seu modelo físico.

| Modelo acústico | Representação |
| --- | --- |
| Exploratório | Picos espectrais sem imposição de fundamental ou ordem harmônica. É o padrão de Outro. |
| Série harmônica | Frequência-base inferida, atribuição de ordens e desvios em relação à série. |
| Corda rígida | Estimativa experimental do coeficiente B em condições elegíveis de corda isolada. |
| Componentes não harmônicos | Inspeção de componentes sem obrigatoriedade de uma série de múltiplos inteiros. |

O modelo de corda rígida utiliza a relação `fₙ = n F √(1 + B n²)`, em que F é a escala de frequência ajustada e B é o coeficiente adimensional de inarmonicidade. A análise utiliza perda robusta de Huber em cents, critérios de qualidade espectral e temporal, e revisão explícita das observações.

Na consolidação multiataque, o motor estima um B comum, permitindo uma escala F própria por execução. A repetibilidade é investigada por reamostragem de ataques independentes (bootstrap), análise de resíduos e influência das execuções. Um bom ajuste não comprova, isoladamente, que os componentes pertençam à mesma corda, nem constitui uma determinação metrológica de B.

Os perfis mantêm o contexto acústico, a identificação física, os parâmetros utilizados, os resultados e suas revisões. Medições da família Outro não são fontes elegíveis para geração de curvas, ainda que apresentem B consistente.

## Curvas de afinação

O otimizador experimental é específico para **piano, fortepiano e cravo**, com políticas de ponderação intervalar próprias. A análise considera relações entre parciais de teclas diferentes, a base musical, a disponibilidade e qualidade das fontes, e restrições de preservação intervalar.

Há dois objetivos distintos: **fidelidade ao temperamento**, que procura conservar as características intervalares da receita, e **otimização acústica**, que privilegia a coincidência das componentes consideradas. O modelo contempla oitavas, duplas oitavas, quintas, quartas, duodécimas e, quando habilitadas, terças maiores e menores. Os pesos são hipóteses experimentais de projeto, não prescrições históricas universalmente válidas.

A frequência instrumental é composta com a referência teórica segundo `f_curva = f_teórica × 2^(δ/1200)`, onde δ representa a correção em cents. O motor mantém uma âncora fixa, limita as correções a ±30 cents e proíbe extrapolação. Interpolações dependem de suporte acústico e declaração de homogeneidade física.

As versões são auditáveis e podem ser comparadas e revisadas. A geração ou aprovação de uma revisão não modifica a afinação automaticamente. A aplicação experimental exige histórico local, fontes verificáveis, reprodução coerente do cálculo e confirmação explícita; pode ser invalidada por mudanças da base musical ou dos dados. Não é restaurada ao reiniciar a página.

Por padrão, o Afinador funciona com a referência teórica. Quando há uma curva aplicada, os alvos instrumentais são identificados na interface; teclas sem evidência suficiente conservam os alvos teóricos. O Emissor pode seguir opcionalmente a correção instrumental, sem modificar as frequências originais de uma reconstrução espectral. O cilindro e as tabelas de temperamento permanecem representações teóricas.

## Arquitetura técnica

O aplicativo é distribuído como um único arquivo HTML autocontido, com CSS, JavaScript, recursos visuais, código de Workers e binários WebAssembly incorporados. Não depende de serviços de terceiros ou bibliotecas carregadas de CDN durante a execução.

| Camada | Tecnologias e responsabilidades |
| --- | --- |
| Interface | HTML, CSS, JavaScript, Canvas 2D e SVG; layout responsivo e temas claro/escuro. |
| Áudio | Web Audio API e AudioWorklet para captura e síntese. |
| DSP do Afinador | Web Worker dedicado, FFT PFFFT em WebAssembly SIMD128 ou escalar, planos reutilizáveis e fallback nativo nos caminhos compatíveis. SWIPE′ exige PFFFT/WASM. |
| Análise instrumental | Motor separado de aquisição e análise multiataque, FFT radix-2 em JavaScript, janela Hann, interpolação de picos, ajuste robusto e consolidação estatística. |
| Motor musical | Catálogo canônico de frequências, motor racional de temperamentos e representação de teclas e graus. |
| Otimização | Construção de curvas, restrições, auditoria dos intervalos e verificação de consistência das versões. |
| Persistência | `localStorage` para preferências e biblioteca; IndexedDB para perfis instrumentais e históricos de curvas. |
| Segurança | CSP, validação de importações e WebCrypto/SHA-256 para verificações de integridade. |

O porte de SWIPE′ realiza análise causal de buffers incrementais, em vez de processamento de arquivos de áudio completos. O caminho acústico de Parciais é independente do detector de altura e não passa a executar continuamente durante a afinação convencional.

## Compatibilidade

O projeto requer navegador moderno com JavaScript habilitado. A aquisição depende de permissão de microfone e contexto seguro (HTTPS ou `localhost`). Web Workers, AudioWorklet, WebAssembly, WebCrypto e armazenamento local são necessários conforme os recursos utilizados. SIMD128 não é indispensável quando a variante escalar é suportada.

A distribuição publicada é hospedada no GitHub Pages. O HTML não exige etapa de compilação para ser servido; a abertura direta por `file://` pode restringir APIs e não garante funcionamento integral. A compatibilidade varia entre navegadores e dispositivos; o funcionamento offline depende de uma cópia local acessível.

## Privacidade, dados e segurança

O áudio é captado por autorização explícita e processado no dispositivo. Não há transmissão automática das amostras, medições ou perfis para um serviço remoto de análise. O armazenamento é local à origem do site e ao navegador, sem sincronização por conta.

O projeto possui monitor de diagnóstico com sessões limitadas a 20 segundos e exportação local de ZIP, incluindo dados técnicos e WAV opcional. Arquivos de diagnóstico podem conter áudio ambiente ou informações privadas. Os backups JSON permitem conservar independentemente receitas musicais, sessões, perfis e históricos.

As importações passam por verificações de estrutura, tamanho, coerência e integridade aplicáveis. A Content Security Policy restringe scripts não autorizados, conexões externas e outros recursos. SHA-256 verifica integridade em relação ao conteúdo esperado, não autoria, autenticidade da captação ou validade científica. Essas medidas não representam uma certificação de segurança.

## Estado de validação e limitações

O projeto permanece experimental. A qualidade das estimativas depende do instrumento, do microfone, da taxa de amostragem, do ruído, da estabilidade do sinal e das hipóteses acústicas. Não há garantia de erro universal em cents, de incerteza física calibrada de B ou de adequação de uma curva a qualquer instrumento.

Os testes computacionais realizados ao longo do desenvolvimento incluem regressões de detecção, catálogo musical, análise acústica, configurações, síntese, validadores de importação e CSP. O trabalho mais recente contempla a separação de famílias e modelos acústicos, sem substituir a necessidade de ensaios com instrumentos físicos. A validação metrológica, a cobertura integral de aparelhos móveis e a auditoria independente de segurança permanecem pendentes.

A aplicação de curvas não representa homologação de um procedimento de afinação. A síntese aditiva de espectros medidos é uma aproximação de frequências e amplitudes, não uma reprodução da fase, do ruído, dos transientes ou da evolução temporal do som original.

## Organização do repositório

| Caminho | Conteúdo |
| --- | --- |
| [`index.html`](index.html) | Aplicativo autocontido e ponto de entrada da publicação. |
| [`GUIA_DE_USO.md`](GUIA_DE_USO.md) | Manual completo, procedimentos, configurações, interpretação e troubleshooting. |
| [`README.md`](README.md) | Apresentação do projeto e documentação técnica geral. |
| [`Aulas/`](Aulas/) | Diretório de materiais do repositório. |
| [`LICENSE`](LICENSE) | Licença do código próprio do projeto. |

## Créditos e código de terceiros

A autoria dos métodos científicos é distinta da autoria das implementações de software. Os componentes incorporados abaixo conservam suas licenças e avisos de copyright.

### PFFFT — Pretty Fast FFT / WebAssembly

- **Autoria:** Julien Pommier, copyright © 2013.
- **Origem:** FFTPACKv4, código Fortran de Paul Swarztrauber (NCAR, 1985).
- **Licença:** FFTPACK/UCAR, com copyright © 2004 University Corporation for Atmospheric Research (UCAR), conforme os avisos originais de PFFFT.
- **Fontes:** [arquivo do projeto original PFFFT](https://github.com/source-archive/pffft) · [FFTPACK no Netlib](https://www.netlib.org/fftpack/).

A adaptação para o Afinador compreende compilação do núcleo para WebAssembly SIMD128 e escalar, adaptação de macros SIMD, wrapper C de FFT real, reaproveitamento de planos, tratamento de DC/Nyquist, ponte JavaScript e integração com o Worker. A licença integral é mantida no bloco `licencaPFFFTEtapa2` do `index.html`. A adaptação e os binários não substituem nem anulam a autoria e as condições de redistribuição do código original.

### SWIPE′ — Sawtooth Waveform Inspired Pitch Estimator

- **Método científico:** Arturo Camacho, tese de doutorado (2007); Arturo Camacho e John G. Harris, artigo de 2008.
- **Implementação de origem:** SWIPE′ v1.5 em C por Kyle Gorman, copyright © 2009–2013.
- **Licença do código de Gorman:** MIT.
- **Fonte:** [kylebgorman/swipe](https://github.com/kylebgorman/swipe), incluindo `swipe.c`, `vector.c` e referências à implementação MATLAB de Camacho.

O Afinador contém um porte causal em JavaScript, adaptado para Web Worker, com FFTs calculadas por PFFFT/WASM. A adaptação preserva os princípios multijanela, a grade de candidatos, a escala ERB, os kernels com harmônicos de ordem 1 e prima e o refinamento do estimador. Substitui o processamento offline por buffers incrementais, reamostragem quando necessária e reutilização de kernels e planos. O resultado causal não é necessariamente idêntico ao programa offline original, em especial nos transientes e bordas temporais.

O código adaptado está no bloco `fonteSWIPEOriginalAdaptado`, e a licença integral de Gorman em `licencaSWIPEGormanMIT`, ambos no `index.html`. FFTW e libsndfile, dependências da implementação C original, não constituem dependências de execução desse porte.

## Referências científicas

As referências a seguir fundamentam os métodos empregados; não significam que o projeto incorpore ou reproduza integralmente os programas dos autores.

- DE CHEVEIGNÉ, A.; KAWAHARA, H. (2002). *YIN, a fundamental frequency estimator for speech and music*. Journal of the Acoustical Society of America, 111(4), 1917–1930.
- MAUCH, M.; DIXON, S. (2014). *pYIN: A Fundamental Frequency Estimator Using Probabilistic Threshold Distributions*. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP).
- CAMACHO, A. (2007). *A sawtooth waveform inspired pitch estimator for speech and music*. Tese de doutorado, University of Florida.
- CAMACHO, A.; HARRIS, J. G. (2008). *A sawtooth waveform inspired pitch estimator for speech and music*. Journal of the Acoustical Society of America. [DOI: 10.1121/1.2951592](https://doi.org/10.1121/1.2951592).
- FLETCHER, H. (1964). *Normal Vibration Frequencies of a Stiff Piano String*. Journal of the Acoustical Society of America, 36, 203–209.
- HUBER, P. J. (1964). *Robust Estimation of a Location Parameter*. Annals of Mathematical Statistics.
- EFRON, B. (1979). *Bootstrap Methods: Another Look at the Jackknife*. Annals of Statistics.

As implementações de YIN e pYIN no Afinador incluem decisões próprias de integração, causalidade e desempenho. As referências históricas específicas dos temperamentos são mantidas junto aos presets no aplicativo.

## Contribuições e suporte

Relatos de problemas, sugestões e contribuições podem ser encaminhados pelos [Issues](https://github.com/mv-pereira/Afinador/issues) e [Pull Requests](https://github.com/mv-pereira/Afinador/pulls) do repositório. Informações sobre navegador, dispositivo, versão do arquivo, contexto musical, detector e condições de captação facilitam a reprodução de problemas. O [guia de uso](GUIA_DE_USO.md#relatos) apresenta orientações para preservar e compartilhar evidências.

Mudanças em DSP, catálogo musical, políticas acústicas e formatos de dados devem ser acompanhadas por testes de regressão. Alterações dos scripts incorporados exigem a atualização dos respectivos hashes da CSP; as licenças de terceiros devem permanecer intactas nas redistribuições.

## Licença e autoria

Copyright © 2026 Mario Victor da Rocha Pereira — Oficina Pernambuco.

O código próprio é distribuído sob a [licença MIT](LICENSE). Os componentes de terceiros permanecem sujeitos às respectivas licenças e condições de atribuição e redistribuição. A licença do software não implica autorização automática de uso da identidade visual da Oficina Pernambuco.

O software é disponibilizado sem garantias, nos termos das licenças aplicáveis.
