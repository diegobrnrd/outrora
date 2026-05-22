# Outrora - História do jogo
#
# Este arquivo separa o conteúdo (narrativa) da lógica de interface (Kivy/KivyMD).
# Assim fica mais fácil editar/expandir a história sem mexer na UI.

STORY_STATES = [
    {
        "pergunta": (
            "Durante um acampamento com amigos, uma noite que era para ser tranquila se transforma em um pesadelo."
            "\n\nAo despertar, você percebe que seus amigos desapareceram."
            "\n\nUm barulho perturbador ecoa na escuridão."
        ),
        "escolhas": ["Investigar Imediatamente", "Voltar a Dormir"],
    },
    {
        "pergunta": (
            "Saindo da barraca de acampamento com uma lanterna em punho, seu objetivo é alcançar uma cabana abandonada situada no coração da floresta."
            "\n\nHá uma suspeita de que seus amigos possam ter ido investigá-la sem você."
            "\n\nAo se deparar com uma bifurcação na floresta, surge a necessidade de escolher qual caminho seguir."
        ),
        "escolhas": ["Caminho Iluminado", "Atalho Sombrio"],
    },
    {
        "pergunta": (
            "Sob o manto da noite, uma presença ameaçadora se materializa nos cantos mais profundos de seus sonhos."
            "\n\nA escuridão te envolve, e risadas sussurrantes acompanham sua jornada além da consciência."
            "\n\nA confusão, silenciosa e implacável, te abraça enquanto você descansa, te levando para além do reino da lucidez."
        ),
        "escolhas": ["Tentar Novamente", "Fechar Jogo"],
    },
    {
        "pergunta": (
            "Conforme a trilha se estreita, você começa a sentir uma presença maligna ao seu redor."
            "\n\nParece que olhares invisíveis o acompanham entre as árvores."
        ),
        "escolhas": ["Ignorar e Continuar", "Retornar Rapidamente"],
    },
    {
        "pergunta": (
            "Ao ignorar os sussurros, a presença invisível se intensifica."
            "\n\nA escuridão, antes apenas percebida, se materializa em sombras assustadoras que o envolvem."
            "\n\nUm frio intenso preenche o ar, enquanto a voz sussurrante se transforma em risadas macabras."
            "\n\nVocê é envolvido por uma escuridão infinita, perdendo-se na confusão que se esconde entre as sombras."
        ),
        "escolhas": ["Tentar Novamente", "Fechar Jogo"],
    },
    {
        "pergunta": (
            "Ao retornar rapidamente pelo caminho iluminado, o trajeto agora é desconhecido."
            "\n\nSombras se movem à medida que a trilha se transforma em um labirinto assustador."
            "\n\nO ar fica pesado, e a voz sussurrante se torna um lamento triste."
            "\n\nVocê, incapaz de encontrar a saída, é consumido pela confusão do labirinto, sua lucidez desaparece como uma vela queimando até o fim."
        ),
        "escolhas": ["Tentar Novamente", "Fechar Jogo"],
    },
    {
        "pergunta": (
            "Enquanto avança pela escuridão, a luz vacilante da sua lanterna é a única companhia. "
            "\n\nDe repente, um filhote de urso-pardo emerge à sua frente, seus olhos curiosos refletem a luz."
        ),
        "escolhas": ["Acariciar o Filhote", "Correr"],
    },
    {
        "pergunta": (
            "Ao acariciar o filhote de urso-pardo, um rugido ensurdecedor rompe a noite, indicando a presença de um urso adulto enfurecido."
            "\n\nNo entanto, em vez do esperado ataque, o urso surpreendentemente envolve você em uma dança inusitada."
            "\n\nA confusão aumenta quando, de repente, o urso se transforma em uma jarra, depois em uma idosa e por fim em um bico-de-tamanco."
            "\n\nA realidade distorcida desafia a lógica, desencadeando uma vertigem mental insuportável."
            "\n\nIncapaz de lidar com a loucura que se desenrola diante dos seus olhos, sua mente sucumbe ao colapso,afundando em um abismo de confusão sem retorno."
        ),
        "escolhas": ["Tentar Novamente", "Fechar Jogo"],
    },
    {
        "pergunta": (
            "Desesperado, você corre pela escuridão; a luz da sua lanterna é insuficiente para tal ato."
            "\n\nVocê tropeça em galhos, esbarra em árvores, até que um impacto abrupto interrompe sua fuga, fazendo-o desmaiar."
            "\n\nQuando seus olhos se abrem novamente, a noite ainda domina o cenário."
            "\n\nAo seu lado, você nota um estranho totem em forma de um pombo obeso."
        ),
        "escolhas": ["Pegar o Totem", "Ignorar o Totem", "Tentar Quebrar o Totem"],
    },
    {
        "pergunta": (
            "Conforme você avança pela floresta, vislumbrando a cabana ao longe, a sensação de urgência cresce a cada passo."
            "\n\nA escuridão parece se intensificar, e a distância até a cabana parece inalterada."
            "\n\nSeguindo pela trilha principal, você se aproxima da cabana, cuja silhueta sombria se destaca contra o céu noturno."
            "\n\nSeus passos ecoam na quietude da floresta enquanto a cabana se torna mais palpável, e você está à beira de explorar seus segredos sombrios."
        ),
        "escolhas": ["Continuar"],
    },
    {
        "pergunta": (
            "Ao se aproximar da cabana, uma calmaria intensa toma conta do ambiente."
            "\n\nO murmúrio da floresta se desvanece, e até mesmo o vento parece reter qualquer movimento."
            "\n\nUma quietude densa paira no ar, criando uma atmosfera de serenidade quase familiar."
            "\n\nEssa tranquilidade peculiar provoca uma instigação momentânea, convidando-o a explorar o interior da cabana e descobrir o que ela esconde."
        ),
        "escolhas": ["Continuar"],
    },
    {
        "pergunta": (
            "Num piscar de olhos, a escuridão da noite se dissipa, dando lugar a uma aurora súbita."
            "\n\nO ambiente, antes envolto em sombras, é agora banhado por uma luz diurna reconfortante. "
            "\n\nO céu se transforma rapidamente de estrelado para um azul claro, como se a noite tivesse sido apenas um breve suspiro na passagem do tempo."
        ),
        "escolhas": ["Continuar"],
    },
    {
        "pergunta": (
            "Ao ficar a apenas três passos da porta da cabana, você é surpreendido por um barulho sutil vindo dos fundos."
        ),
        "escolhas": ["Investigar", "Ignorar"],
    },
    {"pergunta": "", "escolhas": ["Abrir Porta", "Bater na Porta", "Investigar o Barulho"]},
    {
        "pergunta": (
            "Você tenta girar a maçaneta para abrir a porta da frente. No entanto, uma resistência inexplicável frustra seus esforços."
            "\n\nA maçaneta permanece imóvel, como se algo do outro lado estivesse se opondo à sua entrada."
            "\n\nApesar de várias tentativas, a porta continua intransponível."
        ),
        "escolhas": ["Soltar Maçaneta"],
    },
    {
        "pergunta": (
            "Você bate três vezes na porta da cabana, mas um silêncio denso engole as batidas."
            "\n\nO som não reverbera na quietude noturna da floresta."
            "\n\nQuinze segundos se arrastam, e nenhum sinal de resposta."
            "\n\nDecidindo chamar pelos seus amigos, você se vê perplexo quando percebe que os nomes deles escapam de sua mente como sombras evasivas."
        ),
        "escolhas": ["Continuar"],
    },
    {
        "pergunta": (
            "Ao se dirigir para o fundo da cabana, uma descoberta inesperada surge diante de seus olhos. "
            "\n\nUma janela entreaberta revela uma fraca luminosidade no interior."
            "\n\nA escuridão circundante parece recuar da abertura, sugerindo uma possível entrada discreta."
            "\n\nUma brisa suave carrega murmúrios indefinidos que escapam pela janela, criando uma atmosfera de mistério."
        ),
        "escolhas": ["Entrar Pela Janela"],
    },
    {"pergunta": "Ao atravessar o limiar da cabana, você é envolvido por uma luminosidade fugaz.", "escolhas": ["Continuar"]},
    {
        "pergunta": (
            "Diante de seus olhos, surgem vislumbres de memórias há muito esquecidas: risos sob o luar, sombras de amizades perdidas e o calor reconfortante de momentos que parecem pertencer a outra vida."
        ),
        "escolhas": ["Continuar"],
    },
    {"pergunta": "Uma melodia distante ressoa, despertando emoções há muito adormecidas.", "escolhas": ["Continuar"]},
    {
        "pergunta": (
            "Nesse breve instante, o peso do desconhecido se dissipa temporariamente, e você se encontra imerso em um lampejo de clareza fugaz, porém impactante."
        ),
        "escolhas": ["Continuar"],
    },
    {
        "pergunta": (
            "No entanto, como uma estrela cadente que se desvanece no firmamento, essa lucidez efêmera desaparece rapidamente."
        ),
        "escolhas": ["Continuar"],
    },
    {"pergunta": "A cabana, que antes estava iluminada, é agora absorvida pela penumbra da incerteza.", "escolhas": ["Continuar"]},
    {
        "pergunta": (
            "As memórias escorrem por seus dedos como areia, deixando apenas a sensação de algo inatingível."
        ),
        "escolhas": ["Continuar"],
    },
    {
        "pergunta": (
            "Um silêncio melancólico preenche o espaço, enquanto você mergulha novamente na névoa de sua própria mente, envolvido em uma atmosfera de perda e saudade."
        ),
        "escolhas": ["Continuar"],
    },
]


# Tabela de transições: (estado_atual, texto_do_botao) -> proximo_estado
# Use None para indicar "fica" no mesmo estado e/ou ação especial.
TRANSITIONS = {
    (0, "Investigar Imediatamente"): 1,
    (0, "Voltar a Dormir"): 2,

    (1, "Caminho Iluminado"): 3,
    (1, "Atalho Sombrio"): 6,

    (2, "Tentar Novamente"): 0,
    (2, "Fechar Jogo"): "EXIT",

    (3, "Ignorar e Continuar"): 4,
    (3, "Retornar Rapidamente"): 5,

    (4, "Tentar Novamente"): 0,
    (4, "Fechar Jogo"): "EXIT",

    (5, "Tentar Novamente"): 0,
    (5, "Fechar Jogo"): "EXIT",

    (6, "Acariciar o Filhote"): 7,
    (6, "Correr"): 8,

    (7, "Tentar Novamente"): 0,
    (7, "Fechar Jogo"): "EXIT",

    (8, "Pegar o Totem"): 0,
    (8, "Ignorar o Totem"): 9,
    (8, "Tentar Quebrar o Totem"): 0,

    (9, "Continuar"): 10,
    (10, "Continuar"): 11,
    (11, "Continuar"): 12,

    (12, "Investigar"): 16,
    (12, "Ignorar"): 13,

    (13, "Abrir Porta"): 14,
    (13, "Bater na Porta"): 15,
    (13, "Investigar o Barulho"): 16,

    (14, "Soltar Maçaneta"): 13,

    (15, "Continuar"): 13,

    (16, "Entrar Pela Janela"): 17,

    (17, "Continuar"): 18,
    (18, "Continuar"): 19,
    (19, "Continuar"): 20,
    (20, "Continuar"): 21,
    (21, "Continuar"): 22,
    (22, "Continuar"): 23,
    (23, "Continuar"): 24,
    (24, "Continuar"): "CREDITS",
}
