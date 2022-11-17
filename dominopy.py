
import numpy as np
import matplotlib.pyplot as plt
import json

plt.rc('font',family='STIXGeneral',size=12) # STIX looks like latex
plt.rc('mathtext',fontset='stix')
# plt.rc('figure', figsize=(1.41421356237*6.,6.) )
# plt.rc('figure.subplot', right=0.96464466094,top=0.95 )
plt.rc('lines', linewidth=1.8,marker='None',markersize=8 )
plt.rc('axes', linewidth=1.5,labelsize=12,prop_cycle=plt.cycler(color=('k','r','c','darkorange','steelblue','hotpink','gold','b','maroon','darkgreen')) )
plt.rc(('xtick.major','ytick.major'), size=5.2,width=1.5)
plt.rc(('xtick.minor','ytick.minor'), size=3.2,width=1.5,visible=True)
plt.rc(('xtick','ytick'), labelsize=8)#, direction='in' )
# plt.rc(('xtick'), top=True,bottom=True ) # For some stupid reason you have to do these separately
# plt.rc(('ytick'), left=True,right=True )
# plt.rc('legend',numpoints=1,scatterpoints=1,labelspacing=0.2,fontsize=18,fancybox=True,handlelength=1.5,handletextpad=0.5)
# plt.rc('savefig', dpi=150,format='pdf',bbox='tight' )
# plt.rc('errorbar',capsize=3.)
# plt.rc('text',usetex=True)

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
    
    ax.grid()
    

def format_formulatable(ax):
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

def draw_ax_frame(fig,ax):
    bbox = ax.get_tightbbox(fig.canvas.get_renderer())
    x0, y0, width, height = bbox.transformed(fig.transFigure.inverted()).bounds
    # slightly increase the very tight bounds:
    factor = 0.22
    xpad = factor * width
    ypad = factor * height
    fig.add_artist(plt.Rectangle((x0-xpad, y0-ypad), width+2*xpad, height+2*ypad, edgecolor='black', linewidth=2, fill=False))


def make_pages(obj_list):
    
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
            # ax.plot(xarr, yarr)

            format_graph(ax)
            draw_ax_frame(fig,ax)
            
            print(ax.get_xlim())
            print(ax.xaxis.get_major_ticks())
            print([x.get_loc() for x in ax.xaxis.get_major_ticks()])
            # ax.set_xticks([x for x in ax.xaxis.get_major_ticks() if float(x.get_loc()) != 0.], minor=True)
            print('tickz',ax.get_xticks(),ax.get_yticks())
    
    while True:
        try:
            plt.savefig('tst.pdf')
            break
        except:
            input("Close pdf and press enter to try again")
            
    plt.show()
    
    
    
def make_json_file(fname):
    def _func(x):
        return x*x
    xarr = np.linspace(-5,5,1000)
    yarr = _func(xarr)
    
    obj_list = []
    
    
    def new_object():
        thedict = {}
        # thedict['name'] = ""
        thedict['formula'] = {'text': ""}
        thedict['graph'] = {'xrange':[-5,5]}
        thedict['table'] = {'range':[-5,-3,-1,0,1,3,5]}
        thedict['func'] = {'type': 'polynomial','coeff': [0,0,0]}# ax^2 + bx + c
        
        return thedict
    
    def func_to_text(func):
        the_text = ""
        if func['type'] == 'polynomial':
            degree= len(func['coeff'])-1
            the_text = "$y="
            for i,term in enumerate(func['coeff']):
                if term > 0: # Positive
                    if the_text[-1] != "=":
                        the_text += "+"
                    if term != 1:
                        the_text += str(term)
                elif term < 0: # Negative
                    if term != -1:
                        the_text += str(term)
                    else:
                        the_text += "-"
                    
                if term != 0 and i != degree:
                    the_text += "x^{%i}"%(degree-i)
            the_text += "$"
        else:
            print("WARNING: Did not recognize func type: ",func)   
        return the_text
    
    def func_to_name(func,names):
        name = ""
        if func['type'] == 'polynomial':
            base_name = 'poly_'+str(len(func['coeff']))+'_'+str(func['coeff'][0])
            
        i = 0
        name = base_name
        while name in names:
            i += 1
            name = base_name + "_%i"%(i)
        names.append(name)
        return name,names
    
    funcs = [
        {'type': 'polynomial','coeff': [0,1,2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [0,-1,2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [1,0,2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [-1,0,2]}# ax^2 + bx + c
    ]
    
    names = []
    
        
    for func in funcs:
        obj = new_object() 
        
        print(func)
        name,names = func_to_name(func,names)
        print(name)
        the_text = func_to_text(func) # Make formula
        names.append(name)
        obj['name'] = name
        obj['formula']['text'] = the_text
        obj['func'] = func# marshal.dumps(tstfunc.func_code)
        obj_list.append(obj)
        
        
    
    print(obj_list)
    with open(fname,'w') as outfile:
        json.dump(obj_list,outfile, indent=4)

def make_figures(loc,obj):
    
    name = obj.get('name', "noname")
    
    def _inifig():
        fig = plt.figure(figsize=(2,2),frameon=True) # (8.26772,11.6929)
        ax =  fig.add_axes((0, 0, 1, 1))#fig.add_subplot(111)
        
        fig.subplots_adjust(left=0,right=1.,bottom=0,top=1.,wspace=0.,hspace=0.)
        return fig,ax
    ## Formula
    fig,ax = _inifig()
    ax.text(0.5, 0.5, obj['formula'].get('text',""), horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
    
    format_formulatable(ax)
    plt.savefig(loc+'%s_formula.png'%(name), bbox_inches='tight')
    
    ## Table
    fig,ax = _inifig()
    
    tablecontent = [[float(x) for x in obj['table']['range']],[]]
    
    tablecontent[1] = [ 2*x+1 for x in tablecontent[0] ]
    
    the_table = ax.table( cellText = tablecontent , rowLabels=['$x$','$y$'], edges='open', loc='center')
    
    for j in range(2):
        for i in range(len(tablecontent[0])):
            cell = the_table[j,i]
            
            cell.loc = 'center'
            cell.visible_edges=""
            if j == 0:
                cell.visible_edges += "B"
            if i != len(tablecontent[0])-1:
                cell.visible_edges += "R"
    
    format_formulatable(ax)
    plt.savefig(loc+'%s_table.png'%(name), bbox_inches='tight')
    
    
    ## Graph
    fig,ax = _inifig()
    
    xarr = np.linspace(obj['graph']['xrange'][0],obj['graph']['xrange'][1],100)
    yarr = xarr*xarr
    # print(obj['graph']['xrange'][0],obj['graph']['xrange'][1])
    # print(xarr,yarr)
    ax.plot(xarr,yarr)
    
    format_graph(ax)
    
    plt.savefig(loc+'%s_graph.png'%(name), bbox_inches='tight')
    
    # plt.savefig('tst.png', bbox_inches='tight')
    # plt.show()

def main():
    print("Hello World!")
    loc = "linquad/"
    fname = "out.json"

    make_json_file(fname)
    
    with open(fname) as infile:
        in_obj_list = json.load(infile)
    for i in range(len(in_obj_list)):
        obj = in_obj_list[i]
        # obj['func'] = types.FunctionType(the_obj['func'], globals(), "some_func_name") 
        
        make_figures(loc,obj)
        
    
    
    
if __name__ == "__main__":
    main()