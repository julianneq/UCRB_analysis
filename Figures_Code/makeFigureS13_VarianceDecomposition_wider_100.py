import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from utils import Sobol_per_structure
from makeFigure7_VarianceDecomposition import plotSums

def makeFigureS13_VarianceDecomposition_wider_100():

    sns.set_style("white")
    
    designs = ['LHsamples_wider_1000_AnnQonly','LHsamples_wider_100_AnnQonly']
    structures = ['53_ADC022','7200645','3704614']
    
    colors = ["#de2d26", "#fb6a4a", "#3182bd", "#6baed6", "#a50f15", "#08519c", "#9e9ac8"]
    mu0 = plt.Rectangle((0,0), 1, 1, fc=colors[0], edgecolor='none')
    sigma0 = plt.Rectangle((0,0), 1, 1, fc=colors[1], edgecolor='none')
    mu1 = plt.Rectangle((0,0), 1, 1, fc=colors[2], edgecolor='none')
    sigma1 = plt.Rectangle((0,0), 1, 1, fc=colors[3], edgecolor='none')
    p00 = plt.Rectangle((0,0), 1, 1, fc=colors[4], edgecolor='none')
    p11 = plt.Rectangle((0,0), 1, 1, fc=colors[5], edgecolor='none')
    Interact = plt.Rectangle((0,0), 1, 1, fc=colors[6], edgecolor='none')
    
    # perform variance decomposition
    #for structure in structures:
    #    Sobol_per_structure('LHsamples_wider_100_AnnQonly', structure)
    
    # plot variance decomposition
    fig = plt.figure()
    count = 1 # subplot counter
    for design in designs:
        for i, structure in enumerate(structures):
            # load sensitivity indices
            S1_values = pd.read_csv('../Simulation_outputs/' + design + '/'+ structure + '_S1.csv')
            
            # plot shortage distribution
            ax = fig.add_subplot(2,3,count)
            plotSums(S1_values, ax, colors)
            
            # only put labels on bottom row, title experiment
            if count <= 3:
                ax.tick_params(axis='x',labelbottom='off')
                ax.set_title('User ' + str(i+1),fontsize=16)
            else:
                ax.tick_params(axis='x',labelsize=14)
                
            # iterate subplot counter
            count += 1
    
    fig.set_size_inches([12,8])
    fig.subplots_adjust(bottom=0.22)
    fig.text(0.5, 0.15, 'Percentile of Shortage', ha='center', fontsize=16)
    fig.text(0.05, 0.5, 'Portion of Variance Explained', va='center', rotation=90, fontsize=16)
    legend = fig.legend([mu0,sigma0,mu1,sigma1,p00,p11,Interact],\
                      [r'$\mu_d$',r'$\sigma_d$',r'$\mu_w$',r'$\sigma_w$',r'$p_{d,d}$',r'$p_{w,w}$','Interactions'],\
                      loc='lower center', ncol=4, fontsize=16, frameon=True)
    plt.setp(legend.get_title(),fontsize=16)
    fig.savefig('FigureS13_VarianceDecomposition_wider_100.pdf')
    fig.clf()

    return None