import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from utils import Sobol_per_structure, setupProblem, getSamples
from makeFigure6_ShortageDistns import plotSDC
from makeFigure7_VarianceDecomposition import plotSums

def makeFigureS10_VarianceDecomposition_User3():

    sns.set_style("white")
    
    designs = ['LHsamples_original_1000_AnnQonly','CMIPunscaled_SOWs','Paleo_SOWs','LHsamples_wider_1000_AnnQonly']
    nsamples = [1000,97,366,1000] # before removing those out of bounds
    titles = ['Box Around Historical','CMIP','Paleo','All-Encompassing']
    structure = '3704614'
    nrealizations = 10
    short_idx = np.arange(2,22,2)
    demand_idx = np.arange(1,21,2)
    
    colors = ["#de2d26", "#fb6a4a", "#3182bd", "#6baed6", "#a50f15", "#08519c", "#9e9ac8"]
    mu0 = plt.Rectangle((0,0), 1, 1, fc=colors[0], edgecolor='none')
    sigma0 = plt.Rectangle((0,0), 1, 1, fc=colors[1], edgecolor='none')
    mu1 = plt.Rectangle((0,0), 1, 1, fc=colors[2], edgecolor='none')
    sigma1 = plt.Rectangle((0,0), 1, 1, fc=colors[3], edgecolor='none')
    p00 = plt.Rectangle((0,0), 1, 1, fc=colors[4], edgecolor='none')
    p11 = plt.Rectangle((0,0), 1, 1, fc=colors[5], edgecolor='none')
    Interact = plt.Rectangle((0,0), 1, 1, fc=colors[6], edgecolor='none')
    
    # perform variance decomposition
    #for i, design in enumerate(designs):
    #    Sobol_per_structure(design, structure)
    
    # plot shotrage distributions
    fig = plt.figure()
    count = 1 # subplot counter
    
    # load historical shortage and demand data and convert acre-ft to m^3
    hist_short = np.loadtxt('../Simulation_outputs/' + structure + '_info_hist.txt')[:,2]*1233.48/1E6
    hist_demand = np.loadtxt('../Simulation_outputs/' + structure + '_info_hist.txt')[:,1]*1233.48/1E6
    # replace failed runs with np.nan (currently -999.9)
    hist_short[hist_short < 0] = np.nan
    for i, design in enumerate(designs):
        # find which samples are still in param_bounds after flipping misidentified wet and dry states
        param_bounds, param_names, params_no, problem = setupProblem(design)
        _, rows_to_keep = getSamples(design, params_no, param_bounds)
        nsamples[i] = len(rows_to_keep) # after removing those out of bounds after reclassification
        
        # load shortage data for this experimental design
        SYN = np.load('../Simulation_outputs/' + design + '/' + structure + '_info.npy')
        # extract columns for year shortage and demand and convert acre-ft to m^3
        SYN_short = SYN[:,short_idx,:]*1233.48/1E6
        SYN_demand = SYN[:,demand_idx,:]*1233.48/1E6
        # use just the samples within the experimental design
        SYN_short = SYN_short[:,:,rows_to_keep]
        SYN_demand = SYN_demand[:,:,rows_to_keep]
        # reshape into 12*nyears x nsamples*nrealizations
        SYN_short = SYN_short.reshape([np.shape(SYN_short)[0],np.shape(SYN_short)[1]*np.shape(SYN_short)[2]])
        SYN_demand = SYN_demand.reshape([np.shape(SYN_demand)[0],np.shape(SYN_demand)[1]*np.shape(SYN_demand)[2]])
        # replace failed runs with np.nan (currently -999.9)
        SYN_short[SYN_short < 0] = np.nan
        
        # plot shortage distribution
        ax = fig.add_subplot(2,4,count)
        handles, labels = plotSDC(ax, SYN_short, SYN_demand, hist_short, hist_demand, nsamples[i], nrealizations)
        
        # only put labels left column, make y ranges consistent, title experiment
        if count == 1:
            ax.tick_params(axis='y', labelsize=14)
            ax.set_ylabel('Annual Shortage\n(millions of m' + r'$^3$' + ')', fontsize=16)
        else:
            ax.tick_params(axis='y', labelleft='off')
            
        ax.set_title(titles[count-1],fontsize=16)
        ax.tick_params(axis='x',labelbottom='off')
            
        # iterature subplot counter
        count += 1
    
    # plot variance decomposition
    for design in designs:
        # load sensitivity indices
        S1_values = pd.read_csv('../Simulation_outputs/' + design + '/'+ structure + '_S1.csv')
        
        # plot shortage distribution
        ax = fig.add_subplot(2,4,count)
        plotSums(S1_values, ax, colors)
        
        ax.tick_params(axis='x',labelsize=14)
        
        if count == 5:
            ax.tick_params(axis='y',labelsize=14)
            ax.set_ylabel('Portion of\nVariance Explained', fontsize=16)
        else:
            ax.tick_params(axis='y', labelleft='off')
            
        # iterate subplot counter
        count += 1
    
    fig.set_size_inches([16,8])
    fig.subplots_adjust(bottom=0.22)
    fig.text(0.5, 0.15, 'Percentile of Shortage', ha='center', fontsize=16)
    fig.savefig('FigureS10_VarianceDecomposition_User3.pdf')
    fig.clf()

    return None