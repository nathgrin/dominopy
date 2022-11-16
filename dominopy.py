
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font',family='STIXGeneral',size=14) # STIX looks like latex
plt.rc('mathtext',fontset='stix')
# plt.rc('figure', figsize=(1.41421356237*6.,6.) )
# plt.rc('figure.subplot', right=0.96464466094,top=0.95 )
plt.rc('lines', linewidth=1.8,marker='None',markersize=8 )
plt.rc('axes', linewidth=1.5,labelsize=24,prop_cycle=plt.cycler(color=('k','r','c','darkorange','steelblue','hotpink','gold','b','maroon','darkgreen')) )
plt.rc(('xtick.major','ytick.major'), size=5.2,width=1.5)
# plt.rc(('xtick.minor','ytick.minor'), size=3.2,width=1.5,visible=True)
# plt.rc(('xtick','ytick'), labelsize=20, direction='in' )
# plt.rc(('xtick'), top=True,bottom=True ) # For some stupid reason you have to do these separately
# plt.rc(('ytick'), left=True,right=True )
# plt.rc('legend',numpoints=1,scatterpoints=1,labelspacing=0.2,fontsize=18,fancybox=True,handlelength=1.5,handletextpad=0.5)
# plt.rc('savefig', dpi=150,format='pdf',bbox='tight' )
# plt.rc('errorbar',capsize=3.)

# plt.rc('image',cmap='gist_rainbow')


def format_graph(ax):
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['right'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['top'].set_position('zero')

    # remove the ticks from the top and right edges
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    

def draw_ax_frame(fig,ax):
    bbox = ax.get_tightbbox(fig.canvas.get_renderer())
    x0, y0, width, height = bbox.transformed(fig.transFigure.inverted()).bounds
    # slightly increase the very tight bounds:
    factor = 0.22
    xpad = factor * width
    ypad = factor * height
    fig.add_artist(plt.Rectangle((x0-xpad, y0-ypad), width+2*xpad, height+2*ypad, edgecolor='black', linewidth=2, fill=False))


def main():
    print("Hello World!")
    
    
    def _func(x):
        return x*x
    xarr = np.linspace(-5,5,1000)
    yarr = _func(xarr)
    
    
    fig,axarr = plt.subplots(4,5, sharex=False, sharey=False, figsize=(11.6929,8.26772)) # (8.26772,11.6929)

    pad = 0.5
    sp = 0.05
    # plt.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.95,wspace=0.05,hspace=0.05)
    # plt.subplots_adjust(left=sp,right=1.-sp,bottom=sp,top=1-sp,wspace=pad,hspace=1.5*pad)
    plt.subplots_adjust(left=sp,right=1.-sp,bottom=0.075,top=1-sp,wspace=pad,hspace=1.5*pad)
    # plt.subplots_adjust(left=pad*5,right=1.-pad*5,bottom=pad*4,top=1.-pad*4,wspace=pad,hspace=pad)
    # plt.setp(axarr, xticks=[], yticks=[])
    
    print(axarr)
    
    for i,row in enumerate(axarr):
        for j,ax in enumerate(row):
            ax.plot(xarr, yarr)

            format_graph(ax)
            draw_ax_frame(fig,ax)
    
    
    while True:
        try:
            plt.savefig('tst.pdf')
            break
        except:
            input("Close pdf and press enter to try again")
            
    plt.show()
    
    
if __name__ == "__main__":
    main()