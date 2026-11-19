# Guia de uso — Afinador · Oficina Pernambuco

**[Abrir o Afinador](https://mv-pereira.github.io/Afinador/)** · [README do projeto](README.md)

Este manual corresponde ao HTML da **Etapa 18 — Simplificação das famílias instrumentais e seleção explícita do modelo acústico**, incluindo a ajuda contextual das etapas 16 e 16.5 e as curvas experimentais da Etapa 17, em português do Brasil. Abrange as cinco ferramentas, seus controles, a interpretação dos resultados e a resolução de problemas. Se a página publicada apresentar controles diferentes, confira se está usando a versão correspondente a este guia.

> **Importante:** o afinador convencional permite comparar uma nota com uma referência musical. As medições de inarmonicidade, os ajustes físicos e as curvas instrumentais são experimentais e ainda não foram homologados fisicamente. Uma revisão aprovada de piano, fortepiano ou cravo pode ser aplicada experimentalmente aos alvos do Afinador, após armazenamento local, revalidação das fontes, reprodução do cálculo e confirmação explícita. Isso não constitui homologação física nem recomendação universal de afinação.

<a name="sumario"></a>
## Sumário

- [Capítulo 0 — Panorama e preparação](#cap-0): [qual ferramenta usar](#escolha), [primeiro acesso](#preparacao), [configurações](#configuracoes), [ajuda contextual](#ajuda-contextual), [dados e privacidade](#dados).
- [Capítulo 1 — Afinador](#cap-1): [afinar uma nota](#afinar), [correção instrumental](#correcao-afinador), [detectores](#detectores), [FFT](#fft), [temperamentos](#temperamentos), [cilindro e edição](#cilindro), [teclados e EDO](#teclados), [biblioteca](#biblioteca), [configurações](#cfg-1), [diagnóstico](#diagnostico), [troubleshooting](#ts-1).
- [Capítulo 2 — Parciais e inarmonicidade](#cap-2): [modelos por instrumento](#modelos), [captura individual](#captura-individual), [multiataque](#multiataque), [interpretar parciais](#interpretar-parciais), [coeficiente B](#coeficiente-b), [consolidação](#consolidacao), [configurações](#cfg-2), [troubleshooting](#ts-2).
- [Capítulo 3 — Perfis instrumentais](#cap-3): [criar perfil](#criar-perfil), [salvar sessões](#salvar-sessoes), [consultar e comparar](#comparar-sessoes), [backup](#backup-perfil), [configurações](#cfg-3), [troubleshooting](#ts-3).
- [Capítulo 4 — Curvas de afinação](#cap-4): [pré-requisitos](#pre-curva), [gerar prévia](#gerar-curva), [interpretação](#ler-curva), [revisões](#revisar-curva), [histórico](#historico-curva), [aplicação experimental](#aplicar-curva), [configurações](#cfg-4), [troubleshooting](#ts-4).
- [Capítulo 5 — Emissor de notas](#cap-5): [emitir](#emitir), [síntese aditiva](#sintese), [espectro medido](#reconstrucao), [espectro personalizado](#personalizado), [configurações](#cfg-5), [troubleshooting](#ts-5).
- [Apêndice A — Glossário](#glossario) · [Apêndice B — Relatar problemas e preservar dados](#relatos).

<a name="cap-0"></a>
# Capítulo 0 — Panorama e preparação

<a name="escolha"></a>
## 0.1. O que cada ferramenta faz

Abra **Ferramentas** na barra superior e selecione o ambiente de trabalho desejado. O botão **Configurações** acompanha a ferramenta ativa. Não há uma aba de configurações gerais; o tema é um controle independente.

| Ferramenta | Pergunta que responde | Entrada | Saída |
| --- | --- | --- | --- |
| Afinador | A nota está acima ou abaixo da afinação desejada? | Som isolado e referência musical | Frequência, nota ou grau e desvio em cents; espectro; representação do temperamento |
| Parciais e inarmonicidade | Quais componentes existem no som? Eles obedecem a uma série ou a um modelo físico? | Uma captura ou repetições da mesma nota | Picos, parciais, evidências de qualidade, ajuste experimental de B quando elegível |
| Perfis instrumentais | Como conservar e comparar as medições do meu instrumento? | Sessões finalizadas e identificação física | Histórico local, mapa de teclas, comparações e backups JSON |
| Curvas de afinação | Que correções poderiam conciliar as propriedades de piano, fortepiano ou cravo com uma afinação escolhida? | Perfil instrumental elegível, referência musical e objetivos | Prévia, auditoria, revisões e aplicação experimental reversível |
| Emissor de notas | Como soa uma frequência, uma série de parciais ou uma reconstrução sintética? | Nota-alvo, parâmetros de síntese ou medição | Som gerado e inspeção do espectro sintético |

Não é necessário atravessar todas as ferramentas. Para afinar um violão, por exemplo, basta o Afinador. Para estudar uma flauta, use Parciais → Outro → Série harmônica; para repetir a experiência em outro dia, use também Perfis. O Emissor pode ser usado sozinho, sem microfone. As Curvas exigem uma preparação acústica muito mais rigorosa do que a afinação convencional.

### Fluxos de trabalho recomendados

| Finalidade | Percurso |
| --- | --- |
| Afinação habitual | Afinador → referência → detector → nota → ajuste físico |
| Estudo de um temperamento histórico | Afinador → preset → cilindro/matriz → biblioteca → Emissor |
| Investigar um timbre | Parciais → captura individual ou multiataque → inspeção → Emissor (opcional) |
| Investigar repetibilidade de uma corda | Parciais → multiataque → confirmar tecla e corda → revisar → salvar em Perfis → comparar em outra sessão |
| Estudo de curva de piano, fortepiano ou cravo | Preparar referência, registro e mapa → medir cordas isoladas → guardar perfis → Curvas → gerar prévia → revisar e exportar |
| Aplicar uma curva experimental | Curvas → aprovar revisão → guardar histórico local → aplicar experimentalmente → confirmar → Afinador; desligar quando necessário |

### O que é compartilhado e o que é independente

A referência musical (temperamento, teclas, ajustes e frequência de referência) fornece os alvos teóricos do Afinador e do Emissor e o contexto para identificar medições. Alterá-la não modifica o som que já foi registrado. Uma sessão acústica conserva seu contexto original; uma curva depende de uma base musical compatível. A referência teórica é o padrão; uma curva aplicada modifica somente os alvos instrumentais, não a receita de temperamento. O Emissor começa sem seguir a correção. O detector de frequência, a análise de parciais, a otimização de curvas e o sintetizador são processos diferentes.

<a name="preparacao"></a>
## 0.2. Primeiro acesso e preparação

1. Acesse o [aplicativo publicado](https://mv-pereira.github.io/Afinador/) em um navegador moderno com JavaScript habilitado.
2. Para medir som, pressione **Ativar microfone** e autorize a captura. Para apenas estudar temperamentos, consultar perfis, calcular curvas ou emitir notas, não é necessário ligar o microfone.
3. Escolha a ferramenta e confira a referência musical na área de seleção de temperamento quando pertinente. O padrão musical de fábrica do Afinador é o sistema Pitagórico com Lá4 = 415,3 Hz; não presuma que seja o temperamento igual a 440 Hz.
4. Posicione o instrumento e o dispositivo de modo a obter um som claro, sem saturação. Evite TV, ventilador, conversas, outros instrumentos e reverberação excessiva.
5. Toque uma nota isolada. Aguarde uma leitura útil antes de ajustar o instrumento ou interpretar a análise.
6. Ao terminar de medir, desligue o microfone no botão superior. Ao terminar de ouvir, pressione **Parar som** no Emissor.

O acesso ao microfone depende de permissão do navegador e de contexto seguro (HTTPS ou localhost). Um HTML aberto diretamente do disco pode funcionar parcialmente; não é garantido que todas as APIs de captura, integridade e armazenamento estejam disponíveis. Abrir por HTTP através do endereço IP de outro computador também pode impedir a captura. Consulte o [README](README.md) para execução local.

### Boas práticas de captação

- Escolha uma distância que não sature o microfone e não deixe o som desaparecer no ruído; mantenha posição, orientação e intensidade semelhantes ao comparar registros.
- Evite tocar acordes para o detector de altura. Para analisar uma nota composta por várias cordas, declare a condição real; não declare uma corda isolada se outras vibram.
- Em instrumentos de sopro, mantenha dedilhado, embocadura e intensidade controlados. Em cordas e percussão, repita técnica e ponto de excitação.
- Mantenha a página em primeiro plano durante uma sessão; navegadores móveis podem suspender o áudio em segundo plano.
- Não emita som pelo alto-falante enquanto mede o instrumento. Fones podem reduzir a contaminação acústica, mas a síntese não substitui um padrão físico calibrado.

<a name="configuracoes"></a>
## 0.3. Configurações, salvamento e restauração

Em cada ferramenta, pressione **⚙ Configurações**. Grupos simples começam expandidos; grupos avançados começam recolhidos. Abra um grupo para ver seus parâmetros e a indicação do padrão original.

| Ação | Efeito nesta visita | Efeito na próxima inicialização |
| --- | --- | --- |
| Alterar um campo válido | Aplica a preferência; nos campos numéricos, confirme a edição ou saia do campo | Não muda por si só o registro salvo |
| Salvar alterações | Mantém os valores em uso, sem um reset adicional | Grava as preferências da ferramenta |
| Fechar | Fecha a janela, mantendo alterações válidas | Não salva nem restaura |
| Restaurar padrões | Após confirmação, aplica os valores de fábrica | Sobrescreve o registro salvo; não precisa salvar outra vez |

Valores inválidos ou conjuntos incompatíveis não substituem os últimos valores válidos. Leia a mensagem da janela, corrija os campos ou restaure os padrões. Se o navegador não permitir gravar, as mudanças podem funcionar somente nesta visita.

Há exceções propositais à aplicação imediata: os parâmetros de aquisição e análise em Parciais são fixados no início da sessão; novas preferências valem para a próxima. Em Curvas, mudanças de otimização valem no novo cálculo, não alterando resultados anteriores. As preferências visuais não reinicializam detectores. Durante um diagnóstico ativo, finalize-o antes de modificar as configurações do Afinador.

**Restaurar padrões não é apagar dados.** O comando atua apenas na ferramenta aberta. Não restaura o temperamento, não exclui medições ou históricos e não apaga preferências das outras ferramentas. Há comandos próprios para restaurar a receita musical e para gerenciar registros.

<a name="ajuda-contextual"></a>
## 0.4. Ajuda contextual

O botão **Ajuda** acompanha a ferramenta ativa. A **Ajuda rápida** apresenta o procedimento essencial; abra **Ajuda avançada** e seus capítulos recolhíveis para detalhes, fundamentos, parâmetros, glossário e problemas comuns. Feche pelo controle **Fechar ×**. A consulta não inicia microfone, emissão ou cálculo. A ajuda incorporada funciona sem rede; os links para o capítulo completo deste guia e para tabelas de parâmetros abrem o GitHub e exigem conexão.

<a name="dados"></a>
## 0.5. Armazenamento, privacidade e arquivos

O processamento ocorre no navegador. O aplicativo não envia automaticamente as amostras de áudio ou as medições a um servidor. As preferências e a biblioteca musical são locais; perfis e históricos de curvas usam o banco de dados do navegador (IndexedDB). Navegação privada, limpeza de dados do site, alteração de endereço e troca de aparelho podem tornar esses registros indisponíveis. Salvar no navegador não é fazer um backup externo.

| Arquivo | Finalidade | Onde nasce |
| --- | --- | --- |
| JSON de afinação | Receita musical e disposição das teclas | Biblioteca pessoal |
| JSON de perfil musical | Receita e frequência de referência, com identificação opcional de instrumento | Biblioteca pessoal |
| JSON de análise individual | Observações acústicas de uma captura | Parciais |
| JSON de sessão | Execuções, evidências, configuração, revisões e resultados da sessão | Parciais/Perfis |
| JSON de perfil instrumental | Instrumento, mapa físico e registros acústicos | Perfis |
| JSON de prévia/histórico de curvas | Correções, origens e versões experimentais | Curvas |
| ZIP de diagnóstico | `diagnostico.json` e, opcionalmente, `audio.wav` | Afinador |

Não confunda o **perfil musical** (receita de afinação) com o **perfil instrumental** (coleção de medições de um instrumento físico). Abra os arquivos na ferramenta correspondente; o aplicativo não é um importador genérico de escalas, WAV ou outros formatos. As importações válidas passam por verificação de estrutura, limites e coerência. Nesta etapa, novas sessões usam o contexto acústico de versão 2 e as quatro famílias atuais; não se garante compatibilidade com arquivos acústicos anteriores. Não converta famílias, modelos ou hashes manualmente. Essa restrição não significa que os arquivos musicais independentes tenham mudado de formato. Um hash SHA-256 confere integridade, não autoria nem veracidade da captação. Nunca substitua o HTML por cópia desconhecida ou desative proteções para abrir um arquivo recusado.

[Voltar ao sumário](#sumario)

<a name="cap-1"></a>
# Capítulo 1 — Afinador

A ferramenta convencional estima a altura de um som e a compara com um alvo musical. É possível utilizá-la tanto em uma afinação cromática usual quanto em temperamentos históricos e divisões iguais alternativas.

<a name="afinar"></a>
## 1.1. Como afinar uma nota

1. Selecione **Ferramentas → Afinador**.
2. Escolha o **Temperamento** e a frequência de **Lá de referência (A4)** na barra inferior. Para a afinação moderna usual, selecione **Igual (-1/12 c.p.)** e 440 Hz, se isso corresponder ao instrumento ou conjunto.
3. Ative o microfone e selecione **YIN + FFT**, o detector padrão.
4. Escolha **Automático** ou **Nota fixa** no seletor de modo.
5. Toque uma nota isolada e sustente-a, ou deixe a corda soar naturalmente. Observe a estabilidade da frequência e do nome apresentado.
6. Ajuste a altura física do instrumento, respeitando o procedimento próprio dele, até aproximar o desvio de zero. Faça uma nova leitura após o ajuste.

Não force a tensão de uma corda, a posição de uma chave ou a pressão do som para perseguir oscilações momentâneas. Num instrumento histórico, verifique primeiro a altura de referência e os limites de tensão adequados.

### O que o mostrador significa

| Informação | Significado |
| --- | --- |
| Frequência estimada (Hz) | Rapidez da repetição acústica encontrada pelo detector; pode ficar indisponível em sinal insuficiente |
| Nota ou grau | Identificação musical segundo o catálogo atual; não é uma medição direta da tecla física |
| Desvio em cents (¢) | Distância relativa entre a frequência estimada e a referência escolhida |
| Desvio negativo | Som abaixo do alvo (grave) |
| Desvio positivo | Som acima do alvo (agudo) |
| Zero | Coincidência com o alvo dentro da leitura apresentada, não certificação metrológica |

Um cent é 1/1200 de oitava; no igual de 12 divisões há 100 cents por semitom. A fórmula é `1200 × log₂(f medida / f alvo)`. Por exemplo, se o alvo é 440 Hz, 442 Hz representa aproximadamente +7,85 cents. A mesma diferença de 2 Hz representa mais cents numa nota grave que numa aguda. Em temperamentos desiguais e EDOs alternativos, não suponha que cada passo físico tenha 100 cents.

### Automático e Nota fixa

**Automático** escolhe um alvo compatível com a frequência detectada. Use para percorrer notas sucessivas sem selecionar cada uma. Uma frequência entre duas referências pode provocar mudança de nome; uma enarmonia acusticamente coincidente não informa qual tecla física foi usada.

**Nota fixa** mantém o alvo escolhido, mesmo quando o som se desvia. É indicada para ajustar uma corda específica, conferir um instrumento com teclas divididas ou evitar que o alvo mude durante a afinação. Escolha a tecla física no seletor quando disponível. Os botões internos `<` e `>` percorrem alvos adjacentes; os externos `« 8ª` e `» 8ª` mudam de oitava sem trocar a identidade da tecla. Nos limites do catálogo, não há alvo adicional. Para EDOs, um passo adjacente corresponde a um grau, não a um semitom convencional.

Pressione o botão da nota para alternar o destaque entre notação científica (ex.: A4/Lá4) e notação de Helmholtz (ex.: a′). O formato alternativo permanece menor. Isso muda somente a apresentação. Graus sem grafia musical tradicional não precisam de uma notação de Helmholtz inventada.

<a name="correcao-afinador"></a>
### Referência teórica e correção instrumental experimental

Por padrão, o Afinador usa apenas a referência teórica e não mostra um painel de curva nem um botão para abrir Curvas. Para gerar ou aplicar uma curva, vá deliberadamente a **Ferramentas → Curvas de afinação** e siga [4.5](#aplicar-curva). Uma prévia ou aprovação não modifica a afinação.

Quando uma curva estiver efetivamente aplicada, aparece o painel **Correção instrumental EXPERIMENTAL**, com identificação do perfil, família, registro quando informado, versão, temperamento, referência e objetivo. A leitura da tecla distingue frequência teórica, frequência instrumental e correção Δ em cents; **Intervalos afetados** resume os pares alterados e as teclas sem evidência. O desvio do Afinador passa a referir-se ao alvo efetivo. Teclas sem correção suportada e fora do mapa permanecem teóricas. Coincidências acústicas efetivas podem exigir a escolha da tecla física.

**Desligar correção** retorna aos alvos teóricos e oculta o painel. A correção também é desligada quando a base musical é republicada ou os dados de perfis/curvas são modificados; quando disponível, a comunicação entre abas detecta alterações em outra aba. A aplicação não é restaurada automaticamente ao reabrir a página. O cilindro e as tabelas de temperamento continuam teóricos. Confira o painel sempre que pretender trabalhar com uma curva.

<a name="detectores"></a>
## 1.2. Métodos de detecção de altura

Selecione diretamente um dos quatro botões sob o título **Espectro FFT**. Somente o detector escolhido atua como detector de altura por quadro.

| Método | Princípio | Quando experimentar | Limitações |
| --- | --- | --- | --- |
| YIN + FFT | Procura repetição da forma de onda, verifica evidências harmônicas e refina a frequência com o espectro | Primeira escolha para vozes e instrumentos monofônicos | Pode errar oitava ou ficar inconclusivo; depende do sinal |
| pYIN | Avalia vários candidatos de periodicidade e acompanha a sequência ao longo do tempo | Quando uma nota sustentada apresenta saltos espúrios | A continuidade pode retardar uma mudança verdadeira; custo adicional |
| SWIPE′ | Busca padrões espectrais harmônicos com várias janelas | Timbres em que a fundamental não domina o espectro; comparação com estimadores temporais | Mais exigente; requer PFFFT/WebAssembly; não é um detector universal de acordes |
| Pico | Seleciona o componente espectral predominante | Inspecionar uma senoide ou localizar a componente mais intensa | Pode retornar um harmônico, não a fundamental (aviso em vermelho claro) |

A implementação YIN + FFT integra o refinamento adaptativo abaixo de 350 Hz, com estratégia conservadora a partir de 350 Hz. Não há botão para operar YIN puro. As janelas temporais de YIN/pYIN e as janelas multiespectrais do SWIPE′ são administradas pelo motor e não equivalem ao seletor de pontos da FFT principal.

Exemplo: uma nota de 220 Hz pode ter um segundo harmônico de 440 Hz mais intenso que a fundamental. O modo Pico pode indicar 440 Hz, enquanto um detector de periodicidade pode encontrar 220 Hz. Isso não representa necessariamente defeito do microfone. Compare os métodos em condições equivalentes e verifique o espectro; não suponha que o resultado que parece mais estável seja sempre o correto.

### Leitura bruta e filtrada

**Bruta** mostra a saída do detector sem suavização adicional do medidor. O método pode possuir acompanhamento próprio, como o pYIN. **Filtrada** suaviza a leitura temporal para reduzir oscilações visuais; quanto maior a intensidade, maior a tendência de amortecer variações, com possível atraso. Para estudar resposta a uma troca de nota ou um erro de oitava, prefira a leitura bruta. A suavização não corrige um detector que escolheu a fundamental errada.

<a name="fft"></a>
## 1.3. Espectro FFT, escalas e zoom

O gráfico mostra a distribuição de componentes em frequência. Na horizontal há Hz; na vertical, magnitude em dB segundo a representação do espectro. Um pico indica energia de uma componente naquela região. A leitura dos detectores não é obtida simplesmente contando os pixels do gráfico.

- **Logarítmica:** padrão; oitavas ocupam distâncias horizontais iguais, favorecendo a leitura do registro grave e de uma grande faixa de frequências.
- **Linear:** distâncias iguais em Hz ocupam espaços iguais; facilita ver espaçamento regular entre harmônicos.
- **Zoom na nota-alvo (±100 cents):** aproxima a região do alvo para inspeção local. Desmarque para retornar à visão geral.

O gráfico usa o teto de 24.000 Hz ou a frequência de Nyquist da captura, a que for menor. A 44,1 kHz o teto efetivo é 22.050 Hz; a 48 kHz, 24.000 Hz. Isso não significa que o microfone tenha resposta plana até o teto. O limite inferior da escala logarítmica é positivo (16 Hz); a detecção possui sua própria faixa nominal de 16–4.600 Hz. Frequências superiores podem aparecer como componentes espectrais, não como alvos de altura do detector. Não existe mais o campo **Máx. gráfico**.

A resolução visual é adaptada aos pixels disponíveis, preservando os máximos de grupos de bins. O zoom e a escala não reinicializam o DSP. Eles não aumentam a resolução física da captura.

### Pontos de FFT e resolução

| Pontos | Bins analisados | Espaçamento aproximado a 48 kHz | Janela nominal a 48 kHz |
| ---: | ---: | ---: | ---: |
| 4.096 | 2.048 | 11,72 Hz | 85 ms |
| 8.192 | 4.096 | 5,86 Hz | 171 ms |
| 16.384 | 8.192 | 2,93 Hz | 341 ms |
| 32.768 | 16.384 | 1,46 Hz | 683 ms |

O espaçamento entre bins é `taxa de amostragem / pontos FFT`. A janela Blackman usada no espectro convencional reduz vazamento espectral, com compromisso na largura dos picos. A duração acima não é a latência total, e o espaçamento não é a precisão final em Hz: interpolação e métodos temporais podem estimar frequências entre bins. Mais pontos custam processamento e podem piorar a resposta a mudanças rápidas. Comece com 8.192; reduza se o aparelho estiver lento, aumente para investigar componentes próximas e sustentadas. A FFT acústica da ferramenta de Parciais é independente dessa configuração.

<a name="temperamentos"></a>
## 1.4. Referência musical e catálogo de temperamentos

O Lá4 de referência (300–500 Hz na interface histórica) determina a escala absoluta das frequências. Mudar de 415,3 para 440 Hz não altera a receita relativa dos intervalos. Nos EDOs há referência própria por grau e oitava. A4 = 415,3 Hz é uma escolha de fábrica próxima de um semitom abaixo de 440 Hz, não uma altura universal da música antiga.

Uma quinta pura tem razão 3:2 e mede cerca de 701,955 cents. Doze quintas puras excedem sete oitavas em cerca de 23,460 cents: o coma pitagórico (c.p.). Quatro quintas puras reduzidas à oitava dão uma terça maior de 81:64, mais larga que a terça pura 5:4 em cerca de 21,506 cents: o coma sintônico (c.s.). Os temperamentos distribuem essas diferenças de maneiras distintas. Os comas não são intercambiáveis.

| Sistema disponível | Característica para estudo |
| --- | --- |
| Pitagórico | Cadeia de quintas puras; lobo no fechamento convencional |
| Igual (-1/12 c.p.) | Doze quintas de 700 cents; semitons iguais |
| Mesotônico 1/4 c.s. | Quintas estreitas e terças maiores puras na cadeia regular |
| Mesotônico 1/5 c.s. | Quintas menos estreitas; compromisso diferente nas terças |
| Mesotônico 1/6 c.s. | Outra redução regular; não confundir com Vallotti |
| Kirnberger III (1779) | Ciclo com redução de quatro quintas por c.s. e compensação |
| Werckmeister III (1691) | Ciclo com quatro quintas estreitadas por c.p. |
| Werckmeister IV | Distribuição com quintas estreitas e largas |
| Vallotti (1754, rótulo do preset) | Seis quintas reduzidas em 1/6 c.p.; seis puras |
| Young II (1800) | Seis reduções de 1/6 c.p. em outra região do ciclo |
| Neidhardt – Kleine Stadt (1732) | Variante histórica identificada pela edição |
| Neidhardt – Große Stadt (1724) | Variante distinta da anterior |
| Rameau 1726 — reconstrução | Receita interpretativa de tradição francesa |
| d’Alembert 1752 — reconstrução | Outra reconstrução de tradição francesa |
| Bach/Barnes (1979) | Hipótese moderna associada a Bach |
| Bach/Lehman (2005) | Hipótese moderna de atribuição controversa |
| 13-EDO | Oitava com 13 graus iguais na receita-base |
| 14-EDO | Oitava com 14 graus iguais na receita-base |

A escolha depende do instrumento, repertório e finalidade. Abra **Fontes, variante e atribuição deste temperamento** para consultar a documentação do preset. Uma reconstrução não é uma receita histórica inequivocamente comprovada. Não confunda um preset escolhido com a afinação já existente no instrumento.

<a name="cilindro"></a>
## 1.5. Cilindro acústico, frações e matriz de intervalos

O **Cilindro acústico · quintas** representa relações em perspectiva 2,5D. A posição angular acompanha a ordem das quintas (ou o gerador dos EDOs); a altura representa o desvio acumulado comparado com a quinta de referência. Nos ciclos históricos a referência é 700 cents; no EDO é o intervalo-base do gerador. A perspectiva, o espaçamento aparente entre pontos e eventuais deslocamentos de rótulos não são uma medida independente de frequência.

É possível distinguir uma cadeia aberta (como a mesotônica) de um ciclo fechado (como Vallotti). A quinta do lobo é a relação residual entre extremos quando o teclado condensa uma cadeia em doze teclas; ela não constitui a regra regular das extensões. O fechamento de um ciclo exige exatamente sete oitavas ao percorrer doze quintas.

### Editar uma receita histórica

1. Escolha o preset mais próximo do compromisso musical desejado.
2. Abra **Tabela de ajuste de comas**. Cada quinta dispõe de frações independentes de c.p. e c.s. Use valores exatos, como `-1/4`, `0` ou `1/6`; decimais finitos são aceitos dentro dos limites do motor (até nove casas decimais).
3. Em um ciclo de doze quintas, selecione a **Quinta compensatória (ao editar um ciclo)**. Ela absorve a alteração necessária ao fechamento. A soma dos coeficientes de c.p. deve ser −1, e a de c.s., 0. Por isso, mudar uma quinta pode também mudar a compensatória.
4. Observe a disposição, as larguras individuais e a **Tabela de intervalos - Desvios** antes de utilizar a nova afinação. Para teclas adicionais, use **Editar quintas adicionais · c.p. e c.s.** quando disponível.
5. Guarde uma cópia na biblioteca se precisar reaproveitar a receita. **Zerar ajustes** restaura os ajustes da receita do preset; não é um comando para tornar todas as quintas puras. **Restaurar preset original**, na biblioteca, é a ação de voltar à definição original do preset.

Um decimal aproximado como `-0,083333333` não é exatamente −1/12. O motor racional rejeita frações inválidas, denominador zero e valores além de seus limites. Não arredonde manualmente todas as quintas esperando fechamento perfeito. Uma receita inválida não deve substituir a última publicação válida.

### Ler a tabela de intervalos

Consulte a **Tabela de intervalos - Desvios** para identificar o erro de um intervalo relativamente à razão pura usada como comparação. Uma terça com +13,686 cents, por exemplo, é mais larga que a terça pura de 5:4; não indica que a nota superior esteja necessariamente desafinada de seu próprio temperamento. Em EDOs, selecione o **Grau inicial** da matriz quando disponível; a comparação usa graus e razões, sem exigir nomes cromáticos.

Para ouvir diferenças, compare notas no [Emissor](#cap-5). Para medir os componentes que produzem batimentos num instrumento, recorra a [Parciais](#cap-2). O cilindro e as tabelas representam a receita teórica, não uma medição de cordas reais.

<a name="teclados"></a>
## 1.6. Teclados históricos ampliados e EDOs

No domínio histórico, **Teclas por oitava** permite 12, 13 ou 14 teclas. As ampliações podem separar Ré♯/Mi♭ e Sol♯/Lá♭; o botão de alternância enarmônica e o seletor **Grafia enarmônica** controlam as variantes apresentadas. Confira os nomes exibidos antes de escolher a tecla-alvo. **Desfazer disposição** volta à disposição anterior quando disponível.

Uma tecla adicional não necessariamente cria uma nova frequência. No igual de doze divisões, as extensões inicialmente duplicam alturas existentes. Nas cadeias, as quintas adicionais seguem a regra da cadeia; nos ciclos históricos começam com quintas puras. Os ajustes das extensões podem mudar essas relações. O programa preserva diferentes identidades físicas mesmo se as frequências coincidirem. Assim, a detecção automática não é capaz de decidir qual de duas teclas coincidentes foi pressionada; use nota fixa ou confirme a tecla na análise acústica.

**13-EDO e 14-EDO não são a mesma coisa que teclados históricos com 13 e 14 teclas.** A primeira opção divide a oitava em 13 passos de 92,3077 cents; a segunda, em 14 passos de 85,7143 cents. Abra **Divisão igual · gerador, referência e offsets por grau** para ajustar o gerador (quantos graus são percorridos por ligação), o grau-âncora e a oitava de referência. Os graus são numéricos; a âncora não precisa ser uma nota tradicional.

Com gerador de 8 passos, o 13-EDO dá uma órbita com 13 graus; o 14-EDO dá duas com sete. Isso decorre de somar o gerador e voltar ao começo ao completar a oitava: em 14 graus, somar 8 preserva a paridade. Um gerador diferente pode mudar a quantidade de órbitas sem mudar as alturas-base. O campo de gerador aceita os valores válidos para a divisão selecionada (respeite os limites mostrados).

Em **Personalizar graus · offsets independentes de c.p. e c.s.**, é possível alterar cada grau. Com offsets diferentes de zero, a receita-base continua identificada como EDO, mas as alturas efetivas não constituem necessariamente uma divisão rigorosamente igual. **Restaurar EDO puro (offsets zero)** elimina esses offsets.

<a name="biblioteca"></a>
## 1.7. Biblioteca pessoal de afinações

Abra **Biblioteca pessoal · salvar e compartilhar afinações**. Ela guarda receitas e contextos musicais, não observações de microfone. Prepare a receita no Afinador antes de salvar.

| Controle | Uso |
| --- | --- |
| Nome da cópia | Identifica a definição na biblioteca |
| Instrumento | Informação opcional do perfil musical |
| Salvar afinação | Guarda a definição musical e disposição |
| Salvar perfil com referência | Guarda a definição e a referência de frequência |
| Criar cópia | Guarda a configuração musical atual como uma cópia independente, sem substituir a original |
| Restaurar preset original | Recupera o preset de fábrica |
| Minha biblioteca / Carregar seleção | Escolhe e aplica uma cópia |
| Excluir seleção | Remove a entrada escolhida da biblioteca |
| Exportar afinação JSON / Exportar perfil JSON | Gera arquivo portátil do tipo indicado |
| Importar arquivo JSON | Abre arquivo musical de até 256 KiB para prévia validada |
| Confirmar importação / Cancelar prévia | Confirma a entrada na biblioteca ou abandona a operação; carregue a seleção para aplicar |

Salvar uma definição que já foi carregada ou salva pode atualizar sua entrada existente; use **Criar cópia** para preservar a anterior. A exportação representa o estado musical atual, não necessariamente a entrada destacada na lista. Após confirmar uma importação, pressione **Carregar seleção** para aplicar a receita importada. Exporte as definições importantes. Ao compartilhar uma afinação personalizada, informe se deseja preservar somente a relação entre notas ou também sua referência absoluta. Não confunda exportar um perfil musical com guardar um perfil instrumental. Depois de carregar uma configuração, verifique o temperamento, A4/âncora e disposição; mudanças da base musical podem tornar uma sessão ou curva anterior incompatível.

<a name="cfg-1"></a>
## 1.8. Configurações do Afinador

Aplique mudanças de modo incremental e teste o mesmo instrumento antes e depois. As regras de [salvamento e restauração](#configuracoes) valem para todos os grupos.

### Processamento e desempenho (aberto)

| Campo | Padrão | Opções e efeito |
| --- | --- | --- |
| Pontos da FFT | 8.192 | 4.096, 8.192, 16.384, 32.768; ver [resolução](#fft) |
| Desempenho | Automático | Econômico reduz a cadência de análise |
| Leitura acústica | Bruta | Filtrada suaviza a apresentação temporal |
| Intensidade do filtro (%) | 70 | 0–95; atua na leitura filtrada |

### Visualização (aberto)

| Campo | Padrão | Efeito |
| --- | --- | --- |
| Escala espectral | Logarítmica | Linear ou logarítmica |
| Zoom na nota-alvo | Não | Visualiza ±100 cents em torno do alvo |
| Monitor de diagnóstico | Não | Mostra medições internas do detector; não inicia captura |

### YIN + FFT (recolhido)

| Campo | Padrão | Faixa | Efeito |
| --- | ---: | ---: | --- |
| Limiar CMNDF | 0,17 | 0,05–0,26 | Limiar da função de diferença normalizada: aumentar admite mínimos menos profundos; pode aceitar ambiguidades. Diminuir exige repetição mais clara; pode rejeitar notas úteis. |

### pYIN (recolhido)

| Campo | Padrão | Faixa | Efeito |
| --- | ---: | ---: | --- |
| Quantidade de limiares | 100 | 20–200 | Mais valores representam a distribuição com mais detalhe, elevando custo |
| Distribuição Beta — α | 2 | 0,5–10 | Altera o peso relativo de limiares na distribuição |
| Distribuição Beta — β | 18 | 1–40 | Atua junto de α; não é uma confiança em porcentagem |
| Confirmação de oitava (quadros) | 2 | 1–5 | Aumentar torna a troca de oitava mais lenta de confirmar |
| Peso contextual da oitava | 0,72 | 0–0,95 | Aumentar favorece continuidade e pode retardar mudanças reais |

### SWIPE′ (recolhido)

| Campo | Padrão | Faixa | Efeito |
| --- | ---: | ---: | --- |
| Limiar de saliência | 0,20 | 0,05–0,50 | Aumentar exige padrão espectral mais convincente; reduzir aceita candidatas mais fracas |

Alterar o limiar não aumenta a faixa de análise nem calibra a confiança. Os parâmetros técnicos podem reinicializar o detector conforme necessário. Os controles exclusivamente visuais não o fazem.

<a name="diagnostico"></a>
## 1.9. Monitor e registro de diagnóstico

Use quando houver erro de oitava, demora, leitura instável, ausência de nota ou comportamento dependente de um aparelho. Não é preciso ativá-lo durante uma afinação normal.

1. Em Configurações → Visualização, habilite **Monitor de diagnóstico**. Observe o estado do método ativo.
2. Ative o microfone, selecione o detector que apresenta o problema e prepare a situação de teste.
3. Se desejar preservar o PCM contínuo, marque **Incluir áudio WAV (opcional)** antes da captura. Essa opção depende de AudioWorklet e da continuidade do áudio. Considere a privacidade do ambiente.
4. Pressione **Iniciar · 20 s**. Durante o contador, reproduza o problema, preferencialmente com notas isoladas e pausas identificáveis. Use **Parar** se precisar interromper.
5. Examine **Resumo da última sessão** e **Eventos recentes**. Pressione **Exportar ZIP** para guardar a evidência.

O monitor atualiza a interface em cadência própria (aproximadamente 250 ms); esse intervalo não é a cadência efetiva dos cálculos. O ZIP contém decisões e candidatos do detector, configurações, eventos, informações de ambiente e desempenho disponíveis, e opcionalmente `audio.wav`. Uma candidata não é necessariamente uma leitura aceita. Os limites de tempo e memória podem encerrar a sessão antes de 20 s. Não rode um diagnóstico enquanto realiza outra captura acústica ou emite som.

<a name="ts-1"></a>
## 1.10. Troubleshooting — Afinador

| Sintoma | O que verificar e fazer |
| --- | --- |
| Não pede microfone / permissão negada | Use HTTPS/localhost; confira permissão do site e do sistema; feche aplicativos que estejam usando o áudio e recarregue se necessário. |
| O medidor não sai de `--` | Confirme microfone ativo, som isolado e intensidade suficiente; aproxime moderadamente o instrumento; tente YIN + FFT com padrões restaurados. |
| Indica nota uma oitava acima | O segundo harmônico pode dominar. Experimente YIN + FFT/pYIN; confira o espectro; não use Pico como prova da fundamental. |
| Nota muda perto da fronteira | Use Nota fixa e verifique o catálogo, especialmente em teclas divididas. Nota flutuante também pode refletir variação real. |
| Desvio constante em todo instrumento | Confira A4, temperamento, modo e eventual correção instrumental aplicada; 415,3 Hz não é 440 Hz. Não compense erro de referência com ajuste físico indiscriminado. |
| Painel de correção desapareceu | Sem curva ativa, a referência é teórica e o painel fica oculto. Confira se a base musical ou os dados mudaram; revalide em Curvas antes de reaplicar. |
| Alteração de nota lenta | Use leitura bruta, pontos de FFT menores quando pertinente e padrões de confirmação pYIN; compare com YIN + FFT. |
| SWIPE′ indisponível | O navegador pode não oferecer o motor PFFFT/WASM necessário. Use outro método; não há substituição silenciosa equivalente. |
| Espectro parece truncado | Desative zoom; confira Nyquist e escala. O teto é determinado pela captura e pela política dos 24 kHz. |
| Picos aparecem próximos demais | Em log, harmônicos altos ficam visualmente próximos; alterne para linear ou aplique zoom. |
| Edição de quinta rejeitada | Reveja fração, limites e quinta compensatória; volte ao preset se necessário. |
| Teclas adicionais coincidem | Pode ser correto; duas identidades físicas podem compartilhar frequência. Use Nota fixa. |
| Configurações voltaram ao reabrir | Salve explicitamente; verifique se há armazenamento local disponível. |
| Não consegue modificar configurações | Termine a captura diagnóstica ativa; corrija campos inválidos. |
| WAV não foi incluído | Confirme que a opção estava marcada, AudioWorklet disponível e captura válida. O JSON ainda serve para investigação. |
| Problema persiste | Restaure só os padrões do Afinador, reproduza com nota conhecida e exporte diagnóstico conforme [1.9](#diagnostico). |

[Voltar ao sumário](#sumario)

<a name="cap-2"></a>
# Capítulo 2 — Parciais e inarmonicidade

O objetivo aqui não é apenas encontrar a nota: é investigar a composição do som. Uma nota musical pode conter uma componente fundamental, harmônicos superiores e componentes não harmônicos. O motor de análise acústica é independente do detector convencional. Não é preciso escolher SWIPE′ ou mudar os pontos da FFT do Afinador para medir parciais.

<a name="modelos"></a>
## 2.1. Escolha do instrumento e do modelo

Uma série harmônica ideal tem frequências `fₙ = n × f₁`. Um instrumento real pode apresentar desvios, componentes fracas, ruído, batimentos ou modos que não obedecem à série. Um pico espectral, por si só, não comprova a origem física de uma componente.

A captura multiataque utiliza quatro famílias: **Piano, Fortepiano, Cravo e Outro**. A família identifica o instrumento; o modelo acústico define a hipótese de interpretação. A escolha não é uma classificação automática do instrumento.

| Família | Condição e modelo utilizado | Orientação prática |
| --- | --- | --- |
| Piano | Corda isolada: corda rígida (B). Nota completa, condição desconhecida ou uníssono: série harmônica, sem B físico | Identifique a corda; não declare isolamento se houver outras cordas vibrando. |
| Fortepiano | Mesmas regras de seleção de modelo que piano | Identifique a corda e conjunto; use a extensão física real e altura soante. |
| Cravo | Mesmas regras de seleção de modelo que piano | Informe registro, corda e técnica; use um perfil por registro, com a altura efetivamente soante (4′ soa uma oitava acima de 8′). |
| Outro | Exploratório por padrão; modelo selecionável explicitamente | Abrange qualquer outro instrumento ou fonte sonora; identifique a fonte e técnica quando útil. |

Para os três instrumentos de teclado, **Usar somente picos exploratórios (sem ajuste físico)** substitui a análise harmônica ou de corda rígida pelo modo exploratório. Nenhuma família tem homologação física implícita.

### Outro: selecionar o modelo acústico

Abra **Modelo acústico de Outro (avançado)**. Ao selecionar Outro no fluxo normal, o modo inicial é Exploratório; uma medição encaminhada de um perfil Outro recupera o modelo desse perfil.

| Modelo | O que examina | B | Exemplos de uso |
| --- | --- | --- | --- |
| Exploratório (padrão) | Picos sem impor ordem harmônica ou fundamental | Não | Fonte desconhecida, timbre incomum, inspeção geral |
| Série harmônica | Frequência-base inferida, ordens e desvios de uma série | Não | Flauta, voz ou nota aproximadamente periódica |
| Corda rígida — B experimental | Parciais e ajuste físico de corda rígida quando elegíveis | Sim, se elegível | Monocórdio, clavicórdio, violão ou guitarra de corda isolada e sinal limpo |
| Componentes não harmônicos | Picos sem atribuição obrigatória de ordens | Não | Sinos, placas e percussões; picos não comprovam modos próprios |

Nos modos exploratório e não harmônico, a análise é centrada nos picos; a identificação de nota e as apresentações dependentes de ordens harmônicas não são usadas. Em Série harmônica, a identificação de nota pode ser útil, mas não há B. Em Corda rígida, selecione **Como a nota soa? → Uma corda isolada**, mesmo que já tenha usado esse modelo antes. Sem declaração de isolamento, a sessão de Outro neste modelo não pode iniciar. **Qual corda?** permite identificar a fonte; use sinal limpo, sem efeitos, e documente técnica, posição, casa (se pertinente) e condições em **Técnica / condição (opcional)**. Não existem mais seletores específicos de trastes ou de instrumento elétrico. A declaração é responsabilidade do usuário; escolher o modelo não comprova isolamento nem adequação física.

Mudar o modelo de Outro limpa a condição e identificação de corda anteriormente selecionadas. Escolha antes de iniciar: o contexto fica fixado para a sessão. Nenhum modelo de Outro é elegível para gerar curvas de afinação, mesmo se B for consistente.

Para estudar um piano, não desmonte, abafe ou manipule componentes internos sem conhecimento técnico apropriado. Se não for possível isolar a corda de modo seguro, registre a nota completa como tal. Os resultados ainda podem ser úteis para inspeção acústica, mesmo sem B.

<a name="captura-individual"></a>
## 2.2. Captura individual genérica

A opção é indicada para experimentar rapidamente o espectro de uma nota, sem preparar uma sessão com identificação e condições físicas detalhadas.

1. Abra **Ferramentas → Parciais e inarmonicidade** e ative o microfone.
2. Expanda **Alternativa: captura individual genérica (sem seleção de modelo)**.
3. Pressione **Capturar uma nota**. Toque uma única nota sustentada e aguarde o resultado. Use **Encerrar captura** para interromper a aquisição quando necessário.
4. Examine o resultado e abra **Inspecionar espectro, desvios e cada parcial**. Mesmo se aparecer como inconclusivo, inspecione as evidências disponíveis.
5. Use **Congelar resultado** para evitar substituir o resultado durante a inspeção. Use **Liberar resultado** antes de medir novamente.
6. Se desejar, pressione **Baixar análise (JSON)** ou **Ouvir no Emissor** para aproveitar componentes elegíveis do resultado.

A captura individual não é uma sessão multiataque com tecla e corda confirmadas. Não a use como substituto de uma sessão física para construir perfis ou curvas. **Ouvir no Emissor** cria uma reconstrução sintética, não reproduz o áudio original da captura. Veja [5.4](#reconstrucao).

<a name="multiataque"></a>
## 2.3. Medir a mesma nota várias vezes

A coleta de várias execuções independentes permite analisar a repetibilidade. Várias janelas de uma única execução não equivalem a várias notas tocadas de novo. A meta inicial é de dez ataques utilizáveis; você pode finalizar antes, quando o objetivo for apenas explorar os picos, ou continuar dentro dos limites quando precisar de mais dados.

### Preparar a sessão

1. Configure o temperamento, a referência e o layout que correspondem às teclas do instrumento (ver [1.4](#temperamentos) e [1.6](#teclados)).
2. Escolha **Instrumento**. Para Outro, selecione o modelo nas opções avançadas se não desejar o Exploratório. Indique **Como a nota soa?** e **Qual corda?** quando esses campos estiverem disponíveis. Em Outro com corda rígida declare isolamento; documente instrumento, técnica e condições relevantes no campo livre.
3. Determine a **Identificação da nota**: **Sugerir automaticamente** para obter uma sugestão acústica, ou **Escolher tecla antes de medir** se souber a tecla. Para sinais não harmônicos ou exploratórios, não confunda um pico com uma nota identificada.
4. Selecione **Reconhecimento de toques** automático ou manual. Confira as configurações acústicas antes de iniciar; a sessão registra e conserva os parâmetros de análise usados.
5. Ative o microfone e pressione **Iniciar medição**.

### Coleta automática

Toque sempre a mesma nota/corda e deixe o som diminuir entre as execuções. O sistema procura o início do toque, descarta parte do transiente inicial e analisa um trecho útil. Aguarde as indicações da interface: som em análise, verificação dos parciais, nova execução ou orientação de repetir. Não interprete simplesmente a contagem de tentativas como quantidade de medições válidas.

### Coleta manual

Escolha **Manual — marcar cada toque**. Durante a sessão, pressione **Iniciar execução**, toque a nota, sustente ou deixe soar, e use **Encerrar execução** quando necessário. Respeite o trecho mínimo e máximo úteis; o motor analisa o áudio recebido, e não o instante do clique como frequência. A marcação manual ajuda quando o reconhecimento automático do início do som é difícil, mas não elimina os critérios acústicos.

### Pausar, confirmar e finalizar

- **Pausar** interrompe a coleta sem apagar execuções anteriores. Após a pausa, retome pelo controle de medição, se o contexto continuar válido.
- Quando houver uma sugestão, confira **Confirme a tecla (ou deixe sem identificação)** e pressione **Confirmar tecla** somente se souber qual tecla física foi tocada. Se duas grafias coincidirem ou não for possível identificar, use **Continuar sem identificar a tecla**. O registro continua útil de forma exploratória.
- **Finalizar e revisar** encerra a escuta e permite inspecionar todas as execuções. Uma finalização por meta, quando habilitada, não confirma automaticamente a tecla nem B.
- Em **Histórico de execuções**, pressione **Inspecionar** na execução desejada para examinar seus resultados. **Mais antigas** e **Mais recentes** navegam pelas páginas disponíveis. Com a coleta pausada ou finalizada, use **Excluir do conjunto** ou **Restaurar ao conjunto** nas execuções elegíveis; excluir uma execução da consolidação não apaga sua observação original. Em **Revisar parciais (avançado)**, quando disponível, use **Excluir parcial n** ou **Restaurar parcial n** para retirar ou devolver uma ordem ao ajuste daquela execução. O resultado original de B é preservado, o ajuste revisado pode ficar inconclusivo e a alteração fica registrada. Se a inspeção estiver congelada, libere o resultado antes de selecionar outra execução. Se alterar inclusões, aguarde o recálculo ou use **Recalcular resultado**.
- **Salvar no perfil** encaminha a sessão concluída para o registro instrumental. **Baixar sessão (JSON)** guarda os dados sem depender do banco local. **Descartar sessão** elimina a sessão de trabalho; exporte ou salve antes se precisar dela.

Não mude de nota, corda, posição do microfone, família, modelo acústico ou contexto musical no meio da sessão. Se a base ou a captação mudar, revise/exporte o conjunto anterior e comece outro. O sistema pode pausar em caso de suspensão do áudio, perda de continuidade, mudança do microfone, mudança de ferramenta, segundo plano ou limite de memória; há também limite de dez minutos de escuta contínua. Os registros já obtidos devem ser examinados antes de retomar ou descartar.

<a name="interpretar-parciais"></a>
## 2.4. Interpretar o resultado acústico

Abra as áreas progressivas da interface conforme a pergunta que deseja responder. Comece pelo resumo, depois examine a evidência espectral e, por último, o ajuste numérico se houver.

| Elemento | Significado e uso |
| --- | --- |
| Frequência observada | Posição estimada de uma componente no espectro, em Hz |
| Fundamental inferida | Hipótese de frequência-base da série; pode estar ausente ou ambígua |
| Ordem do parcial | Posição `n` atribuída à componente na série; não é obrigatória em sinos ou sinais exploratórios |
| Amplitude / dB relativos | Nível associado a uma componente relativamente à referência do espectro; não é dB SPL calibrado |
| SNR local | Relação sinal/ruído estimada nas vizinhanças do pico; uma componente fraca pode ser válida se estiver bem acima do ruído |
| Aceito / candidato | Componente admitida pelos critérios em uso ou ainda não confirmada. Um candidato não deve ser tratado como evidência física garantida |
| Desvio em cents | Distância entre a frequência observada e a referência harmônica indicada no gráfico/tabela |
| Variação temporal | Diferença observada entre janelas disjuntas da mesma execução, quando disponível; não é intervalo de confiança |
| Pico sem atribuição | Componente detectada que não recebeu ordem harmônica válida; não invente uma ordem para utilizá-la |
| Ressalvas | Motivos de rejeição e condições que limitam a interpretação |

### Espectro acústico e inspeção localizada

Em **Inspecionar espectro, desvios e cada parcial**, alterne **Logarítmica/Linear**, use **+ Ampliar**, **− Reduzir** ou **Visão geral**. A exibição não modifica a análise. O gráfico pode usar uma representação resumida dos bins; ampliar não recupera informação não conservada no resumo. Consulte as frequências exatas e valores de cada componente na tabela. Pressione o botão **Parcial n** para destacar e examinar a ordem correspondente e suas evidências; a seleção não muda o ajuste. Capturas de versões anteriores conservam sua faixa espectral original.

O teto de busca atual é 24 kHz, limitado pela Nyquist e pela configuração acústica. No entanto, a quantidade de ordens analisadas, os critérios de qualidade, a duração útil e a resposta do microfone também limitam os parciais encontrados. Não espere que um som de 1 kHz necessariamente apresente 24 parciais detectáveis.

### Exemplo: nota de flauta com poucos parciais

Selecione Outro → Série harmônica para este exemplo. É possível encontrar a fundamental com clareza e não alcançar os critérios mínimos de uma série harmônica. Uma flauta pode produzir componentes superiores muito mais fracas do que a primeira. Isso é uma característica possível do som, não prova de falha do programa. O modelo de corda rígida não se aplica à flauta.

Primeiro, sustente a nota em condições estáveis, examine o espectro e os candidatos. Se houver picos fracos mas consistentes, faça uma segunda sessão experimental reduzindo somente **Nível relativo mínimo**, por exemplo de −35 para −45 ou −55 dB. Compare o mesmo registro, intensidade, técnica e posicionamento. Aceitar componentes mais fracas também pode admitir ruído; não diminua todos os limiares de uma vez. Restaure os padrões para retornar aos critérios de referência do projeto. Ver [2.7](#cfg-2).

<a name="coeficiente-b"></a>
## 2.5. Inarmonicidade de cordas e ajuste individual de B

Para uma corda com rigidez, o modelo experimental usa `fₙ = n × F × √(1 + B × n²)`, em que F é a escala de frequência ajustada e B, o coeficiente adimensional de inarmonicidade. A frequência prevista do primeiro parcial é `F × √(1 + B)`, e não necessariamente F. B = 0 recupera a série ideal. Valores positivos fazem os parciais superiores ficarem progressivamente mais agudos em relação aos múltiplos do primeiro.

Os tetos numéricos experimentais de B são 0,02 para Piano, Fortepiano e Cravo, e 0,05 para Outro com corda rígida, tanto no ajuste individual quanto no consolidado. Esses tetos não representam limites físicos universais e não dispensam os critérios de qualidade.

O cálculo não parte simplesmente da nota-alvo musical. Ajusta F e B às frequências medidas, utilizando uma perda robusta em cents (Huber, que reduz a influência de grandes resíduos). A rigidez é uma hipótese física; um bom ajuste matemático não demonstra por si só que as componentes venham da mesma corda ou que o valor esteja calibrado.

Quando o modelo for elegível e houver evidência suficiente, abra **Inarmonicidade da execução → Por que este B? — modelo, parciais e resíduos**. Examine:

| Indicador/gráfico | Como interpretar |
| --- | --- |
| B individual | Estimativa da execução, com critérios e ressalvas do modelo |
| F (Hz) | Escala acústica ajustada; não é a frequência teórica da nota |
| Medido × previsto | Desvios observados e previstos em relação a `n·f₁` do modelo |
| Resíduos | Diferença em cents entre medido e previsto; positivos e negativos indicam sentidos do erro |
| Ordens e SNR | Evidência disponível; poucas ordens ou componentes instáveis podem tornar B não identificável |
| Variação/estabilidade | Diagnóstico de adequação do modelo, não precisão metrológica |

Um resíduo pequeno em todas as ordens identificadas indica que o modelo explica bem aquelas observações. Não prova que a ordem foi corretamente atribuída ou que a corda seja idealmente isolada. Resíduos sistemáticos, componentes sobrepostas, instabilidade e valores incompatíveis pedem revisão. Um resultado inconclusivo deve ser conservado como tal; não adote B = 0 por conveniência.

<a name="consolidacao"></a>
## 2.6. Resultado da sessão: consolidação e repetibilidade

Para sessões de corda rígida elegíveis, o motor procura um B comum e permite uma escala F diferente por execução. Não é uma simples média dos B individuais; cada execução conserva sua evidência, inclusive a relação entre frequências e resíduos. Por padrão, são requeridas ao menos três execuções elegíveis para consolidação e dez para a avaliação por reamostragem. Há outros testes de consistência, contexto, identificabilidade e qualidade.

| Estado | Significado | Próxima ação |
| --- | --- | --- |
| Aguardando medições | Sessão sem evidência suficiente | Toque novamente |
| Primeira medição — ainda sem B consolidado | Estimativa individual pode existir, sem conjunto | Repita de modo independente |
| B não aplicável | Modelo ou condição não corresponde a corda rígida elegível | Use os componentes observados; não force B |
| B inconclusivo / consolidação indisponível | Ordem, contexto, repetibilidade ou ajuste insuficientes | Consulte motivos; confirme tecla e corda, revise ou repita |
| Consistente pelos critérios experimentais | Execuções incluídas passaram nas verificações do conjunto | Examine dispersão, resíduos e condições; não confunda com homologação |
| Incerteza não estimável / degenerada | Dados insuficientes ou reamostragem incapaz de produzir intervalo utilizável | Conserve os resultados e faça novas execuções independentes |

Em **Comparar as execuções e ver os cálculos**, a tabela apresenta B individual, diferença em relação ao B conjunto, F, peso, resíduo máximo e B sem ataque (efeito de retirar aquela execução). Um resultado fortemente dependente de um único ataque merece investigação; quando a retirada completa não foi possível, a interface pode indicar uma aproximação. Deslize horizontalmente a tabela em telas estreitas. Os dados completos são preservados no JSON.

O bootstrap reamostra ataques independentes, por padrão em 399 repetições, para investigar a variação entre execuções. A meta relativa de largura de B de 5% diz respeito ao comportamento experimental do conjunto; não equivale a erro absoluto de 5% nem certifica precisão física. Se os ataques forem praticamente idênticos, o intervalo pode ser degenerado. Um intervalo estreito também não elimina viés de microfone, identificação ou modelo. Sessões extensas podem exceder o orçamento de verificação completa.

Em **Execuções fora do ajuste**, examine os motivos: rejeição, contexto incompatível, nota não confirmada, frequência divergente, exclusão manual, parcial inválido ou condição física inadequada. Excluir observações só para reduzir resíduos introduz viés. Prefira registrar o motivo físico de uma exclusão e preservar as observações originais.

<a name="cfg-2"></a>
## 2.7. Configurações de Parciais e inarmonicidade

Os grupos avançados permitem experimentos controlados. Configurações acústicas personalizadas são registradas nas sessões, consideradas exploratórias para fins de curvas e não habilitam uma medição automaticamente como fonte de correções. A alteração durante uma sessão em curso não muda os parâmetros congelados daquela sessão; para testar novos critérios, finalize e inicie outra. A escala e o filtro de candidatos são visuais.

### Aquisição e apresentação (aberto)

| Campo | Padrão | Opções e efeito |
| --- | --- | --- |
| Reconhecimento de ataques | Automático | Automático ou manual; padrão de novas sessões |
| Identificação da nota | Sugerir automaticamente | Sugestão ou escolha anterior à medição |
| Meta de ataques utilizáveis | 10 | 1–64; não garante qualidade nem elimina exigências do modelo |
| Encerrar ao alcançar a meta | Não | Encerra a escuta automaticamente; ainda requer revisão |
| Escala espectral | Logarítmica | Linear ou logarítmica |
| Mostrar parciais candidatos | Sim | Filtro visual; não apaga evidências |

### Análise espectral (recolhido)

| Campo | Padrão | Faixa | Efeito |
| --- | ---: | ---: | --- |
| Janela mínima (ms) | 160 | 100–500, passo 20 | Trecho mínimo desejado; mais duração favorece separação, se houver sinal estável |
| Janela máxima (ms) | 1.500 | 500–1.500, passo 20 | Limita trecho analisado e custo |
| Ciclos desejados | 16 | 8–32 | Adapta duração ao período estimado |
| Ordens máximas | 24 | 4–24 | Limita as ordens consideradas, não a quantidade de picos genéricos |
| Frequência máxima analisada (Hz) | 24.000 | 1.000–24.000, passo 100 | Limita busca de componentes, independentemente do zoom; Nyquist continua obrigatório |
| Zero-padding | 4× | 1×, 2×, 4× | Adiciona zeros para obter grade mais densa; não aumenta a resolução física nem inventa dados |

O analisador utiliza FFT própria em JavaScript e janela Hann. A duração se adapta à frequência e ao áudio disponível, sob limites de memória; os controles exprimem valores desejados e nunca autorizam ultrapassar os buffers. A duração real e o tamanho efetivo da FFT podem ser menores que o solicitado.

### Identificação e qualidade (recolhido)

| Campo | Padrão | Faixa | Efeito |
| --- | ---: | ---: | --- |
| SNR mínimo do pico (dB) | 8 | 6–20 | Menor valor admite picos mais próximos do ruído |
| SNR mínimo do parcial (dB) | 12 | 8–30 | Menor valor flexibiliza a aceitação de componentes atribuídas à série |
| Nível relativo mínimo (dB) | −35 | −60 a −20 | Mais negativo permite componentes fracas; o piso absoluto permanece ativo |
| Mínimo de parciais da série | 2 | 2–6 | Maior número exige mais evidências para caracterizar série |

### Reconhecimento de ataques (recolhido)

| Campo | Padrão (ms) | Faixa (ms) | Efeito |
| --- | ---: | ---: | --- |
| Descarte inicial | 60 | 0–140 | Evita parte do transiente; não se aplica à captura individual |
| Duração útil mínima | 160 | 100–500 | Requer trecho sustentado suficiente |
| Duração útil máxima | 1.740 | 500–1.740 | Limita duração do trecho analisável |
| Silêncio / liberação | 120 | 60–500 | Define término/rearme do reconhecimento |
| Período refratário | 160 | 80–500 | Evita registrar novo ataque cedo demais |

Todos esses campos variam em passos de 20 ms. O buffer de aquisição é de 1.800 ms: descarte inicial + duração útil máxima não pode exceder 1.800 ms. Se aumentar o descarte, pode ser necessário reduzir antes a duração útil máxima. Um descarte grande pode perder o som útil de instrumentos de curto decaimento; muito pequeno pode incluir transientes difíceis de modelar.

### Ajuste matemático de B (recolhido)

| Campo | Padrão | Faixa / passo | Efeito |
| --- | ---: | --- | --- |
| Ordens distintas mínimas | 4 | 4–12 | Exigência de diversidade de ordens para ajustar B |
| Transição Huber (cents) | 1 | 0,5–2 / 0,1 | Limite a partir do qual resíduos grandes têm influência reduzida |
| Mediana máxima de resíduos (cents) | 1,5 | 0,5–3 / 0,1 | Controla erro típico permitido |
| Resíduo máximo (cents) | 6 | 2–10 / 0,5 | Limita desvio individual |
| SNR mediano mínimo (dB) | 20 | 12–40 | Exige nível de evidência do conjunto de componentes |
| Instabilidade temporal máxima (cents) | 3 | 1–6 / 0,5 | Limita variação temporal quando estimável |

### Validação estatística (recolhido)

| Campo | Padrão | Faixa | Efeito |
| --- | ---: | ---: | --- |
| Mínimo para consolidação | 3 | 3–10 | Número mínimo de execuções elegíveis |
| Mínimo para bootstrap | 10 | 10–32 | Número mínimo de ataques independentes para reamostragem |
| Reamostragens | 399 | 99–399 | Mais reamostragens aumentam computação; não corrigem viés |
| Meta relativa de largura de B (%) | 5 | 1–10 | Meta exploratória de repetibilidade |

### Restrições de compatibilidade entre parâmetros

Além dos limites individuais, janela mínima ≤ máxima; duração útil mínima ≤ máxima; descarte + duração útil máxima ≤ 1.800 ms; SNR mínimo do pico ≤ SNR mínimo do parcial; mínimos de ordens e de parciais não podem superar as ordens máximas; mediana máxima de resíduos ≤ resíduo máximo; mínimo para consolidação ≤ mínimo para bootstrap. A janela conserva os últimos valores válidos quando alguma dessas relações não é satisfeita. Ajuste primeiro o parâmetro que permite a transição ou use **Restaurar padrões**.

<a name="ts-2"></a>
## 2.8. Troubleshooting — Parciais e inarmonicidade

| Sintoma | Ação recomendada |
| --- | --- |
| Não inicia aquisição | Ative o microfone, use contexto seguro e confirme suporte a AudioWorklet/Workers; encerre o Emissor ou diagnóstico. Consulte a mensagem do controlador. |
| Não reconhece toques | Deixe silêncio entre notas, use uma fonte isolada e teste o reconhecimento manual. |
| Som útil muito curto | Prolongue o som quando possível; revise descarte e duração útil em uma nova sessão exploratória. Um instrumento de decaimento curto pode oferecer poucos dados. |
| Poucos parciais separáveis | Confira ruído, distância, candidatos e teto de frequência. Aumentar janela pode ajudar em som estável; em sinais fracos, experimente o nível relativo em nova sessão. |
| Flauta sem B | Esperado: use Outro → Série harmônica. O modelo de corda rígida não é aplicável. |
| Piano completo sem B | Declare corretamente a nota completa/uníssono. B físico exige corda isolada elegível. |
| Outro sem B | Confira o modelo escolhido. Apenas Corda rígida admite B; exige uma corda isolada e evidência suficiente. |
| Outro com corda rígida não inicia | Selecione Uma corda isolada em Como a nota soa?; se a condição não for verdadeira, escolha outro modelo. |
| Outro não apresenta tecla ou ordens | Esperado em Exploratório e Componentes não harmônicos. Examine os picos e guarde a sessão sem tecla. |
| Fundamental ambígua | Toque uma nota de cada vez, reduza ruído e confirme a tecla se souber qual foi. A frequência-base pode permanecer inconclusiva. |
| Frequência incompatível com a sessão | Confirme mesma tecla e corda, A4, temperamento e contexto; se mudou de nota, finalize e inicie outra sessão. |
| B individual existe, conjunto não | Verifique número de execuções, confirmação de tecla, qualidade e consistência. Não basta atingir a meta numérica. |
| Bootstrap sem resultado | Aumente a quantidade de ataques independentes, reveja degeneração, dispersão e limites de verificação; não assuma incerteza zero. |
| Gráfico sem dados novos | Libere a captura congelada; selecione nova execução. Captura antiga não ganha frequências novas ao ampliar. |
| Configuração não afetou a sessão | Sessões em andamento conservam os parâmetros de início. Finalize, preserve e comece outra. |
| Escuta pausada/interrompida | Mantenha a página em primeiro plano, confira a continuidade do microfone e não use Emissor/diagnóstico simultaneamente; retome com contexto válido. |
| Limite de memória atingido | Exporte a sessão e reduza o volume de novas revisões; conclua ou descarte antes de recomeçar. |
| Não consegue guardar no perfil | Finalize, aguarde a conclusão do cálculo e confira família, corda e modelo de Outro. Exporte JSON para não perder a sessão. Veja [Capítulo 3](#cap-3). |
| Sessão personalizada não aparece para curva | É uma restrição deliberada: restaure critérios de referência e adquira novas medições elegíveis de Piano, Fortepiano ou Cravo. Outro não é fonte de curvas. Não edite manualmente o JSON para contorná-la. |

[Voltar ao sumário](#sumario)

<a name="cap-3"></a>
# Capítulo 3 — Perfis instrumentais

Um perfil instrumental é um prontuário acústico do instrumento: identificação, extensão, ordem física das teclas, condições das medições e sessões. Ele não muda a afinação nem armazena WAV. É possível guardar resultados inconclusivos para acompanhar a qualidade das medições ao longo do tempo.

<a name="criar-perfil"></a>
## 3.1. Criar e organizar um perfil

1. Configure o layout musical correspondente ao instrumento no Afinador. É especialmente importante quando existem teclas divididas ou graus alternativos.
2. Abra **Ferramentas → Perfis instrumentais → Novo perfil**.
3. Preencha **Nome**, **Família** (Piano, Fortepiano, Cravo ou Outro), **Subtipo / fabricante** e **Observações** (os dois últimos são opcionais). Em Outro, abra **Modelo acústico de Outro (avançado)** e escolha o modelo desejado; o padrão é Exploratório. Use o subtipo para identificar o instrumento específico. Uma identificação consistente facilita repetir estudos no mesmo instrumento.
4. Escolha **Extensão física**: piano convencional de 88 teclas se compatível ou extensão no layout musical atual. Neste último caso, selecione primeira e última tecla. Não imponha 88 teclas a uma configuração incompatível.
5. Pressione **Criar e salvar perfil** e confira a confirmação de sucesso. Se desistir, use **Cancelar**.
6. Examine **Informações do instrumento e disposição física**. Se a ordem inicial não corresponder à disposição real, selecione uma tecla e use **Mover antes / Mover depois**. Antes de calcular uma curva, a ordem deve estar correta.

Na lista **Instrumento**, selecione o perfil de interesse. **Renomear** muda sua identificação; **Duplicar perfil** cria uma cópia; **Excluir perfil** remove o registro escolhido do armazenamento local. Faça backup antes de operações destrutivas. Não use a exclusão para esconder uma medição desfavorável.

### Tecla, corda e contexto

Duas cordas da mesma tecla do piano podem ter propriedades diferentes. Identifique cada corda/grupo de modo estável (por exemplo, uma convenção de posição que você reconheça) e não use nomes distintos para a mesma observação física. Mantenha a família compatível com a sessão. Para piano, fortepiano e cravo, o perfil tem corda rígida como modelo de referência, mas pode guardar sessões da mesma família em outros modelos permitidos. Para Outro, o modelo do perfil deve coincidir exatamente com o modelo da sessão; crie perfis distintos para estudar a mesma fonte sob hipóteses diferentes. Para cravo ou fortepiano, separe registros/conjuntos de cordas e represente as oitavas soantes. Um perfil de fonte não harmônica ainda tem uma disposição musical, mas os registros sem nota ficam fora do mapa. A identidade de tecla não é apenas o nome da nota: o layout, oitava e grafias podem diferir, mesmo quando duas frequências coincidem.

<a name="salvar-sessoes"></a>
## 3.2. Associar uma sessão a um instrumento

1. No [Capítulo 2](#multiataque), finalize a sessão, confirme a tecla quando conhecida e examine a condição da fonte. Aguarde o cálculo terminar.
2. Pressione **Salvar no perfil**, em Parciais. A ferramenta Perfis mostra **Sessão pronta para salvar**.
3. Selecione o instrumento correto ou crie um perfil novo da mesma família e, no caso de Outro, do mesmo modelo acústico. Confira **Identificação física da corda/grupo (da mesma tecla)**.
4. Pressione **Salvar sessão neste perfil**. Aguarde a confirmação do banco; não suponha que foi armazenada antes da confirmação.
5. Alternativamente, use **Baixar sessão sem salvar** para fazer uma cópia independente, ou **Cancelar salvamento** para abandonar o encaminhamento sem criar um registro.

O histórico mantém a referência e as frequências originais da sessão. O aplicativo impede duplicações conflitantes e a associação de uma mesma observação a cordas diferentes no mesmo perfil. Uma revisão salva não é uma nova execução independente. Medições sem tecla confirmada ou fora do mapa podem ser preservadas e consultadas separadamente; não invente uma associação só para preencher o mapa.

<a name="comparar-sessoes"></a>
## 3.3. Consultar, comparar e medir novamente

O **Mapa de teclas** permite escolher a tecla e abrir seu **Histórico**. Use **Medições sem tecla / fora do mapa** para consultar registros que não se associam à disposição. A ordenação pode ser por mais recentes, mais antigas ou qualidade provisória; essa última é uma ajuda de triagem, não classificação metrológica definitiva.

Ao selecionar uma sessão, procure os dados de modelo, família, fonte, identificação, condições de áudio, parâmetros acústicos registrados, execuções, resíduos e intervalo de B, quando disponíveis. O espectro armazenado possui sua própria faixa; não é áudio reexecutável e não ganha conteúdo ao alternar a escala. Os detalhes de uma execução conservam evidências e ressalvas; filtros visuais não apagam os itens ocultos.

Para comparar, selecione **Primeira sessão**, **Segunda sessão** e **Comparar sessões**. Prefira duas sessões distintas, da mesma tecla e corda, com técnica, captação e parâmetros equivalentes. Verifique a mensagem de compatibilidade antes de interpretar diferenças.

| Situação | Interpretação |
| --- | --- |
| Duas sessões compatíveis de corda rígida | É possível observar diferenças de frequência e B, dispersão, qualidade e contexto; não são combinadas automaticamente em um novo ajuste conjunto. |
| Contextos de áudio diferentes | Comparação limitada; a diferença pode resultar da captação. |
| Configurações acústicas diferentes | Consulte as observações separadamente; não trate resultados como fisicamente equivalentes. |
| Família, procedimento ou modelo diferente | Não atribua a diferença a variação física de B sem evidência. |
| Modelos sem B | Compare frequências e espectros observados; não há correspondência modal automática. |
| Revisões de uma mesma sessão | Mostram efeito da revisão; não são duas aquisições independentes. |

**Medir novamente** encaminha a tecla selecionada para Parciais, desde que ela exista na configuração musical atual. O modelo de Outro é recuperado do perfil; nos modelos Exploratório e Componentes não harmônicos, o botão **Medir novamente (sem tecla)** encaminha a captura sem atribuição de tecla. Em Corda rígida, declare novamente a condição de isolamento. Confira novamente a corda e o contexto. Se existir uma sessão anterior em memória, finalize/exporte ou descarte-a explicitamente antes de trocar de nota. Se a tecla estiver ausente do layout atual, recupere a configuração musical correspondente. Não altere o mapa para forçar coincidência.

<a name="backup-perfil"></a>
## 3.4. Exportação, importação e armazenamento

- **Exportar perfil (JSON)** guarda uma cópia portátil do perfil com os registros; a exportação de uma sessão isolada, quando disponível no histórico, guarda apenas aquela sessão. Faça cópias independentes dos arquivos importantes.
- **Solicitar armazenamento persistente** pede ao navegador proteção contra certas remoções automáticas. A solicitação pode ser negada ou indisponível; não impede limpeza manual e não substitui backup.
- **Importar arquivo** abre uma revisão após validação. Use **Importar como novo** para conservar uma cópia independente; **Mesclar com perfil de mesmo ID** somente para o mesmo perfil compatível. Revise a prévia e os conflitos. **Cancelar** abandona a importação.

Também é possível importar um JSON de sessão multiataque exportado de Parciais pelo mesmo controle **Importar arquivo**. Depois de validado, ele é apresentado como sessão pendente; selecione o instrumento e confirme o salvamento conforme [3.2](#salvar-sessoes). Caso já haja outra sessão pendente, preserve-a antes de substituir. Uma análise individual genérica não é uma sessão multiataque. Há limites de 2.000 perfis locais e 2.000 registros por perfil, além da cota do navegador.

Não renomeie IDs ou hashes manualmente para forçar mesclagem. Um arquivo JSON de outra ferramenta não é necessariamente um perfil importável, embora todos tenham a mesma extensão. O limite geral de arquivos acústicos corresponde ao orçamento de segurança de 32 MiB, com restrições adicionais de estrutura e conteúdo; um perfil muito grande deve ser preservado e dividido por procedimentos suportados (por exemplo, exportar sessões e organizar perfis menores para novas coletas), sem descartar a única cópia existente.

Os dados locais podem ser perdidos quando a origem do site muda (por exemplo, localhost versus GitHub Pages), quando o navegador limpa o armazenamento ou quando o aparelho é substituído. Para migrar, exporte no aparelho antigo e importe no novo. Os arquivos novos registram família, modelo e condição da sessão; para Outro, a compatibilidade do modelo é verificada também na importação e no salvamento. A Etapa 18 não garante leitura de contextos acústicos antigos nem das famílias substituídas. A validação requer APIs de segurança como SHA-256; se indisponíveis, use HTTPS/localhost em navegador compatível.

<a name="cfg-3"></a>
## 3.5. Configurações de Perfis instrumentais

Aqui não há parâmetros de DSP. Essas escolhas afetam a consulta, comparação e apresentação, não recálculo das evidências.

| Grupo | Campo | Padrão | Efeito |
| --- | --- | --- | --- |
| Apresentação (aberto) | Ordenação das sessões | Mais recentes | Mais recentes, antigas ou qualidade provisória |
| Apresentação | Mostrar sessões inconclusivas | Sim | Mostra ou filtra os registros sem resultado conclusivo |
| Apresentação | Mostrar execuções excluídas | Sim | Controla a exibição das execuções fora do ajuste |
| Apresentação | Escala do espectro arquivado | Logarítmica | Logarítmica ou linear; não aumenta a faixa armazenada |
| Detalhes da evidência (recolhido) | Unidade do desvio de frequência | Cents | Cents ou Hz na comparação |
| Detalhes | Mostrar resíduos do ajuste | Sim | Mostra erros de previsão quando registrados |
| Detalhes | Mostrar intervalo de B | Sim | Mostra intervalo exploratório existente |
| Detalhes | Expandir detalhes das execuções | Não | Controla a expansão ao consultar medição |
| Detalhes | Expandir parâmetros acústicos registrados | Não | Mostra configuração original, quando disponível |

Aplique as preferências, reabra uma evidência se necessário e use **Salvar alterações** para conservá-las. **Restaurar padrões** não exclui perfis, medições nem histórico de curvas.

<a name="ts-3"></a>
## 3.6. Troubleshooting — Perfis instrumentais

| Sintoma | O que fazer |
| --- | --- |
| IndexedDB ou banco indisponível | Use navegador moderno, verifique permissões de armazenamento e origem; exporte evidências sem salvar se necessário. |
| SHA-256 indisponível | Use HTTPS/localhost. Não há confirmação segura de gravação sem os recursos necessários. |
| Família/modelo incompatível | Escolha o perfil da família correta e, para Outro, do mesmo modelo acústico, ou crie outro. Não altere a declaração da sessão só para guardar em perfil inadequado. |
| Não há sessão pronta | Finalize a coleta, aguarde o cálculo, pressione Salvar no perfil em Parciais. |
| Registro já salvo ou duplicado | Consulte a sessão existente ou sua revisão. Não duplique uma mesma execução como se fosse nova observação de outra corda. |
| Tecla não aparece no mapa | Abra Medições sem tecla / fora do mapa; reveja layout e identidade física. |
| Medir novamente não está disponível | Recupere a configuração musical da tecla; conclua sessão de trabalho anterior. |
| Resultados inconclusivos/excluídos não aparecem | Confira os filtros de apresentação; restaurar padrões não recupera arquivos realmente excluídos. |
| Comparação física recusada/limitada | Confira identidade, modelo, procedimento, configuração e condição de áudio; examine as sessões separadamente. |
| Importação recusada | Verifique tipo de arquivo, integridade, tamanho e mensagem da validação. Use o backup original; não contorne o validador. |
| Mesclagem recusada | IDs ou definições não são compatíveis. Importe como novo se o arquivo for válido e essa for a finalidade. |
| Cota de armazenamento atingida | Exporte perfis/sessões, confirme as cópias, organize novas coletas em outro perfil; só então remova dados dispensáveis. |
| Perfil desapareceu após troca de aparelho | Importe cópia JSON. O armazenamento é local, não sincronizado por conta. |

[Voltar ao sumário](#sumario)

<a name="cap-4"></a>
# Capítulo 4 — Curvas de afinação

Esta ferramenta investiga correções instrumentais para **piano, fortepiano e cravo**. Outro não é suportado na otimização de curvas, independentemente do modelo acústico. Uma corda rígida apresenta parciais desviados em relação a uma série ideal, de modo que relações entre parciais de teclas diferentes podem sugerir correções nas frequências de afinação. O objetivo é permitir o estudo dessas relações com evidência rastreável e restrições explícitas, não produzir uma receita universal de estiramento de oitavas.

> **Todas as curvas desta versão são experimentais e não homologadas fisicamente.** Gerar, aprovar ou guardar uma revisão não modifica a afinação por si só. A aplicação experimental é uma operação distinta, reversível, que exige fontes locais verificadas, recálculo coincidente e confirmação explícita. Consulte [4.5](#aplicar-curva).

<a name="pre-curva"></a>
## 4.1. Pré-requisitos e preparação do perfil

1. Escolha a base musical adequada (temperamento, referência e layout). Guarde uma definição na [biblioteca pessoal](#biblioteca) para poder recuperá-la posteriormente.
2. Crie um perfil de **Piano, Fortepiano ou Cravo** com o mapa físico correto, conforme [3.1](#criar-perfil). Para cravo e fortepiano, use um perfil por registro ou conjunto de cordas, com extensão e oitavas efetivamente soantes; não misture 8′ e 4′.
3. Obtenha sessões multiataque de cordas isoladas, com identificação inequívoca de tecla e corda, utilizando os parâmetros acústicos de referência. Consulte [2.3](#multiataque) e [2.6](#consolidacao).
4. Salve as sessões no perfil. Use várias teclas da região que pretende estudar; poucas teclas podem permitir inspecionar alguns intervalos, mas não necessariamente construir uma curva completa.
5. Confira a ordem real das teclas. Registre condições de corda, grupos de uníssono e transições construtivas. Não suponha que todo o instrumento constitua uma região fisicamente homogênea.

Sessões personalizadas de análise, registros inconclusivos e famílias diferentes não são intercambiáveis com as fontes de uma curva do instrumento escolhido. A seleção das fontes avalia compatibilidade da base musical, identidade física, qualidade e consistência das observações. Quando há mais de uma corda medida para a tecla, selecione a fonte representativa se a interface solicitar, ou deixe a tecla sem correção. Uma fonte representativa não descreve automaticamente todas as cordas de um uníssono.

### O que significa uma correção de curva

A frequência musical teórica de uma tecla é `fₜ`. Uma correção instrumental de δ cents propõe `f curva = fₜ × 2^(δ/1200)`. Se o alvo teórico é 440 Hz e δ = +2 cents, a proposta é aproximadamente 440,509 Hz. Zero significa manter a frequência teórica daquele temperamento. A curva não substitui a própria receita musical.

Ao escolher uma âncora, a correção desta tecla permanece zero. As demais são calculadas relativamente a ela. O limite de correção é ±30 cents; não se pode deslocar a âncora ou usar esse intervalo para contornar exigências de cobertura e proteção.

<a name="gerar-curva"></a>
## 4.2. Gerar uma prévia

Em **Ferramentas → Curvas de afinação**, siga a sequência numerada da interface.

### 1. Escolha o instrumento

Selecione um **Perfil** de piano, fortepiano ou cravo. **Atualizar perfis** atualiza a lista; **Ir para Perfis instrumentais** permite organizar os dados antes do estudo. Se o banco local estiver indisponível ou se quiser analisar uma cópia, use **Abrir backup de perfil (sem importar)**. O backup é validado para uso nesta ferramenta, sem criar automaticamente um novo perfil local.

Examine o quadro de disponibilidade e escolha, quando solicitadas, as fontes de cada tecla. Registros de cordas diferentes ou sessões divergentes requerem revisão; o aplicativo pode deixar a tecla sem evidência utilizável.

### 2. Escolha o objetivo

| Objetivo | Interpretação |
| --- | --- |
| Fidelidade ao temperamento (recomendado) | Procura preservar os desvios intervalares assinados da receita musical, conciliando-os com as propriedades acústicas e as proteções escolhidas. Não busca zerar indiscriminadamente todos os batimentos. |
| Otimização acústica | Busca coincidência das componentes intervalares consideradas; pode alterar intencionalmente relações do temperamento. Deve ser comparada com a base musical. |

Escolha uma **Tecla fixa de referência** entre as opções elegíveis. No cravo, preencha **Registro / conjunto representado** (obrigatório); no fortepiano, identifique o conjunto quando pertinente. Confirme explicitamente a ordem física das teclas e, para instrumentos históricos, que as fontes representam o mesmo registro/conjunto e altura soante. A âncora é obrigatória e permanece na frequência teórica.

### Opções avançadas (opcionais)

| Campo | Uso |
| --- | --- |
| Estilo de pesos | Conservador, Equilibrado ou Acústico: modifica a importância relativa das relações entre teclas; não é classificação de qualidade do instrumento. |
| Fonte de parciais | Automática conservadora, Modelo B ou Parciais medidos. O motor respeita critérios de elegibilidade; escolher uma fonte não torna dados insuficientes válidos. |
| Proteger estritamente quintas e quartas centrais | Na política experimental de Fidelidade, protege as relações centrais definidas na região de ±600 cents da âncora. |
| Incluir terças maiores (5:4) e menores (6:5) no cálculo | Acrescenta relações de terças quando há evidência; começa desmarcado no piano e marcado em fortepiano e cravo. |
| Preservar estritamente terças próximas das puras | No objetivo Fidelidade, protege a largura fundamental de terças a até 1 cent da razão justa; começa marcado no cravo e desmarcado nos demais. Pode limitar a compensação acústica. |
| Declaro uma região fisicamente homogênea | Autoriza interpolação limitada entre primeira e última tecla selecionadas. Declare somente se a região realmente não tiver quebras de escala ou mudanças de categoria de corda relevantes. |

O estilo Equilibrado e a fonte Automática conservadora são pontos de partida. Cada família possui pesos-base específicos, que são hipóteses experimentais de projeto, não regras históricas comprovadas nem parâmetros calibrados. A seguir, os pesos-base do estilo Equilibrado antes dos multiplicadores do usuário:

| Família de intervalo | Piano | Fortepiano | Cravo |
| --- | ---: | ---: | ---: |
| Oitava | 1 | 1 | 1 |
| Duodécima | 1 | 0,5 | 0,25 |
| Quinta | 0,65 | 0,9 | 1 |
| Quarta | 0,3 | 0,6 | 0,8 |
| Dupla oitava | 0,7 | 0,4 | 0,25 |
| Terça maior | 0,5 | 0,9 | 1,2 |
| Terça menor | 0,35 | 0,65 | 0,9 |

Os pesos são distribuídos pelas relações disponíveis de cada família; relações desativadas ou sem evidência não fornecem termos acústicos. No piano há ainda uma ênfase experimental de registro (certos parciais mais altos no grave e mais baixos no agudo). O Modelo B usa previsões de componentes do modelo de corda rígida quando elegível; Parciais medidos usa observações compatíveis. Por padrão, não há interpolação ou suavização entre teclas sem confirmação de uma região homogênea. **Extrapolação é proibida**: não se deve prolongar uma tendência além da evidência disponível.

Pressione **Gerar prévia**. Aguarde a conclusão; **Cancelar cálculo** interrompe a operação. Se a base musical mudar durante o cálculo, a operação pode ser invalidada. Se houver dados insuficientes, preserve as orientações e retorne à coleta em vez de forçar a geração. A prévia inicial não altera as frequências ativas do Afinador.

<a name="ler-curva"></a>
## 4.3. Interpretar a prévia e inspecionar intervalos

O gráfico apresenta a correção em cents ao longo da ordem física do perfil. Não equivale a um espectro FFT.

| Símbolo / origem | Significado |
| --- | --- |
| Ponto preenchido | Correção calculada com evidência (ou âncora, conforme o contexto) |
| Ponto vazio | Frequência teórica, sem correção suportada |
| Quadrado | Interpolação limitada e consentida |
| Losango, no editor de versões | Correção manual |
| Traço cinza, no editor | Versão escolhida para comparação |
| Barras de sensibilidade | Variação condicional do resultado sob a análise disponível; não são intervalo de confiança calibrado |

Em **Todos os pontos e origens**, confira tecla, frequência teórica, frequência proposta, Δ em cents e origem. Um ponto sem correção não prova que o instrumento precise de exatamente zero; significa que não foi aplicada uma correção suportada naquele ponto. Alterar a apresentação para **Curva total relativa ao temperamento igual** muda somente o referencial visual, quando há notas cromáticas e referência A4 compatíveis. Nesse modo, zero representa o igual, e não necessariamente a receita escolhida.

### 3. Inspecione uma tecla

Selecione a tecla e leia **Por que esta correção?**. Escolha um **Intervalo e parciais** para conferir as relações que influenciam a proposta. O motor contempla famílias de oitavas, duplas oitavas, quintas, quartas e duodécimas e, se habilitadas, terças maiores e menores quando há dados e relações compatíveis.

| Intervalo | Pares de ordens considerados (parcial da nota inferior : parcial da superior) |
| --- | --- |
| Oitava | 2:1, 4:2, 6:3, 8:4, 10:5 |
| Dupla oitava | 4:1, 8:2 |
| Quinta | 3:2, 6:4 |
| Quarta | 4:3, 8:6 |
| Duodécima | 3:1, 6:2, 9:3 |
| Terça maior | 5:4, 10:8 |
| Terça menor | 6:5, 12:10 |

Em Fidelidade o alvo para o desvio assinado entre parciais é aquele previsto pelo temperamento com uma série ideal. Em Otimização acústica, o alvo é a coincidência das componentes consideradas. As proteções explícitas conservam intervalos fundamentais e podem restringir o ajuste. Mesmo com B zero, a otimização acústica pode alterar relações desiguais intencionalmente temperadas.

Uma oitava de frequências fundamentais 2:1 não garante que o segundo parcial da tecla inferior coincida com a primeira componente da tecla superior. Para comparar acusticamente um intervalo, observe as ordens de parciais efetivamente usadas (por exemplo, 2:1 numa oitava ou 3:2 numa quinta) e as frequências correspondentes. Nem todas as relações serão reproduzidas perfeitamente ao mesmo tempo; pesos e restrições definem o compromisso.

Examine os resíduos antes e depois do ajuste, a diferença em Hz entre componentes, a origem de cada termo e **Proteção e diagnóstico**. Uma diferença de frequência não demonstra por si só um batimento audível: amplitudes, envelope, proximidade entre componentes, percepção e condições de captação também importam. A sensibilidade apresentada não foi calibrada como incerteza física de uma correção.

**Comparar os dois objetivos** calcula uma referência comparativa sem substituir a prévia original. Use para verificar o efeito de privilegiar a fidelidade à receita ou a coincidência acústica. **Exportar prévia inicial (JSON)** preserva o resultado inicial; **Descartar prévia** abandona a prévia de trabalho. Antes de descartar, exporte dados que deseje manter e confira separadamente o histórico de revisões.

<a name="revisar-curva"></a>
## 4.4. Revisar, editar e aprovar experimentalmente

### 4. Revisar e guardar curvas

A prévia deve existir antes de começar uma revisão nova. Em **Versão em revisão**, escolha o resultado que deseja inspecionar. O editor conserva uma história de versões, permitindo comparar efeitos sem alterar a versão original. Uma versão importada pode estar somente em leitura até que as fontes e a base sejam revalidadas.

| Ação | Efeito |
| --- | --- |
| Revalidar fontes para editar | Tenta verificar as fontes, reproduzir o cálculo e habilitar edição de uma versão. Se não reproduzir o resultado, mantenha o histórico em leitura e gere nova prévia a partir do perfil. |
| Desfazer / versão anterior | Retorna à versão anterior disponível para inspeção |
| Restaurar prévia original | Retorna à raiz da prévia original, preservando a distinção entre versões |
| Aprovar revisão experimental | Registra uma revisão completa e auditável após confirmação; não aplica os alvos |
| Aplicar experimentalmente e abrir Afinador | Revalida a revisão aprovada e guardada localmente, reproduz o cálculo e solicita confirmação explícita antes de aplicar |

### Editar correções e proteções (opcional)

1. Escolha uma **Tecla** com evidência suficiente no editor. Digite a **Correção fixa em cents** dentro de −30 a +30; acrescente um **Motivo** para rastreabilidade.
2. Pressione **Fixar e recalcular**. As outras correções são novamente calculadas sob as restrições. Não é simplesmente arrastar um ponto gráfico ou somar uma alteração a todas as frequências.
3. Use **Voltar ao cálculo automático** para remover a correção manual da tecla. A âncora não pode receber deslocamento diferente de zero; teclas sem evidência não podem ser usadas para inventar correções manuais.
4. Se quiser preservar um intervalo específico, escolha outra tecla em **Preservar o intervalo desta tecla com** e pressione **Proteger intervalo**. Use **Remover proteção individual** para retirar a restrição correspondente. A âncora e as proteções estritas têm prioridade. Restrições incompatíveis podem impedir a revisão.
5. Para investigar pesos, escolha estilo e objetivo, selecione **Família de intervalo** e **Multiplicador de peso (0,1 a 10)**. **Recalcular objetivo e peso** inicia nova otimização; o multiplicador atua sobre o peso-base do estilo escolhido. Ele não representa quantidade de cents. A caixa de proteção central mantém seu papel em Fidelidade. O editor também permite incluir terças maiores e menores e preservar terças próximas das puras.
6. Use **Cancelar revisão** se necessário. Em **Comparar versões e ver consequências musicais**, escolha uma versão compatível, outra tecla para o intervalo fundamental e uma relação de parciais para comparação. Observe as consequências antes de aprovar.

Não altere muitos pesos e correções simultaneamente durante um estudo. Registre o motivo das mudanças, compare com a prévia inicial e avalie se a relação melhorada foi obtida à custa de outras relações. Aprovação experimental significa revisão registrada para fins de estudo, não aplicação automática, homologação física ou garantia de qualidade.

<a name="historico-curva"></a>
## 4.5. Histórico local, exportação e compatibilidade

| Controle | Uso |
| --- | --- |
| Guardar histórico local | Armazena as versões no navegador; aguarde a confirmação da transação |
| Abrir histórico local | Recupera versões guardadas |
| Abrir backup de versões | Carrega um histórico JSON validado |
| Exportar histórico (JSON) | Faz cópia portátil das versões e evidências de auditoria, sem áudio |
| Limpar histórico temporário | Remove o histórico de trabalho em memória; exporte dados importantes antes |
| Gerenciar espaço local → Excluir cópia local do histórico | Remove a cópia armazenada correspondente, após verificação/confirmação solicitada |

O histórico possui limites de 128 versões e 32 MiB. Não presuma que novas revisões sobrescrevam automaticamente as antigas. Em caso de limite, exporte o histórico e trabalhe com os conjuntos necessários. Uma colisão de ID ou erro de integridade não deve ser resolvido editando identificadores no JSON.

A receita, a referência, o mapa físico e as fontes formam parte do contexto do cálculo. Alterá-los pode tornar versões incompatíveis com nova edição ou comparação. Recupere a configuração musical original e verifique as fontes. O histórico ainda pode servir como documentação de estudo em modo de leitura.

<a name="aplicar-curva"></a>
### Aplicar experimentalmente uma revisão ao Afinador

1. Gere uma prévia completa de Piano, Fortepiano ou Cravo, com a política de otimização da Etapa 17 (`17-1.0-experimental`). Revise as correções, intervalos fundamentais, origens e ressalvas.
2. Selecione a versão desejada em **Versão em revisão**, use **Aprovar revisão experimental** e confirme. Se necessário revalide antes as fontes para editar/aprovar.
3. Pressione **Guardar histórico local** e aguarde a confirmação de gravação. Exportar JSON não substitui este passo. Um backup aberto somente para estudo, sem os registros originais no banco local, não é suficiente para aplicar.
4. Escolha **Aplicar experimentalmente e abrir Afinador**. O programa confere a versão local, integridade, base musical, mapa e fontes acústicas exatas, inclusive se foram descartadas do modelo. Reproduz o cálculo e compara objetivo, correções, auditoria intervalar, diagnóstico e disposição. Se a reprodução divergir, gere nova prévia; não tente contornar os validadores.
5. Leia a confirmação **APLICAÇÃO EXPERIMENTAL — SEM HOMOLOGAÇÃO FÍSICA**. Verifique instrumento, versão, registro, base musical, intervalos modificados e cobertura; confirme somente se quiser ativar aqueles alvos. Cancelar não ativa a nova curva.
6. No Afinador, confira o painel de correção aplicada, compare alvos teórico e instrumental e examine os intervalos afetados. **Desligar correção** retorna à referência teórica.

A versão aplicada fica congelada: editar outra revisão não a substitui automaticamente. A aplicação é temporária, não volta ao reiniciar e pode ser invalidada por mudanças de base musical ou alterações nos dados de perfis/curvas. Teclas sem suporte, sem ligação à âncora ou fora do mapa permanecem teóricas. O Emissor começa com referência teórica mesmo quando a curva está aplicada; habilite **Seguir correção instrumental** ali somente se desejar (ver [5.1](#emitir)).

O recálculo tem limite de 60 segundos e pode ser cancelado ou invalidado por mudança de contexto. Não havendo confirmação de sucesso, confira o estado do Afinador antes de usar qualquer alvo. O aplicativo não emite recibo de homologação, e os campos científicos permanecem experimentais (`physicalValidation: pending`, `curveEligible: false`); não são uma autorização que possa ser obtida editando o JSON. A aplicação permite investigar as hipóteses do modelo de forma reversível, não certificar a afinação ou os limites seguros de tensão do instrumento.

<a name="cfg-4"></a>
## 4.6. Configurações de Curvas de afinação

As preferências de otimização se destinam a novos cálculos. A apresentação pode mudar sem recalcular as versões guardadas.

### Preferências de otimização (aberto)

| Campo | Padrão | Opções |
| --- | --- | --- |
| Objetivo | Fidelidade ao temperamento | Fidelidade ou Otimização acústica |
| Estilo | Equilibrado | Conservador, Equilibrado, Acústico |
| Fonte de parciais | Automática conservadora | Automática, Modelo B, Parciais medidos |
| Preferir proteção central | Sim | Preferência de proteção estrita no contexto aplicável |

### Pesos dos intervalos (recolhido)

| Família | Padrão | Faixa |
| --- | ---: | ---: |
| Oitava | 1 | 0,1–10 |
| Dupla oitava | 1 | 0,1–10 |
| Quinta | 1 | 0,1–10 |
| Quarta | 1 | 0,1–10 |
| Duodécima | 1 | 0,1–10 |
| Terça maior | 1 | 0,1–10 |
| Terça menor | 1 | 0,1–10 |

Os multiplicadores variam em passos de 0,1. Eles modificam o peso das relações presentes em novos cálculos. Não criam relações ausentes, não removem a âncora e não autorizam extrapolação. O editor de revisões possui controles próprios para recalcular uma versão.

### Apresentação (aberto)

| Campo | Padrão | Efeito |
| --- | --- | --- |
| Mostrar gráfico da prévia | Sim | Visibilidade do gráfico |
| Mostrar tabela de correções | Sim | Visibilidade da tabela de pontos |
| Mostrar pontos calculados | Sim | Filtro de resultados calculados |
| Mostrar interpolados | Sim | Filtro de interpolações |
| Mostrar pontos sem evidência | Sim | Filtro dos pontos sem correção suportada |
| Exibir sensibilidade | Sim | Barras quando disponíveis |
| Curva total relativa ao temperamento igual | Não | Referência visual alternativa em disposição cromática compatível |

A interpolação é confirmada na área de geração, não autorizada genericamente nas configurações. Restaurar padrões não desfaz revisões nem exclui históricos. O limite de correção ±30 cents, a âncora obrigatória, a proibição de extrapolação e as verificações de segurança continuam ativos.

<a name="ts-4"></a>
## 4.7. Troubleshooting — Curvas de afinação

| Sintoma | O que verificar |
| --- | --- |
| Perfil não aparece | Atualize a lista; crie/importe um perfil em Perfis ou abra backup compatível sem importar. |
| Família não suportada | Curvas são implementadas para Piano, Fortepiano e Cravo. Outro não é elegível, mesmo com B consistente. |
| Registro do cravo ausente | Informe o registro único representado e use fontes da mesma altura soante; não misture registros. |
| Não há âncora/teclas candidatas | Confira sessões elegíveis, identidade da tecla, corda isolada, mapa e referência musical. |
| Dados insuficientes | Examine as fontes recusadas e meça novas teclas/cordas. Não autorize interpolações sem justificativa física. |
| Sessões parecem consistentes mas não são usadas | Verifique os parâmetros acústicos personalizados, família, modelo, confirmação da tecla e coerência das fontes. |
| Mais de uma corda medida | Selecione fonte representativa quando possível ou deixe a tecla sem correção. Não some cordas diferentes como se fossem uma. |
| Não permite gerar prévia | Confirme ordem física, âncora e perfil elegíveis; veja restrições e mensagens. |
| Interpolação não aparece | Confirme região efetivamente homogênea e limites válidos; são necessários dados de suporte. Extrapolação não é permitida. |
| Gráfico tem lacunas ou pontos vazios | Indicam ausência de correção suportada ou filtro de apresentação; leia origens e tabelas. |
| Curva relativa ao igual indisponível | A disposição não permite aquela comparação cromática com A4; use referência ao temperamento base. |
| Correção manual recusada | Revise limite ±30, âncora, evidência da tecla e conflitos com proteções. |
| Revisão não recalcula | Verifique base musical, compatibilidade das fontes e restrições; aguarde/cancele cálculo ativo. |
| Backup abre apenas para leitura | Revalide as fontes. Se a reprodução não coincidir, preserve o histórico e gere nova prévia. |
| Não consegue aprovar | A revisão precisa ser completa, válida e auditável. Examine problemas da geração. |
| Aprovou mas o Afinador não mudou | Esperado: aprovação não aplica. Guarde o histórico local e use Aplicar experimentalmente e abrir Afinador. |
| Aplicação recusada | Confira versão aprovada e salva, fontes locais intactas, base musical e mapa; gere nova prévia se o recálculo divergir. |
| Curva não reaparece ao reabrir | Esperado: a aplicação não persiste; selecione revisão local, revalide e confirme novamente quando necessário. |
| Limite de espaço ou versões | Exporte histórico, verifique cópia e organize trabalhos menores; não apague a única evidência. |

[Voltar ao sumário](#sumario)

<a name="cap-5"></a>
# Capítulo 5 — Emissor de notas

O Emissor sintetiza sons a partir das referências musicais ou dos componentes de uma medição. Serve para estudar afinações, ouvir frequências, comparar séries harmônicas e inarmônicas e experimentar timbres sintéticos. Não é um player de gravações acústicas. Não requer microfone e não modifica as frequências do temperamento.

<a name="emitir"></a>
## 5.1. Emitir uma nota de referência

1. Escolha o temperamento e a referência musical desejados, conforme [Capítulo 1](#temperamentos).
2. Abra **Ferramentas → Emissor de notas**.
3. Escolha uma **Nota** na lista ou percorra as disponíveis com **◀ Nota / Nota ▶**. Confira as notações e a frequência selecionada.
4. A extensão padrão histórica vai de F1 a F7 (inclusive); **Ampliar extensão (C0–B9)** amplia o catálogo, respeitando a disponibilidade de alvos do layout. Em EDOs, a referência pode ser um grau.
5. Selecione o **Tipo de som**, começando por **Senoidal — som puro**. Deixe o **Volume** baixo (o padrão é 20%).
6. Pressione **▶ Emitir nota**. Use **■ Parar som** para interromper a emissão. Ao sair da ferramenta, o aplicativo encerra o som.

O controle de volume regula o ganho, não uma intensidade acústica calibrada. Mesmo com 20%, um amplificador ou fone pode produzir níveis elevados. Mantenha volume moderado, especialmente com ondas ricas em componentes agudas. Em frequências extremas, a resposta do equipamento e Nyquist limitam o som realizável.

Quando uma curva estiver aplicada experimentalmente ao Afinador, aparece **Seguir correção instrumental** no Emissor, inicialmente desmarcado. Marque para usar o alvo instrumental na geração baseada na nota selecionada; desmarque para retornar à frequência teórica. O modo Espectro medido Original continua usando as frequências observadas e não é transposto pela curva. Sem curva aplicada o controle fica oculto. Sons reconstruídos não se tornam alvos do Afinador.

## 5.2. Formas de onda e envelope

| Tipo de som | Característica esperada |
| --- | --- |
| Senoidal — som puro | Uma frequência idealmente dominante |
| Triangular — suave | Harmônicos ímpares com queda relativamente rápida |
| Quadrada — harmônicos ímpares | Timbre mais rico em harmônicos ímpares |
| Dente de serra — som brilhante | Série harmônica rica, com componentes pares e ímpares |
| Série inarmônica (B) | Modelo sintético de corda rígida, ajustável |
| Espectro medido | Reconstrução aditiva de componentes observados |
| Espectro personalizado | Componentes definidos pelo usuário por relação de frequência e amplitude relativa |

Estas são categorias de síntese; a resposta real do alto-falante, do navegador e do ouvido pode modificar a percepção.

Em **Envelope**, escolha **Contínuo** para sustentar o som até interromper ou **Ataque e decaimento** para uma emissão temporária de acordo com **Duração (segundos)** (0,2–20 s; padrão 3 s). O envelope é sintético e não recupera o transiente ou o decaimento particular de um instrumento medido. Ao mudar parâmetros durante emissão, observe o estado indicado e pare se necessário.

<a name="sintese"></a>
## 5.3. Série inarmônica: estudar o coeficiente B por audição

Escolha **Série inarmônica (B)**. Diferentemente da fórmula de ajuste acústico do [Capítulo 2](#coeficiente-b), aqui o primeiro parcial é ancorado na frequência da nota selecionada. O modelo de emissão é equivalente a:

`fₙ = n × f₁ × √[(1 + B × n²)/(1 + B)]`

Assim, alterar B conserva f₁ e desloca as componentes superiores. As amplitudes são sintéticas e seguem uma queda proporcional a `1/n^α`, antes da normalização de ganho.

| Campo | Padrão | Faixa e efeito |
| --- | ---: | --- |
| B (adimensional) | 0,00042 | 0–0,02; zero produz série idealmente harmônica |
| Quantidade de parciais | 8 | 1–32; componentes acima de Nyquist não são emitidas |
| Queda de amplitude (1/n^α) | 1 | 0–3; maior expoente enfraquece as componentes superiores |

### Experimento sugerido

Selecione Lá3 ou outra nota confortável. Mantenha quantidade e queda iguais; ouça primeiro B = 0 e, depois, B = 0,00042 ou outro valor permitido. Compare em volume baixo. Abra **Inspecionar espectro sintético** e observe quais frequências mudaram. Esse experimento isola uma propriedade do modelo; não pretende imitar integralmente o som de um piano.

**Usar B da medição selecionada** aproveita uma estimativa elegível fornecida pela medição escolhida, quando existente e compatível com os limites da síntese (0–0,02, independentemente do teto de 0,05 na análise de Outro). B ausente, inconclusivo ou não aplicável não deve ser substituído por um valor supostamente medido. É possível inserir valores manualmente para uma experiência teórica sem afirmar que representam o instrumento.

<a name="reconstrucao"></a>
## 5.4. Reconstruir um espectro medido

O aplicativo utiliza observações de uma execução, não gravações WAV e não uma média que apague as características da execução.

1. Obtenha uma captura em [Parciais](#cap-2) ou abra uma sessão em [Perfis](#cap-3).
2. No Emissor, selecione **Espectro medido**. Em Parciais, também é possível usar **Ouvir no Emissor** quando o resultado estiver disponível.
3. Escolha **Origem da medição**: **Último resultado exibido** ou **Perfil instrumental salvo**. Use **Carregar medições** para buscar as fontes.
4. Para perfil salvo, selecione **Instrumento**, **Sessão / nota / corda** e **Execução**. As opções dependem das medições verificadas e dos componentes utilizáveis.
5. Escolha **Reconstrução** e confira a lista de componentes. Se o modo exigir uma referência modal, escolha o **Pico de referência para transpor**.
6. Ajuste o volume, pressione **Emitir nota** e pare após ouvir.

| Reconstrução | Frequências emitidas | Uso |
| --- | --- | --- |
| Original · frequências observadas | Frequências registradas da execução | Ouvir uma aproximação do espectro tal como medido; mudar a nota selecionada não transpõe o original |
| Transposta · preservar relações | Frequências escaladas para a nota escolhida, mantendo proporções da fonte | Comparar estrutura em outro registro; sem fundamental atribuída, selecione pico de referência quando requerido |
| Harmônica equivalente | Componentes com ordem válida reorganizadas segundo múltiplos inteiros da mesma base | Comparar a estrutura harmônica ideal com o padrão observado/transposto compatível |

A versão harmônica equivalente só está disponível quando a fonte possui informação harmônica adequada. Para uma comparação controlada, o programa considera a mesma base, amplitudes e componentes reproduzíveis nos dois planos compatíveis; não se deve inventar uma fundamental ou ordens para um sino. Para séries harmônicas, a síntese seleciona parciais aceitos; em espectros modais/exploratórios, usa picos resolvidos provisoriamente, sem lhes atribuir ordens físicas. Parciais excluídos da revisão do perfil ficam de fora. Quando há mais de 32 componentes, o motor seleciona os de maior amplitude, respeitando a faixa reproduzível. O número de componentes também respeita limites de síntese e Nyquist.

A reconstrução não recupera fase original, ruído, ataque, modulações ou decaimentos reais. Um timbre reconstruído diferente do instrumento gravado não é necessariamente erro: o conjunto de frequências e magnitudes não determina toda a evolução temporal do som. Compare com o espectro sintético e não use a semelhança auditiva como prova do modelo físico.

<a name="personalizado"></a>
## 5.5. Construir um espectro personalizado

Escolha **Espectro personalizado** e abra **Editar componentes personalizados**. Cada linha contém a relação com a frequência-base e a amplitude em dB relativos, separadas por ponto e vírgula. Relações não precisam ser inteiras. Use número positivo para a relação e sinal de menos normal (`-`) para valores negativos. Por exemplo:

```text
1;0
2.01;-6
3.05;-12
4.12;-18
```

Para uma base de 220 Hz, esse exemplo define 220 Hz, 442,2 Hz, 671 Hz e 906,4 Hz. As magnitudes são relativas: −6 dB equivale aproximadamente à metade da amplitude (não metade da frequência). Não são níveis acústicos absolutos no ambiente.

Mude apenas uma linha de cada vez para estudar a contribuição de um componente. Aceita-se de 1 a 32 componentes personalizados, com relação maior que zero e até 128 e amplitude de −120 a 0 dB. Pontos ou vírgulas decimais são admitidos; linhas vazias e comentários iniciados por `#` são ignorados. Componentes calculados fora da faixa de 1 Hz até abaixo de Nyquist não são emitidos; se nenhum restar, a síntese é recusada. Confira as mensagens de validação se a entrada for recusada. O código normaliza ganhos para limitar a soma das amplitudes; aumentar a quantidade de componentes não aumenta incondicionalmente o volume total.

Em **Inspecionar espectro sintético**, confira componente, frequência em Hz, dB relativos e ganho normalizado. Antes de iniciar áudio, a prévia pode usar 48 kHz; a emissão real respeita a taxa de amostragem do contexto de áudio aberto. O gráfico/tabela descreve o sinal que o motor pretende sintetizar, não mede a resposta física do alto-falante.

<a name="cfg-5"></a>
## 5.6. Configurações do Emissor

### Reprodução (aberto)

| Campo | Padrão | Opções/faixa |
| --- | --- | --- |
| Volume inicial (%) | 20 | 0–100 |
| Forma de onda inicial | Senoidal | Senoidal, triangular, quadrada, dente de serra, série inarmônica |
| Envelope | Contínuo | Contínuo ou ataque e decaimento |
| Duração (s) | 3 | 0,2–20, passo 0,1 |
| Extensão ampliada de notas | Não | Ativa o catálogo ampliado |

O seletor inicial não inclui espectro medido ou personalizado: essas modalidades dependem da escolha operacional de fonte/componentes. Nenhum ajuste inicia áudio automaticamente.

### Síntese aditiva (recolhido)

| Campo | Padrão | Faixa/efeito |
| --- | ---: | --- |
| Quantidade de componentes | 8 | 1–32 |
| Coeficiente B | 0,00042 | 0–0,02, passo 0,00001 |
| Queda de amplitudes | 1 | 0–3, passo 0,1 |
| Expandir espectro sintético | Não | Abre a inspeção detalhada |

### Espectro medido (recolhido)

| Campo | Padrão | Efeito |
| --- | --- | --- |
| Reconstrução preferida | Original | Original, Transposta ou Harmônica equivalente; depende da compatibilidade efetiva da fonte |

Use os controles diretamente no Emissor para alterações de uso frequente. Salvar conserva as preferências admitidas pela janela, não cria uma gravação, não salva a seleção de um perfil inteiro como preset sonoro e não inicia a reprodução na próxima visita. Restaurar padrões aplica os valores de fábrica do Emissor e não exclui medições nem altera a receita musical.

<a name="ts-5"></a>
## 5.7. Troubleshooting — Emissor de notas

| Sintoma | O que verificar |
| --- | --- |
| Sem som | Pressione Emitir nota explicitamente, confira volume do aplicativo/dispositivo, saída de áudio, estado do navegador e nota válida. Não precisa ativar microfone. |
| Som termina antes do esperado | Confira envelope e duração; sair do Emissor encerra a emissão. |
| Som permanece contínuo | Use Parar som ou escolha Ataque e decaimento para emissão temporária. |
| A frequência parece errada | Confira temperamento, referência, nota e oitava; no modo Original, a seleção de nota não modifica frequências observadas. |
| Nota extrema não aparece | Confira extensão ampliada, catálogo e layout atual; Nyquist e limites do motor ainda se aplicam. |
| B não pode ser usado | A fonte pode não possuir B elegível ou o valor pode estar fora dos limites de síntese. Escolha experiência manual, sem atribuí-la à medição. |
| Perfil/sessão não carrega | Confira banco, compatibilidade e integridade. Se necessário, selecione último resultado exibido em Parciais. |
| Nenhuma execução com componentes utilizáveis | Revise aceitação dos parciais e condições da captura. Faça nova medição se necessário. |
| Harmônica equivalente indisponível | A fonte não possui atribuições harmônicas compatíveis. Use Original ou Transposta, conforme as opções disponíveis. |
| Transposição exige referência | Escolha um pico medido de referência, se a interface solicitar. Não invente fundamental. |
| Componentes superiores não aparecem | Confira limite de 32 componentes, ordem desejada e frequência de Nyquist. A prévia e a taxa real podem diferir. |
| Espectro personalizado recusado | Verifique uma relação e um valor em dB por linha, ponto e vírgula, sinais e valores numéricos finitos. |
| Reconstrução não parece com o instrumento | Esperado em muitos casos: fase, ruído, envoltória e transientes reais não são recuperados. |
| Medição entra em realimentação ou mostra som emitido | Pare o Emissor antes de medir; evite captação do alto-falante. |
| Curva aprovada não afeta a emissão | Aprovar não aplica. Aplique experimentalmente em Curvas e habilite Seguir correção instrumental no Emissor. O modo Original preserva as frequências observadas. |

[Voltar ao sumário](#sumario)

<a name="glossario"></a>
# Apêndice A — Glossário

| Termo | Definição operacional |
| --- | --- |
| A4 / Lá4 | Referência musical absoluta do domínio histórico |
| Altura | Propriedade periódica ou percebida associada à frequência de uma nota; não necessariamente o maior pico |
| Ataque / execução | Um evento de produção de som; na coleta multiataque constitui uma unidade de observação independente quando efetivamente repetido |
| Âncora | Tecla mantida na frequência teórica em uma curva; em EDO, referência de grau, oitava e frequência |
| B | Coeficiente adimensional de inarmonicidade do modelo de corda rígida |
| Batimento | Variação de amplitude que pode ocorrer entre componentes de frequências próximas; sua frequência ideal é a diferença absoluta em Hz |
| Bin | Posição discreta de frequência na FFT |
| Bootstrap | Reamostragem de observações para avaliar variação estatística; não elimina viés físico |
| Cent (¢) | Intervalo logarítmico; 1.200 cents por oitava |
| Correção instrumental | Deslocamento em cents sobre o alvo teórico, calculado ou revisto para um perfil; aplicação temporária e experimental. |
| CMNDF | Função de diferença cumulativa normalizada do YIN |
| Coma pitagórico | Diferença entre 12 quintas puras e 7 oitavas (~23,460 cents) |
| Coma sintônico | Diferença entre terça de quatro quintas puras e terça pura 5:4 (~21,506 cents) |
| dB | Unidade logarítmica de razão; amplitude relativa não é nível acústico SPL calibrado |
| EDO | Divisão igual da oitava |
| Enarmonia | Grafias musicais distintas que podem coincidir ou não em frequência |
| FFT | Algoritmo de transformada de Fourier que calcula representação em frequência |
| Fundamental | Frequência-base da periodicidade ou série inferida; o primeiro parcial observado pode estar ausente |
| Harmônico | Componente correspondente a múltiplo inteiro da fundamental no modelo ideal |
| Histerese | Regra de estabilidade que evita mudanças de estado pouco sustentadas |
| Huber | Perda robusta que reduz a influência de grandes erros de previsão |
| Inarmonicidade | Desvio em relação a uma série ideal de múltiplos inteiros |
| Interpolação | Estimativa entre pontos com evidência, condicionada à homogeneidade da região |
| Janela | Trecho de áudio analisado; uma função de ponderação como Hann/Blackman modifica a distribuição espectral |
| Modelo acústico | Hipótese de interpretação: corda rígida, série harmônica, componentes não harmônicos ou exploratório; não é sinônimo de família instrumental. |
| Nyquist | Metade da taxa de amostragem; limite de representação do sinal digital |
| Parcial | Componente de frequência de um som; nem todo parcial é harmônico |
| PCM | Amostras digitais que representam o sinal de áudio |
| Pico | Máximo local no espectro; não necessariamente fundamental ou modo físico |
| Quintas — cadeia/ciclo | Relações sucessivas de quinta; a cadeia tem extremos, o ciclo fecha |
| Quinta do lobo | Relação residual excepcional entre extremos de uma cadeia num teclado limitado |
| Resíduo | Diferença entre valor observado e valor previsto pelo modelo |
| Saliência | Evidência de um padrão de frequência no método SWIPE′; não é probabilidade calibrada por si só |
| SHA-256 | Função de hash usada para verificar integridade de conteúdos |
| SNR | Relação sinal/ruído estimada, geralmente expressa em dB |
| Temperamento | Distribuição das relações intervalares de uma afinação |
| Viterbi causal | Acompanhamento de estados de altura usando as observações disponíveis ao longo do tempo |
| WAV | Formato que pode guardar PCM; opcional no diagnóstico convencional |
| Worker / AudioWorklet | Mecanismos do navegador para processamento separado e coleta de áudio |
| WebAssembly / SIMD | Código compilado e operações vetoriais utilizados para otimizar cálculos |
| Zero-padding | Acrescentar zeros antes da FFT para representar uma grade espectral mais densa; não aumenta a informação captada |

<a name="relatos"></a>
# Apêndice B — Relatar problemas e preservar dados

Para uma investigação reproduzível, comece com os padrões da ferramenta e altere somente o parâmetro em estudo. Anote as configurações e a referência musical; diferencie falha de aquisição, falha de interpretação do resultado e falta efetiva de evidência. Não confunda dados insuficientes com defeito automático do programa.

Antes de limpar armazenamento, atualizar o arquivo local ou trocar de aparelho, exporte a biblioteca musical, os perfis, as sessões em andamento e os históricos de interesse, conforme aplicável. Confirme que as cópias foram gravadas. Não limpe o armazenamento como primeira medida de troubleshooting: isso pode apagar a única evidência.

Ao abrir um [relato de problema no GitHub](https://github.com/mv-pereira/Afinador/issues), inclua:

- Versão/arquivo HTML utilizado, ferramenta, navegador, sistema operacional e tipo de dispositivo (quando conhecido).
- Família, modelo acústico e condição do instrumento, nota, temperamento, frequência de referência e forma de produção do som, quando afetarem o resultado.
- Passos para reproduzir, comportamento esperado, resultado observado e mensagem apresentada.
- Preferências diferentes do padrão, possibilidade de reproduzir após restaurá-las e efeito de mudar somente um parâmetro.
- Evidência apropriada: diagnóstico ZIP para problemas do detector convencional; JSON de análise/sessão para problemas de parciais/B; backup de perfil ou histórico para falhas de organização ou curva; parâmetros e lista de componentes para síntese. Um screenshot real da interface também pode ajudar a explicar o problema.

Revise os arquivos antes de compartilhar. Um WAV pode conter vozes, sons do ambiente e informações privadas; os JSONs podem incluir nomes de instrumento, observações e contexto técnico. A captura de áudio é opcional no diagnóstico e não é necessária para todo relato.

## Limites de interpretação e validação

Os cálculos do projeto foram submetidos a testes computacionais, incluindo regressões de detectores, análises, configurações, importações e síntese. Isso não é homologação física para todos os instrumentos, navegadores e microfones. A precisão depende da cadeia de captação, do sinal, do modelo e das configurações. Não há garantia de exatidão universal em cents, de incerteza calibrada de B ou de correções instrumentais apropriadas para uso real. A possibilidade de aplicar uma curva experimental aos alvos não altera esse limite científico. Consulte o [README](README.md) para os fundamentos, créditos, arquitetura, condições de compatibilidade e licença.

[Voltar ao sumário](#sumario) · [Abrir o Afinador](https://mv-pereira.github.io/Afinador/)
