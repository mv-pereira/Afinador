# Guia de uso — Afinador · Oficina Pernambuco

**[Abrir o Afinador](https://mv-pereira.github.io/Afinador/)** · [README do projeto](README.md)

Este guia em português do Brasil apresenta as cinco ferramentas do Afinador · Oficina Pernambuco. Em cada capítulo, primeiro vem o **uso básico**, depois o **inventário de controles operacionais e de Avançado**, seguido dos **parâmetros de Configurações com padrões, faixas, significado e riscos**. Os fundamentos acústicos, exemplos, importação/exportação, segurança, solução de problemas e glossário completam a consulta. Consulte também a Ajuda da ferramenta aberta.

> **Limite científico importante:** o afinador convencional permite comparar uma nota com uma referência musical. As medições de inarmonicidade, os ajustes físicos e as curvas instrumentais são experimentais e ainda não foram homologados fisicamente. Uma revisão aprovada de piano, fortepiano ou cravo, ou de Outro pela fonte empírica independente de B, pode ser aplicada experimentalmente aos alvos do Afinador, após armazenamento local, revalidação das fontes, reprodução do cálculo e confirmação explícita. Isso não constitui homologação física nem recomendação universal de afinação.

<a name="sumario"></a>
## Sumário

- [Comece aqui — uso rápido](#inicio-rapido)
- [Capítulo 0 — Panorama e preparação](#cap-0): [ferramentas](#escolha), [primeiro acesso](#preparacao), [configurações](#configuracoes), [ajuda](#ajuda-contextual), [dados](#dados).
- [Capítulo 1 — Afinador](#cap-1): [afinar](#afinar), [controles](#controles-afinador), [configurações](#cfg-1), [detectores](#detectores), [FFT](#fft), [temperamentos](#temperamentos), [cilindro](#cilindro), [teclados e EDO](#teclados), [biblioteca](#biblioteca), [diagnóstico](#diagnostico).
- [Capítulo 2 — Aquisição e Análise acústica](#cap-2): [modelos](#modelos), [captura individual](#captura-individual), [multiataque e salvamento](#multiataque), [revisão](#revisao-historica), [sete gráficos instrumentais](#analise-instrumental), [controles](#controles-parciais), [configurações](#cfg-2), [interpretação](#interpretar-parciais), [B](#coeficiente-b), [consolidação](#consolidacao), [caracterização empírica](#empirica), [problemas](#ts-2).
- [Capítulo 3 — Gerenciador de instrumentos](#cap-3): [criar perfil](#criar-perfil), [salvar sessões](#salvar-sessoes), [controles](#controles-perfis), [configurações](#cfg-3), [mapa e histórico](#comparar-sessoes), [backup](#backup-perfil), [problemas](#ts-3).
- [Capítulo 4 — Curvas de afinação](#cap-4): [pré-requisitos](#pre-curva), [gerar](#gerar-curva), [controles](#controles-curvas), [configurações](#cfg-4), [fonte empírica](#curva-empirica), [interpretar](#ler-curva), [revisar](#revisar-curva), [histórico](#historico-curva), [aplicar](#aplicar-curva), [problemas](#ts-4).
- [Capítulo 5 — Emissor de notas](#cap-5): [emitir](#emitir), [controles](#controles-emissor), [configurações](#cfg-5), [síntese](#sintese), [espectro medido](#reconstrucao), [síntese consolidada](#sintese-empirica), [personalizado](#personalizado), [problemas](#ts-5).
- [Apêndice A — Glossário](#glossario) · [Apêndice B — Relatar problemas e preservar dados](#relatos).

<a name="inicio-rapido"></a>
## Comece aqui — uso rápido

Escolha a ferramenta no menu **Ferramentas**. Não é necessário criar um perfil para afinar ou emitir notas.

| Quero… | Procedimento essencial |
| --- | --- |
| Afinar | Afinador → escolha temperamento e referência → ative microfone → toque uma nota → ajuste até aproximar o desvio de zero. [Detalhes](#afinar) |
| Medir uma nota | Aquisição acústica → escolha família, condição e identificação → Iniciar medição → repita a mesma nota → Finalizar medição. [Detalhes](#multiataque) |
| Medir várias notas | Aquisição acústica → Instrumentos → Novo perfil → criar → Voltar à ferramenta → medir e finalizar → **Salvar e medir próxima nota**. Repita com as notas desejadas, sem preencher a extensão. [Detalhes](#salvar-sessoes) |
| Estudar as medições | Análise acústica → escolha Rascunho atual, Medições armazenadas ou Abrir sessão… → Sessão, Nota ou Instrumento. [Detalhes](#revisao-historica) |
| Ver o timbre e a inarmonicidade de um instrumento | Análise acústica → Instrumento → Calcular / atualizar → escolha a fonte e abra o gráfico desejado. [Detalhes](#analise-instrumental) |
| Transferir um instrumento | Aquisição acústica → Instrumentos → Exportar perfil (.afp) ou Importar instrumento. [Detalhes](#backup-perfil) |
| Estudar correções | Curvas de afinação → perfil e objetivo → Gerar curva → revisar → Aplicar ao Afinador, se elegível e desejado. |
| Ouvir uma nota | Emissor de notas → escolha nota, tipo de som e volume → Emitir nota → Parar som. |

**Avançado** reúne controles complementares; **Configurações** define preferências persistentes; **Ajuda** explica controles e limitações. O gerenciador **Instrumentos** é contextual: use **Voltar à ferramenta** para continuar o trabalho. Selecionar um instrumento não altera automaticamente o temperamento ou a curva aplicada.

[Voltar ao sumário](#sumario)

<a name="cap-0"></a>
# Capítulo 0 — Panorama e preparação

<a name="escolha"></a>
## 0.1. O que cada ferramenta faz

Abra **Ferramentas** na barra superior e selecione o ambiente de trabalho desejado. Os botões **Configurações** e **Ajuda** acompanham a ferramenta ativa, inclusive o gerenciador Instrumentos. A Aquisição possui parâmetros de captação e processamento; a Análise possui somente preferências de apresentação da sessão. O tema é um controle independente.

| Ferramenta | Pergunta que responde | Entrada | Saída |
| --- | --- | --- | --- |
| Afinador | A nota está acima ou abaixo do alvo? | Som isolado e referência musical | Altura, desvio, espectro e temperamento |
| Aquisição acústica | Como obter evidência acústica repetível? | Captura individual ou multiataque | Sessão, resumo e salvamento assistido |
| Análise acústica | Quais propriedades acústicas as observações sustentam? | Rascunho, sessões importadas ou armazenadas | Revisões, estatísticas e gráficos de sessão, nota e instrumento |
| Curvas de afinação | Que correções poderiam conciliar propriedades acústicas e afinação? | Perfil elegível, referência e objetivos | Prévia, revisões e aplicação experimental reversível |
| Emissor de notas | Como soa uma frequência ou um espectro sintetizado? | Nota, parâmetros ou medição | Som gerado e espectro sintético |

O gerenciador contextual **Instrumentos** conserva e organiza medições, perfis e backups. Não é necessário usá-lo para afinar uma nota ou emitir som.

### Fluxos recomendados

| Finalidade | Percurso |
| --- | --- |
| Afinação habitual | Afinador → referência → detector → ajuste físico |
| Estudo de temperamento | Afinador → preset → cilindro/matriz → biblioteca → Emissor |
| Investigação de timbre | Aquisição → ataques → Análise → Sessão ou Instrumento → Emissor (opcional) |
| Medição de um cravo | Instrumentos → criar perfil → Aquisição → salvar e medir próxima nota em ordem livre → Análise |
| Repetibilidade | Aquisição → repetir ataques → salvar → Análise → Nota ou Instrumento → G06 |
| Estudo de curva | Medir fontes isoladas e identificadas → salvar → Curvas → selecionar fonte elegível → gerar e revisar |

### O que é compartilhado e o que é independente

A referência musical (temperamento, teclas, ajustes e frequência de referência) fornece os alvos teóricos do Afinador e do Emissor e o contexto para identificar medições. Alterá-la não modifica o som que já foi registrado. Uma sessão acústica conserva seu contexto original; uma curva depende de uma base musical compatível. A referência teórica é o padrão; uma curva aplicada modifica somente os alvos instrumentais, não a receita de temperamento. O Emissor começa sem seguir a correção. O detector de frequência, a análise de parciais, a otimização de curvas e o sintetizador são processos diferentes.

**Segurança de curvas.** O padrão é referência teórica, sem botão de curva no Afinador. Salvar medições novas não gera nem aplica uma curva. Alterar quantidade de teclas, enarmonia adicional de 13 teclas, receita/referência musical ou disposição do perfil usado por uma curva ativa desativa sua aplicação com aviso; voltar à configuração anterior não a reativa. Curvas salvas e sessões não são excluídas pela desativação. A aplicação posterior exige escolha explícita e revalidação.

**Instrumento ativo.** Aquisição, Análise, Curvas e Emissor compartilham a identidade do instrumento e, quando pertinente, a seleção de tecla, sessão e execução durante a visita. A escolha fica disponível ao navegar pelo menu; recarregar a página exige selecionar novamente o instrumento. As evidências são lidas sob demanda, não todas de uma vez. A revisão histórica não substitui uma aquisição em trabalho. O Afinador conserva seus próprios alvos e controles; selecionar um instrumento não aplica curvas nem altera a receita musical.

<a name="preparacao"></a>
## 0.2. Primeiro acesso e preparação

1. Acesse o [aplicativo publicado](https://mv-pereira.github.io/Afinador/) em um navegador moderno com JavaScript habilitado.
2. Para medir som, pressione **Ativar microfone** e autorize a captura. Para apenas estudar temperamentos, consultar perfis, calcular curvas ou emitir notas, não é necessário ligar o microfone.
3. Escolha a ferramenta e confira a referência musical na área de seleção de temperamento quando pertinente. O padrão musical de fábrica do Afinador é o sistema Pitagórico com Lá4 = 415,3 Hz; não presuma que seja o temperamento igual a 440 Hz.
4. Posicione o instrumento e o dispositivo de modo a obter um som claro, sem saturação. Evite TV, ventilador, conversas, outros instrumentos e reverberação excessiva.
5. Toque uma nota isolada. Aguarde uma leitura útil antes de ajustar o instrumento ou interpretar a análise.
6. Ao terminar de medir, desligue o microfone no botão superior. Ao terminar de ouvir, pressione **Parar som** no Emissor.

A publicação pode ser instalada como PWA quando o navegador oferecer a opção. O uso offline depende da preparação bem-sucedida do cache; teste sem rede antes de depender dele. O arquivo HTML local não garante as mesmas APIs nem compartilha necessariamente os dados do site.

O acesso ao microfone depende de permissão do navegador e de contexto seguro (HTTPS ou localhost). Um HTML aberto diretamente do disco pode funcionar parcialmente; não é garantido que todas as APIs de captura, integridade e armazenamento estejam disponíveis. Abrir por HTTP através do endereço IP de outro computador também pode impedir a captura. Consulte o [README](README.md) para execução local.

### Boas práticas de captação

- Escolha uma distância que não sature o microfone e não deixe o som desaparecer no ruído; mantenha posição, orientação e intensidade semelhantes ao comparar registros.
- Evite tocar acordes para o detector de altura. Para analisar uma nota composta por várias cordas, declare a condição real; não declare uma corda isolada se outras vibram.
- Em instrumentos de sopro, mantenha dedilhado, embocadura e intensidade controlados. Em cordas e percussão, repita técnica e ponto de excitação.
- Mantenha a página em primeiro plano durante uma sessão. Ao ocultar a página ou sair dela, o aplicativo encerra a captura, inclusive uma ativação pendente; ao retornar, ligue o microfone manualmente. A entrega dos eventos de visibilidade depende do navegador e do sistema.
- Não emita som pelo alto-falante enquanto mede o instrumento. Fones podem reduzir a contaminação acústica, mas a síntese não substitui um padrão físico calibrado.

<a name="configuracoes"></a>
## 0.3. Configurações, salvamento e restauração

Em cada ferramenta, pressione **⚙ Configurações**. Grupos simples começam expandidos; grupos avançados começam recolhidos. Abra um grupo para ver seus parâmetros e a indicação do padrão original. Em Aquisição, Análise, Instrumentos, Curvas e Emissor, as seções **Avançado** da própria tela reúnem opções operacionais complementares e começam recolhidas. Recolher não desfaz valores. As Configurações definem padrões persistentes; consultar a Ajuda não altera preferências.

| Ação | Efeito nesta visita | Efeito na próxima inicialização |
| --- | --- | --- |
| Alterar um campo válido | Aplica a preferência; nos campos numéricos, confirme a edição ou saia do campo | Não muda por si só o registro salvo |
| Salvar alterações | Mantém os valores em uso, sem um reset adicional | Grava as preferências da ferramenta |
| Fechar | Fecha a janela, mantendo alterações válidas | Não salva nem restaura |
| Restaurar padrões | Após confirmação, aplica os valores de fábrica | Sobrescreve o registro salvo; não precisa salvar outra vez |

Valores inválidos ou conjuntos incompatíveis não substituem os últimos valores válidos. Leia a mensagem da janela, corrija os campos ou restaure os padrões. Se o navegador não permitir gravar, as mudanças podem funcionar somente nesta visita.

Há exceções propositais à aplicação imediata: os parâmetros acústicos da aquisição são fixados no início da sessão; novas preferências valem para a próxima. Em Curvas, mudanças de otimização valem no novo cálculo, não alterando resultados anteriores. As preferências visuais não reinicializam detectores. Durante um diagnóstico ativo, finalize-o antes de modificar as configurações do Afinador.

**Restaurar padrões não é apagar dados.** O comando atua apenas na ferramenta aberta. Não restaura o temperamento, não exclui medições ou históricos e não apaga preferências das outras ferramentas. Há comandos próprios para restaurar a receita musical e para gerenciar registros.

<a name="ajuda-contextual"></a>
## 0.4. Ajuda contextual

O botão **Ajuda** acompanha a ferramenta ativa. A **Ajuda rápida** apresenta o procedimento essencial; abra **Ajuda avançada** e seus capítulos recolhíveis para detalhes, fundamentos, parâmetros, glossário e problemas comuns. Feche pelo controle **Fechar ×**. A consulta não inicia microfone, emissão ou cálculo. A ajuda incorporada funciona sem rede; os links para o capítulo completo deste guia e para tabelas de parâmetros abrem o GitHub e exigem conexão.

<a name="dados"></a>
## 0.5. Armazenamento, privacidade e arquivos

O processamento ocorre no navegador. O aplicativo não envia automaticamente as amostras de áudio ou as medições a um servidor. As preferências e a biblioteca musical são locais; perfis e históricos de curvas usam o banco de dados do navegador (IndexedDB). Navegação privada, limpeza de dados do site, alteração de endereço e troca de aparelho podem tornar esses registros indisponíveis. Salvar no navegador não é fazer um backup externo. Use apenas uma aba ou janela do Afinador por vez, inclusive durante importações, exportações ou recuperação de transferências.

| Arquivo | Finalidade | Onde nasce |
| --- | --- | --- |
| JSON de afinação / perfil musical | Receita musical, disposição e, no perfil, referência de frequência | Biblioteca pessoal do Afinador |
| JSON de análise individual | Observações acústicas de uma captura | Aquisição / Análise |
| AFS (.afs) | Sessão multiataque binária, com evidências e revisões | Aquisição / Análise / Instrumentos |
| AFP (.afp) | Backup binário de perfil instrumental e registros | Instrumentos |
| AFC (.afc) | Backup binário do histórico de curvas | Curvas |
| JSON de sessão, perfil instrumental ou histórico de curvas | Intercâmbio científico estruturado, conforme o tipo | Aquisição / Análise / Instrumentos / Curvas |
| ZIP de diagnóstico | `diagnostico.json` e, opcionalmente, `audio.wav` | Afinador |
| JSON de desempenho | Tempos, contagens, tamanhos e limites observados, sem dados acústicos ou identificação | Avançado das ferramentas com diagnóstico de desempenho |

Não confunda **perfil musical** (receita de afinação) com **perfil instrumental** (coleção de evidências acústicas). Perfis e curvas usam armazenamento binário; os formatos JSON compatíveis estão disponíveis para intercâmbio. Use arquivos exportados pelo aplicativo no formato aceito; arquivos com esquemas não suportados são recusados. AFP, AFS e AFC não contêm gravações WAV. Abra cada arquivo na ferramenta apropriada; o aplicativo não é um importador genérico de escalas ou áudio. Os arquivos passam por validação estrutural, limites e coerência. SHA-256 verifica integridade, não autoria nem veracidade física. Não edite modelos, identificadores ou hashes para forçar aceitação. Consulte [backups e limites](#backup-perfil).

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

Por padrão, o Afinador usa apenas a referência teórica e não mostra um painel de curva nem um botão para abrir Curvas. Para gerar ou aplicar uma curva, vá deliberadamente a **Ferramentas → Curvas de afinação** e siga [4.7](#aplicar-curva). Uma prévia ou aprovação não modifica a afinação.

Após aplicar uma curva, o Afinador mostra apenas **Correção instrumental · Fidelidade ao temperamento** (ou **Otimização acústica**, conforme o objetivo) e um seletor entre **Sem correção** e **Correção ativa**. Não mostra nome extenso do perfil, quantidade de teclas ou contagem de intervalos. Enquanto o seletor está à direita, os alvos elegíveis são corrigidos; teclas sem correção suportada e fora do mapa permanecem teóricas. Coincidências acústicas efetivas podem exigir seleção de tecla física.

Mover o seletor para **Sem correção** retorna imediatamente aos alvos teóricos, mantendo o painel visível nesta visita. Para religar, mova-o à direita: o aplicativo verifica novamente a revisão armazenada, as fontes e a compatibilidade antes de ativar os alvos. Se a verificação falhar, permanece desligado e informa o motivo sem janela do navegador. Alterações na base musical ou nos perfis/curvas invalidam a aplicação e ocultam o painel; a curva não volta automaticamente ao reabrir a página. O cilindro e as tabelas de temperamento continuam teóricos.

<a name="controles-afinador"></a>
## 1.2. Controles selecionáveis, edição musical e opções avançadas

Esta seção é o **inventário de controles operacionais** do Afinador. Os valores de processamento ajustáveis em **⚙ Configurações** aparecem imediatamente na seção seguinte, com os padrões e limites. Os controles da referência musical não são parâmetros do detector acústico: mudar o temperamento modifica o alvo com que o som é comparado, não a frequência que o microfone captou.

### Operação principal e leitura

| Controle | Objetivo e quando usar | Efeito, observações e limites |
| --- | --- | --- |
| **Ativar microfone / Parar microfone** | Iniciar ou interromper a captação | Requer permissão em contexto seguro; permite cancelar uma ativação pendente. Ocultar a página encerra a captura; retornar não a reativa. Não inicia análise da análise acústica nem salva sessões. |
| **Ferramentas** | Alternar Afinador, Aquisição acústica, Análise acústica, Curvas e Emissor | A troca pode encerrar operações de áudio em curso; não é comando de gravação. |
| **Ajuda** | Consultar procedimentos, explicações e limitações | Não altera a configuração e pode ser consultada sem rede. |
| **Tema claro/escuro** | Melhorar contraste segundo o ambiente | Só modifica a aparência; não recalcula frequências. |
| **Automático / Nota fixa** | Decidir como selecionar a referência musical | Automático acompanha a nota detectada; Nota fixa conserva a tecla escolhida, ideal para teclas enarmônicas ou sons instáveis. |
| **Seletor de tecla** | Determinar o alvo no modo Nota fixa | Oferece as identidades musicais da configuração atual; notas acusticamente coincidentes podem continuar sendo teclas físicas distintas. |
| **< e >** | Percorrer teclas ou graus adjacentes | No cromático de 12 notas equivalem a semitons; em EDO percorrem graus; dependem dos limites do catálogo. |
| **« 8ª / » 8ª** | Descer/subir uma oitava sem mudar a identidade da tecla | Não se confundem com o avanço de um grau e não ultrapassam o catálogo. |
| **Botão da nota (científica / Helmholtz)** | Alternar qual notação aparece em destaque | A notação alternativa fica menor; não muda a frequência nem a tecla física. |
| **YIN + FFT, pYIN, SWIPE′, Pico** | Escolher **um** método de detecção por vez | YIN + FFT é o ponto de partida; pYIN acompanha continuidade; SWIPE′ usa saliência espectral; Pico pode escolher um harmônico em vez da fundamental. |
| **Toque ou clique no Espectro FFT** | Alternar a escala horizontal entre logarítmica e linear | Também disponível pelo teclado e em Configurações → Visualização → Escala espectral. Logarítmica é o padrão. Só redesenha o gráfico, sem reiniciar o DSP. |
| **Zoom na nota-alvo (±100 cents)** | Inspecionar o espectro próximo ao alvo | Não aumenta resolução acústica, não muda bins nem reinicia detector. |
| **Temperamento** | Escolher a receita de intervalos | Pode invalidar imediatamente uma curva instrumental aplicada; não modifica medições históricas já gravadas. |
| **Lá de referência (A4)** | Definir a altura absoluta da receita histórica | Padrão 415,3 Hz; escolha 440 Hz somente se for a referência pretendida; mudança de referência pode desativar uma curva aplicada. |
| **Correção ativa / Sem correção** | Habilitar/desabilitar uma curva **já aplicada explicitamente** em Curvas | Não aparece no estado inicial sem curva; reativação exige revalidação. Alteração incompatível da base musical desativa a curva com aviso, sem reativá-la ao voltar à escolha anterior. |
| **Dispensar aviso de incompatibilidade** | Fechar a mensagem que explica uma desativação | Fechar o aviso **não reativa** a curva; o estado permanece teórico. |

### Temperamento histórico, teclas adicionais e quinta compensatória

| Controle / área | Para que serve | Cuidados técnicos |
| --- | --- | --- |
| **Teclas por oitava: 12, 13, 14** | Configurar a disposição musical usada pelo Afinador e como ponto de partida de **novos** perfis | O perfil instrumental já criado mantém sua disposição própria. Mudar aqui não altera seu mapa físico, mas invalida a curva ativa incompatível. |
| **Alternar par enarmônico** | Escolher qual divisão histórica aparece na disposição de 13 teclas | Distingue Ré♯/Mi♭ da divisão Sol♯/Lá♭; a tecla extra é uma identidade física, não uma simples troca de grafia. |
| **Grafia enarmônica** | Variar a designação musical apresentada | Muda nomes/seleção quando aplicável; verifique a identidade antes de medições e curvas. |
| **Desfazer disposição** | Reverter a última mudança de layout quando houver histórico aplicável | Não recupera automaticamente curva desativada por incompatibilidade. |
| **Fontes, variante e atribuição deste temperamento** | Consultar procedência e ressalvas do preset | Atribuições históricas ou reconstruções não são provas de autenticidade inequívoca. |
| **Tabela de ajuste de comas** | Editar cada quinta por coeficientes independentes de coma pitagórico (c.p.) e sintônico (c.s.) | Aceita frações racionais e decimais dentro dos limites; valores inválidos não são publicados. Observe as alterações em toda a receita. |
| **Quinta compensatória (ao editar um ciclo)** | Escolher qual quinta absorve a compensação necessária ao fechamento | Em ciclo de doze quintas, os coeficientes devem fechar: soma de c.p. = −1 e soma de c.s. = 0. Não se aplica como regra de fechamento a toda cadeia aberta. |
| **Zerar ajustes** | Voltar aos ajustes associados ao preset | Não significa transformar todas as quintas em puras. |
| **Editar quintas adicionais · c.p. e c.s.** | Ajustar frequências das identidades extras de 13/14 teclas | Evite confundir uma tecla adicional com novo grau de EDO; verificações da base podem desativar a correção instrumental. |
| **Cilindro acústico** | Verificar visualmente a sucessão das quintas e desvios acumulados | É uma visualização teórica, não um sensor acústico nem um medidor independente. |
| **Tabela de intervalos — Desvios** | Comparar intervalos gerados com razões puras de referência | Desvio de uma terça em relação à terça pura não equivale a “erro” do próprio temperamento. |
| **Grau inicial** (matriz EDO) | Definir de qual grau começa a matriz intervalar | Modifica a comparação exibida; não retuna graus. |

### Divisão igual da oitava (13-EDO e 14-EDO)

| Controle | Uso e objetivo | Interpretação |
| --- | --- | --- |
| **Gerador · passos** | Determinar a ligação entre graus no cilindro e nas relações | Pode formar uma ou várias órbitas conforme a divisão e o máximo divisor comum; não altera por si só os passos de frequência do EDO puro. |
| **Grau de referência** | Definir o grau-âncora para frequências absolutas | Use quando o sistema não possui um Lá4 cromático tradicional. |
| **Oitava de referência** | Fixar a oitava da âncora | Atua junto da frequência de referência do grau, não deve ser confundida com número de teclas por oitava. |
| **Personalizar graus · offsets de c.p. e c.s.** | Aplicar desvios individuais sobre os graus do EDO-base | Após offsets não nulos, as frequências efetivas já não são estritamente equidistantes. |
| **Restaurar EDO puro (offsets zero)** | Eliminar os offsets individuais | Recupera a divisão igual-base, sem apagar perfis ou medições. |

### Biblioteca musical e diagnóstico

| Controle | Objetivo | Observação |
| --- | --- | --- |
| **Nome da cópia / Instrumento (opcional)** | Identificar uma receita na biblioteca | “Instrumento” aqui é metadado musical e **não** corresponde ao perfil instrumental com sessões acústicas. |
| **Salvar afinação / Salvar perfil com referência** | Guardar só receita ou receita com referência absoluta | Escolha o formato de acordo com o que precisa reproduzir em outro aparelho. |
| **Criar cópia / Restaurar preset original** | Preservar edição paralela ou retomar receita original | Não são comandos de limpeza de dados acústicos. |
| **Minha biblioteca / Carregar seleção / Excluir seleção** | Escolher, aplicar ou remover uma definição pessoal | Verifique receita e referência após carregar; exclusão pode ser definitiva no armazenamento local. |
| **Exportar afinação JSON / Exportar perfil JSON** | Compartilhar configuração musical | Diferentes do AFP instrumental e do AFC de curvas. |
| **Importar arquivo JSON / Confirmar importação / Cancelar prévia** | Examinar e aceitar ou desistir de uma definição importada | Importar para a biblioteca e **carregar** a receita são ações distintas. |
| **Monitor de diagnóstico** | Observar estado do detector, RMS, candidatos, decisões e tempo | Precisa ser habilitado nas Configurações; não grava áudio automaticamente. |
| **Incluir áudio WAV (opcional)** | Acrescentar PCM ao registro de diagnóstico | Pode capturar sons privados; depende de AudioWorklet. |
| **Iniciar · 20 s / Parar / Exportar ZIP** | Gravar um caso reproduzível de instabilidade ou erro do detector | O ZIP contém metadados/eventos e WAV opcional; limites de memória podem encerrar antes. Não confunda com sessão AFS. |

As seções [Detectores](#detectores), [FFT](#fft), [temperamentos](#temperamentos), [edição racional](#cilindro), [EDO](#teclados), [biblioteca](#biblioteca) e [diagnóstico](#diagnostico) fornecem os fundamentos e exemplos para interpretar esses controles.

<a name="cfg-1"></a>
## 1.3. Configurações do Afinador

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
| Escala espectral | Logarítmica | Linear ou logarítmica; também alternável ao tocar no gráfico |
| Zoom na nota-alvo | Não | Visualiza ±100 cents em torno do alvo |
| Monitor de diagnóstico | Não | Mostra medições internas do detector; não inicia captura |

### YIN + FFT (recolhido)

| Campo | Padrão | Faixa | Efeito |
| --- | ---: | ---: | --- |
| Limiar CMNDF | 0,17 | 0,05–0,26 | Limiar da função de diferença normalizada: aumentar admite mínimos menos profundos; pode aceitar ambiguidades. Diminuir exige repetição mais clara; pode rejeitar notas úteis. |

### pYIN (recolhido)

| Campo | Padrão | Faixa | Efeito |
| --- | ---: | ---: | --- |
| Passo de cálculo (CMNDF) | 4 | 1, 2, 4 ou 8 | Passos menores aumentam o custo de processamento; o passo 8 é mais rápido, mas pode produzir erros importantes de frequência. |
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

<a name="detectores"></a>
## 1.4. Métodos de detecção de altura

Selecione diretamente um dos quatro botões sob o título **Espectro FFT**. Somente o detector escolhido atua como detector de altura por quadro.

| Método | Princípio | Quando experimentar | Limitações |
| --- | --- | --- | --- |
| YIN + FFT | Procura repetição da forma de onda, verifica evidências harmônicas e refina a frequência com o espectro | Primeira escolha para vozes e instrumentos monofônicos | Pode errar oitava ou ficar inconclusivo; depende do sinal |
| pYIN | Avalia vários candidatos de periodicidade e acompanha a sequência ao longo do tempo | Quando uma nota sustentada apresenta saltos espúrios | A continuidade pode retardar uma mudança verdadeira; custo adicional |
| SWIPE′ | Busca padrões espectrais harmônicos com várias janelas | Timbres em que a fundamental não domina o espectro; comparação com estimadores temporais | Mais exigente; requer PFFFT/WebAssembly; não é um detector universal de acordes |
| Pico | Seleciona o componente espectral predominante | Inspecionar uma senoide ou localizar a componente mais intensa | Pode retornar um harmônico, não a fundamental (aviso em vermelho claro) |

A implementação YIN + FFT integra refinamento espectral adaptativo e estratégias conservadoras de validação. O pYIN possui proteção de oitava e auditoria espectral; o SWIPE′ possui ancoragem espectral seletiva. O passo CMNDF do pYIN pode ser ajustado nas Configurações; prefira o padrão 4 inicialmente. Não há botão para operar YIN puro. As janelas temporais de YIN/pYIN e as janelas multiespectrais do SWIPE′ são administradas pelo motor e não equivalem ao seletor de pontos da FFT principal.

Exemplo: uma nota de 220 Hz pode ter um segundo harmônico de 440 Hz mais intenso que a fundamental. O modo Pico pode indicar 440 Hz, enquanto um detector de periodicidade pode encontrar 220 Hz. Isso não representa necessariamente defeito do microfone. Compare os métodos em condições equivalentes e verifique o espectro; não suponha que o resultado que parece mais estável seja sempre o correto.

### Leitura bruta e filtrada

**Bruta** mostra a saída do detector sem suavização adicional do medidor. O método pode possuir acompanhamento próprio, como o pYIN. **Filtrada** suaviza a leitura temporal para reduzir oscilações visuais; quanto maior a intensidade, maior a tendência de amortecer variações, com possível atraso. Para estudar resposta a uma troca de nota ou um erro de oitava, prefira a leitura bruta. A suavização não corrige um detector que escolheu a fundamental errada.

<a name="fft"></a>
## 1.5. Espectro FFT, escalas e zoom

O gráfico mostra a distribuição de componentes em frequência. Na horizontal há Hz; na vertical, magnitude em dB segundo a representação do espectro. Um pico indica energia de uma componente naquela região. A leitura dos detectores não é obtida simplesmente contando os pixels do gráfico. Toque ou clique no próprio Espectro FFT para alternar entre logarítmica e linear; com foco no gráfico, também é possível usar o teclado. A mesma preferência está em **Configurações → Visualização → Escala espectral**. Para conservá-la na próxima inicialização, use **Salvar alterações**.

- **Logarítmica:** padrão; oitavas ocupam distâncias horizontais iguais, favorecendo a leitura do registro grave e de uma grande faixa de frequências.
- **Linear:** distâncias iguais em Hz ocupam espaços iguais; facilita ver espaçamento regular entre harmônicos.
- **Zoom na nota-alvo (±100 cents):** aproxima a região do alvo para inspeção local. Desmarque para retornar à visão geral.

O gráfico usa o teto de 24.000 Hz ou a frequência de Nyquist da captura, a que for menor. A 44,1 kHz o teto efetivo é 22.050 Hz; a 48 kHz, 24.000 Hz. Isso não significa que o microfone tenha resposta plana até o teto. O limite inferior da escala logarítmica é positivo (16 Hz); a detecção possui sua própria faixa nominal de 16–4.600 Hz. Frequências superiores podem aparecer como componentes espectrais, não como alvos de altura do detector. O teto do gráfico é automático.

A resolução visual é adaptada aos pixels disponíveis, preservando os máximos de grupos de bins. O zoom e a escala não reinicializam o DSP. Eles não aumentam a resolução física da captura.

### Pontos de FFT e resolução

| Pontos | Bins analisados | Espaçamento aproximado a 48 kHz | Janela nominal a 48 kHz |
| ---: | ---: | ---: | ---: |
| 4.096 | 2.048 | 11,72 Hz | 85 ms |
| 8.192 | 4.096 | 5,86 Hz | 171 ms |
| 16.384 | 8.192 | 2,93 Hz | 341 ms |
| 32.768 | 16.384 | 1,46 Hz | 683 ms |

O espaçamento entre bins é `taxa de amostragem / pontos FFT`. A janela Blackman usada no espectro convencional reduz vazamento espectral, com compromisso na largura dos picos. A duração acima não é a latência total, e o espaçamento não é a precisão final em Hz: interpolação e métodos temporais podem estimar frequências entre bins. Mais pontos custam processamento e podem piorar a resposta a mudanças rápidas. Comece com 8.192; reduza se o aparelho estiver lento, aumente para investigar componentes próximas e sustentadas. A FFT acústica da ferramenta da análise acústica é independente dessa configuração.

<a name="temperamentos"></a>
## 1.6. Referência musical e catálogo de temperamentos

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
## 1.7. Cilindro acústico, frações e matriz de intervalos

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

Para ouvir diferenças, compare notas no [Emissor](#cap-5). Para medir os componentes que produzem batimentos num instrumento, recorra a [Aquisição e Análise](#cap-2). O cilindro e as tabelas representam a receita teórica, não uma medição de cordas reais.

<a name="teclados"></a>
## 1.8. Teclados históricos ampliados e EDOs

No domínio histórico, **Teclas por oitava** permite 12, 13 ou 14 teclas. As ampliações podem separar Ré♯/Mi♭ e Sol♯/Lá♭; o botão de alternância enarmônica e o seletor **Grafia enarmônica** controlam as variantes apresentadas. Confira os nomes exibidos antes de escolher a tecla-alvo. **Desfazer disposição** volta à disposição anterior quando disponível.

Uma tecla adicional não necessariamente cria uma nova frequência. No igual de doze divisões, as extensões inicialmente duplicam alturas existentes. Nas cadeias, as quintas adicionais seguem a regra da cadeia; nos ciclos históricos começam com quintas puras. Os ajustes das extensões podem mudar essas relações. O programa preserva diferentes identidades físicas mesmo se as frequências coincidirem. Assim, a detecção automática não é capaz de decidir qual de duas teclas coincidentes foi pressionada; use nota fixa ou confirme a tecla na análise acústica.

**13-EDO e 14-EDO não são a mesma coisa que teclados históricos com 13 e 14 teclas.** A primeira opção divide a oitava em 13 passos de 92,3077 cents; a segunda, em 14 passos de 85,7143 cents. Abra **Divisão igual · gerador, referência e offsets por grau** para ajustar o gerador (quantos graus são percorridos por ligação), o grau-âncora e a oitava de referência. Os graus são numéricos; a âncora não precisa ser uma nota tradicional.

Com gerador de 8 passos, o 13-EDO dá uma órbita com 13 graus; o 14-EDO dá duas com sete. Isso decorre de somar o gerador e voltar ao começo ao completar a oitava: em 14 graus, somar 8 preserva a paridade. Um gerador diferente pode mudar a quantidade de órbitas sem mudar as alturas-base. O campo de gerador aceita os valores válidos para a divisão selecionada (respeite os limites mostrados).

Em **Personalizar graus · offsets independentes de c.p. e c.s.**, é possível alterar cada grau. Com offsets diferentes de zero, a receita-base continua identificada como EDO, mas as alturas efetivas não constituem necessariamente uma divisão rigorosamente igual. **Restaurar EDO puro (offsets zero)** elimina esses offsets.

<a name="biblioteca"></a>
## 1.9. Biblioteca pessoal de afinações

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

<a name="diagnostico"></a>
## 1.10. Monitor e registro de diagnóstico

Use quando houver erro de oitava, demora, leitura instável, ausência de nota ou comportamento dependente de um aparelho. Não é preciso ativá-lo durante uma afinação normal.

1. Em Configurações → Visualização, habilite **Monitor de diagnóstico**. Observe o estado do método ativo.
2. Ative o microfone, selecione o detector que apresenta o problema e prepare a situação de teste.
3. Se desejar preservar o PCM contínuo, marque **Incluir áudio WAV (opcional)** antes da captura. Essa opção depende de AudioWorklet e da continuidade do áudio. Considere a privacidade do ambiente.
4. Pressione **Iniciar · 20 s**. Durante o contador, reproduza o problema, preferencialmente com notas isoladas e pausas identificáveis. Use **Parar** se precisar interromper.
5. Examine **Resumo da última sessão** e **Eventos recentes**. Pressione **Exportar ZIP** para guardar a evidência.

O monitor atualiza a interface em cadência própria (aproximadamente 250 ms); esse intervalo não é a cadência efetiva dos cálculos. O ZIP contém decisões e candidatos do detector, configurações, eventos, informações de ambiente e desempenho disponíveis, e opcionalmente `audio.wav`. Uma candidata não é necessariamente uma leitura aceita. Os limites de tempo e memória podem encerrar a sessão antes de 20 s. Não rode um diagnóstico enquanto realiza outra captura acústica ou emite som.

<a name="ts-1"></a>
## 1.11. Solução de problemas — Afinador

| Sintoma | O que verificar e fazer |
| --- | --- |
| Não pede microfone / permissão negada | Use HTTPS/localhost; confira permissão do site e do sistema; feche aplicativos que estejam usando o áudio e recarregue se necessário. |
| Microfone desligado ao retornar à página | Comportamento de privacidade esperado. Ative-o manualmente para continuar. |
| O medidor não sai de `--` | Confirme microfone ativo, som isolado e intensidade suficiente; aproxime moderadamente o instrumento; tente YIN + FFT com padrões restaurados. |
| Indica nota uma oitava acima | O segundo harmônico pode dominar. Experimente YIN + FFT/pYIN; confira o espectro; não use Pico como prova da fundamental. |
| Nota muda perto da fronteira | Use Nota fixa e verifique o catálogo, especialmente em teclas divididas. Nota flutuante também pode refletir variação real. |
| Desvio constante em todo instrumento | Confira A4, temperamento, modo e eventual correção instrumental aplicada; 415,3 Hz não é 440 Hz. Não compense erro de referência com ajuste físico indiscriminado. |
| Painel de correção desapareceu | Sem curva ativa, a referência é teórica e o painel fica oculto. Confira se a base musical ou os dados mudaram; revalide em Curvas antes de reaplicar. |
| Análise sem resposta | O Afinador tenta recuperar o Worker DSP uma vez; se a recuperação falhar, encerra a captura com aviso. Confira o método, a resolução e as condições do aparelho antes de reativar. |
| Alteração de nota lenta | Use leitura bruta, pontos de FFT menores quando pertinente e padrões de confirmação pYIN; compare com YIN + FFT. |
| SWIPE′ indisponível | O navegador pode não oferecer o motor PFFFT/WASM necessário. Use outro método; não há substituição silenciosa equivalente. |
| Espectro parece truncado | Desative zoom; confira Nyquist e escala. O teto é determinado pela captura e pela política dos 24 kHz. |
| Picos aparecem próximos demais | Em log, harmônicos altos ficam visualmente próximos; alterne para linear ou aplique zoom. |
| Edição de quinta rejeitada | Reveja fração, limites e quinta compensatória; volte ao preset se necessário. |
| Teclas adicionais coincidem | Pode ser correto; duas identidades físicas podem compartilhar frequência. Use Nota fixa. |
| Configurações voltaram ao reabrir | Salve explicitamente; verifique se há armazenamento local disponível. |
| Não consegue modificar configurações | Termine a captura diagnóstica ativa; corrija campos inválidos. |
| WAV não foi incluído | Confirme que a opção estava marcada, AudioWorklet disponível e captura válida. O JSON ainda serve para investigação. |
| Problema persiste | Restaure só os padrões do Afinador, reproduza com nota conhecida e exporte diagnóstico conforme [1.10](#diagnostico). |

[Voltar ao sumário](#sumario)

<a name="cap-2"></a>
# Capítulo 2 — Aquisição acústica e Análise acústica

O objetivo aqui não é apenas encontrar a nota: é investigar a composição do som. Uma nota musical pode conter uma componente fundamental, harmônicos superiores e componentes não harmônicos. O motor de análise acústica é independente do detector convencional. Não é preciso escolher SWIPE′ ou mudar os pontos da FFT do Afinador para medir parciais.

<a name="modelos"></a>
## 2.1. Escolha do instrumento e do modelo

Uma série harmônica ideal tem frequências `fₙ = n × f₁`. Um instrumento real pode apresentar desvios, componentes fracas, ruído, batimentos ou modos que não obedecem à série. Um pico espectral, por si só, não comprova a origem física de uma componente.

A captura multiataque utiliza quatro famílias: **Piano, Fortepiano, Cravo e Outro**. A família identifica o instrumento; o modelo acústico define a hipótese de interpretação. A escolha não é uma classificação automática do instrumento.

| Família | Condição e modelo utilizado | Orientação prática |
| --- | --- | --- |
| Piano | Corda isolada: corda rígida (B). Nota completa, condição desconhecida ou uníssono: série harmônica, sem B físico | Identifique a corda; não declare isolamento se houver outras cordas vibrando. |
| Fortepiano | Mesmas regras de seleção de modelo que piano | Identifique a corda e conjunto quando úteis; respeite a identidade física e altura soante. |
| Cravo | Mesmas regras de seleção de modelo que piano | Informe registro, corda e técnica quando úteis; para estudos de curvas, prefira um perfil por registro, com a altura efetivamente soante (4′ soa uma oitava acima de 8′). |
| Outro | Automático por padrão; modelo selecionável em Avançado | Abrange qualquer outro instrumento ou fonte sonora; identifique a fonte e técnica quando útil. |

Para os três instrumentos de teclado, **Avançado → Somente picos exploratórios** substitui a análise harmônica ou de corda rígida pelo modo exploratório. Nenhuma família tem homologação física implícita.

### Outro: selecionar o modelo acústico

Abra **Avançado → Modelo acústico de Outro**. O padrão é Automático. Selecionar um perfil Outro recupera a hipótese acústica daquele perfil; confira antes de iniciar.

| Modelo | O que examina | B | Exemplos de uso |
| --- | --- | --- | --- |
| Automático (padrão) | Investiga ordens harmônicas; se insuficientes, apresenta picos sem atribuição | Não | Fonte cuja estrutura ainda não é conhecida, voz ou sopro |
| Exploratório | Picos sem impor ordem harmônica ou fundamental | Não | Inspeção geral sem hipótese de série |
| Série harmônica | Frequência-base inferida, ordens e desvios de uma série | Não | Flauta, voz ou nota aproximadamente periódica |
| Corda rígida — B experimental | Parciais e ajuste físico de corda rígida quando elegíveis | Sim, se elegível | Monocórdio, clavicórdio, violão ou guitarra de corda isolada e sinal limpo |
| Componentes não harmônicos | Picos sem atribuição obrigatória de ordens | Não | Sinos, placas e percussões; picos não comprovam modos próprios |

Nos modos exploratório e não harmônico, a análise é centrada nos picos; a identificação de nota e as apresentações dependentes de ordens harmônicas não são usadas. Em Série harmônica, a identificação de nota pode ser útil, mas não há B. Em Corda rígida, selecione **Aquisição de nota → Isolada**, mesmo que já tenha usado esse modelo antes. Sem declaração de isolamento, a sessão de Outro neste modelo não pode iniciar. **Corda / registro** permite identificar a fonte; use sinal limpo, sem efeitos, e documente técnica, posição, casa (se pertinente) e condições em **Avançado → Técnica / condição**. A declaração é responsabilidade do usuário; escolher o modelo não comprova isolamento nem adequação física.

O modelo solicitado fica fixado durante a sessão. Automático investiga a série harmônica e pode apresentar apenas picos. Em Outro com Corda rígida, se o ajuste físico falhar, pode haver reanálise das mesmas amostras como série harmônica e, se insuficiente, como picos. Série harmônica escolhida manualmente não força outra interpretação. A hipótese solicitada e a efetivamente usada ficam registradas por execução em **Decisões da análise e estabilidade relativa**. Outro pode alimentar curvas somente pela fonte **Parciais empíricos — independente de B (experimental)**, com Automático que identificou ordens, Série harmônica ou Corda rígida, quando os critérios da fonte forem atendidos. Ter B consistente não é suficiente nem necessário nessa via.

Para estudar um piano, não desmonte, abafe ou manipule componentes internos sem conhecimento técnico apropriado. Se não for possível isolar a corda de modo seguro, registre a nota completa como tal. Os resultados ainda podem ser úteis para inspeção acústica, mesmo sem B.

<a name="captura-individual"></a>
## 2.2. Captura individual genérica

A opção é indicada para experimentar rapidamente o espectro de uma nota, sem preparar uma sessão com identificação e condições físicas detalhadas.

1. Abra **Ferramentas → Aquisição acústica**.
2. Expanda **Avançado → Captura individual genérica**.
3. Pressione **Capturar uma nota**. Toque uma única nota sustentada e aguarde o resultado. Use **Encerrar captura** para interromper a aquisição quando necessário.
4. Abra **Análise acústica** para examinar o resultado e consulte **Espectro acústico — execução selecionada** e **Dados e desvios da execução selecionada**. Mesmo se aparecer como inconclusivo, inspecione as evidências disponíveis.
5. Use **Congelar resultado** para evitar substituir o resultado durante a inspeção. Use **Liberar resultado** antes de medir novamente.
6. Se desejar, pressione **Baixar análise (JSON)**. Para sintetizar os componentes, abra Emissor pelo menu e escolha a origem Último resultado exibido.

A captura individual não substitui uma sessão multiataque, nem representa uma gravação reproduzível. O Emissor faz reconstrução sintética, não reproduz o áudio original. Veja [5.6](#reconstrucao).

<a name="multiataque"></a>
## 2.3. Medir a mesma nota várias vezes

A coleta de várias execuções independentes permite analisar a repetibilidade. Várias janelas de uma única execução não equivalem a várias notas tocadas de novo. A meta inicial é de dez ataques utilizáveis; você pode finalizar antes, quando o objetivo for apenas explorar os picos, ou continuar dentro dos limites quando precisar de mais dados.

### Preparar a sessão

1. Configure o temperamento, a referência e o layout que correspondem às teclas do instrumento (ver [1.6](#temperamentos) e [1.8](#teclados)).
2. Escolha o perfil ativo ou a família em **Instrumento**. Para Outro, abra Avançado para escolher o modelo quando necessário (Automático é o padrão). Indique a condição em **Aquisição de nota** e **Corda / registro (opcional)** quando disponíveis; declare isolamento somente se verdadeiro. Registre condições em Avançado → Técnica / condição, se útil.
3. Por padrão, a identificação é **Automática**. Em **Identificação da nota**, na área principal, escolha **Escolher tecla antes de medir** se souber a tecla. Um pico não comprova uma nota nem a identidade física.
4. O reconhecimento de toques é automático por padrão; escolha Manual em Avançado quando necessário. Confira os parâmetros nas Configurações antes de iniciar, pois são conservados na sessão.
5. Pressione **Iniciar medição**. O aplicativo solicita/ativa o microfone quando necessário.

### Coleta automática

Toque sempre a mesma nota/corda e deixe o som diminuir entre as execuções. O sistema procura o início do toque, descarta parte do transiente inicial e analisa um trecho útil. Aguarde as indicações da interface: som em análise, verificação dos parciais, nova execução ou orientação de repetir. Não interprete simplesmente a contagem de tentativas como quantidade de medições válidas. O círculo vazado indica espera, registro ou pausa; verde indica pronto ou análise (pulsante); vermelho indica falha ou execução inconclusiva. Registrada significa aproveitamento para análise espectral, não aprovação de B.

### Coleta manual

Em Avançado → Reconhecimento de toques, escolha **Manual — marcar cada toque**. Durante a sessão, pressione **Iniciar execução**, toque a nota, sustente ou deixe soar, e use **Encerrar execução** quando necessário. Respeite o trecho mínimo e máximo úteis; o motor analisa o áudio recebido, e não o instante do clique como frequência. A marcação manual ajuda quando o reconhecimento automático do início do som é difícil, mas não elimina os critérios acústicos.

### Pausar, confirmar e finalizar

- **Pausar** suspende a coleta preservando ataques. Retome se o contexto ainda for válido.
- Confira **Confirme a tecla (ou deixe sem identificação)**. Confirme apenas a identidade física conhecida; use **Continuar sem identificar a tecla** se houver ambiguidade. B pode ser válido sem tecla confirmada; uma curva exige vínculo físico válido.
- Desvio superior a 45 cents entre fundamental estimada e tecla escolhida exige revisão da identidade. A confirmação excepcional não altera as frequências nem dispensa outros critérios de qualidade.
- **Finalizar medição** encerra a escuta após a última análise. A consolidação pode demorar; aguarde o resumo da sessão não salva. Para explorar os detalhes, escolha **Analisar resultados**.
- Na Análise, inspecione ataques e revise inclusões quando disponíveis. Excluir do conjunto ou excluir um parcial preserva a observação original; aguarde o recálculo. Uma revisão histórica é somente leitura.
- **Salvar** grava sem iniciar uma nova captura. **Salvar e medir próxima nota** grava, confere o registro, rola até a medição e inicia automaticamente outra sessão. Em modo automático, toque qualquer próxima nota; em modo fixo, confira a sugestão de próximo alvo. A identificação física da nota é necessária para avançar nesse fluxo; o texto de corda/registro é opcional.
- A barra integrada ao botão avança conforme as etapas reais de salvamento; só completa após a confirmação. Não há pop-up nem clique adicional após o sucesso. Em caso de falha, o rascunho fica disponível para nova tentativa ou exportação. Não feche a página durante a gravação.
- **Baixar sessão (.afs)** ou **Baixar sessão (JSON)** preserva a sessão externamente. **Repetir / descartar sessão** abandona o trabalho atual; preserve os dados importantes antes.

O rótulo de corda/registro informado é reaproveitado nas próximas medições do mesmo instrumento durante o fluxo; altere-o ou apague-o quando mudar de fonte. Não mude de nota dentro de uma sessão. Ao ocultar a página, mudar de ferramenta ou perder continuidade do áudio, a captura pode ser encerrada ou pausada. Retome explicitamente ao retornar; o reinício após salvamento só deve ocorrer no contexto ativo e seguro. Há limites de memória e de escuta contínua; se atingidos, preserve os dados obtidos.

<a name="revisao-historica"></a>
### Revisar medições e comparar sessões

1. Abra **Análise acústica** pelo menu ou por **Analisar resultados** na aquisição. Escolha **Rascunho atual**, **Medições armazenadas**, **Sessão importada pendente** ou **Abrir sessão…** conforme a origem.
2. Selecione o instrumento, a tecla e a sessão quando consultar registros armazenados; pressione **Abrir revisão**. A vista **Sessão** mostra os gráficos originais, execução por execução, proveniência e consolidação. A consulta não inicia áudio e não recalcula B de registros históricos.
3. Para comparar, escolha outra sessão compatível e utilize **Comparar com a sessão exibida**, quando disponível. Compare fontes físicas e procedimentos equivalentes; revisões da mesma sessão não são ataques independentes.
4. Use **Exportar sessão (.afs)** para preservar uma sessão consultada. Uma sessão importada pendente pode ser salva pelo comando **Salvar sessão importada…**, escolhendo um perfil compatível.
5. Use **Voltar à aquisição** para recuperar o trabalho em andamento, sem ligar o microfone automaticamente por esse simples retorno.

| Comparação | Interpretação |
| --- | --- |
| Corda rígida compatível | Diferenças descritivas de frequência, B e dispersão; não é novo ajuste conjunto. |
| Série com ordens comparáveis | Compare as ordens comuns com suporte suficiente. |
| Contexto ou fonte divergente | A comparação numérica pode ser recusada; examine separadamente. |
| Revisões da mesma sessão | Não são aquisições independentes. |
| Picos sem ordens | Compare espectros; não há correspondência modal automática. |

A comparação histórica pode ser invalidada por alterações dos registros. Evidências grandes podem exceder o orçamento de memória; consulte uma sessão por vez quando necessário. Não há áudio bruto recuperável a partir de AFS.

### Espectros de uma sessão e estabilidade

Em **Espectro acústico — execução selecionada**, escolha a execução e use **Absoluta** ou **Alinhada à fundamental** quando disponível. A segunda facilita comparar relações, sem modificar as frequências originais. O espectro consolidado é descritivo; linhas de referência inferidas são identificadas e não substituem uma medição de P1. Exclusões de execuções retiram suas contribuições do consolidado; excluir um parcial retira sua marca e eventual referência de alinhamento, não a energia medida no espectro original.

### Gráficos de desvios e estabilidade

Os gráficos de revisão apresentam os dados em cents, com a referência zero identificada. Os títulos e as referências dependem dos dados disponíveis.

| Painel | O que mostra | Significado de zero |
| --- | --- | --- |
| **Desvios da série harmônica ideal** | Mediana de `1200 × log₂(fₙ/(n × f₁))` para ordens com P1 medido e verificado | Coincidência com o múltiplo ideal da fundamental medida |
| **Desvios em relação ao n-ésimo parcial** | Mediana de `1200 × log₂(fₖ × n/(fₙ × k))`; a referência superior medida é escolhida por presença nas execuções, com preferência pela menor ordem em empate | Coincidência com a proporção harmônica; o parcial de referência tem zero por definição |
| **Desvios em relação ao modelo físico** | Resíduos assinados entre frequências medidas e previstas pelo ajuste de corda rígida | Concordância com o modelo, não ausência de inarmonicidade |

Nos gráficos, use o ícone de informação **ⓘ** para consultar o significado científico e o controle de ampliação para examinar detalhes. Toque nos pontos ou navegue por teclado para ver valores; as legendas interativas permitem controlar camadas quando disponíveis. Em **Desvios da série harmônica ideal**, use **Todas as ordens** e **Dispersão / bootstrap** quando necessário. A visão principal privilegia ordens com três ou mais observações e cobertura mínima de 60%; se nenhuma satisfizer esse critério, exibe todas as ordens disponíveis. A dispersão máxima observada e o intervalo bootstrap são grandezas distintas. Valores positivos indicam frequência acima da referência; negativos, abaixo. As escalas são independentes e adaptadas a cada gráfico.

**Estabilidade das medições** apresenta barras por parcial. Comece em **Consolidado** e use as setas, o gesto horizontal ou as teclas de seta com foco no painel para consultar as análises individualmente. O seletor mantém a métrica escolhida durante a navegação:

| Métrica | Interpretação |
| --- | --- |
| Frequência absoluta | Variação temporal da frequência do próprio parcial |
| Relação utilizada | Estabilidade relativa efetivamente considerada durante a aquisição: coorte ou combinação de P1 verificado e coorte, conforme a evidência disponível |
| Relação com a fundamental | Variação relativa ao primeiro parcial, quando há comparação independente disponível |
| Relação com o conjunto | Estabilidade relativa ao comportamento coletivo dos parciais |

O consolidado contabiliza somente parciais aceitos, únicos e não excluídos de execuções harmônicas incluídas. Cada barra distingue estáveis, instáveis e sem dados; a contagem mostra observações estáveis sobre o total da ordem, e o toque revela os totais. Nas análises individuais, a barra indica a magnitude em cents numa escala comum à métrica, com marca do limite de estabilidade definido na sessão (padrão de 3 cents). Execuções excluídas ou inconclusivas e parciais excluídos são identificados. **Sem dados** não é zero nem instabilidade; P1 comparado consigo mesmo não é evidência independente. Uma razão estável não substitui os critérios de estabilidade absoluta para curvas. A apresentação não recalcula as medições.


<a name="analise-instrumental"></a>
## Caracterização acústica — Sessão, Nota e Instrumento

### Como abrir os gráficos

1. Em **Análise acústica**, selecione **Medições armazenadas** e o instrumento desejado.
2. Escolha **Instrumento** e pressione **Calcular / atualizar**. Para examinar uma única tecla, use **Nota**; para um conjunto de ataques, **Sessão**.
3. Abra **Restringir fontes ou escolher sessões** se quiser limitar o escopo. Em **Fonte / coorte**, selecione o conjunto pertinente e leia **Protocolo e limitações**. Os grupos consideram família, modelo, condição, registro comum, configuração e contexto da captura; não pressupõem que cordas de notas diferentes sejam a mesma corda física. Rótulos distintos, como `8` e `8'`, não são automaticamente equivalentes.
4. Abra um gráfico e acione seu cálculo específico quando houver botão. Toque em células ou pontos e use os seletores e tabelas para examinar valores. Use **Abrir Nota** onde disponível para detalhar a tecla. Os mapas maiores têm navegação por blocos.

Uma coorte com metadados incompletos é exploratória: não confirma igualdade de condições. A inclusão de registros excluídos é somente visualização. Ataques elegíveis e incluídos sustentam os agregados usuais; a mediana por sessão antecede a mediana por tecla, evitando que uma sessão longa domine as outras. Em geral, MAD requer três observações e quartis quatro. O número de sessões e ataques importa para avaliar evidência. Lacunas, ordens não detectadas, fora de banda, fontes incompatíveis e valores excluídos são situações distintas. O mapa observado não preenche posições cromáticas intermediárias; em perfis declarados podem existir posições sem medição. O eixo horizontal é categórico.

### G02 — Mapa espectral instrumental em cores

Selecione **Amplitude relativa (dB)** ou **Cobertura dos parciais (%)**, P1–P12 ou P1–P24 e faixa −60 a 0 ou −80 a 0 dB. Use **Ampliar células** e a tabela da tecla. Cada linha representa uma ordem, não uma frequência absoluta. A taxa de cobertura descreve a presença do parcial nos ataques incluídos; não é um índice de completude do instrumento. Hachuras e símbolos distinguem dados ausentes, excluídos, incompatíveis ou fora de banda. Um ponto branco sobre a cor identifica evidência limitada. Níveis são relativos ao pico de cada ataque, não dB SPL; saturação de cor não altera o número armazenado.

### G03 — Perfil instrumental de inarmonicidade

Pressione **Calcular perfil de B**. São exibidos apenas coeficientes B consolidados provisoriamente consistentes do modelo de corda rígida isolada. O eixo de B é logarítmico e adimensional; círculos representam sessões, losango a mediana por tecla, barra mínimo–máximo e caixa Q1–Q3 quando estimável. Habilite bootstrap para ver intervalos nominais da própria sessão. A faixa de estados distingue inconclusivo, zero, inválido, não aplicável, sem B consolidado, incompatível/excluído e sem medição. Nenhum desses estados é lançado como zero no eixo log. Não há ajuste de curva ou interpolação. B individual e candidato inconclusivo não são promovidos a valor consolidado.

### G04 — Perfil tímbrico instrumental

Escolha a janela P1–P12/P1–P24, limite comum de 4, 8, 12, 16 ou 24 kHz e um descritor; pressione **Calcular perfil**. Os pesos são potências relativas `w = 10^(dB/10)`, calculadas sobre componentes detectados. Cada descritor usa seu próprio eixo.

| Descritor | Interpretação |
| --- | --- |
| Centroide por frequência (Hz) | `Σ(w·f)/Σw`; centro da distribuição observada em frequência. |
| Centroide por ordem | `Σ(w·n)/Σw`; centro da distribuição por ordem harmônica. |
| Dispersão por ordem | Desvio-padrão ponderado das ordens em torno do centroide. |
| Fração de componentes superiores (%) | Participação das ordens a partir de P5. |
| Razão pares/ímpares (dB) | `10 log10(Σw_pares/Σw_ímpares)`, quando ambos os grupos são observados. |
| Potência observada P1–P4, P5–P8, P9–P12 (%) | Frações da potência dos componentes observados na janela escolhida. |

É necessário suporte de ao menos dois componentes distintos. Ausência de P1 ou de uma faixa não implica potência zero. Para picos não harmônicos, apenas centroide por frequência é pertinente. O gráfico mostra medianas por sessão e por tecla e dispersão min–máx, não intervalos de confiança. Em perfis observados, os pontos não são ligados por linhas que sugiram continuidade física. Brilho, amplitude e distribuição espectral dependem também da captação; não são uma nota de qualidade sonora.

### G05 — Mapa instrumental de desvios harmônicos

Escolha **Adaptativa (P1 empírica ou parcial alternativo)** ou **Modelo físico extrapolado (quando aceito)**, o grupo de referência, ordens e escala simétrica ±10, ±20, ±50 ou ±100 cents. Pressione **Calcular desvios**. Para uma âncora de ordem `r`, o desvio da ordem `n` é `1200 log₂[(fₙ/n)/(fᵣ/r)]`. P1 é usada quando admissível; P2, P3 ou outra ordem medida pode servir de âncora quando necessário. O zero da âncora é definido pela fórmula. Não se misturam grupos de referência e não se usa o temperamento como âncora. O modo físico é separado e não representa P1 medida. Cores divergentes distinguem desvios negativos e positivos; valores fora da faixa mantêm o número original. Não depende necessariamente de B e não alimenta curvas diretamente.

### G06 — Repetibilidade acústica

Selecione **MAD intrassessão (mediana)**, **MAD entre sessões** ou **Taxa de aceitação (%)**, janela de ordens e escala MAD (0–5, 0–10, 0–20 ou 0–50 cents). Pressione **Calcular repetibilidade**. A frequência de referência descritiva é a mediana das medianas das frequências observadas na coorte, por tecla e ordem. MAD é a mediana dos afastamentos absolutos em relação à mediana dos desvios em cents. Dentro de uma sessão, descreve a variação dos ataques; entre sessões, a variação de suas medianas. Uma única sessão não estima dispersão entre sessões. Uma única observação não significa estabilidade perfeita. Nenhum extremo é excluído automaticamente.

Selecione a tecla, o componente e a sessão; use **Inspecionar ataques da sessão** para ver as observações. Consulte **Dispersão da fundamental por tecla** e, separadamente, **desvio do alvo histórico da fundamental**. Fundamental inferida não é P1 medida; o alvo histórico não é a afinação corrente. A taxa de aceitação não é sinônimo de estabilidade nem qualidade acústica.

### G07 — Proximidade intervalar espectral (experimental)

Selecione explicitamente **Nota A** e **Nota B** na mesma coorte, escolha o padrão de pares (oitava 2:1, quinta 3:2, terça maior 5:4, terça menor 6:5, duodécima 3:1 ou par avançado P1–P24) e pressione **Calcular proximidade**. A tabela compara frequências medianas de parciais observados e informa amplitudes, desvios e batimento previsto. A posição das teclas não determina automaticamente a família do intervalo.

`Δ = 1200 log₂(fA/fB)`; `batimento previsto = |fA − fB|` Hz. Por exemplo, 300 e 301 Hz dão aproximadamente −5,76 cents e 1 Hz. Inverter A/B e ordens troca o sinal, não o batimento. O mapa usa uma nota fixa e candidatas, com mínimo ou mediana de `|Δ|` e escala 0–10, 0–20, 0–50 ou 0–100 cents. Confira quantos pares sustentam cada comparação. Se a comparabilidade não estiver comprovada, a exploração exige a opção explícita correspondente. As notas foram gravadas separadamente: o cálculo não mede batimentos simultâneos, não prediz sua audibilidade e não constitui métrica validada de consonância, recomendação de temperamento ou curva de afinação.

### G08 — Mapa espectral de frequência contínua

Escolha a fonte **Grade 20.2** ou **Pontos legados (aproximação)**, eixo de frequência absoluta (16 Hz–24 kHz) ou relativo `f/f₀` (0,25–128, apenas para fontes harmônicas com referência válida), 128/256/512 bandas e escala −60 ou −80 a 0 dB. Pressione **Calcular mapa de frequência**. Para cada ataque, utiliza-se o máximo das amostras armazenadas em cada banda; depois as medianas por sessão e por tecla. As bandas logarítmicas preservam picos sem extrapolar além de Nyquist, da configuração ou do suporte armazenado. Fontes legadas e grade não têm necessariamente resolução equivalente.

Use **Detalhe 4.096 bandas** para inspecionar uma tecla e **Voltar ao bloco** para o mapa geral. O detalhe não aumenta a resolução física. Uma banda sem amostra não é amplitude zero. Esta vista pode mostrar componentes não harmônicos, diferentemente do mapa por ordens. Não é espectrograma temporal, PSD ou nível SPL calibrado.

### Quando um gráfico não apresenta dados

Confira se o escopo inclui sessões compatíveis e se a coorte escolhida contém as notas desejadas. Para G03, B individual ou inconclusivo não é suficiente; para G05, a âncora deve estar disponível; para G06, uma sessão única não permite estimar MAD entre sessões; para G07, são necessárias duas teclas na coorte e pares observados. No G08, escolha a fonte espectral compatível com o arquivo e respeite a banda útil. Se um protocolo é desconhecido, não o declare equivalente apenas para obter um gráfico. Ausência de evidência não é defeito por si só.

### Exemplo de estudo instrumental descontínuo

Num cravo, meça Dó2, Sol2, Dó3 e Sol3, em qualquer ordem, usando o mesmo registro e captação. Não é necessário completar as notas intermediárias. Em G02, observe a distribuição de parciais; em G08, as regiões de frequência; em G03, apenas os B consolidados válidos; em G06, a variabilidade dos ataques; em G07, escolha Dó2/Sol2 para a quinta e Dó2/Dó3 para a oitava. Se faltar uma componente, aceite a lacuna. Para comparar dias diferentes, salve novas sessões da mesma nota sem sobrescrever a primeira. Exporte AFP para preservar o estudo.

<a name="controles-parciais"></a>
## 2.4. Controles operacionais de Aquisição e Análise

| Controle | Finalidade e precauções |
| --- | --- |
| **Instrumentos** / **Instrumento selecionado** | Abrir o gerenciador e escolher perfil; também é possível fazer aquisição avulsa. |
| **Teclas por oitava / Tecla adicional** | Corrigir a disposição do perfil sem alterar o catálogo do Afinador; leia as consequências antes de confirmar. |
| **Instrumento / Aquisição de nota** | Família e condição da fonte (isolada ou uníssono, quando aplicável). Declare isolamento somente quando verdadeiro. |
| **Corda / registro (opcional)** | Rótulo da fonte; mantenha nomenclatura consistente. Não é obrigatório para salvar; pode ser necessário para curvas. |
| **Identificação da nota** | Automática ou Escolher tecla antes de medir. Em teclas enarmônicas coincidentes, confirme a identidade física. |
| **Teclado de uma oitava / ‹ ›** | Selecionar ou consultar a nota; ponto verde indica medição. Não é inventário de teclas existentes. |
| **Iniciar medição / Pausar / Finalizar medição** | Iniciar, suspender ou concluir o conjunto de ataques; os parâmetros ficam fixos na sessão. |
| **Iniciar execução / Encerrar execução** | Delimitar um ataque em reconhecimento manual. |
| **Confirmar tecla / Continuar sem identificar a tecla** | Confirmar a identidade ou manter a observação sem vínculo inventado. |
| **Analisar resultados** | Abrir a análise do rascunho sem alterar a evidência original. |
| **Salvar / Salvar e medir próxima nota** | Gravar o resumo finalizado; o segundo comando reinicia a medição após sucesso verificado. |
| **Baixar sessão (JSON / .afs) / Cancelar exportação AFS** | Exportar a evidência da sessão ou cancelar a transferência. |
| **Repetir / descartar sessão** | Abandonar a sessão de trabalho; exporte antes se necessário. |

### Avançado da aquisição

| Controle | Objetivo |
| --- | --- |
| Reconhecimento de toques | Automático ou manual; o modo manual é útil para fontes com ataques difíceis de reconhecer. |
| Modelo acústico de Outro | Automático, Exploratório, Série harmônica, Corda rígida ou Componentes não harmônicos; veja [modelos](#modelos). |
| Técnica / condição | Documentar a excitação, posição, intensidade e outras condições. |
| Somente picos exploratórios | Inspecionar picos sem impor série ou B em instrumentos históricos. |
| Captura individual genérica | Capturar uma nota, encerrar e inspecionar o resultado, sem equivaler a uma sessão multiataque. |
| Diagnóstico de desempenho | Investigar tempos e contagens; não contém PCM. |

### Controles da análise

| Controle | Objetivo |
| --- | --- |
| Rascunho atual / Medições armazenadas / Sessão importada pendente / Abrir sessão… | Escolher a origem sem substituir uma aquisição em trabalho. |
| Sessão / Nota / Instrumento | Alterar o nível de análise, da execução individual à comparação instrumental. |
| Histórico de execuções / Inspecionar | Percorrer os ataques da sessão. |
| Excluir do conjunto / Restaurar ao conjunto; Revisar parciais | Rever o rascunho quando permitido; não apaga a evidência original. |
| Recalcular resultado | Atualizar a consolidação do rascunho após revisão. |
| Espectro e gráficos de desvios / estabilidade / B | Consultar evidências, critérios e ajuste físico; veja as seções seguintes. |
| Calcular / atualizar / Cancelar | Construir ou interromper uma projeção de nota ou instrumento. |
| Restringir fontes ou escolher sessões / Fonte / coorte | Selecionar o escopo e a fonte de comparação; consultar limitações do protocolo. |
| Incluir registros excluídos da modelagem (somente visualização) | Explorar dados excluídos sem readmiti-los como fonte de curva. |
| Abrir Nota / seletores / tabelas dos gráficos | Inspecionar valores e aprofundar uma identidade física. |
| Exportar sessão (.afs) / Salvar sessão importada… | Exportar a sessão consultada ou associar uma importação a um perfil. |

Veja [os sete gráficos instrumentais](#analise-instrumental) para os controles e a interpretação de cada projeção.

<a name="cfg-2"></a>
## 2.5. Configurações de Aquisição acústica

Os grupos avançados permitem experimentos controlados. Configurações acústicas personalizadas são registradas nas sessões, consideradas exploratórias para fins de curvas e não habilitam uma medição automaticamente como fonte de correções. A alteração durante uma sessão em curso não muda os parâmetros congelados daquela sessão; para testar novos critérios, finalize e inicie outra. A apresentação dos resultados pertence às configurações de Análise acústica, descritas abaixo. Os limiares próprios da caracterização empírica e da fonte independente de curvas não são substituídos pelas preferências de ajuste de B; consulte [a caracterização empírica](#empirica).

### Aquisição (aberto)

| Campo | Padrão | Opções e efeito |
| --- | --- | --- |
| Reconhecimento de ataques | Automático | Automático ou manual; padrão de novas sessões |
| Identificação da nota | Automática | Sugestão ou escolha anterior à medição |
| Meta de ataques utilizáveis | 10 | 1–64; não garante qualidade nem elimina exigências do modelo |
| Encerrar ao alcançar a meta | Não | Encerra a escuta automaticamente; ainda requer revisão |

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
| Nível relativo mínimo (dB) | −35 | −60 a −20 | Limiar fixo no modelo físico; na análise adaptativa, SNR local forte pode admitir componentes abaixo dele |
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

<a name="cfg-analise"></a>
### Configurações de Análise acústica

Abra **Configurações** estando na Análise acústica. O grupo **Apresentação da sessão** contém somente preferências visuais:

| Campo | Padrão | Opções e efeito |
| --- | --- | --- |
| Escala espectral | Logarítmica | Linear ou logarítmica; não altera a resolução |
| Notação dos parciais | Numérica | Numérica (P1, P2, P3), intervalos decompostos (f, 8ª, 8ª + 5ª) ou compostos (f, 8ª, 12ª); muda rótulos, não ordens |
| Mostrar parciais candidatos | Sim | Filtro da tabela; não exclui evidências |

Os sete gráficos instrumentais têm controles próprios de seleção, escala, referências e visualização. A janela de Configurações da Análise não contém reconhecimento de ataques, identificação de nota, janelas de aquisição, limiares de aceitação ou parâmetros de ajuste de B: esses parâmetros pertencem à Aquisição e são preservados nas evidências originais. Salvar alterações ou Restaurar padrões na Análise afeta somente as suas três preferências de apresentação; a ação correspondente na Aquisição preserva as preferências visuais da Análise. Fechar mantém os valores válidos nesta visita sem persistir alterações ainda não salvas.

<a name="interpretar-parciais"></a>
## 2.6. Interpretar o resultado acústico

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

Em **Espectro acústico — execução selecionada**, alterne **Log/Linear**, use **+**, **−** ou **Geral**. Selecione um parcial em Dados e desvios da execução selecionada para inspecionar suas evidências. A exibição não modifica o cálculo; ampliar não recupera bins ausentes no espectro preservado. Consulte as frequências e valores de cada componente na tabela.

O teto de busca atual é 24 kHz, limitado pela Nyquist e pela configuração acústica. No entanto, a quantidade de ordens analisadas, os critérios de qualidade, a duração útil e a resposta do microfone também limitam os parciais encontrados. Não espere que um som de 1 kHz necessariamente apresente 24 parciais detectáveis.

### Exemplo: nota de flauta com poucos parciais

Selecione Outro → Série harmônica para este exemplo. É possível encontrar a fundamental com clareza e não alcançar os critérios mínimos de uma série harmônica. Uma flauta pode produzir componentes superiores muito mais fracas do que a primeira. Isso é uma característica possível do som, não prova de falha do programa. O modelo de corda rígida não se aplica à flauta.

Primeiro, sustente a nota em condições estáveis, examine o espectro e os candidatos. Se houver picos fracos mas consistentes, faça uma segunda sessão experimental reduzindo somente **Nível relativo mínimo**, por exemplo de −35 para −45 ou −55 dB. Compare o mesmo registro, intensidade, técnica e posicionamento. Aceitar componentes mais fracas também pode admitir ruído; não diminua todos os limiares de uma vez. Restaure os padrões para retornar aos critérios de referência do projeto. Ver [2.5](#cfg-2). A investigação adaptativa pode admitir uma componente de SNR local forte (18 dB ou o limiar de parcial, se superior) mesmo com nível relativo baixo. Uma janela adicional pode ser testada quando P1 não é aceito ou a evidência é instável; maior janela não é sempre melhor.

<a name="coeficiente-b"></a>
## 2.7. Inarmonicidade de cordas e ajuste individual de B

Para uma corda com rigidez, o modelo experimental usa `fₙ = n × F × √(1 + B × n²)`, em que F é a escala de frequência ajustada e B, o coeficiente adimensional de inarmonicidade. A frequência prevista do primeiro parcial é `F × √(1 + B)`, e não necessariamente F. B = 0 recupera a série ideal. Valores positivos fazem os parciais superiores ficarem progressivamente mais agudos em relação aos múltiplos do primeiro.

Os tetos numéricos experimentais de B são 0,02 para Piano, Fortepiano e Cravo, e 0,05 para Outro com corda rígida, tanto no ajuste individual quanto no consolidado. Esses tetos não representam limites físicos universais e não dispensam os critérios de qualidade.

O cálculo não parte simplesmente da nota-alvo musical. Ajusta F e B às frequências medidas, utilizando uma perda robusta em cents (Huber, que reduz a influência de grandes resíduos). A rigidez é uma hipótese física; um bom ajuste matemático não demonstra por si só que as componentes venham da mesma corda ou que o valor esteja calibrado. A atribuição de ordens considera hipóteses concorrentes, periodicidade, resíduos, cobertura, amplitude e SNR. O ajuste exclui instáveis, reduz o peso de observações com estabilidade desconhecida e exige pelo menos três observações estáveis e metade das ordens com estabilidade confirmada. A estabilidade relativa a P1 só participa do ajuste quando P1 está verificado; coortes de outros parciais podem fornecer evidência auxiliar. O reconhecimento por previsão de picos acima da última ordem do ajuste não os incorpora à estimativa; ajustes recuperados por essa verificação não alimentam curvas. Consulte Decisões da análise e estabilidade relativa.

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
## 2.8. Resultado da sessão: consolidação de B e repetibilidade

Para sessões de corda rígida elegíveis, o motor procura um B comum e permite uma escala F diferente por execução. Não é uma simples média dos B individuais; cada execução conserva sua evidência, inclusive a relação entre frequências e resíduos. Por padrão, são requeridas ao menos três execuções elegíveis para consolidação e dez para a avaliação por reamostragem. Há outros testes de consistência, contexto, identificabilidade e qualidade. A tecla física confirmada não é requisito para consolidar B: a identidade e repetibilidade da mesma corda são essenciais. A confirmação da tecla e a coerência da identidade física são necessárias para usar evidência em curvas. Desvios acima de 45 cents em relação à tecla exigem autorização excepcional válida, inclusive para a fonte empírica independente.

| Estado | Significado | Próxima ação |
| --- | --- | --- |
| Aguardando medições | Sessão sem evidência suficiente | Toque novamente |
| Primeira medição — ainda sem B consolidado | Estimativa individual pode existir, sem conjunto | Repita de modo independente |
| B não aplicável | Modelo ou condição não corresponde a corda rígida elegível | Use os componentes observados; não force B |
| B inconclusivo / consolidação indisponível | Ordem, contexto, repetibilidade ou ajuste insuficientes | Consulte motivos, reveja a corda, revise ou repita |
| Consistente pelos critérios experimentais | Execuções incluídas passaram nas verificações do conjunto | Examine dispersão, resíduos e condições; não confunda com homologação |
| Incerteza não estimável / degenerada | Dados insuficientes ou reamostragem incapaz de produzir intervalo utilizável | Conserve os resultados e faça novas execuções independentes |

Em **Comparar as execuções e ver os cálculos**, a tabela apresenta B individual, diferença em relação ao B conjunto, F, peso, resíduo máximo e B sem ataque (efeito de retirar aquela execução). Um resultado fortemente dependente de um único ataque merece investigação; quando a retirada completa não foi possível, a interface pode indicar uma aproximação. Deslize horizontalmente a tabela em telas estreitas. Os dados completos são preservados nos formatos AFS e JSON de sessão.

O bootstrap reamostra ataques independentes, por padrão em 399 repetições, para investigar a variação entre execuções. A meta relativa de largura de B de 5% diz respeito ao comportamento experimental do conjunto; não equivale a erro absoluto de 5% nem certifica precisão física. Se os ataques forem praticamente idênticos, o intervalo pode ser degenerado. Um intervalo estreito também não elimina viés de microfone, identificação ou modelo. Sessões extensas podem exceder o orçamento de verificação completa.

Em **Execuções fora do ajuste**, examine os motivos: rejeição, contexto incompatível, frequência divergente, exclusão manual, parcial inválido ou condição física inadequada. Excluir observações só para reduzir resíduos introduz viés. Prefira registrar o motivo físico de uma exclusão e preservar as observações originais.

<a name="empirica"></a>
### Caracterização espectral empírica (independente de B)

A caracterização empírica descreve as relações de frequência efetivamente observadas, sem ajustar a equação da corda rígida. Não é um modelo acústico adicional nem um novo coeficiente B. Está disponível para sessões multiataque com Automático que identificou ordens, Série harmônica e Corda rígida, inclusive piano, fortepiano e cravo. Não se aplica a Exploratório e Componentes não harmônicos, que não atribuem ordens à série.

1. Escolha a família e o modelo apropriados. Para investigar um instrumento sem hipótese de corda rígida, use **Outro → Modelo acústico de Outro (avançado) → Série harmônica**.
2. Meça várias execuções independentes da mesma nota e fonte física. Preserve a técnica, a condição da fonte e a captação.
3. Pause ou finalize a sessão e abra **Caracterização espectral empírica (independente de B)**. Examine o número de ataques com primeiro parcial medido e aceito, o gráfico e a tabela. A apresentação não depende da existência de B individual ou consolidado.
4. Revise observações e exclusões quando houver justificativa acústica. Salve a sessão no perfil para consultar posteriormente. Para experimentar curvas, confirme a tecla e identifique a fonte física (ver [4.2](#curva-empirica)).

#### Como os desvios são calculados

Para cada execução `i`, o primeiro parcial `f₁,ᵢ` medido, aceito e com referência verificada serve de referência. A aceitação espectral de P1 não basta para considerá-lo referência metrológica: são necessárias observações temporais coerentes e concordância com evidências auxiliares. Se não houver P1 verificado, os gráficos descritivos podem mostrar relações entre parciais medidos ou extrapolação identificada de um modelo físico aceito, sem fornecer suporte empírico para curvas. Para uma ordem `n` com frequência observada `fₙ,ᵢ`:

- Razão observada: `rₙ,ᵢ = fₙ,ᵢ / f₁,ᵢ`.
- Desvio da série ideal: `δₙ,ᵢ = 1200 × log₂[rₙ,ᵢ / n]`, em cents.
- Desvio consolidado: mediana dos desvios daquela ordem entre os ataques admitidos.
- Razão consolidada: `rₙ = n × 2^(mediana(δₙ)/1200)`.

Por exemplo, numa execução em que o primeiro parcial mede 220 Hz, o segundo mede 440,5 Hz e o terceiro 659,2 Hz, os desvios são aproximadamente +1,97 e −2,10 cents. O primeiro parcial tem desvio zero por construção. Essa normalização permite comparar a estrutura da série mesmo quando a altura absoluta varia um pouco entre ataques. Não significa que as alturas absolutas tenham ficado constantes.

O cálculo admite somente execuções elegíveis, incluídas no conjunto, com resultado experimental e sem códigos de rejeição. Usa parciais aceitos, não excluídos, com frequência positiva, amplitude válida, SNR local de pelo menos 12 dB e ordem inteira de 1 a 24. Ordens duplicadas entre esses candidatos não são utilizadas. Um ataque precisa ter um único primeiro parcial admitido e verificado, a até 15 cents da fundamental estimada e, quando há frequência acústica de referência válida da sessão, a até 45 cents dela. Essa verificação de coerência entre ataques é distinta do limite de 45 cents em relação ao alvo teórico escolhido para a identificação da tecla. Não se utiliza uma fundamental virtual como substituta de um primeiro parcial ausente. O reconhecimento automático de ordens continua sujeito às tolerâncias do analisador; não há atribuição manual de ordem a picos arbitrários.

#### Ler a tabela e o gráfico

| Indicador | Interpretação |
| --- | --- |
| Razão mediana | Multiplicador de frequência consolidado em relação ao primeiro parcial |
| Desvio (¢) | Mediana dos desvios assinados em cents; negativo significa componente abaixo do múltiplo ideal |
| MAD (¢) | Mediana dos desvios absolutos em relação à mediana da ordem; medida descritiva robusta de dispersão |
| Máx. \|desvio da mediana\| (¢) | Maior afastamento absoluto observado da mediana; não é intervalo de confiança |
| Ataques | Observações admitidas para a ordem / total de execuções elegíveis e incluídas, inclusive as que não forneceram primeiro parcial válido |
| Estáveis | Observações em que tanto a ordem quanto o primeiro parcial têm estabilidade temporal registrada entre 0 e 3 cents |
| Bootstrap 95% (¢) | Intervalo exploratório da mediana, quando calculável |
| Suporte para curva* | Provisório ou Insuficiente, segundo os critérios por ordem; não autoriza por si só uma curva |

Na seção de caracterização espectral empírica, o gráfico próprio apresenta as medianas por ordem e barras de dispersão máxima simétricas em torno delas; a cor distingue suporte provisório para curva de evidência insuficiente. Não confunda esse gráfico com **Desvios da série harmônica ideal**, cujo controle **Dispersão / bootstrap** também pode mostrar intervalos quando disponíveis. A tabela pode ser deslocada horizontalmente. O **RMS descritivo** é a raiz da média dos quadrados dos desvios medianos das ordens superiores com pelo menos três ataques e cobertura de 60%; o primeiro parcial não entra nesse RMS. Compare RMS apenas com cobertura e ordens equivalentes. Um RMS pequeno não confirma a causa física dos desvios.

O bootstrap empírico usa 399 reamostragens por ordem quando há de 10 a 64 observações admitidas naquela ordem. O intervalo de 95% é descritivo, não uma incerteza calibrada; um intervalo zero pode ser degenerado. A ausência de intervalo não equivale a certeza nem impede necessariamente uma curva. Não confunda os critérios estatísticos fixos desta caracterização com as preferências do ajuste de B.

#### Descrever, sintetizar e usar em curvas são finalidades distintas

Uma tabela empírica pode existir com poucos dados, desvios irregulares ou sem B válido. A síntese consolidada requer a ordem 1 e pelo menos outra ordem com três ataques e 60% de cobertura, mas não exige suporte para curva. A fonte de curvas exige adicionalmente repetibilidade, estabilidade, identidade física e contexto de referência (ver [4.2](#curva-empirica)). Assim, um resultado útil para estudo pode permanecer inadequado para definir alvos de afinação. Nenhum desses caminhos inventa ordens ausentes.

<a name="ts-2"></a>
## 2.9. Solução de problemas — Aquisição e Análise acústica

| Sintoma | Ação recomendada |
| --- | --- |
| Não inicia aquisição | Ative o microfone, use contexto seguro e confirme suporte a AudioWorklet/Workers; encerre o Emissor ou diagnóstico. Consulte a mensagem do controlador. |
| Não reconhece toques | Deixe silêncio entre notas, use uma fonte isolada e teste o reconhecimento manual. |
| Som útil muito curto | Prolongue o som quando possível; revise descarte e duração útil em uma nova sessão exploratória. Um instrumento de decaimento curto pode oferecer poucos dados. |
| Poucos parciais separáveis | Confira ruído, distância, candidatos e teto de frequência. Aumentar janela pode ajudar em som estável; em sinais fracos, experimente o nível relativo em nova sessão. |
| Flauta sem B | Esperado: use Outro → Série harmônica. O modelo de corda rígida não é aplicável. |
| Piano completo sem B | Declare corretamente a nota completa/uníssono. B físico exige corda isolada elegível. |
| Outro sem B | Automático não ajusta B. Escolha Corda rígida apenas se houver corda isolada e evidência suficiente; reanálises harmônicas podem não fornecer B. |
| Outro com corda rígida não inicia | Selecione Isolada em Aquisição de nota; se a condição não for verdadeira, escolha outro modelo. |
| Outro não apresenta tecla ou ordens | Esperado em Exploratório, Componentes não harmônicos ou análise automática sem ordens aceitas. Examine picos e guarde sem tecla. |
| Fundamental ambígua | Toque uma nota de cada vez, reduza ruído e confirme a tecla se souber qual foi. A frequência-base pode permanecer inconclusiva. |
| Frequência incompatível com a sessão | Confirme mesma tecla e corda, A4, temperamento e contexto; se mudou de nota, finalize e inicie outra sessão. |
| B individual existe, conjunto não | Verifique número de execuções, mesma corda, qualidade e consistência. A tecla confirmada não é requisito para B. |
| Bootstrap sem resultado | Aumente a quantidade de ataques independentes, reveja degeneração, dispersão e limites de verificação; não assuma incerteza zero. |
| Gráfico sem dados novos | Libere a captura congelada; selecione nova execução. Captura antiga não ganha frequências novas ao ampliar. |
| Configuração não afetou a sessão | Sessões em andamento conservam os parâmetros de início. Finalize, preserve e comece outra. |
| Escuta pausada/interrompida | Mantenha a página em primeiro plano, confira a continuidade do microfone e não use Emissor/diagnóstico simultaneamente; retome com contexto válido. |
| Limite de memória atingido | Exporte a sessão e reduza o volume de novas revisões; conclua ou descarte antes de recomeçar. |
| Não consegue guardar no perfil | Finalize, aguarde a conclusão do cálculo e confira família, identificação da tecla quando exigida e modelo de Outro. Exporte AFS ou JSON para não perder a sessão. Veja [Capítulo 3](#cap-3). |
| Caracterização empírica vazia | Confira modelo harmônico ou de corda rígida, ataques incluídos, primeiro parcial medido e aceito, SNR e ordens válidas. Não force uma fundamental ausente. |
| Desvios aparecem, mas suporte para curva é insuficiente | Confira cobertura, estabilidade do primeiro parcial e da ordem, dispersão e SNR. Repita em condições equivalentes; veja [4.2](#curva-empirica). |
| Sessão personalizada não aparece para curva | É uma restrição deliberada: restaure critérios de referência e adquira novas medições elegíveis de Piano, Fortepiano ou Cravo. Para Outro, use Automático com ordens identificadas, Série harmônica ou Corda rígida e escolha a fonte empírica independente em Curvas, com parâmetros de referência. Não edite manualmente o JSON para contorná-la. |
| Revisão histórica não abre | Confira perfil, sessão, integridade e vínculos; recarregue a seleção se necessário. Compare uma sessão por vez se houver limite de recursos. |
| Comparação recusada | Confira fonte física, condições, parâmetros e modelo. Uma revisão da mesma sessão não é nova aquisição. |
| Diagnóstico de desempenho | Em Avançado, ative o registro antes da operação a investigar e exporte o JSON oferecido. Ele contém tempos e contagens, não PCM ou espectros. |
[Voltar ao sumário](#sumario)

<a name="cap-3"></a>
# Capítulo 3 — Instrumentos

Um perfil instrumental é um prontuário acústico do instrumento: identificação, extensão, ordem física das teclas, condições das medições e sessões. Ele não muda a afinação nem armazena WAV. É possível guardar resultados inconclusivos para acompanhar a qualidade das medições ao longo do tempo. O gerenciador administra a biblioteca; a visualização e a comparação científicas ficam na Análise acústica.

<a name="criar-perfil"></a>
## 3.1. Criar um perfil instrumental

1. Confira o temperamento, referência e disposição musical do Afinador, especialmente quando houver teclas divididas ou EDO.
2. Abra **Aquisição acústica → Instrumentos → Novo perfil**.
3. Informe **Nome** e **Família**. Em **Avançado**, acrescente fabricante/subtipo e observações se desejar; para Outro, escolha o modelo acústico correspondente.
4. Pressione **Criar e salvar perfil**. Não é necessário escolher primeira ou última tecla.
5. Use **Voltar à ferramenta**. Meça as notas desejadas e salve as sessões.

O perfil começa com mapa observado vazio. Ao salvar uma sessão com identidade física confirmada e compatível, somente essa identidade é acrescentada. Medir Sol2, Dó2 e Mi2 nessa ordem cadastra Dó2, Mi2 e Sol2, não as demais notas. A extensão observada Dó2–Sol2 não prova a existência de todas as teclas intermediárias. Isso permite estudar oitavas curtas, oitavas quebradas e instrumentos parcialmente medidos. Perfis com mapa explicitamente declarado preservam sua disposição.

A família e o modelo precisam ser compatíveis com a aquisição. Para Outro, preserve a hipótese acústica do perfil. Em instrumentos de múltiplas cordas ou registros, use rótulos consistentes (ou perfis separados) para facilitar comparação. A ausência do rótulo não impede guardar evidências, mas pode limitar a comparabilidade e a elegibilidade para curvas.

<a name="salvar-sessoes"></a>
## 3.2. Salvar sessões em sequência

1. Escolha o instrumento na Aquisição acústica.
2. Inicie medição, toque a mesma nota em ataques independentes e finalize.
3. Confira o resumo e a identificação. Se necessário, abra **Analisar resultados** e retorne à aquisição.
4. Pressione **Salvar e medir próxima nota**. Aguarde a barra e o retorno automático à medição.
5. Toque a próxima nota desejada no modo automático, ou confira/ajuste o alvo no modo fixo. É permitido saltar notas e oitavas. Repita.
6. Na última nota, use **Salvar** se não quiser reiniciar a aquisição. Exporte AFP como backup.

Se não houver identidade física confirmada, preserve a sessão sem inventar uma tecla; use o salvamento sem avanço quando disponível ou exporte AFS. Se houver falha de gravação, não descarte o rascunho: leia o motivo e tente novamente. Os critérios de integridade, deduplicação e compatibilidade continuam ativos. Uma sessão com B inconclusivo pode ser preservada.

<a name="controles-perfis"></a>
## 3.3. Gerenciamento e disposição física

| Controle | Uso |
| --- | --- |
| Instrumento / Novo perfil / Criar e salvar perfil | Selecionar ou criar uma coleção acústica. |
| Importar instrumento / Abrir sessão | Trazer um perfil AFP/JSON ou uma sessão compatível. |
| Renomear / Editar metadados | Corrigir identificação documental. |
| Excluir perfil | Remover perfil e registros locais; faça backup primeiro. |
| Exportar perfil (.afp) / Exportar perfil (JSON) | Criar backup binário ou intercâmbio estruturado. |
| Mapa de teclas / setas de oitava | Consultar medições por identidade física. |
| Medições sem tecla / fora do mapa | Consultar sessões não vinculadas ou arquivadas. |
| Histórico / Avançado do registro | Consultar e gerenciar sessões, incluindo exportação individual. |
| Salvar sessão neste perfil / Baixar sessão sem salvar / Cancelar salvamento | Concluir, preservar externamente ou abandonar uma associação pendente. |
| Voltar à ferramenta | Fechar o gerenciador sem iniciar áudio. |

### Avançado

| Controle | Uso e cuidados |
| --- | --- |
| Duplicar perfil | Criar cópia independente; não mescla perfis. |
| Informações do instrumento e disposição física | Inspecionar metadados e ordem de identidades. |
| Editar extensão física | Declarar deliberadamente primeira e última tecla; leia as consequências. Essa edição deixa de ser apenas mapa observado. |
| Mover antes / Mover depois | Corrigir a ordem física quando conhecida. |
| Solicitar persistência | Pedir armazenamento menos sujeito a remoção automática; não substitui backup. |
| Limpar transferências | Recuperar recursos de transferências interrompidas; não apaga perfis publicados. |
| Diagnóstico de desempenho | Registrar tempos e tamanhos de operações. |

Ao corrigir a disposição de 12/13/14 teclas ou reduzir uma extensão declarada, as medições incompatíveis podem ser arquivadas fora do mapa, não apagadas. Restaurar identidades compatíveis permite recuperar os vínculos, respeitando decisões manuais de descarte. Nos perfis de observação automática, a mudança de disposição não cria posições nunca medidas. Não use a edição de extensão apenas para completar lacunas. Antes de alterar mapas, exporte AFP; alterações de fontes podem invalidar curvas.

<a name="cfg-3"></a>
## 3.4. Preferências do gerenciador

Abra **Configurações** enquanto o gerenciador Instrumentos estiver aberto, seja pela Aquisição ou pela Análise. O grupo **Apresentação** oferece **Ordenação das sessões** (Mais recentes, Mais antigas ou Qualidade provisória; padrão Mais recentes) e **Mostrar sessões inconclusivas** (padrão Sim). A ordenação por qualidade é triagem, não classificação metrológica. O filtro não apaga registros. O histórico também dispõe de Ordenar em Avançado. Restaurar padrões atua somente nas preferências do gerenciador. Ao usar Voltar à ferramenta, Configurações e Ajuda voltam a corresponder à ferramenta de origem.

<a name="comparar-sessoes"></a>
## 3.5. Mapa e histórico

O teclado SVG compartilhado pela aquisição e pelo gerenciador mostra uma oitava por vez. Bolinha verde indica uma medição; sem bolinha significa que não há medição naquela posição, não necessariamente que a tecla existe. As metades das teclas divididas são selecionáveis separadamente. EDO usa graus, não divisões enarmônicas históricas fictícias. A disposição armazenada é independente da escolha musical corrente do Afinador.

No gerenciador, selecione a tecla para consultar seu histórico; em **Análise acústica**, abra a sessão para examinar os gráficos. Consulte **Medições sem tecla / fora do mapa** se não encontrar um registro. Descartar da modelagem é distinto de excluir definitivamente. Uma sessão arquivada não alimenta curvas enquanto estiver fora do mapa. Exporte antes de excluir dados importantes.

<a name="backup-perfil"></a>
## 3.6. Exportação, importação e armazenamento

### Backup e restauração

1. Selecione o perfil e pressione **Exportar perfil (.afp)**. Esse é o formato preferencial para transportar o instrumento e suas sessões. Confira o arquivo no destino selecionado pelo navegador. Em Avançado, **Exportar perfil (JSON)** oferece a alternativa estruturada; no Avançado de um registro do histórico, **Exportar sessão (.afs)** guarda somente aquela sessão.
2. Para restaurar ou transferir um instrumento, use **Importar instrumento** e escolha AFP ou JSON de perfil compatível. A importação valida e cria um perfil diretamente, sem confirmação redundante. Em colisão de ID, cria uma cópia independente; não sobrescreve nem mescla perfis existentes.
3. Para importar uma sessão multiataque (.afs ou JSON), use **Abrir sessão** no gerenciador ou **Abrir sessão…** na Análise acústica. A sessão validada fica pendente: escolha perfil compatível e confirme **Salvar sessão neste perfil**. Substituir uma sessão ainda pendente exige confirmação. Uma análise individual genérica não é uma sessão multiataque importável como registro.
4. Acompanhe a janela de progresso nas transferências binárias. A porcentagem refere-se à fase atual, não ao tempo restante. É possível cancelar antes da finalização; não considere o arquivo salvo ou o perfil publicado até a confirmação de conclusão. Se a operação for interrompida, confira o destino e não descarte a cópia original.

### Limites e armazenamento (avançado)

| Recurso | Limite / condição |
| --- | --- |
| Perfis locais e registros por perfil | Até 2.000 de cada, sujeitos à quota e validação |
| JSON acústico | Até 32 MiB, sujeito a limites de estrutura e conteúdo |
| Evidência bruta AFB individual | Até 32 MiB |
| Contêiner AFP | Até 1 GiB, sujeito à quota e demais restrições de validação |
| Exportação binária sem gravação direta em arquivo | Até 128 MiB no caminho de download por Blob; para arquivos maiores, use navegador com gravação em arquivo |

Os limites são tetos, não garantia de que o dispositivo tenha memória ou espaço suficiente. Em **Avançado**, confira o uso estimado da origem, use **Solicitar persistência** para reduzir certas remoções automáticas e **Limpar transferências** para recuperar transferências interrompidas. Persistência pode ser negada; não impede limpeza manual e não substitui backup. Se houver falha, preserve os arquivos válidos e divida novas coletas em perfis menores; não edite IDs ou hashes.

Os dados ficam no IndexedDB da origem do navegador, sem sincronização automática entre aparelhos. Para migrar, exporte AFP no aparelho de origem, importe no destino e abra algumas sessões para verificar o conteúdo. SHA-256 confere integridade, não autoria. Use uma origem segura com APIs compatíveis. O armazenamento de perfis e curvas é binário; JSON compatível é intercâmbio, não um segundo banco de dados.

### Diagnóstico de desempenho

Abra Avançado → Diagnóstico de desempenho e habilite o registro antes de importar/exportar. Ao concluir, guarde o JSON de diagnóstico disponibilizado pela ferramenta. Ele registra tempos, contagens e tamanhos, não inclui evidências acústicas nem identificação. O tempo ativo exclui esperas de interação registradas (por exemplo, escolher destino). Os tempos internos podem se sobrepor; não some métricas hierarquicamente aninhadas. Memória linear WASM e tamanhos de buffers não equivalem a RAM física total. Desative o diagnóstico quando não precisar investigar.

<a name="ts-3"></a>
## 3.7. Solução de problemas — Instrumentos

| Sintoma | O que fazer |
| --- | --- |
| IndexedDB ou banco indisponível | Use navegador moderno, verifique permissões de armazenamento e origem; exporte evidências sem salvar se necessário. |
| SHA-256 indisponível | Use HTTPS/localhost. Não há confirmação segura de gravação sem os recursos necessários. |
| Família/modelo incompatível | Escolha o perfil da família correta e, para Outro, do mesmo modelo acústico, ou crie outro. Não altere a declaração da sessão só para guardar em perfil inadequado. |
| Não há sessão pronta | Finalize e revise, aguarde o cálculo e use **Salvar** ou **Salvar e medir próxima nota** na Aquisição acústica. |
| Registro já salvo ou duplicado | Consulte a sessão existente ou sua revisão. Não duplique uma mesma execução como se fosse nova observação de outra corda. |
| Tecla não aparece no mapa | Abra Medições sem tecla / fora do mapa; reveja layout e identidade física. |
| Não consigo revisar uma sessão | Selecione o instrumento, abra Análise acústica pelo menu e escolha a tecla e a sessão em Medições armazenadas. |
| Resultados inconclusivos não aparecem | Confira o filtro de apresentação; restaurar padrões não recupera arquivos realmente excluídos. |
| Comparação física recusada/limitada | Confira identidade, modelo, procedimento, configuração e condição de áudio; examine as sessões separadamente. |
| Importação recusada | Verifique tipo de arquivo, integridade, tamanho e mensagem da validação. Use o backup original; não contorne o validador. |
| Perfil importado aparece em duplicidade | A importação cria uma cópia independente em caso de colisão de ID. Não há mesclagem automática. Confira os dados antes de excluir qualquer cópia. |
| Cota de armazenamento atingida | Exporte perfis/sessões, confirme as cópias, organize novas coletas em outro perfil; só então remova dados dispensáveis. |
| Perfil ausente após trocar de aparelho | Importe o backup AFP ou JSON compatível. O armazenamento é local, não sincronizado por conta. |

[Voltar ao sumário](#sumario)

<a name="cap-4"></a>
# Capítulo 4 — Curvas de afinação

Esta ferramenta investiga correções instrumentais para **piano, fortepiano e cravo**. **Outro**, com Automático que identificou ordens, Série harmônica ou Corda rígida, também pode ser estudado pela fonte empírica independente de B, explicitamente selecionada e sujeita a condições adicionais. Parciais de uma fonte real podem desviar da série ideal, e as relações entre parciais de teclas diferentes podem sugerir correções nas frequências de afinação, tanto por um modelo físico quanto por razões medidas repetíveis. O objetivo é permitir o estudo dessas relações com evidência rastreável e restrições explícitas, não produzir uma receita universal de estiramento de oitavas.

> **Todas as curvas instrumentais são experimentais e não homologadas fisicamente.** Gerar uma curva não altera a afinação. O botão **Aplicar ao Afinador** registra a aprovação experimental, guarda a revisão e exige a revalidação das fontes e o recálculo coincidente antes de ativar a correção. O clique é a autorização explícita, sem janelas adicionais de confirmação do navegador. Consulte [4.7](#aplicar-curva).

<a name="pre-curva"></a>
## 4.1. Pré-requisitos e preparação do perfil

1. Escolha a base musical adequada (temperamento, referência e layout). Guarde uma definição na [biblioteca pessoal](#biblioteca) para poder recuperá-la posteriormente.
2. Crie um perfil de **Piano, Fortepiano ou Cravo**, ou de **Outro** com Automático que identificou ordens, Série harmônica ou Corda rígida se estudar a fonte empírica, com o mapa físico correto, conforme [3.1](#criar-perfil). Para cravo e fortepiano, use um perfil por registro ou conjunto de cordas, com extensão e oitavas efetivamente soantes; não misture 8′ e 4′.
3. Obtenha sessões multiataque com identificação inequívoca de tecla e fonte física, utilizando os parâmetros acústicos de referência. Piano, fortepiano e cravo exigem corda isolada, inclusive na fonte empírica. Outro com Corda rígida também exige isolamento; Outro com Automático ou Série harmônica admite nota completa ou condição desconhecida. Uníssonos declarados não são aceitos para curvas. Consulte [2.3](#multiataque) e [2.8](#consolidacao).
4. Salve as sessões no perfil. Use várias teclas da região que pretende estudar; poucas teclas podem permitir inspecionar alguns intervalos, mas não necessariamente construir uma curva completa.
5. Confira a ordem real das teclas. Registre condições de corda, grupos de uníssono e transições construtivas. Não suponha que todo o instrumento constitua uma região fisicamente homogênea.

Sessões personalizadas de análise e famílias diferentes não são intercambiáveis com as fontes de uma curva do instrumento escolhido. Na fonte empírica independente, B ausente ou inconclusivo não é impedimento por si só, mas a evidência por ordem deve ser elegível. A seleção das fontes avalia compatibilidade da base musical, identidade física, qualidade e consistência das observações. Em ambas as fontes, discrepâncias de identidade superiores a 45 cents exigem confirmação excepcional vinculada às evidências; essa autorização não substitui os critérios de qualidade nem os limites próprios da curva. Quando há mais de uma corda medida para a tecla, selecione a fonte representativa se a interface solicitar, ou deixe a tecla sem correção. Uma fonte representativa não descreve automaticamente todas as cordas de um uníssono.

### O que significa uma correção de curva

A frequência musical teórica de uma tecla é `fₜ`. Uma correção instrumental de δ cents propõe `f curva = fₜ × 2^(δ/1200)`. Se o alvo teórico é 440 Hz e δ = +2 cents, a proposta é aproximadamente 440,509 Hz. Zero significa manter a frequência teórica daquele temperamento. A curva não substitui a própria receita musical.

Ao escolher uma âncora, a correção desta tecla permanece zero. As demais são calculadas relativamente a ela. O limite de correção é ±30 cents; não se pode deslocar a âncora ou usar esse intervalo para contornar exigências de cobertura e proteção.

<a name="gerar-curva"></a>
## 4.2. Gerar uma curva

Em **Ferramentas → Curvas de afinação**, o fluxo principal tem duas ações: **Gerar curva** e **Aplicar ao Afinador**. O detalhamento matemático e o gerenciamento de versões estão recolhidos em **Avançado**.

### 1. Escolha o instrumento

O instrumento ativo é selecionado quando compatível. Selecione outro **Perfil** se necessário. Os metadados completos do instrumento, a cobertura e o histórico ficam no gerenciador **Instrumentos**; em Curvas aparece apenas um resumo. A lista se atualiza ao entrar em Curvas, e as evidências são recuperadas quando necessárias ao cálculo. Em **Avançado → Cálculo, referência, arquivos e diagnóstico**, use **Atualizar perfis** para recuperação manual ou **Abrir backup de perfil (sem importar)** para estudar uma cópia JSON validada sem criar perfil local. Para AFP, importe primeiro em Instrumentos.

Examine o quadro de disponibilidade e escolha, quando solicitadas, as fontes de cada tecla. Registros de cordas diferentes ou sessões divergentes requerem revisão; o aplicativo pode deixar a tecla sem evidência utilizável.

### 2. Escolha o objetivo

| Objetivo | Interpretação |
| --- | --- |
| Fidelidade ao temperamento (recomendado) | Procura preservar os desvios intervalares assinados da receita musical, conciliando-os com as propriedades acústicas e as proteções escolhidas. Não busca zerar indiscriminadamente todos os batimentos. |
| Otimização acústica | Busca coincidência das componentes intervalares consideradas; pode alterar intencionalmente relações do temperamento. Deve ser comparada com a base musical. |

O aplicativo preseleciona uma **Tecla fixa de referência** (preferencialmente Lá4 quando disponível). Para alterá-la, abra **Avançado → Cálculo, referência, arquivos e diagnóstico**, no fim da ferramenta. Quando um registro único estiver claramente identificado no perfil, ele será utilizado automaticamente. Se não estiver, o cravo mostrará um campo curto **Registro**; informe o registro verdadeiro antes de gerar. Subtipo ou fabricante genérico não substitui essa identificação.

Não há uma caixa extra de confirmação da ordem física. A sequência de teclas é a do mapa armazenado no perfil. Antes de medir e salvar, confira que o mapa está correto e que as fontes pertencem ao mesmo registro/conjunto, têm técnica comparável e representam as alturas realmente soantes. Num cravo, não misture cordas 8′ e 4′ como se pertencessem a uma mesma série. Os validadores continuam verificando metadados e evidências; não podem inferir todos os fatos físicos a partir de números.

### Avançado — opções de cálculo e referência (opcional)

| Campo | Uso |
| --- | --- |
| Estilo de pesos | Conservador, Equilibrado ou Acústico: modifica a importância relativa das relações entre teclas; não é classificação de qualidade do instrumento. |
| Fonte de parciais | Automática conservadora, Modelo B, Parciais medidos ou Parciais empíricos — independente de B (experimental). Escolher uma fonte não torna dados insuficientes válidos. |
| Proteger quintas e quartas centrais | Na política experimental de Fidelidade, protege relações centrais na região de ±600 cents da âncora. |
| Incluir terças maiores e menores | Acrescenta relações de terças quando há evidência; começa desmarcado no piano e marcado em fortepiano e cravo. |
| Preservar terças próximas das puras | No objetivo Fidelidade, protege a largura fundamental de terças a até 1 cent da razão justa; começa marcado no cravo e desmarcado nos demais. Pode limitar a compensação acústica. |
| Declarar região homogênea para interpolação | Para Automática conservadora, Modelo B e Parciais medidos, autoriza interpolação limitada entre a primeira e a última tecla selecionadas. Na fonte empírica independente, a interpolação é proibida. Declare apenas se a região realmente não contém quebras de escala ou mudanças relevantes de corda. |

O estilo Equilibrado e a fonte Automática conservadora são pontos de partida. Piano, fortepiano e cravo possuem pesos-base específicos; em Outro, todos os estilos partem de pesos unitários iguais por família intervalar, ajustáveis por multiplicadores. Esses pesos são hipóteses experimentais de projeto, não regras históricas comprovadas nem parâmetros calibrados. A seguir, os pesos-base do estilo Equilibrado antes dos multiplicadores do usuário:

| Família de intervalo | Piano | Fortepiano | Cravo |
| --- | ---: | ---: | ---: |
| Oitava | 1 | 1 | 1 |
| Duodécima | 1 | 0,5 | 0,25 |
| Quinta | 0,65 | 0,9 | 1 |
| Quarta | 0,3 | 0,6 | 0,8 |
| Dupla oitava | 0,7 | 0,4 | 0,25 |
| Terça maior | 0,5 | 0,9 | 1,2 |
| Terça menor | 0,35 | 0,65 | 0,9 |

Os pesos são distribuídos pelas relações disponíveis de cada família; relações desativadas ou sem evidência não fornecem termos acústicos. No piano há ainda uma ênfase experimental de registro (certos parciais mais altos no grave e mais baixos no agudo). O Modelo B usa previsões de componentes do modelo de corda rígida quando elegível; Parciais medidos usa observações compatíveis, mas ainda requer B consolidado elegível. Na fonte empírica independente, somente razões de ordens observadas com suporte são utilizadas. Em Automática conservadora, Modelo B e Parciais medidos, por padrão não há interpolação ou suavização entre teclas sem confirmação de uma região homogênea; a fonte empírica independente não permite interpolação em nenhuma hipótese. **Extrapolação é proibida**: não se deve prolongar uma tendência além da evidência disponível.

Pressione **Gerar curva**. Aguarde a conclusão; **Cancelar cálculo** interrompe a operação. Se a base musical mudar durante o cálculo, a operação pode ser invalidada. Se houver dados insuficientes, preserve as orientações e retorne à coleta em vez de forçar a geração. A prévia inicial não altera as frequências ativas do Afinador.

<a name="curva-empirica"></a>
### Fonte empírica independente de B (experimental)

A quarta opção de fonte não substitui o caminho usual. Ela permite estudar correções quando as relações dos parciais são repetíveis, mesmo que a equação de corda rígida não consiga explicá-las. O otimizador utiliza as razões empíricas consolidadas em lugar de depender de B. Para duas teclas A e B, com razões medidas `rA,p` e `rB,q`, as frequências previstas das componentes para determinados alvos fundamentais `fA` e `fB` são `fA × rA,p` e `fB × rB,q`. Os objetivos musicais, pesos e proteções continuam definindo o compromisso entre as relações disponíveis. A hipótese de que essas razões permanecem estáveis durante pequenas mudanças de afinação não está homologada fisicamente.

| Fonte de parciais | B consolidado provisoriamente consistente | Ordens utilizadas | Outro |
| --- | --- | --- | --- |
| Automática conservadora (padrão) | Exigido | Modelo ou evidência medida segundo os critérios físicos de B | Não |
| Modelo B | Exigido | Previsões elegíveis do modelo físico | Não |
| Parciais medidos | Exigido | Observações compatíveis, subordinadas à validação anterior | Não |
| Parciais empíricos — independente de B (experimental) | Não exigido | Somente razões realmente medidas e repetíveis | Sim, em Automático com ordens identificadas, Série harmônica ou Corda rígida |

#### Preparar e verificar a evidência

1. No perfil, reúna sessões de várias teclas, com parâmetros de referência, tecla confirmada e fonte física identificada. Não combine fontes diferentes como se fossem uma única observação. Consulte a [caracterização empírica](#empirica) de cada sessão.
2. Abra **Ferramentas → Curvas de afinação** e selecione o perfil. Em **Avançado → Cálculo, referência, arquivos e diagnóstico**, confira **Parciais empíricos — independente de B (experimental)**. Em Outro essa fonte é preselecionada; o usuário pode conferir e alterá-la quando o modelo e a política permitirem.
3. Examine a disponibilidade de teclas e escolha as fontes representativas quando solicitado. Confira o mapa físico em Instrumentos e, se necessário, ajuste a âncora em Avançado. Configure objetivo e proteções como no procedimento anterior. Deixe a declaração de região homogênea desmarcada.
4. Gere a prévia somente quando houver evidência suficiente. Revise as origens, as relações efetivamente usadas e a cobertura. Se houver lacunas ou sessões conflitantes, faça novas medições ou reveja as fontes. Não complete a curva artificialmente.

| Critério de suporte por ordem | Exigência experimental |
| --- | --- |
| Primeiro parcial | Medido e aceito, conforme os filtros da caracterização empírica |
| Ataques estáveis | Pelo menos 3 |
| Cobertura | Pelo menos 60% do total de execuções elegíveis e incluídas |
| SNR local | Pelo menos 12 dB em cada observação admitida |
| SNR mediano da ordem | Pelo menos 20 dB |
| Estabilidade temporal | Todas as observações da ordem e respectivos primeiros parciais com estabilidade disponível de até 3 cents |
| Afastamento máximo da mediana | Até 1 cent |

A tecla precisa ter suporte na ordem 1 e em pelo menos outra ordem superior. O indicador **Suporte para curva** na tabela empírica é apenas uma triagem por ordem: o cálculo verifica ainda a tecla física confirmada, a fonte identificada, as condições de isolamento aplicáveis, o contexto musical compatível, os parâmetros de referência e a integridade das fontes. Uma sessão descartada do modelo não pode ser utilizada. Os critérios são fixos e provisórios; não constituem homologação física. Um intervalo de bootstrap não é requisito adicional obrigatório nessa fonte.

A fonte não prevê ordens que não foram medidas, não interpola teclas e não extrapola além da evidência. Se não houver correção sustentada, o alvo permanece teórico. A prévia, revisão, histórico e eventual aplicação estão sujeitos às verificações de integridade e compatibilidade; não há aplicação automática. Em Outro, os pesos unitários são uma hipótese genérica de estudo, não uma recomendação universal de como afinar instrumentos de outras famílias.

<a name="controles-curvas"></a>
## 4.3. Todos os parâmetros selecionáveis e opções de Avançado — Curvas de afinação

Uma curva é uma **proposta de correção calculada** a partir de evidências elegíveis e de uma base musical definida. **Gerar curva** produz prévia; **Aplicar ao Afinador** aprova, salva, revalida e aplica de forma explícita. Nenhuma medição nova substitui automaticamente uma curva aplicada. A seguir estão os controles operacionais e os blocos recolhidos de Avançado. Os padrões persistentes e multiplicadores ficam imediatamente na seção de Configurações.

### Seleção e cálculo

| Controle | Objetivo | Critérios e limites |
| --- | --- | --- |
| **Perfil** | Determinar o instrumento cujas evidências serão utilizadas | Seleção atualizada ao entrar em Curvas e após commit de sessões; não garante elegibilidade científica de cada registro. |
| **Objetivo: Fidelidade ao temperamento** | Conciliar propriedades acústicas preservando a intenção intervalar da receita | Ponto de partida recomendado para estudo de temperamentos históricos. |
| **Objetivo: Otimização acústica** | Priorizar coincidências entre componentes parciais consideradas | Pode alterar intencionalmente quintas, quartas e terças do temperamento, conforme pesos/proteções. |
| **Registro** (quando solicitado) | Identificar o registro de cravo tratado como fonte física única | Não misture 8′ e 4′ nem use fabricante como substituto do registro. |
| **Seleção de fontes por tecla** | Escolher corda/sessão representativa quando houver ambiguidades | Não combine uníssonos distintos indiscriminadamente; evidência insuficiente deixa o alvo teórico. |
| **Gerar curva / Cancelar cálculo** | Iniciar ou interromper explicitamente a otimização | Recalcular após sessões novas; gerar não altera o Afinador nem reinstala curva antiga. |
| **Aplicar ao Afinador** | Aprovar, guardar, reproduzir o cálculo e ativar a correção | Só fica disponível se revalidação e regras de segurança forem satisfeitas. É experimental, não homologação física. |
| **Desligar correção** | Remover imediatamente a correção aplicada nesta visita | Preserva medições e histórico; não precisa recalcular para voltar a referências teóricas. |
| **Intervalos que serão afetados** | Antecipar alterações fundamentais de cada família de intervalos | Desvio positivo alarga e negativo estreita; consulte as famílias reais da prévia, não presuma que todas foram usadas. |

### Avançado → Cálculo, referência, arquivos e diagnóstico

| Parâmetro / comando | Objetivo | Interpretação e restrições |
| --- | --- | --- |
| **Tecla fixa de referência** | Escolher a âncora cuja correção permanece zero | Preferência inicial por Lá4 quando disponível; nenhuma versão pode deslocar a âncora. |
| **Estilo de pesos: Conservador / Equilibrado / Acústico** | Distribuir prioridades entre famílias de relações | Não altera a qualidade científica da fonte, apenas o compromisso do otimizador. |
| **Fonte de parciais: Automática conservadora** | Usar previsão ou evidência medida sob política conservadora de B | Exige B consolidado provisoriamente consistente. |
| **Fonte: Modelo B** | Prever parciais pelo modelo de corda rígida aceito | Exige dados físicos e B elegíveis; não transforma um espectro exploratório em corda rígida. |
| **Fonte: Parciais medidos** | Usar frequências observadas elegíveis, com as verificações de B | Não é a fonte empírica independente; requer B provisoriamente consistente. |
| **Fonte: Parciais empíricos — independente de B (experimental)** | Usar razões parciais consolidadas e estáveis sem exigir B | Compatível com Outro sob modelos adequados; exige primeiro parcial, ordem superior, identidade, estabilidade e contexto; proíbe interpolação. |
| **Proteger quintas e quartas centrais** | Impor restrições aos intervalos próximos da âncora em Fidelidade | Protege a região central definida pelo algoritmo; pode reduzir graus de liberdade para compensar desvios. |
| **Incluir terças maiores e menores** | Adicionar essas famílias ao objetivo quando houver dados | Desmarcada por padrão para piano; marcada para fortepiano e cravo no fluxo operacional indicado. |
| **Preservar terças próximas das puras** | Restringir terças cujo intervalo fundamental já está perto da razão justa | Política de Fidelidade; útil para não sacrificar terças históricas próximas das puras. |
| **Declarar região homogênea para interpolação** | Autorizar preenchimento **limitado entre evidências** nas fontes permitidas | Só marque se construção e escala forem fisicamente homogêneas; na fonte empírica é ignorada/proibida. Extrapolação nunca é permitida. |
| **Primeira tecla / Última tecla** | Delimitar a região declarada para interpolação | Não inventam dados nem definem automaticamente uma região homogênea. |
| **Atualizar perfis** | Recarregar a lista e evidências locais | Útil após importar ou salvar novas sessões; não gera curva nem aplica automaticamente. |
| **Abrir backup de perfil (sem importar)** | Examinar perfil JSON compatível de forma transitória | Para AFP, importe em Instrumentos; visualização temporária não equivale a publicação no banco. |
| **Diagnóstico de desempenho** | Investigar custo e transferência de dados do cálculo | Registra tempos, contagens e tamanhos, não é arquivo acústico nem áudio. |

### Avançado → Dados e diagnósticos da curva

| Controle / informação | Uso | Cuidados |
| --- | --- | --- |
| **Comparar os dois objetivos** | Ver resultado alternativo de Fidelidade versus Otimização | Não substitui silenciosamente a prévia escolhida. |
| **Descartar prévia / Exportar prévia (JSON)** | Abandonar cálculo de trabalho ou guardar seu resultado inicial | Descartar não exclui automaticamente históricos armazenados. |
| **Inspecionar tecla e origens → Tecla** | Escolher ponto e rastrear frequência teórica, proposta, correção e fonte | Ponto teórico sem correção não significa prova física de desvio exatamente zero. |
| **Todos os pontos e origens** | Abrir tabela completa de frequências, Δ em cents e proveniência | Diferencie ponto calculado, interpolado, manual e teórico. |
| **Por que esta correção? → Intervalo e parciais** | Inspecionar pares de ordens empregados em cada intervalo | P.ex., 2:1 na oitava e 3:2 na quinta; só relações elegíveis entram na otimização. |
| **Proteção e diagnóstico** | Conferir resíduos, limiares, restrições e auditoria | Sensibilidade não equivale a intervalo de confiança calibrado. |

### Avançado → Histórico, versões e revisão

| Controle | Objetivo | Efeito e restrições |
| --- | --- | --- |
| **Abrir histórico local** | Recuperar curvas e revisões salvas | Recuperação não ativa uma curva por conta própria. |
| **Abrir backup de versões / Exportar histórico (.afc)** | Transportar conjunto de versões e auditoria | AFC é histórico de curvas, não AFP instrumental. |
| **Exportar histórico (JSON)** | Intercâmbio estruturado | Não contorna verificações de fontes nem assinatura de integridade. |
| **Limpar histórico temporário** | Retirar versões de trabalho da memória | Não é sinônimo de excluir a cópia local persistente. |
| **Gerenciar espaço local → Excluir cópia local do histórico** | Excluir histórico persistente selecionado | Faça backup e confira o alvo antes de confirmar. |
| **Versão em revisão** | Escolher qual estado editar ou inspecionar | Uma versão importada pode abrir em somente leitura. |
| **Revalidar fontes para editar** | Verificar perfil, snapshots, hashes e reprodutibilidade do cálculo | A edição só é liberada quando a revisão continua compatível. |
| **Desfazer / versão anterior; Restaurar prévia original** | Navegar na genealogia de revisões | Não altera automaticamente a versão aplicada anteriormente. |
| **Tecla / Correção fixa em cents / Motivo** | Fixar uma proposta justificada e recalcular as demais | Limite ±30 cents; âncora não pode ser deslocada, nem pontos sem evidência recebem correção inventada. |
| **Fixar e recalcular / Voltar ao cálculo automático** | Impor/remover a restrição manual | O otimizador resolve novamente as demais relações; não basta editar um ponto gráfico. |
| **Preservar o intervalo desta tecla com / Proteger intervalo / Remover proteção individual** | Adicionar/remover restrição intervalar específica | Restrições conflitantes podem impedir cálculo; verifique consequências musicais. |
| **Estilo / Objetivo / Família de intervalo / Multiplicador de peso (0,1–10)** | Reponderar intervalos e recalcular revisões | Multiplicador não está em cents nem inventa evidência; altere uma hipótese por vez. |
| **Proteger quintas e quartas centrais / Incluir terças / Preservar terças próximas das puras** | Alterar restrições no editor | Recalcule e compare com a prévia original antes da aprovação. |
| **Recalcular objetivo e peso / Cancelar revisão** | Publicar nova solução de trabalho ou interromper | Alterações não aprovadas não se aplicam automaticamente. |
| **Comparar versões e ver consequências musicais → Comparar com / Intervalo fundamental: outra tecla / Comparação de parciais** | Auditar diferenças de afinação entre versões | Compare sempre sob a mesma base musical e fontes compatíveis. |
| **Aprovar revisão (opcional) / Guardar histórico local** | Registrar uma revisão sem aplicá-la | O comando principal **Aplicar ao Afinador** já contém aprovação e gravação, quando elegível. |

### Segurança automática das curvas

Mudar a quantidade de teclas da **Afinação**, a enarmonia adicional de 13 teclas, o temperamento ou a referência de frequência **desativa imediatamente uma curva ativa que dependia do contexto anterior**, com aviso. Alterar a disposição do **perfil instrumental usado pela curva** faz o mesmo. Alterações relevantes nas sessões/fontes podem invalidar prévias e aplicações. Retornar à configuração anterior **não reativa** a curva; gerar outra é uma ação explícita, e reaplicar uma versão exige revalidação. Sessões arquivadas por incompatibilidade física não entram no cálculo. Teclas sem evidência elegível conservam a frequência teórica. Curvas guardadas e medições não são apagadas por essa desativação.

<a name="cfg-4"></a>
## 4.4. Configurações de Curvas de afinação

As preferências de otimização se destinam a novos cálculos. A apresentação pode mudar sem recalcular as versões guardadas.

### Preferências de otimização (aberto)

| Campo | Padrão | Opções |
| --- | --- | --- |
| Objetivo | Fidelidade ao temperamento | Fidelidade ou Otimização acústica |
| Estilo | Equilibrado | Conservador, Equilibrado, Acústico |
| Fonte de parciais | Automática conservadora | Automática, Modelo B, Parciais medidos, Parciais empíricos — independente de B (experimental) |
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

Em Automática conservadora, Modelo B e Parciais medidos, a interpolação é confirmada na área de geração, não autorizada genericamente nas configurações. A fonte empírica independente proíbe interpolação mesmo com região homogênea declarada. Restaurar padrões não desfaz revisões nem exclui históricos. O limite de correção ±30 cents, a âncora obrigatória, a proibição de extrapolação e as verificações de segurança continuam ativos.

<a name="ler-curva"></a>
## 4.5. Interpretar a prévia e inspecionar intervalos

O gráfico apresenta a correção em cents ao longo da ordem física do perfil. Não equivale a um espectro FFT.

| Símbolo / origem | Significado |
| --- | --- |
| Ponto preenchido | Correção calculada com evidência (ou âncora, conforme o contexto) |
| Ponto vazio | Frequência teórica, sem correção suportada |
| Quadrado | Interpolação limitada e consentida |
| Losango, no editor de versões | Correção manual |
| Traço cinza, no editor | Versão escolhida para comparação |
| Barras de sensibilidade | Variação condicional do resultado sob a análise disponível; não são intervalo de confiança calibrado |

Em **Inspecionar tecla e origens → Todos os pontos e origens**, confira tecla, frequência teórica, frequência proposta, Δ em cents e origem. Um ponto sem correção não prova que o instrumento precise de exatamente zero; significa que não foi aplicada uma correção suportada naquele ponto. Alterar a apresentação para **Curva total relativa ao temperamento igual** muda somente o referencial visual, quando há notas cromáticas e referência A4 compatíveis. Nesse modo, zero representa o igual, e não necessariamente a receita escolhida.

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

**Comparar os dois objetivos** calcula uma referência comparativa sem substituir a prévia original. Use para verificar o efeito de privilegiar a fidelidade à receita ou a coincidência acústica. **Avançado → Exportar prévia inicial (JSON)** preserva o resultado inicial; **Descartar prévia** abandona a prévia de trabalho. Antes de descartar, exporte dados que deseje manter e confira separadamente o histórico de revisões.

<a name="revisar-curva"></a>
## 4.6. Revisar, editar e aprovar experimentalmente

### 4. Revisar e guardar curvas

A prévia deve existir antes de começar uma revisão nova. Em **Versão em revisão**, escolha o resultado que deseja inspecionar. O editor conserva uma história de versões, permitindo comparar efeitos sem alterar a versão original. Uma versão importada pode estar somente em leitura até que as fontes e a base sejam revalidadas.

| Ação | Efeito |
| --- | --- |
| Revalidar fontes para editar | Tenta verificar as fontes, reproduzir o cálculo e habilitar edição de uma versão. Se não reproduzir o resultado, mantenha o histórico em leitura e gere nova prévia a partir do perfil. |
| Desfazer / versão anterior | Retorna à versão anterior disponível para inspeção |
| Restaurar prévia original | Retorna à raiz da prévia original, preservando a distinção entre versões |
| Aprovar revisão (opcional, Avançado) | Registra uma revisão experimental sem aplicar. No fluxo principal, essa operação é feita internamente ao pressionar Aplicar ao Afinador. |
| Aplicar ao Afinador | Botão principal abaixo do gráfico: aprova, guarda, revalida e aplica em uma operação, quando tudo estiver elegível. |

### Editar correções e proteções (Avançado — revisão)

1. Escolha uma **Tecla** com evidência suficiente no editor. Digite a **Correção fixa em cents** dentro de −30 a +30; acrescente um **Motivo** para rastreabilidade.
2. Pressione **Fixar e recalcular**. As outras correções são novamente calculadas sob as restrições. Não é simplesmente arrastar um ponto gráfico ou somar uma alteração a todas as frequências.
3. Use **Voltar ao cálculo automático** para remover a correção manual da tecla. A âncora não pode receber deslocamento diferente de zero; teclas sem evidência não podem ser usadas para inventar correções manuais.
4. Se quiser preservar um intervalo específico, escolha outra tecla em **Preservar o intervalo desta tecla com** e pressione **Proteger intervalo**. Use **Remover proteção individual** para retirar a restrição correspondente. A âncora e as proteções estritas têm prioridade. Restrições incompatíveis podem impedir a revisão.
5. Para investigar pesos, escolha estilo e objetivo, selecione **Família de intervalo** e **Multiplicador de peso (0,1 a 10)**. **Recalcular objetivo e peso** inicia nova otimização; o multiplicador atua sobre o peso-base do estilo escolhido. Ele não representa quantidade de cents. A caixa de proteção central mantém seu papel em Fidelidade. O editor também permite incluir terças maiores e menores e preservar terças próximas das puras.
6. Use **Cancelar revisão** se necessário. Em **Comparar versões e ver consequências musicais**, escolha uma versão compatível, outra tecla para o intervalo fundamental e uma relação de parciais para comparação. Observe as consequências antes de aprovar.

Não altere muitos pesos e correções simultaneamente durante um estudo. Registre o motivo das mudanças, compare com a prévia inicial e avalie se a relação melhorada foi obtida à custa de outras relações. Aprovação experimental significa revisão registrada para fins de estudo, não aplicação automática, homologação física ou garantia de qualidade.

<a name="historico-curva"></a>
## 4.7. Histórico local, exportação e compatibilidade

| Controle | Uso |
| --- | --- |
| Guardar histórico local (Avançado) | Operação opcional de gerenciamento; Aplicar ao Afinador já a executa automaticamente. |
| Abrir histórico local | Recupera versões guardadas |
| Abrir backup de versões (Avançado — histórico e armazenamento) | Carrega histórico AFC ou JSON validado |
| Exportar histórico (.afc) | Backup binário das versões e evidências de auditoria, sem áudio |
| Exportar histórico (JSON), em Avançado — revisão | Cópia estruturada para intercâmbio |
| Limpar histórico temporário | Remove o histórico de trabalho em memória; exporte dados importantes antes |
| Gerenciar espaço local → Excluir cópia local do histórico | Remove a cópia armazenada correspondente, após verificação/confirmação solicitada |

O histórico possui limites de 128 versões e 32 MiB. Não presuma que novas revisões sobrescrevam automaticamente as antigas. Em caso de limite, exporte o histórico e trabalhe com os conjuntos necessários. Uma colisão de ID ou erro de integridade não deve ser resolvido editando identificadores ou hashes. A lista de perfis se atualiza ao entrar; fontes alteradas podem invalidar a prévia. Revalide ou gere outra antes de editar/aplicar. O diagnóstico de desempenho fica no bloco unificado de cálculo, referência, arquivos e diagnóstico, dentro do Avançado no fim da ferramenta.

A receita, a referência, o mapa físico e as fontes formam parte do contexto do cálculo. Alterá-los pode tornar versões incompatíveis com nova edição ou comparação. Recupere a configuração musical original e verifique as fontes. O histórico ainda pode servir como documentação de estudo em modo de leitura.

<a name="aplicar-curva"></a>
### Aplicar experimentalmente uma curva ao Afinador

1. Abra **Curvas de afinação**, confira o instrumento, o objetivo e, quando necessário, o campo curto **Registro**, apenas se solicitado. Escolha **Gerar curva** e aguarde o gráfico aparecer. Dados insuficientes mantêm a aplicação indisponível.
2. Examine a forma geral da curva. Logo abaixo de **Aplicar ao Afinador**, abra **Intervalos que serão afetados** para consultar as relações musicais com evidência, agrupadas em quintas, quartas, terças, oitavas e outras famílias presentes. Cada linha apresenta as notas e a alteração do intervalo em cents (positiva: mais largo; negativa: mais estreito). A seção fica recolhida por padrão. Para resíduos, justificativas acústicas e auditoria completa, use **Avançado**.
3. Pressione **Aplicar ao Afinador**, logo abaixo do gráfico. O programa executa em sequência a aprovação da revisão experimental, a gravação no histórico local, a verificação de hashes e compatibilidade, a recuperação das fontes originais e a reprodução do cálculo. **Não aparecem janelas adicionais de confirmação.** Se houver problema, a curva não é ativada; leia a mensagem próxima ao botão.
4. Quando concluir, deverá aparecer **Curva ativa no Afinador** na própria ferramenta Curvas. Pelo menu, abra **Afinação** e confira o painel compacto **Correção instrumental** com o seletor à direita em **Correção ativa**, destacado em azul. Para voltar aos alvos teóricos, mova-o para **Sem correção**. Para religar a curva nesta visita, selecione **Correção ativa**: a revisão armazenada será revalidada. Em Curvas, o botão **Desligar correção** também encerra a aplicação atual.

**Gerar curva não equivale a aplicar.** A ativação só acontece depois de todas as verificações terem sido concluídas. Não é necessário aprovar e guardar manualmente para usar o fluxo principal. Para usuários avançados, essas operações continuam disponíveis separadamente em Avançado, assim como histórico AFC, exportação JSON, comparação de objetivos e revisões manuais.

A versão aplicada fica congelada: editar outra revisão não a substitui automaticamente. A aplicação é temporária, não volta ao reiniciar e pode ser invalidada por mudanças de base musical ou alterações nos dados de perfis/curvas. Teclas sem suporte, sem ligação à âncora ou fora do mapa permanecem teóricas. O Emissor começa com referência teórica mesmo quando a curva está aplicada; habilite **Seguir correção instrumental** ali somente se desejar (ver [5.1](#emitir)).

O recálculo tem limite de 60 segundos e pode ser cancelado ou invalidado por mudança de contexto. Se não surgir a indicação de **Curva ativa no Afinador**, a aplicação não foi confirmada; confira o motivo ao lado do botão antes de utilizar qualquer alvo. O aplicativo não emite recibo de homologação, e os campos científicos permanecem experimentais (`physicalValidation: pending`, `curveEligible: false`); não são uma autorização que possa ser obtida editando o JSON. A aplicação permite investigar as hipóteses do modelo de forma reversível, não certificar a afinação ou os limites seguros de tensão do instrumento.

<a name="ts-4"></a>
## 4.8. Solução de problemas — Curvas de afinação

| Sintoma | O que verificar |
| --- | --- |
| Perfil não aparece | Abra Avançado → Atualizar perfis; crie/importe o perfil em Instrumentos. Para estudo sem importar, abra backup JSON compatível. |
| Família não suportada | Outro exige Automático com ordens identificadas, Série harmônica ou Corda rígida e seleção explícita da fonte empírica independente. Exploratório e Componentes não harmônicos não geram curvas. |
| Existe descrição empírica, mas a curva não usa a sessão | Confira fonte escolhida, critérios de referência, tecla e identificação física, isolamento quando exigido e suporte na ordem 1 e pelo menos outra superior. |
| Registro do cravo ausente | Informe o registro único representado e use fontes da mesma altura soante; não misture registros. |
| Não há âncora/teclas candidatas | Confira sessões elegíveis, identidade da tecla, corda isolada, mapa e referência musical. |
| Dados insuficientes | Examine as fontes recusadas e meça novas teclas/cordas. Não autorize interpolações sem justificativa física. |
| Sessões parecem consistentes mas não são usadas | Verifique os parâmetros acústicos personalizados, família, modelo, confirmação da tecla e coerência das fontes. |
| Mais de uma corda medida | Selecione fonte representativa quando possível ou deixe a tecla sem correção. Não some cordas diferentes como se fossem uma. |
| Não permite gerar curva | Confira se há mapa físico, tecla de referência válida, perfil elegível e fontes compatíveis; veja as mensagens e Avançado. |
| Interpolação não aparece | Na fonte empírica independente é proibida. Nas demais, confirme região efetivamente homogênea e limites válidos; são necessários dados de suporte. Extrapolação não é permitida. |
| Gráfico tem lacunas ou pontos vazios | Indicam ausência de correção suportada ou filtro de apresentação; leia origens e tabelas. |
| Curva relativa ao igual indisponível | A disposição não permite aquela comparação cromática com A4; use referência ao temperamento base. |
| Correção manual recusada | Revise limite ±30, âncora, evidência da tecla e conflitos com proteções. |
| Cálculo ou revisão sem resposta | A operação possui prazo máximo e é encerrada em caso de expiração; uma prévia compatível já existente é preservada. Leia o aviso, confira as condições e tente novamente. |
| Revisão não recalcula | Verifique base musical, compatibilidade das fontes e restrições; aguarde/cancele cálculo ativo. |
| Backup abre apenas para leitura | Revalide as fontes. Se a reprodução não coincidir, preserve o histórico e gere nova prévia. |
| Não consegue aprovar | A revisão precisa ser completa, válida e auditável. Examine problemas da geração. |
| Cliquei em Gerar curva e o Afinador não mudou | Esperado: a geração apenas calcula. Pressione Aplicar ao Afinador abaixo do gráfico. |
| Aplicação recusada | Confira a mensagem sob Aplicar ao Afinador, as fontes locais, a base musical e o mapa; gere outra curva se o recálculo divergir. |
| Curva não reaparece ao reabrir | Esperado: a aplicação não persiste; gere ou carregue uma revisão compatível e pressione Aplicar ao Afinador novamente. |
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
4. A extensão padrão histórica vai de F1 a F7 (inclusive); **Avançado → Ampliar extensão (C0–B9)** amplia o catálogo, respeitando a disponibilidade de alvos do layout. Em EDOs, a referência pode ser um grau.
5. Selecione o **Tipo de som**, começando por **Senoidal — som puro**. Deixe o **Volume** baixo (o padrão é 20%).
6. Pressione **▶ Emitir nota**. Use **■ Parar som** para interromper a emissão. Ao sair da ferramenta, o aplicativo encerra o som.

O controle de volume regula o ganho, não uma intensidade acústica calibrada. Mesmo com 20%, um amplificador ou fone pode produzir níveis elevados. Mantenha volume moderado, especialmente com ondas ricas em componentes agudas. Em frequências extremas, a resposta do equipamento e Nyquist limitam o som realizável.

Quando uma curva estiver aplicada experimentalmente ao Afinador, aparece **Seguir correção instrumental** no Emissor, inicialmente desmarcado. Marque para usar o alvo instrumental na geração baseada na nota selecionada; desmarque para retornar à frequência teórica. O modo Espectro medido Original continua usando as frequências observadas e não é transposto pela curva. Sem curva aplicada o controle fica oculto. Sons reconstruídos não se tornam alvos do Afinador.

<a name="controles-emissor"></a>
## 5.2. Todos os parâmetros selecionáveis e opções de Avançado — Emissor

O Emissor é um sintetizador, não um tocador de WAV nem um microfone. Seus controles operacionais servem para escolher a frequência-base, a forma do som e os componentes, sem mudar as medidas instrumentais nem a receita do temperamento. **A emissão só começa com Emitir nota**, mesmo após alterar preferências.

### Controles principais

| Controle | Objetivo | Efeito ou limitação |
| --- | --- | --- |
| **Nota / ◀ Nota / Nota ▶** | Selecionar frequência musical e percorrer catálogo | Usa referência/temperamento atual; em EDO há graus numéricos. |
| **Notação científica / Helmholtz apresentada** | Reconhecer a identidade musical selecionada | A grafia não modifica a frequência. |
| **Tipo de som: Senoidal** | Ouvir uma frequência predominantemente pura | Melhor comparação inicial para alvos musicais. |
| **Triangular / Quadrada / Dente de serra** | Ouvir timbres com diferentes séries de harmônicos | Triangular e quadrada favorecem ímpares; dente de serra contém pares e ímpares. |
| **Série inarmônica (B)** | Ouvir parciais deslocados por rigidez sintética | B modifica sobretudo parciais superiores; a primeira frequência é ancorada na nota selecionada. |
| **Espectro medido** | Sintetizar frequências/parciais de uma observação ou consolidado | Não recria fase, transientes, ruído ou envoltória da fonte. |
| **Espectro personalizado** | Definir razões de frequências e amplitudes próprias | Sujeito a limites de 1–32 componentes, validade das linhas e Nyquist. |
| **B (adimensional)** | Controlar a inarmonicidade do modo Série inarmônica | 0–0,02; valor manual não deve ser rotulado como medição real. |
| **Usar B da medição selecionada** | Copiar B elegível da sessão/ataque escolhido | Não copia automaticamente ao selecionar; fonte inconclusiva, sem B ou fora de 0–0,02 é recusada. |
| **Origem da medição: Último resultado exibido / Perfil instrumental salvo** | Escolher a fonte de B ou espectro | Em perfis, exige banco e integridade; alteração das fontes pode pedir recarga. |
| **Carregar medições / Instrumento / Sessão / Execução** | Selecionar o registro a sintetizar | “Consolidado empírico” é uma síntese estatística e não substitui uma execução real. |
| **Editar componentes personalizados / Relações; dB** | Informar pares `relação;amplitude` por linha | Relação positiva maior que zero e até 128 e amplitude de −120 a 0 dB; a aplicação exige valores válidos e componentes reproduzíveis. |
| **Volume (%)** | Ajustar ganho do sintetizador | 20% é padrão de início; não corresponde a nível SPL calibrado. Use saída baixa. |
| **Emitir nota / Parar som** | Iniciar e encerrar a saída | Sair da ferramenta encerra a emissão; evite realimentação no microfone. |
| **Seguir correção instrumental** | Quando houver curva ativa, emitir com alvo corrigido se desejado | Oculto sem curva ativa, desmarcado por padrão; modo Original de espectro medido preserva frequências observadas. |

### Avançado → extensão, envelope, componentes e inspeção

| Parâmetro / controle | Padrão / opções | Objetivo e efeito |
| --- | --- | --- |
| **Ampliar extensão (C0–B9)** | Desmarcado; faixa inicial histórica F1–F7 | Permite selecionar registros extremos quando existentes no catálogo; não garante reprodução física pelo alto-falante. |
| **Envelope** | Contínuo (padrão) ou Ataque e decaimento | Contínuo soa até Parar; Ataque e decaimento encerra após duração definida. Não modela decaimento real medido. |
| **Duração (segundos)** | 3 s; 0,2–20 s, passo 0,1 | Usada no envelope temporário; não determina duração de uma gravação acústica. |
| **Quantidade de parciais** | 8; 1–32 | Limita componentes de Série inarmônica; somente frequências abaixo de Nyquist podem soar. |
| **Queda de amplitude (1/n^α)** | α = 1; 0–3, passo 0,1 | α maior torna parciais altos progressivamente mais fracos; 0 aproxima amplitudes não atenuadas antes da normalização. |
| **Reconstrução: Original · frequências observadas** | Padrão de Espectro medido | Preserva frequências da execução ou frequências reconstruídas do consolidado, mesmo que outra nota seja selecionada. |
| **Reconstrução: Transposta · preservar relações** | Alternativa de Espectro medido | Multiplica frequências para levar referência da fonte ao alvo musical, preservando razões. |
| **Reconstrução: Harmônica equivalente** | Somente se ordens forem válidas | Substitui componentes elegíveis por múltiplos inteiros da base comparável; não atribui ordem a sinos ou picos arbitrários. |
| **Pico de referência para transpor** | Aparece quando a fonte o exige | Escolhe componente medida que serve de referência; não inventa uma fundamental ausente. |
| **Inspecionar espectro sintético** | Recolhido por padrão | Exibe frequências, relações, níveis relativos e ganho pretendidos antes ou durante a reprodução. Não mede a resposta do dispositivo. |

A seleção de **Espectro medido** pode usar uma execução individual ou um consolidado empírico de perfil com suporte suficiente; este último precisa de P1 e ao menos outra ordem com pelo menos três ataques e 60% de cobertura. Não exige B elegível para síntese, mas também **não fornece B** para o botão de copiar coeficiente. O motor limita a 32 componentes e à Nyquist, com normalização de ganho. As Configurações a seguir definem os padrões para a próxima utilização; não salvam áudios.

<a name="cfg-5"></a>
## 5.3. Configurações do Emissor

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

## 5.4. Formas de onda e envelope

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

Em **Avançado → Envelope**, escolha **Contínuo** para sustentar o som até interromper ou **Ataque e decaimento** para uma emissão temporária de acordo com **Duração (segundos)** (0,2–20 s; padrão 3 s). O envelope é sintético e não recupera o transiente ou o decaimento particular de um instrumento medido. Ao mudar parâmetros durante emissão, observe o estado indicado e pare se necessário.

<a name="sintese"></a>
## 5.5. Série inarmônica: estudar o coeficiente B por audição

Escolha **Série inarmônica (B)**. Diferentemente da fórmula de ajuste acústico do [Capítulo 2](#coeficiente-b), aqui o primeiro parcial é ancorado na frequência da nota selecionada. O modelo de emissão é equivalente a:

`fₙ = n × f₁ × √[(1 + B × n²)/(1 + B)]`

Assim, alterar B conserva f₁ e desloca as componentes superiores. As amplitudes são sintéticas e seguem uma queda proporcional a `1/n^α`, antes da normalização de ganho.

| Campo | Padrão | Faixa e efeito |
| --- | ---: | --- |
| B (adimensional) | 0,00042 | 0–0,02; zero produz série idealmente harmônica |
| Quantidade de parciais (Avançado) | 8 | 1–32; componentes acima de Nyquist não são emitidas |
| Queda de amplitude (Avançado) (1/n^α) | 1 | 0–3; maior expoente enfraquece as componentes superiores |

### Experimento sugerido

Selecione Lá3 ou outra nota confortável. Mantenha quantidade e queda iguais; ouça primeiro B = 0 e, depois, B = 0,00042 ou outro valor permitido. Compare em volume baixo. Abra **Inspecionar espectro sintético** e observe quais frequências mudaram. Esse experimento isola uma propriedade do modelo; não pretende imitar integralmente o som de um piano.
**Usar B da medição selecionada** aproveita uma estimativa elegível fornecida pela medição escolhida, quando existente e compatível com os limites da síntese (0–0,02, independentemente do teto de 0,05 na análise de Outro). B ausente, inconclusivo ou não aplicável não deve ser substituído por um valor supostamente medido. É possível inserir valores manualmente para uma experiência teórica sem afirmar que representam o instrumento.
Em Série inarmônica, selecione **Origem da medição → Perfil instrumental salvo** ou **Último resultado exibido**. Use **Carregar medições** para atualizar as fontes e escolha instrumento, sessão e **B consolidado (provisório)** ou uma execução elegível quando disponíveis. O instrumento ativo é aproveitado quando compatível. Pressione **Usar B da medição selecionada**: a seleção sozinha não modifica B. A estimativa deve estar dentro dos limites da síntese (0–0,02, independentemente do teto de 0,05 na análise de Outro). O consolidado empírico de razões espectrais não é B consolidado. Não substitua B ausente por zero supostamente medido. Valores manuais são permitidos para experiências teóricas. Se a fonte for alterada ou removida, recarregue as medições antes de reaproveitá-la.

<a name="reconstrucao"></a>
## 5.6. Reconstruir um espectro medido

O aplicativo utiliza observações de uma execução ou, por escolha explícita, estatísticas empíricas de uma sessão multiataque arquivada. Não reproduz gravações WAV. A execução individual continua disponível para preservar suas características próprias.

1. Obtenha uma captura em [Aquisição e Análise](#cap-2) ou selecione um instrumento com sessão armazenada em [Instrumentos](#cap-3).
2. Abra Emissor pelo menu e selecione **Espectro medido**.
3. Escolha **Origem da medição**: **Último resultado exibido** ou **Perfil instrumental salvo**. Use **Carregar medições** para buscar as fontes.
4. Para perfil salvo, selecione **Instrumento**, **Sessão / nota / corda** e **Execução**. As opções dependem das medições verificadas e dos componentes utilizáveis.
5. Escolha **Avançado → Reconstrução** e confira a lista de componentes. Se o modo exigir uma referência modal, escolha o **Pico de referência para transpor**.
6. Ajuste o volume, pressione **Emitir nota** e pare após ouvir.

| Reconstrução | Frequências emitidas | Uso |
| --- | --- | --- |
| Original · frequências observadas | Frequências registradas da execução ou reconstruídas a partir da referência e razões medianas do consolidado | Ouvir uma aproximação do espectro tal como medido; mudar a nota selecionada não transpõe o original |
| Transposta · preservar relações | Frequências escaladas para a nota escolhida, mantendo proporções da fonte | Comparar estrutura em outro registro; sem fundamental atribuída, selecione pico de referência quando requerido |
| Harmônica equivalente | Componentes com ordem válida reorganizadas segundo múltiplos inteiros da mesma base | Comparar a estrutura harmônica ideal com o padrão observado/transposto compatível |

A versão harmônica equivalente só está disponível quando a fonte possui informação harmônica adequada. Para uma comparação controlada, o programa considera a mesma base, amplitudes e componentes reproduzíveis nos dois planos compatíveis; não se deve inventar uma fundamental ou ordens para um sino. Para séries harmônicas, a síntese seleciona parciais aceitos; em espectros modais/exploratórios, usa picos resolvidos provisoriamente, sem lhes atribuir ordens físicas. Parciais excluídos da revisão do perfil ficam de fora. Quando há mais de 32 componentes, o motor seleciona os de maior amplitude, respeitando a faixa reproduzível. O número de componentes também respeita limites de síntese e Nyquist.

A reconstrução não recupera fase original, ruído, ataque, modulações ou decaimentos reais. Um timbre reconstruído diferente do instrumento gravado não é necessariamente erro: o conjunto de frequências e magnitudes não determina toda a evolução temporal do som. Compare com o espectro sintético e não use a semelhança auditiva como prova do modelo físico.

<a name="sintese-empirica"></a>
### Consolidado empírico · síntese descritiva

1. Salve em Instrumentos uma sessão de Automático com ordens identificadas, Série harmônica ou Corda rígida, com múltiplos ataques da mesma fonte.
2. No Emissor, escolha **Espectro medido → Origem da medição → Perfil instrumental salvo** e carregue as medições.
3. Selecione instrumento e sessão; no seletor **Execução**, escolha **Consolidado empírico · síntese descritiva**, quando disponível.
4. Escolha o modo de reconstrução em Avançado, inspecione as componentes e emita em volume moderado.

O consolidado requer a ordem 1 e pelo menos uma superior com três observações ou mais e 60% de cobertura, conforme os filtros da caracterização. Utiliza razões e amplitudes relativas medianas dessas ordens, com referência na mediana dos primeiros parciais medidos admitidos. O modo Original reconstrói frequências a partir dessa referência; Transposta preserva as razões em relação ao alvo escolhido; Harmônica equivalente reorganiza as ordens em múltiplos inteiros quando compatível.

Não é preciso satisfazer todos os requisitos de curva nem possuir B válido. Essa origem não fornece B para **Usar B da medição selecionada**. Uma ordem ausente ou excluída não é inventada. O resultado descreve estatisticamente a estrutura espectral; não é uma gravação de um ataque real nem uma representação de toda a evolução temporal do som. Para ouvir uma execução específica, escolha-a diretamente no seletor.

<a name="personalizado"></a>
## 5.7. Construir um espectro personalizado

Escolha **Espectro personalizado** e abra **Editar componentes personalizados**. Cada linha contém a relação com a frequência-base e a amplitude em dB relativos, separadas por ponto e vírgula. Relações não precisam ser inteiras. Use número positivo para a relação e sinal de menos normal (`-`) para valores negativos. Por exemplo:

```text
1;0
2.01;-6
3.05;-12
4.12;-18
```

Para uma base de 220 Hz, esse exemplo define 220 Hz, 442,2 Hz, 671 Hz e 906,4 Hz. As magnitudes são relativas: −6 dB equivale aproximadamente à metade da amplitude (não metade da frequência). Não são níveis acústicos absolutos no ambiente.

Mude apenas uma linha de cada vez para estudar a contribuição de um componente. Aceita-se de 1 a 32 componentes personalizados, com relação maior que zero e até 128 e amplitude de −120 a 0 dB. Pontos ou vírgulas decimais são admitidos; linhas vazias e comentários iniciados por `#` são ignorados. Componentes calculados fora da faixa de 1 Hz até abaixo de Nyquist não são emitidos; se nenhum restar, a síntese é recusada. Confira as mensagens de validação se a entrada for recusada. O código normaliza ganhos para limitar a soma das amplitudes; aumentar a quantidade de componentes não aumenta incondicionalmente o volume total.

Em **Avançado → Inspecionar espectro sintético**, confira componente, frequência em Hz, dB relativos e ganho normalizado. Antes de iniciar áudio, a prévia pode usar 48 kHz; a emissão real respeita a taxa de amostragem do contexto de áudio aberto. O gráfico/tabela descreve o sinal que o motor pretende sintetizar, não mede a resposta física do alto-falante.

<a name="ts-5"></a>
## 5.8. Solução de problemas — Emissor de notas

| Sintoma | O que verificar |
| --- | --- |
| Sem som | Pressione Emitir nota explicitamente, confira volume do aplicativo/dispositivo, saída de áudio, estado do navegador e nota válida. Não precisa ativar microfone. |
| Som termina antes do esperado | Confira envelope e duração; sair do Emissor encerra a emissão. |
| Som permanece contínuo | Use Parar som ou escolha Ataque e decaimento para emissão temporária. |
| A frequência parece errada | Confira temperamento, referência, nota e oitava; no modo Original, a seleção de nota não modifica frequências observadas. |
| Nota extrema não aparece | Confira extensão ampliada, catálogo e layout atual; Nyquist e limites do motor ainda se aplicam. |
| B não pode ser usado | A fonte pode não possuir B elegível ou o valor pode estar fora dos limites de síntese. Escolha experiência manual, sem atribuí-la à medição. |
| Perfil/sessão não carrega | Confira banco, compatibilidade e integridade. Se necessário, selecione último resultado exibido na Análise acústica. |
| Consolidado empírico indisponível | Escolha uma sessão Automático com ordens identificadas, harmônica ou de corda rígida em perfil salvo, com a ordem 1 e pelo menos outra ordem com três ataques e cobertura de 60%. A captura individual não oferece esse consolidado. |
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
| AFP / AFS / AFC | Formatos binários de intercâmbio de perfil, sessão e histórico de curvas, respectivamente |
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
| Caracterização empírica | Descrição de razões e desvios por ordem medidos e consolidados, sem pressupor uma equação física de corda rígida |
| Cobertura por ordem | Fração dos ataques elegíveis e incluídos que forneceram observação admitida para uma ordem |
| MAD | Desvio absoluto mediano em relação à mediana; medida robusta de dispersão |
| RMS empírico | Raiz da média quadrática dos desvios medianos das ordens superiores com cobertura suficiente |
| Inarmonicidade | Desvio em relação a uma série ideal de múltiplos inteiros |
| Interpolação | Estimativa entre pontos com evidência, condicionada à homogeneidade da região |
| Janela | Trecho de áudio analisado; uma função de ponderação como Hann/Blackman modifica a distribuição espectral |
| Modelo acústico | Hipótese de interpretação: Automático (investigação de ordens),  corda rígida, série harmônica, componentes não harmônicos ou exploratório; não é sinônimo de família instrumental. |
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

Antes de limpar armazenamento, atualizar o arquivo local ou trocar de aparelho, exporte a biblioteca musical, os perfis, as sessões em andamento e os históricos de interesse, conforme aplicável. Confirme que as cópias foram gravadas. Não limpe o armazenamento como primeira medida de solução de problemas: isso pode apagar a única evidência.

Ao abrir um [relato de problema no GitHub](https://github.com/mv-pereira/Afinador/issues), inclua:

- Arquivo HTML utilizado, ferramenta, navegador, sistema operacional e tipo de dispositivo (quando conhecido).
- Família, modelo acústico e condição do instrumento, identidade física da fonte, nota, temperamento, frequência de referência e forma de produção do som, quando afetarem o resultado. Para curvas, informe também a fonte de parciais escolhida e a política de otimização.
- Passos para reproduzir, comportamento esperado, resultado observado e mensagem apresentada.
- Preferências diferentes do padrão, possibilidade de reproduzir após restaurá-las e efeito de mudar somente um parâmetro.
- Evidência apropriada: diagnóstico ZIP para problemas do detector convencional; AFS ou JSON de sessão para problemas de parciais/B; AFP ou AFC para falhas de organização ou curvas; JSON de desempenho para investigar duração de transferências e processamento; parâmetros e lista de componentes para síntese. Uma captura de tela real da interface ajuda a localizar o problema.

Revise os arquivos antes de compartilhar. Um WAV pode conter vozes, sons do ambiente e informações privadas; os JSONs podem incluir nomes de instrumento, observações e contexto técnico. A captura de áudio é opcional no diagnóstico e não é necessária para todo relato.

## Homologação pendente em dispositivo real

As verificações computacionais incluem DSP com sinais sintéticos, Workers e WASM no Chromium, testes controlados de áudio e persistência, decodificação de AFP sintético, gráficos, disposição física, EDO e geração de curvas. Isso **não** substitui homologação integral de persistência em IndexedDB nativo, transferências AFP/AFS/AFC, instalação/atualização offline da PWA, microfone e instrumento físicos ou aplicação acústica de curvas. Há testes de uso com instrumentos reais, mas eles não substituem a validação metrológica ou a homologação abrangente em diferentes aparelhos. Faça backups AFP e AFC e utilize um perfil descartável para testar transições 12/13/14 no aparelho.

## Limites de interpretação e validação

Os cálculos do projeto foram submetidos a testes computacionais, incluindo regressões de detectores, análises, configurações, importações e síntese. Isso não é homologação física para todos os instrumentos, navegadores e microfones. A precisão depende da cadeia de captação, do sinal, do modelo e das configurações. Não há garantia de exatidão universal em cents, de incerteza calibrada de B ou de correções instrumentais apropriadas para uso real. A possibilidade de aplicar uma curva experimental aos alvos não altera esse limite científico. Consulte o [README](README.md) para os fundamentos, créditos, arquitetura, condições de compatibilidade e licença.

[Voltar ao sumário](#sumario) · [Abrir o Afinador](https://mv-pereira.github.io/Afinador/)
