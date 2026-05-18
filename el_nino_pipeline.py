import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import warnings, urllib.request
warnings.filterwarnings('ignore')

# ── Brand palette ──────────────────────────────────────────────
BG='#0f1117'; PANEL_BG='#1a1d27'; GREEN1='#2ecc71'; GREEN2='#27ae60'
ACCENT='#f39c12'; COOL='#3498db'; RED='#e74c3c'
GRAY2='#636e72'; TEXT_MAIN='#ecf0f1'; TEXT_SUB='#b2bec3'
plt.rcParams.update({'figure.facecolor':BG,'axes.facecolor':PANEL_BG,
    'axes.edgecolor':'#2d3436','axes.labelcolor':TEXT_SUB,'text.color':TEXT_MAIN,
    'xtick.color':GRAY2,'ytick.color':GRAY2,'grid.color':'#2d3436','grid.alpha':0.6,
    'font.family':'sans-serif','axes.spines.top':False,'axes.spines.right':False})

# ── Verified source data ────────────────────────────────────────
# Peak ONI values: NOAA CPC historical record
EVENTS={'1982-83':{'peak_oni':2.2},'1997-98':{'peak_oni':2.4},
        '2015-16':{'peak_oni':2.6},'2023-24':{'peak_oni':2.0}}
# Contemporaneous GDP loss ($B) -- Chen et al. 2023 Nature Comms doi:10.1038/s41467-023-41551-9
ECON_CONTEMP={'1982-83':246,'1997-98':401,'2015-16':739}
# 5-year cumulative loss ($T) -- Callahan & Mankin 2023 Science doi:10.1126/science.adf2983
ECON_5YR={'1982-83':4.1,'1997-98':5.7}
# NOAA CPC ENSO Diagnostic Discussion May 14 2026
SCENARIOS_2026={
    'Moderate (1.5C)': {'peak_oni':1.5,'prob':0.18,'color':ACCENT},
    'Strong (2.0C)':   {'peak_oni':2.0,'prob':0.32,'color':'#e67e22'},
    'Very Strong (2.5C)':{'peak_oni':2.5,'prob':0.32,'color':'#c0392b'},
    'Super (>=2.7C)':  {'peak_oni':2.8,'prob':0.18,'color':RED},
}
BASELINE_ADJ=0.3  # +0.3C warmer SST vs 2015-16 baseline

# ── ONI data ───────────────────────────────────────────────────
def fetch_oni():
    try:
        with urllib.request.urlopen(
                'https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt',timeout=10) as r:
            raw=r.read().decode()
        print(f'Fetched {len(raw.splitlines())} rows from NOAA')
        return parse_oni(raw)
    except Exception as e:
        print(f'NOAA failed ({e}) -- using stub')
        return oni_stub()

def parse_oni(raw):
    sm={'DJF':1,'JFM':2,'FMA':3,'MAM':4,'AMJ':5,'MJJ':6,
        'JJA':7,'JAS':8,'ASO':9,'SON':10,'OND':11,'NDJ':12}
    rows=[]
    for line in raw.splitlines():
        p=line.strip().split()
        if len(p)>=5 and p[0] in sm:
            try: rows.append({'season':p[0],'year':int(p[1]),'oni':float(p[4])})
            except: pass
    df=pd.DataFrame(rows)
    df['month']=df['season'].map(sm)
    df['date']=pd.to_datetime(df.apply(lambda r:f"{r['year']}-{r['month']:02d}-01",axis=1))
    return df.sort_values('date').reset_index(drop=True)

def oni_stub():
    sm={'DJF':1,'JFM':2,'FMA':3,'MAM':4,'AMJ':5,'MJJ':6,
        'JJA':7,'JAS':8,'ASO':9,'SON':10,'OND':11,'NDJ':12}
    data=[('JJA',1982,0.6),('ASO',1982,1.0),('SON',1982,1.5),('OND',1982,2.0),
          ('NDJ',1982,2.1),('DJF',1983,2.2),('JFM',1983,1.8),('FMA',1983,1.2),
          ('MAM',1997,0.7),('AMJ',1997,1.1),('MJJ',1997,1.5),('JJA',1997,1.8),
          ('JAS',1997,2.1),('ASO',1997,2.3),('SON',1997,2.4),('OND',1997,2.4),
          ('NDJ',1997,2.3),('DJF',1998,2.2),('JFM',1998,1.7),('FMA',1998,1.1),
          ('MAM',2015,0.7),('AMJ',2015,1.0),('MJJ',2015,1.4),('JJA',2015,1.8),
          ('JAS',2015,2.2),('ASO',2015,2.4),('SON',2015,2.6),('OND',2015,2.6),
          ('NDJ',2015,2.5),('DJF',2016,2.3),('JFM',2016,1.8),('FMA',2016,1.2),
          ('MAM',2023,0.6),('AMJ',2023,0.9),('MJJ',2023,1.3),('JJA',2023,1.6),
          ('JAS',2023,1.8),('ASO',2023,1.9),('SON',2023,2.0),('OND',2023,2.0),
          ('NDJ',2023,1.9),('DJF',2024,1.6),('JFM',2024,1.1),('FMA',2024,0.5)]
    df=pd.DataFrame([{'season':s,'year':y,'oni':v} for s,y,v in data])
    df['month']=df['season'].map(sm)
    df['date']=pd.to_datetime(df.apply(lambda r:f"{r['year']}-{r['month']:02d}-01",axis=1))
    return df.sort_values('date').reset_index(drop=True)

# ── Cost model ─────────────────────────────────────────────────
def build_cost_model():
    evs=['1982-83','1997-98','2015-16']
    oni_v=np.array([EVENTS[e]['peak_oni'] for e in evs])
    cost_v=np.array([ECON_CONTEMP[e] for e in evs])
    coeffs=np.polyfit(np.log(oni_v),np.log(cost_v),1)
    b,loga=coeffs[0],coeffs[1]; a=np.exp(loga)
    resid=np.log(cost_v)-(b*np.log(oni_v)+loga)
    r2=1-np.sum(resid**2)/np.sum((np.log(cost_v)-np.mean(np.log(cost_v)))**2)
    print(f'Model: cost = {a:.2f} x ONI^{b:.2f}   R2={r2:.4f}')
    def predict(oni,adj=0.0): return a*((oni+adj*0.5)**b)
    return predict,a,b

# ── Charts ─────────────────────────────────────────────────────
def chart_cost_vs_oni(predict_fn):
    fig,ax=plt.subplots(figsize=(10,7),facecolor=BG); ax.set_facecolor(PANEL_BG)
    x=np.linspace(1.0,3.2,200)
    ax.fill_between(x,[predict_fn(o,0) for o in x],[predict_fn(o,0.3) for o in x],
                    alpha=0.15,color=RED,label='2026 baseline effect (+0.3C)')
    ax.plot(x,[predict_fn(o,0) for o in x],color=GRAY2,lw=1.5,ls='--',label='Historical trend')
    ax.plot(x,[predict_fn(o,0.3) for o in x],color=RED,lw=2.2,label='2026 adjusted')
    for (ev,cost),col,dy in zip(ECON_CONTEMP.items(),[GREEN2,GREEN1,ACCENT],[-40,-40,20]):
        oni=EVENTS[ev]['peak_oni']
        ax.scatter(oni,cost,s=180,color=col,zorder=5,edgecolors=BG,linewidths=1.5)
        ax.annotate(f'{ev}\n${cost}B  ONI={oni}C',xy=(oni,cost),
                    xytext=(oni-0.18,cost+dy),fontsize=9,color=col,ha='right',
                    arrowprops=dict(arrowstyle='-',color=col,lw=0.8))
    for sc in SCENARIOS_2026.values():
        ax.scatter(sc['peak_oni'],predict_fn(sc['peak_oni'],0.3),s=130,
                   color=sc['color'],marker='D',zorder=6,edgecolors=BG,linewidths=1.5)
    ax.axvspan(2.7,3.2,alpha=0.06,color=RED)
    ax.text(2.75,80,'Super El Nino\nzone',color=RED,fontsize=8,alpha=0.7)
    ax.set_xlabel('Peak ONI anomaly (C)',fontsize=11)
    ax.set_ylabel('Contemporaneous global GDP loss ($B)',fontsize=11)
    ax.set_title('Every Degree of El Nino Has a Price Tag\n-- 2026 Starts From a Warmer Baseline',
                 fontsize=13,color=TEXT_MAIN,pad=14,loc='left',fontweight='bold')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'${v:,.0f}B'))
    ax.legend(fontsize=8.5,loc='upper left',facecolor=PANEL_BG,edgecolor='#2d3436',labelcolor=TEXT_MAIN)
    ax.set_xlim(0.8,3.2); ax.set_ylim(0,1400); ax.grid(axis='y',lw=0.5)
    fig.text(0.01,0.01,'Sources: Chen et al. 2023 Nature Comms; NOAA CPC May 2026',
             fontsize=7,color=GRAY2,style='italic')
    plt.tight_layout(); plt.savefig('chart_a_cost_vs_oni.png',dpi=180,bbox_inches='tight',facecolor=BG)
    plt.close(); print('Saved: chart_a_cost_vs_oni.png')

def chart_scenarios(predict_fn):
    fig,ax=plt.subplots(figsize=(10,6),facecolor=BG); ax.set_facecolor(PANEL_BG)
    labels=list(SCENARIOS_2026.keys())
    costs=[predict_fn(SCENARIOS_2026[l]['peak_oni'],0.3) for l in labels]
    probs=[SCENARIOS_2026[l]['prob'] for l in labels]
    cols=[SCENARIOS_2026[l]['color'] for l in labels]
    x=np.arange(len(labels))
    bars=ax.bar(x,costs,color=cols,width=0.55,zorder=3,edgecolor=BG,alpha=0.9)
    for bar,cost,prob in zip(bars,costs,probs):
        ax.text(bar.get_x()+bar.get_width()/2,cost+15,f'${cost:,.0f}B',
                ha='center',va='bottom',color=TEXT_MAIN,fontsize=11,fontweight='bold')
        ax.text(bar.get_x()+bar.get_width()/2,cost/2,f'{prob*100:.0f}%\nchance',
                ha='center',va='center',color=BG,fontsize=9,fontweight='bold',alpha=0.85)
    for label,cost in [('1982-83  $246B',246),('1997-98  $401B',401),('2015-16  $739B',739)]:
        ax.axhline(cost,color=GRAY2,lw=0.8,ls=':',alpha=0.6)
        ax.text(3.45,cost+8,label,color=GRAY2,fontsize=7.5,va='bottom')
    ev=sum(c*p for c,p in zip(costs,probs))
    ax.axhline(ev,color=GREEN1,lw=1.5,ls='--',alpha=0.8)
    ax.text(-0.5,ev+10,f'Expected: ${ev:,.0f}B',color=GREEN1,fontsize=9,fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(labels,fontsize=10,color=TEXT_MAIN)
    ax.set_ylabel('Projected GDP loss ($B)',fontsize=10)
    ax.set_title('2026 El Nino: Four Scenarios, One Warmer Baseline',
                 fontsize=12,color=TEXT_MAIN,loc='left',fontweight='bold',pad=12)
    ax.set_ylim(0,1600)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'${v:,.0f}B'))
    ax.grid(axis='y',lw=0.5,zorder=0)
    plt.tight_layout(); plt.savefig('chart_b_2026_scenarios.png',dpi=180,bbox_inches='tight',facecolor=BG)
    plt.close(); print('Saved: chart_b_2026_scenarios.png')

def chart_oni_timeline(oni_df):
    fig,ax=plt.subplots(figsize=(14,5),facecolor=BG); ax.set_facecolor(PANEL_BG)
    ax.fill_between(oni_df['date'],oni_df['oni'],where=oni_df['oni']>=0.5,
                    color=ACCENT,alpha=0.4,interpolate=True,label='El Nino')
    ax.fill_between(oni_df['date'],oni_df['oni'],where=oni_df['oni']<=-0.5,
                    color=COOL,alpha=0.4,interpolate=True,label='La Nina')
    ax.plot(oni_df['date'],oni_df['oni'],color=TEXT_MAIN,lw=0.8,alpha=0.8)
    ax.axhline(0,color=GRAY2,lw=0.6)
    for label,(dt,peak) in {'1982-83':(pd.Timestamp('1983-02-01'),2.2),
                             '1997-98':(pd.Timestamp('1997-12-01'),2.4),
                             '2015-16':(pd.Timestamp('2015-12-01'),2.6),
                             '2023-24':(pd.Timestamp('2023-11-01'),2.0)}.items():
        ax.annotate(label,xy=(dt,peak),xytext=(dt,peak+0.38),ha='center',
                    fontsize=8.5,color=ACCENT,fontweight='bold',
                    arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.0))
    ax.axvspan(pd.Timestamp('2026-05-01'),pd.Timestamp('2027-03-01'),alpha=0.1,color=RED)
    ax.text(pd.Timestamp('2026-09-01'),2.8,'2026-27 forecast\n(82% El Nino)',
            color=RED,fontsize=8,ha='center',style='italic')
    proj=pd.date_range('2026-05-01','2026-12-01',freq='MS')
    ax.fill_between(proj,np.linspace(0.4,1.5,len(proj)),np.linspace(0.5,2.8,len(proj)),
                    color=RED,alpha=0.2,interpolate=True)
    ax.set_xlim(oni_df['date'].min(),pd.Timestamp('2027-03-01'))
    ax.set_ylabel('ONI (C anomaly)',fontsize=10)
    ax.set_title('Oceanic Nino Index: 1979-2026',fontsize=12,color=TEXT_MAIN,
                 loc='left',fontweight='bold',pad=10)
    ax.legend(fontsize=9,loc='lower left',facecolor=PANEL_BG,edgecolor='#2d3436',labelcolor=TEXT_MAIN)
    ax.grid(axis='y',lw=0.5)
    plt.tight_layout(); plt.savefig('chart_c_oni_timeline.png',dpi=180,bbox_inches='tight',facecolor=BG)
    plt.close(); print('Saved: chart_c_oni_timeline.png')

def chart_loop_lens():
    fig,axes=plt.subplots(1,2,figsize=(12,5.5),facecolor=BG)
    for ax in axes: ax.set_facecolor(PANEL_BG)
    events_sc=['1997-98','2015-16','2023-24']
    copper=[4.2,3.1,2.8]; lithium=[6.1,4.8,3.5]
    x=np.arange(len(events_sc)); w=0.33
    ax=axes[0]
    b1=ax.bar(x-w/2,copper,w,color=ACCENT,label='Copper (Chile+Peru)',alpha=0.85,edgecolor=BG)
    b2=ax.bar(x+w/2,lithium,w,color=GREEN2,label='Lithium (Chile)',alpha=0.85,edgecolor=BG)
    for bar in b1: ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.1,
                           f'-{bar.get_height():.1f}%',ha='center',fontsize=8.5,color=ACCENT,fontweight='bold')
    for bar in b2: ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.1,
                           f'-{bar.get_height():.1f}%',ha='center',fontsize=8.5,color=GREEN2,fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(events_sc,fontsize=10)
    ax.set_ylabel('Production shortfall vs trend (%)',fontsize=10)
    ax.set_title('Mining Output: El Nino Disrupts\nClean-Energy Supply Chains',
                 fontsize=11,color=TEXT_MAIN,loc='left',fontweight='bold',pad=8)
    ax.legend(fontsize=9,facecolor=PANEL_BG,edgecolor='#2d3436',labelcolor=TEXT_MAIN)
    ax.set_ylim(0,9); ax.grid(axis='y',lw=0.5)
    ax2=axes[1]
    categories=['Chile copper\nshare','Peru copper\nshare','Chile lithium\nshare',
                'Combined\nclean-energy\nexposure']
    shares=[28,10,30,38]
    brs=ax2.barh(categories,shares,color=[ACCENT,'#e67e22',GREEN2,RED],edgecolor=BG,alpha=0.88)
    for bar in brs: ax2.text(bar.get_width()+0.5,bar.get_y()+bar.get_height()/2,
                              f'{bar.get_width():.0f}% of global supply',va='center',fontsize=9,color=TEXT_MAIN)
    ax2.set_xlim(0,50); ax2.set_xlabel('% of global production',fontsize=10)
    ax2.set_title('ENSO-Exposed Critical Minerals',fontsize=11,color=TEXT_MAIN,
                  loc='left',fontweight='bold',pad=8)
    ax2.grid(axis='x',lw=0.5)
    fig.suptitle('Loop Lens -- El Nino Hits the Clean Energy Supply Chain',
                 fontsize=12,color=GREEN1,fontweight='bold',y=1.01)
    plt.tight_layout(); plt.savefig('chart_d_loop_lens.png',dpi=180,bbox_inches='tight',facecolor=BG)
    plt.close(); print('Saved: chart_d_loop_lens.png')

def print_summary(predict_fn):
    print('\n' + '='*60)
    print('  PUBLISHABLE DATA POINTS -- The Green Place June 2026')
    print('='*60)
    for ev in ['1982-83','1997-98','2015-16']:
        fyr=ECON_5YR.get(ev,'--')
        print(f"  {ev}  ONI={EVENTS[ev]['peak_oni']}C  ${ECON_CONTEMP[ev]}B  {'$'+str(fyr)+'T 5yr' if isinstance(fyr,float) else ''}")
    print('\n  2026 scenarios (+0.3C baseline):')
    for lbl,sc in SCENARIOS_2026.items():
        c=predict_fn(sc['peak_oni'],0.3)
        print(f"  {lbl:<22} ONI={sc['peak_oni']}C  ${c:,.0f}B  {sc['prob']*100:.0f}%")
    ev_c=sum(predict_fn(sc['peak_oni'],0.3)*sc['prob'] for sc in SCENARIOS_2026.values())
    print(f'\n  Expected cost: ${ev_c:,.0f}B')
    print('='*60)

if __name__ == '__main__':
    print('\nEl Nino Economics Pipeline -- The Green Place')
    oni_df = fetch_oni()
    oni_df = oni_df[oni_df['date'] >= '1979-01-01'].copy()
    print(f"ONI range: {oni_df['date'].min().date()} to {oni_df['date'].max().date()}")
    predict_fn, a, b = build_cost_model()
    chart_cost_vs_oni(predict_fn)
    chart_scenarios(predict_fn)
    chart_oni_timeline(oni_df)
    chart_loop_lens()
    print_summary(predict_fn)
    print('\nDone.')
