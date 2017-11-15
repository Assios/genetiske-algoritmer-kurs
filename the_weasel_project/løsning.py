#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

"""
Oppgave:

1. Start med en tilfeldig streng på 28 tegn.
2. Lag 100 kopier av strengen.
3. For hvert tegn i hver av kopiene, bytt ut tegnet med et annet tilfeldig tegn med en sannsynlighet på 5%.
4. Sammenlign hver kopi med "METHINKS IT IS LIKE A WEASEL" og gi poeng basert på hvor mange tegn som er på riktig plass.
5. Stopp dersom en av kopiene har en perfekt score. Ellers gå til steg 2.
"""

characters = string.ascii_uppercase + " "

def random_string(n):
	return "".join(random.choice(characters) for _ in range(n))


def fitness(string, target):
    correct = 0
    for ch1, ch2 in zip(string, target):
			if ch1 == ch2:
				correct += 1
    return correct


def mutate(copies):
	for i in range(len(copies)):
		for j in range(len(copies[i])):
			if random.random() < 0.05:
				new_gene = characters[random.randint(0, len(characters)-1)]
				s = list(copies[i])
				s[j] = new_gene
				copies[i] = "".join(s)

	return copies


def fittest(copies, target):
    error = 0
    best_string = None

    for copy in copies:
        score = fitness(copy, target)
        if score > error:
            error = score
            best_string = copy                            

    return best_string     


def main():
	best_string = random_string(28)
	target_string = "METHINKS IT IS LIKE A WEASEL"

	while best_string != target_string:
		copies = [best_string for _ in range(100)]
		mutations = mutate(copies)
		best_string = fittest(mutations, target_string)
		print best_string

main()
