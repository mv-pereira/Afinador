# Afinador — Oficina Pernambuco

Afinador musical para navegador, com **identificação de frequência em tempo real**, **espectro FFT**, **círculo de quintas editável** e comparação entre quatro métodos de detecção: **YIN + FFT**, **pYIN**, **SWIPE'** e **Pico**. Inclui temperamentos, gerador de notas, configurações técnicas, dois temas visuais e um monitor opcional de diagnóstico.

O projeto é um aplicativo de afinação e experimentação acústica — **não** uma página institucional. A interface e as explicações estão em português do Brasil.

> **Padrões ao abrir:** YIN + FFT adaptativo; FFT de **8.192 pontos**; tema **Claro — Marfim e carvão**; monitor oculto; gravação de áudio desativada; A4 **415,3 Hz** e temperamento **Pitagórico**. O acesso ao microfone depende de permissão do navegador e de um contexto seguro (normalmente HTTPS ou `localhost`).

## Índice

1. [Comece aqui](#1-comece-aqui)
2. [Recursos e mostradores](#2-recursos-e-mostradores)
3. [Métodos de detecção](#3-métodos-de-detecção)
4. [Pontos FFT: resolução e limites](#4-pontos-fft-resolução-e-limites)
5. [Referências musicais, temperamentos e círculo de quintas](#5-referências-musicais-temperamentos-e-círculo-de-quintas)
6. [Configurações avançadas](#6-configurações-avançadas)
7. [Salvar e restaurar configurações](#7-salvar-e-restaurar-configurações)
8. [Temas e identidade visual](#8-temas-e-identidade-visual)
9. [Ajuda rápida e Ajuda avançada](#9-ajuda-rápida-e-ajuda-avançada)
10. [Monitor de diagnóstico](#10-monitor-de-diagnóstico)
11. [Captura, JSON, WAV e ZIP](#11-captura-json-wav-e-zip)
12. [Formato do diagnóstico](#12-formato-do-diagnóstico)
13. [Privacidade e segurança](#13-privacidade-e-segurança)
14. [Arquitetura técnica](#14-arquitetura-técnica)
15. [Compatibilidade e limitações](#15-compatibilidade-e-limitações)
16. [Solução de problemas](#16-solução-de-problemas)
17. [Desenvolvimento e testes](#17-desenvolvimento-e-testes)
18. [Organização, evolução e manutenção](#18-organização-evolução-e-manutenção)
19. [Créditos e licenças](#19-créditos-e-licenças)

## 1. Comece aqui

1. Abra o `index.html` **publicado sob HTTPS** ou servido localmente em `http://localhost` em um navegador compatível.
2. Toque em **Ativar microfone** e autorize a captura quando o navegador solicitar.
3. Toque **uma nota sustentada por vez**, em ambiente relativamente silencioso.
4. Observe a **nota**, a **frequência estimada em Hz** e o **desvio em cents**. Aproximar-se de **0 cent** indica aproximação da afinação musical escolhida.
5. Ajuste, se necessário, o **Lá de referência (A4)** e o **temperamento**, na barra inferior.
6. Use **Parar microfone** ao terminar.

O aplicativo não oferece uma URL de hospedagem no HTML. Se houver uma implantação pública, adicione ao repositório seu **endereço verificado**; não há endereço presumido neste documento.

## 2. Recursos e mostradores

| Recurso | O que faz |
|---|---|
| Automático / Nota fixa | Detecta a nota próxima ou compara com a nota-alvo escolhida por semitons. |
| Visor de nota | Mostra a notação científica com equivalente de Helmholtz menor no canto; toque para inverter o destaque. É apenas apresentação. |
| Frequência e escala de cents | Exibem a medição e seu desvio em relação à referência/nota-alvo. |
| Espectro FFT | Mostra a distribuição espectral e marcadores de frequência e, no modo Nota fixa, de referência. |
| Zoom na nota-alvo | Amplia o espectro perto da nota-alvo (±100 cents), sem alterar a FFT analisada. |
| Círculo de quintas | Exibe e permite editar quintas; tabelas mostram ajustes de comas e intervalos. |
| A4 e temperamento | Mudam as frequências musicais de referência. |
| Gerador de notas | Emite ondas selecionáveis, com volume e extensão de notas C0–B9, usando a afinação configurada. |
| Métodos | Alterna entre YIN + FFT, pYIN, SWIPE' e Pico, mantendo **um detector ativo por quadro**. |
| Diagnóstico | Monitor ao vivo, registro de decisões e exportação local mediante ação explícita. |

**Frequência exibida não é necessariamente a frequência fundamental física**: a detecção depende do timbre, ruído, níveis harmônicos, qualidade de captura e decisões de confiança do método.

## 3. Métodos de detecção

### YIN + FFT — padrão

O YIN estima periodicidade na forma de onda usando uma função de diferença cumulativamente normalizada (**CMNDF**). A análise FFT auxilia na validação harmônica, na correção condicional de oitavas e no refinamento da frequência quando existe suporte espectral suficiente. A versão atual usa refinamento **adaptativo para notas abaixo de 350 Hz** e conserva o refinamento mais restrito nas frequências superiores.

**Não existe opção para utilizar YIN puro (vanilla), desativar a FFT ou selecionar uma estratégia diferente de refinamento.** Ajustar o limiar CMNDF não altera essa arquitetura.

### pYIN

Método probabilístico com múltiplas candidatas e acompanhamento temporal por **Viterbi causal**. Os padrões são 100 limiares com distribuição **Beta(2, 18)**. O acompanhamento temporal pode reduzir oscilações e atrasar certas transições repentinas. O peso contextual e a confirmação de saltos de oitava são configuráveis dentro de limites.

### SWIPE'

Detector de altura baseado em **saliência harmônica**, com várias janelas FFT. Usa a infraestrutura PFFFT/WebAssembly e é mais exigente em cálculo. Se o motor necessário não estiver disponível, o aplicativo sinaliza a indisponibilidade; não substitui silenciosamente SWIPE' por um método equivalente improvisado.

### Pico

Exibe a frequência do **componente mais intenso do espectro**. É útil para investigar componentes dominantes, mas um harmônico pode ser mais intenso do que a fundamental: **Pico não garante a fundamental**. A interface apresenta um aviso em vermelho claro ao selecioná-lo.

**Observação sobre filtros:** em leitura **Bruta**, não há suavização visual temporal adicional, mas o pYIN continua usando seu próprio rastreamento probabilístico; não confundir esses dois procedimentos.

## 4. Pontos FFT: resolução e limites

Em **Configurações → Geral e desempenho → Pontos FFT**:

| Resolução | Pontos da FFT | Bins analisados | Duração nominal a 48 kHz |
|---|---:|---:|---:|
| Rápida | 4.096 | 2.048 | ≈85 ms |
| **Padrão** | **8.192** | **4.096** | **≈171 ms** |
| Alta | 16.384 | 8.192 | ≈341 ms |
| Máxima | 32.768 | 16.384 | ≈683 ms |

A separação entre bins é **Δf = taxa de amostragem ÷ pontos FFT**, em Hz. Mais pontos tendem a fornecer uma grade espectral mais fina, com maior exigência de amostras, memória e processamento. Isso **não é uma garantia de maior precisão em cents** e a duração nominal de uma janela **não é a latência total do aplicativo**.

A resolução pode ser trocada com o microfone ligado. Ela atua na FFT principal e no refinamento do YIN; a janela temporal adaptativa YIN/pYIN e as múltiplas janelas do SWIPE' têm regras próprias. FFT de 4.096 pontos pode ser pouco adequada a sinais extremamente graves em taxas de amostragem muito altas.

## 5. Referências musicais, temperamentos e círculo de quintas

- **Lá (A4) inicial:** 415,3 Hz, ajustável no rodapé.
- **Temperamento inicial:** Sistema Pitagórico. O menu permite selecionar os sistemas efetivamente oferecidos pelo aplicativo.
- **Círculo de quintas:** cada quinta pode receber ajustes em frações de **coma sintônico ou pitagórico**. Tabelas mostram os valores resultantes; o comportamento dos pares enarmônicos segue os controles de nomenclatura.
- **Zerar ajustes:** restaura o preset **musical** corrente, não as preferências técnicas.
- **Nota fixa:** permite subir/descer a nota-alvo por semitons. Faixas fora da capacidade nominal do detector podem ter leitura inconclusiva.
- **Emissor:** utiliza o mapa de frequências calculado para o temperamento e o A4 ativos. Use volume moderado, principalmente com fones.

Os cálculos de desvio utilizam relações logarítmicas: `cents = 1200 × log2(frequência medida / frequência de referência)`.

## 6. Configurações avançadas

O painel **Configurações** é expansível. Seções técnicas internas permitem regular o que cada método realmente oferece; limites de entrada são aplicados para evitar parâmetros inválidos.

| Grupo / ajuste | Padrão | Intervalo e efeito |
|---|---|---|
| Geral — FFT | **8.192 pontos** | 4.096 / 8.192 / 16.384 / 32.768. |
| Geral — gráfico | **2.000 Hz** | Limita a escala visível, sem alterar a identificação acústica. |
| Geral — leitura | **Bruta** | Filtrada é alternativa temporal; seu valor inicial é **70%**, configurável de 0–95%. |
| Geral — desempenho | **Automático** | Alternativa Econômico, para reduzir consumo. |
| Geral — enarmonia | **Sol#** | Alternativa Lab, apenas nomenclatura conforme o contexto. |
| YIN + FFT — CMNDF | **0,17** | 0,05–0,26. |
| YIN + FFT — janela temporal | **Automática** | Informativa; não há controle manual da janela ou do modo vanilla. |
| pYIN — número de limiares | **100** | 20–200, passo 10. |
| pYIN — Beta α / β | **2 / 18** | α: 0,5–10; β: 1–40. |
| pYIN — confirmação de oitava | **2 quadros** | 1–5. |
| pYIN — peso contextual de oitava | **0,72** | 0–0,95. |
| SWIPE' — saliência mínima | **0,20** | 0,05–0,50. |
| Diagnóstico — mostrar monitor | **Não** | Exibe/oculta os valores em tempo real. |
| Tema (botão circular ao lado de Ajuda) | **Claro** | Alternativa Escuro; integração ao perfil salvo. |

**Ajustes de algoritmo afetam a detecção.** Valores válidos, mas extremos, podem reduzir a estabilidade ou produzir mais rejeições. O filtro Filtrada modifica a apresentação, não substitui os métodos YIN, pYIN ou SWIPE'.

## 7. Salvar e restaurar configurações

1. Modifique as preferências técnicas em **Configurações** e, se desejar, o tema no botão circular ao lado de **Ajuda**: o efeito é imediato na sessão.
2. Toque em **Salvar configurações** para gravá-las no `localStorage` deste navegador/origem.
3. Ao abrir novamente a mesma origem, os valores salvos são recuperados, se o armazenamento estiver disponível.
4. Toque em **Restaurar padrões** para voltar às preferências técnicas originais e limpar o perfil salvo.

**Restaurar padrões não redefine A4, temperamento, nota-alvo ou quintas editadas.** Para os ajustes musicais do círculo, use **Zerar ajustes**. Limpar os dados de um site no navegador pode apagar as preferências técnicas, independentemente desses botões.

## 8. Temas e identidade visual

| Tema | Aparência | Papel |
|---|---|---|
| **Claro — Marfim e carvão** | Marfim, carvão e verde mineral discreto; baseado na proposta visual 04. | **Padrão** |
| Escuro — Grafite monocromático | Preto/grafite e cinzas; baseado na proposta visual 01. | Alternativa |

O tema é alternado pelo **pequeno botão circular imediatamente à direita de Ajuda**, na barra superior de ações. O círculo representa **o tema de destino**, não o atual: no tema claro, ele é **grafite escuro** (toque para ativar o escuro); no tema escuro, ele é **marfim claro** (toque para voltar ao claro). A seção Aparência foi removida das Configurações. A troca adapta números, botões, FFT, círculo, monitor e configurações **imediatamente, sem reiniciar o microfone ou alterar cálculos**. Para manter a escolha após reabrir, use **Configurações → Salvar configurações**; **Restaurar padrões** devolve o tema claro. A identidade visual incorpora a logo Oficina Pernambuco discretamente no cabeçalho.

## 9. Ajuda rápida e Ajuda avançada

O botão **Ajuda**, ao lado dos controles principais, oferece **somente instruções breves**: iniciar microfone, interpretar nota/Hz/cents, modos, A4, métodos e problemas comuns.

Dentro dele, expanda **Ajuda avançada** para consultar oito capítulos: leitura e referências, métodos, FFT, configurações, diagnóstico, aparência, glossário e solução de problemas/privacidade. Os capítulos têm controles próprios de expansão. Fechar a Ajuda, abrir Configurações, começar a captura ou reabrir a página deixa a ajuda avançada **recolhida novamente**. Pressionar **Esc** ou o botão **Fechar** encerra a ajuda. A consulta não inicia gravações e não modifica a afinação.

## 10. Monitor de diagnóstico

Ative **Configurações → Diagnóstico → Exibir monitor de diagnóstico**. O monitor é **oculto por padrão** e, quando ativado, aparece **imediatamente abaixo do espectro FFT e acima do círculo de quintas**. Ele acompanha apenas o método selecionado, sem executar detectores extras. A interface dos números atualiza-se aproximadamente a cada **250 ms**; o registro de uma sessão mantém cada quadro recebido.

É possível observar frequência candidata, frequência do detector, leitura apresentada, nota/cents, nível RMS, resolução FFT, estimativas de custo do Worker e informações específicas de cada método. Os botões e cartões do monitor são compactos para reduzir a altura ocupada, sem alterar os controles principais do aplicativo. Os nomes completos de Iniciar e Parar permanecem disponíveis para tecnologias assistivas. Valores ausentes significam informação indisponível, não necessariamente zero. O monitor apresenta estimativas e decisões computacionais; não é uma medida direta da verdade física do sinal.

## 11. Captura, JSON, WAV e ZIP

1. Ative o microfone e, se desejar, o monitor.
2. Opcionalmente, marque **Incluir áudio WAV**; a caixa inicia **desmarcada** e só pode ser usada quando a infraestrutura AudioWorklet está disponível.
3. Toque no botão compacto **Iniciar · 20 s** e toque notas durante a contagem regressiva exibida no cabeçalho do monitor.
4. A sessão encerra automaticamente após 20 segundos ou pelo botão compacto **Parar** (interromper diagnóstico). Os limites de quadros/memória também podem encerrar a captura com segurança.
5. Toque em **Exportar ZIP** para produzir localmente o arquivo do diagnóstico.

O ZIP utiliza entradas sem compressão (**STORE**) e contém sempre `diagnostico.json`. Contém `audio.wav` **apenas se a opção foi solicitada e a captura PCM contínua foi considerada íntegra**. A gravação é mono e o WAV é PCM 16 bits. O JSON serve para investigar decisões; o WAV, para reexecutar análises sobre o sinal recebido. Não são armazenadas FFTs integrais a cada quadro por padrão.

O aplicativo **não envia automaticamente arquivos ou telemetria**. Exportar um arquivo e compartilhá-lo posteriormente são ações distintas e voluntárias.

## 12. Formato do diagnóstico

A exportação utiliza `diagnosticSchemaVersion: 1`. O JSON tem os campos principais:

| Campo | Conteúdo |
|---|---|
| `application` | Nome e identificador da versão do aplicativo. |
| `capture` | Instantes, duração solicitada/real, motivo do encerramento, contagens e integridade opcional do áudio. |
| `environment` | Navegador/OS identificáveis, configurações reais e solicitadas de áudio, capacidades WebAssembly/SIMD/AudioWorklet. |
| `settings` | Método ativo, pontos FFT, preferências técnicas e afinação musical da sessão. |
| `summary` | Contagens, notas identificadas, frequências extrema e estatísticas dos quadros. |
| `events` | Histórico de ações/alterações importantes. |
| `frames` | Um objeto por análise recebida, incluindo estimativas, decisões, método e duração. |

Exemplo **esquemático** (não representa valores medidos):

```json
{
  "diagnosticSchemaVersion": 1,
  "application": { "name": "Afinador — Oficina Pernambuco", "version": "mudancas-1-a-6" },
  "capture": { "durationRequestedMs": 20000, "includesAudio": false, "framesRecorded": 1 },
  "environment": { "capabilities": { "webAssembly": true, "audioWorklet": false } },
  "settings": { "algorithm": "yin", "fftSize": 8192 },
  "summary": { "framesRecorded": 1 },
  "events": [],
  "frames": [{ "frameId": 1, "algorithm": "yin", "stagesHz": { "detectorOutput": 220.0, "displayed": 220.0 }, "decision": { "state": "accepted", "reason": "candidate_selected" } }]
}
```

O exportador real inclui outros campos; alguns são `null` quando não suportados ou indisponíveis. O valor `accepted` descreve a decisão daquele quadro, não certifica precisão absoluta. Uma frequência candidata pode ser rejeitada antes da apresentação, e uma transição Viterbi pode aguardar confirmação. Para comparar algoritmos entre versões, o áudio opcional é mais informativo do que apenas os espectros já transformados.

### Dados do dispositivo e limites de identificação

O navegador pode fornecer nome/versão estimados do sistema, categoria do dispositivo, núcleos lógicos, memória estimada, taxa de amostragem e configurações efetivas de captura. Ele **normalmente não expõe** modelo exato do chip, driver de áudio ou versão exata de todos os componentes. O diagnóstico não busca IMEI, MAC, IP, localização nem identificadores persistentes.

## 13. Privacidade e segurança

- O acesso ao **microfone** requer permissão do navegador e só é solicitado ao iniciar a função.
- Processamento e arquivos são gerados **localmente**, sem envio automático do áudio ou diagnóstico a servidores.
- O aplicativo não realiza varreduras de arquivos, rede ou aplicativos instalados e não consulta localização, IP ou identificadores de hardware persistentes.
- A opção **Incluir áudio WAV** é voluntária e desativada inicialmente. **Áudio pode conter conversas e informações sensíveis**; ouça/revise antes de compartilhar.
- Os registros JSON também podem conter informações técnicas sobre dispositivo e ambiente. Não se deve pressupor anonimato completo.
- As configurações salvas em `localStorage` e as exportações ZIP são mecanismos distintos; salvar preferências não inicia nem arquiva diagnósticos.
- APIs do navegador e políticas de permissão variam entre ambientes. O uso de funções convencionais não garante classificação idêntica por todos os sistemas de proteção.

## 14. Arquitetura técnica

O `index.html` é **autocontido** para seu código de aplicação, estilos, marca e núcleos DSP embutidos. Uma descrição simplificada do fluxo é:

```text
Microfone / MediaStream
       │
 Web Audio API ────────► AudioWorklet PCM opcional (diagnóstico WAV)
       │
 AnalyserNode + buffers temporais
       │
 Worker DSP (mensagens com sessão/geração/quadro)
       ├── YIN + refinamento FFT
       ├── pYIN + rastreamento Viterbi causal
       ├── SWIPE' multijanela (quando PFFFT disponível)
       ├── Pico do espectro
       └── PFFFT WASM SIMD/escalar ou FFT nativa de fallback
       │
 Resultado, confiança, espectro e metadados
       │
 Mostrador / escala de cents / canvas FFT / círculo / monitor
```

O **Worker dedicado** evita executar a maior parte do cálculo FFT na thread de interface. A infraestrutura WASM tem variantes SIMD e escalar embutidas; o código também oferece um caminho de fallback de FFT nativa. O SWIPE' depende especificamente da infraestrutura adequada, não de uma aproximação pela FFT nativa. O **AudioWorklet** é usado **somente quando o WAV opcional é solicitado**, para obter uma sequência contínua de amostras, sem remontar buffers sobrepostos do `AnalyserNode`.

O motor pode variar conforme navegador, permissões e recursos disponíveis. Ações sobre configurações relevantes reinicializam os estados necessários dos detectores; selecionar tema/abrir ajuda não deve gerar frames DSP adicionais.

## 15. Compatibilidade e limitações

- A captura de microfone costuma exigir **origem segura** (`https://` ou `http://localhost`) e permissão explícita.
- `file://` pode não suportar Worker, WASM, AudioWorklet ou permissões da mesma maneira entre navegadores.
- O PFFFT SIMD depende de suporte de WebAssembly SIMD; o modo escalar/fallback pode ter desempenho distinto.
- Gravação de WAV requer AudioWorklet no contexto ativo; JSON continua disponível onde o monitor e o Worker funcionam.
- O desempenho real depende de CPU, taxa de amostragem, bateria/gestão térmica e tamanho de FFT. Resoluções maiores e SWIPE' podem aumentar consumo e atraso.
- Microfones podem aplicar redução de ruído, ganho automático ou cancelamento de eco (conforme as configurações efetivamente aplicadas), afetando harmônicos.
- Sinais muito graves, curtos, fracos, polifônicos ou inarmônicos podem não gerar estimativas confiáveis; o método pode rejeitar a nota em vez de exibir uma frequência errada.

**Validação atual:** os testes automatizados deste pacote foram realizados em Chromium controlado e com áudio sintético. Não estabelecem compatibilidade universal nem substituem ensaios em Android/iOS reais, instrumentos reais e HTTPS com microfone físico. Em particular, a captura WAV por AudioWorklet requer essa validação de ponta a ponta.

## 16. Solução de problemas

| Sintoma | O que verificar |
|---|---|
| Microfone não inicia | Permissão do site, HTTPS/localhost, conflito com outro app, navegador atualizado. |
| Sem nota | Fonte sonora, intensidade, ruído, um som por vez, eventual saturação/eco. |
| Nota aparece uma oitava acima/abaixo | Harmônicos fortes; compare YIN + FFT/pYIN e analise o diagnóstico. Pico não representa obrigatoriamente a fundamental. |
| Leitura oscila | Sustente a nota, afaste ruído; experimente leitura Filtrada entendendo o maior tempo de resposta. |
| FFT vazia ou irregular | Verifique microfone, escala máxima e estado de preparação do Worker. |
| Lentidão | Use FFT de 8.192 ou 4.096 pontos; experimente Econômico e evite outras tarefas pesadas. |
| SWIPE' indisponível | Verifique suporte a WebAssembly/PFFFT; use YIN + FFT ou pYIN. |
| WAV não habilita | Verifique se AudioWorklet existe no contexto seguro e se o microfone está ativo. |
| ZIP não baixa | Permissões de download, espaço livre, navegador; exporte após a sessão terminar. |
| Preferências não persistem | Use Salvar configurações e verifique bloqueio/limpeza de armazenamento do site. |
| Falha JavaScript | Abra o console do navegador, registre o erro e, se possível, anexe o ZIP diagnóstico sem dados pessoais. |

## 17. Desenvolvimento e testes

O HTML é projetado para ser servido sem build obrigatório de frontend. Exemplo local, na pasta que contém `index.html`:

```bash
python3 -m http.server 8000
```

Abra `http://localhost:8000/` no **mesmo dispositivo**. Para acessar pelo celular usando outro computador, hospede a página em uma origem HTTPS: uma URL `http://IP-da-rede` em geral **não é equivalente ao `localhost` seguro** para permissões e AudioWorklet.

### Regressões recomendadas

1. Conferir carregamento e ausência de erros JavaScript.
2. Validar os quatro tamanhos FFT e seus bins: 2.048 / 4.096 / 8.192 / 16.384.
3. Reproduzir tons sintéticos e notas reais em YIN + FFT, pYIN e SWIPE' (quando disponível), incluindo transições de oitava; conferir Pico separadamente.
4. Alternar tema, FFT e parâmetros durante a captura; comparar saída antes/depois sem resets indevidos.
5. Testar A4/temperamentos, cent, nota fixa e emissor; verificar preservação dos ajustes musicais após Restaurar padrões.
6. Validar salvar/reabrir/restaurar em uma origem real e conferir que a Ajuda avançada sempre inicia recolhida.
7. Testar monitor e diagnóstico de 20 segundos, parada, limites e conteúdo `diagnostico.json`.
8. Testar WAV 16 bits e integridade dos dados, o ZIP e o fluxo **real** em Android/iOS com microfone físico.
9. Inspecionar layouts de 320, 360, 390, 412 e 768 px em ambos os temas e com os painéis abertos.

Os relatórios/testes de desenvolvimento podem ser arquivados separadamente do aplicativo. **Não presuma que scripts de teste de uma sessão anterior estejam versionados no repositório** se não forem adicionados explicitamente a ele.

## 18. Organização, evolução e manutenção

A entrega mínima para publicação é:

```text
index.html   # Aplicativo completo com DSP, estilos e ajuda incorporados
README.md    # Documentação deste aplicativo
```

O aplicativo acumulou seis conjuntos de alterações: **(1)** YIN FFT adaptativo e escolha dos pontos FFT; **(2)** nome YIN + FFT; **(3)** configurações técnicas com salvamento/restauração; **(4)** monitor e diagnósticos JSON/WAV opcionais; **(5)** temas Claro/Escuro; **(6)** Ajuda em dois níveis e documentação integral.

Antes de publicar, mantenha o README sincronizado com os controles e padrões implementados. Não anuncie o código como release estável em todos os celulares apenas com base em testes sintéticos. Se optar por versionamento semântico, defina a política e um changelog no repositório; **nenhuma tag de release é presumida aqui**.

## 19. Créditos e licenças

- **Oficina Pernambuco:** marca e identidade visual fornecidas para o projeto. O HTML contém a logo incorporada; reutilização fora do projeto requer autorização de seu titular.
- **YIN:** algoritmo de detecção de periodicidade descrito por Alain de Cheveigné e Hideki Kawahara (2002).
- **pYIN:** abordagem probabilística de estimação de altura associada ao trabalho de Matthias Mauch e Simon Dixon (2014); o app utiliza uma adaptação causal própria com Viterbi.
- **SWIPE':** método de Arturo Camacho (tese, 2007), com adaptação da implementação C de **Kyle Gorman (2009–2013)**. O HTML incorpora a declaração de licença **MIT** correspondente em `licencaSWIPEGormanMIT` e a fonte adaptada em `fonteSWIPEOriginalAdaptado`. **Não remova esse aviso.**
- **PFFFT (Pretty Fast FFT):** biblioteca associada a **Julien Pommier**, com antecedentes em FFTPACK de Paul Swarztrauber; o HTML contém adaptação WebAssembly embutida e declaração de atribuição no código de inicialização do Worker. As obrigações específicas da biblioteca devem ser revisadas na publicação ou redistribuição.
- **Web Audio API, Worker, WebAssembly e AudioWorklet:** APIs padronizadas dos navegadores, não serviços de upload.

**Licença do aplicativo:** o material HTML disponível para esta entrega não fornece uma licença global do projeto; portanto, este README **não inventa** uma licença de código aberto. Antes de substituir a documentação em um repositório público, confirme os créditos, autores, URLs e eventuais arquivos de licença originais. **O `README.md` anteriormente hospedado no repositório não estava disponível nos arquivos fornecidos nesta etapa**, de modo que seus avisos adicionais não puderam ser conferidos automaticamente.
