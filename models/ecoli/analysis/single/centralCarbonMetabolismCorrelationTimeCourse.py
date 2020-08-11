"""
@author: Morgan Paull
@organization: Covert Lab, Department of Bioengineering, Stanford University
@date: Created 4/29/2016
"""




import os
import pickle

import numpy as np
from matplotlib import pyplot as plt

from wholecell.io.tablereader import TableReader
from wholecell.utils import units

from models.ecoli.analysis.single.centralCarbonMetabolism import net_flux

from models.ecoli.processes.metabolism import COUNTS_UNITS, VOLUME_UNITS, TIME_UNITS
from wholecell.analysis.analysis_tools import exportFigure
from models.ecoli.analysis import singleAnalysisPlot

FLUX_UNITS = COUNTS_UNITS / VOLUME_UNITS / TIME_UNITS


class Plot(singleAnalysisPlot.SingleAnalysisPlot):
    def do_plot(self, simOutDir, plotOutDir, plotOutFileName, simDataFile, validationDataFile, metadata):
        if not os.path.isdir(simOutDir):
            raise NotADirectoryError("simOutDir does not currently exist as a directory")

        if not os.path.exists(plotOutDir):
            os.mkdir(plotOutDir)

        validation_data = pickle.load(open(validationDataFile, "rb"))
        sim_data = pickle.load(open(simDataFile, "rb"))

        cellDensity = sim_data.constants.cellDensity

        initialTime = TableReader(os.path.join(simOutDir, "Main")).readAttribute("initialTime")
        time = TableReader(os.path.join(simOutDir, "Main")).readColumn("time") - initialTime

        massListener = TableReader(os.path.join(simOutDir, "Mass"))
        cellMass = massListener.readColumn("cellMass") * units.fg
        dryMass = massListener.readColumn("dryMass") * units.fg
        massListener.close()

        fbaResults = TableReader(os.path.join(simOutDir, "FBAResults"))
        reactionIDs = np.array(fbaResults.readAttribute("reactionIDs"))
        reactionFluxes = (COUNTS_UNITS / VOLUME_UNITS / TIME_UNITS) * np.array(fbaResults.readColumn("reactionFluxes"))
        fbaResults.close()

        dryMassFracAverage = np.mean(dryMass / cellMass)

        toya_reactions = validation_data.reactionFlux.toya2010fluxes["reactionID"]
        toya_fluxes = FLUX_UNITS * np.array([(dryMassFracAverage * cellDensity * x).asNumber(FLUX_UNITS) for x in validation_data.reactionFlux.toya2010fluxes["reactionFlux"]])

        netFluxes = []
        for toyaReactionID in toya_reactions:
            fluxTimeCourse = net_flux(toyaReactionID, reactionIDs, reactionFluxes).asNumber(FLUX_UNITS).squeeze()
            netFluxes.append(fluxTimeCourse)

        trimmedReactions = FLUX_UNITS * np.array(netFluxes)

        corrCoefTimecourse = []
        for fluxes in trimmedReactions.asNumber(FLUX_UNITS).T:
            correlationCoefficient = np.corrcoef(fluxes, toya_fluxes.asNumber(FLUX_UNITS))[0,1]
            corrCoefTimecourse.append(correlationCoefficient)

        meanCorr = np.mean(np.array(corrCoefTimecourse)[~np.isnan(corrCoefTimecourse)])

        plt.figure()
        plt.plot(time / 60., corrCoefTimecourse)
        plt.axhline(y=meanCorr, color='r')
        plt.title("Measured vs. Simulated Central Carbon Fluxes")
        plt.text(.5*np.max(time / 60.),.95*meanCorr, "Mean = {:.2}".format(meanCorr), horizontalalignment="center")
        plt.xlabel("Time (min)")
        plt.ylabel("Pearson R")

        exportFigure(plt, plotOutDir, plotOutFileName, metadata)
        plt.close("all")


if __name__ == "__main__":
    Plot().cli()
