# Replication-ABM-Paper-Uninformed-Individuals-Promote-Democratic-Consensus-in-Animal-Groups

## Project Overview
This repository contains the code for one of my master's third semester projects for the course "Computational Modelling of Social Systems". In this course our task was to select a publication is based on an agent-based model (ABM) and write a review report about it. If feasible we should also try to replicate the publication or parts of it, yet that was not mandatory as many ABMs are too complicated to implement them within the course's time. I choose to review the publication:

- Couzin, I. D., Ioannou, C. C., Demirel, G., Gross, T., Torney, C. J., Hartnett, A., ... & Leonard, N. E. (2011). Uninformed individuals promote democratic consensus in animal groups. science, 334(6062), 1578-1580.

The publications centers around spatial model for collective-decision making processes. Due the course of my review report I tried to replicate Counzin et al's (2011) finding that “self-interested and strongly opinionated minorities can exert their influence on group movement decisions” and so their publication's Figure 1. The code of this repository gives this replication attempt.

Unfortunately Figure 3 does not compare well to Figure 1, both distributions differ greatly in their shape even when considering the fact that Figure 3 looks more angular as it was produced with less data points. Contrasting both figures the reproduced results show a fluctuating trend for the effect of the strength of the minority preference 𝜔2 on the majority target approaches rather than a decreasing. Most likely one of the stated obstacles or a mix thereof led to this mismatch in simulation results. Nevertheless, one must note that Figure 3 shows, although having a fluctuating nature, a general downward trend what can be interpreted in favor of Couzin et al. (2011) results. Having also an additional look at the number of groups splits for 𝜔2={0.3,0.325,0.35,0.375,0.4,0.425,0.45,0.475,0.5} per 100 replications the assumption hardens that something must have gone wrong due the model reimplementation process, as the numbers of 𝑠𝑝𝑙𝑖𝑡𝑠={83,88,85,77,71,78,76,78,85} are very high. One explanation for this result and the high splitting numbers could be that the maximal number of time steps for the group to approach the targets was set too low (fixed to 1000), unfortunately this limit must be set due the missing of more powerful computational resources.

## Objectives
- Replicate partly the results of Counzin et al's (2011) agent-based model for collective-decision making processes

## Key Findings
- The results could not be exactly replicated and only show a similiar general trend. This stems likely from the fact that
1. Precise parameter information necessary for exact replication was not given
2. The lack of computational power

## Technologies and Tools
- Simulation
- Agent-based Modelling

## Repository Contents
- `script`: Python program script that implements the ABM of that contains the the whole project's code including the data collection, preprocessing, and analysis.
- `report`: PDF of final report.

## Installation
To run the code in this repository, you'll need to have Python installed. Clone this repository and install the required packages using:

git clone [repository-link]
cd [repository-name]

## Contact
For any questions or further information, please contact:

Gina-Maria Angelina Unger - gina-unger@gmx.de
