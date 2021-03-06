"""
Knockout expression of a gene

Modifies:
	sim_data.process.transcription.rnaSynthProb
	sim_data.process.transcription.rnaExpression
	sim_data.process.transcription_regulation.recruitmentData

Expected variant indices (depends on length of sim_data.process.transcription.rnaData):
	0: control
	1-4558: gene index to knockout
"""

import numpy as np

CONTROL_OUTPUT = dict(
	shortName = "control",
	desc = "Control simulation"
	)

def geneKnockoutTotalIndices(sim_data):
	nGenes = sim_data.process.transcription.rnaData.fullArray().size
	nConditions = nGenes + 1
	return nConditions


def geneKnockout(sim_data, index):
	# Knocks-out genes in order

	nConditions = geneKnockoutTotalIndices(sim_data)

	if index % nConditions == 0:
		return CONTROL_OUTPUT, sim_data

	geneIndex = (index - 1) % nConditions

	factor = 0  # Knockout expression
	recruitment_mask = np.array([hi == geneIndex
		for hi in sim_data.process.transcription_regulation.recruitmentData['hI']])
	for synth_prob in sim_data.process.transcription.rnaSynthProb.values():
		synth_prob[geneIndex] *= factor
	for exp in sim_data.process.transcription.rnaExpression.values():
		exp[geneIndex] *= factor
	sim_data.process.transcription_regulation.recruitmentData['hV'][recruitment_mask] *= factor

	# Renormalize parameters
	for synth_prob in sim_data.process.transcription.rnaSynthProb.values():
		synth_prob /= synth_prob.sum()
	for exp in sim_data.process.transcription.rnaExpression.values():
		exp /= exp.sum()

	geneID = sim_data.process.transcription.rnaData["id"][geneIndex]

	return dict(
		shortName = "{}_KO".format(geneID),
		desc = "Complete knockout of {}.".format(geneID)
		), sim_data
