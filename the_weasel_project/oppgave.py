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
	"""
	Returner hvor mange av tegnene i strengen som er på riktig plass.
	"""
	correct = 0
	return correct


def mutate(copies):
	"""
	Ta en liste av kopier
	For hvert tegn i hver av kopiene, med en sannsynlighet på 5%, bytt tegnet med et annet tilfeldig tegn.
	"""
	return copies


def fittest(copies):
	"""
	Returner strengen med høyest fitness
	"""                      

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
