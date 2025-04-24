
def translator(sequence):
    codons = {
    'AUG' : "Methionine",
    'UGA' : "Stop codon",
    'UGG' : "Tryptophan",
    'GCU' : "Alanine",
    'GAA' : "Glutamic acid",
    'CAG' : "Glutamine",
    'UUU' : "Phenylalanine",
    'UAC' : "Tyrosine",
    'AGA' : "Arginine"
    }

    sequence = sequence.upper()
    protein = codons[sequence]
    return protein

print(translator('Aug'))



def calculator(x_username, slack_username) :
    x_username = x_username.upper()
    slack_username = slack_username.upper()

    if len(x_username) < len(slack_username):
        difference = len(slack_username) - len(x_username)
        x_username = x_username + " " * difference
    elif len(slack_username) < len(x_username) :
        difference = len(x_username) - len(slack_username)
        slack_username = slack_username + " " * difference

    hamming_distance = 0
    character = []
    second_character = []

    #print(x_username, slack_username)
    for charac in x_username :
        character.extend([charac])
    for second_charac in slack_username :
        second_character.extend([second_charac])
    for counter in range(len(character)) :
        if character[counter] != second_character[counter] :
            hamming_distance += 1
    return hamming_distance


print(calculator("gbolxhan", "Gbolahan"))


def simulate_population_growth(initial_population, growth_rate):
   # population = initial_population
    population = initial_population * growth_rate
    return population
simulate_population_growth(100, 1.05)

