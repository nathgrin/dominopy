
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
    
    thelim = list(ax.get_xlim())
    if thelim[0] > -0.5:
        thelim[0] = -0.5
    if thelim[1] < 0.5:
        thelim[1] = 0.5
    ax.set_xlim(thelim)
    thelim = list(ax.get_ylim())
    if thelim[0] > -0.5:
        thelim[0] = -0.5
    if thelim[1] < 0.5:
        thelim[1] = 0.5
    ax.set_ylim(thelim)
    
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

    
    
def make_json_file(fname):
    
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
                    the_text += "x"
                    if degree-i != 1:
                        the_text += "^{%i}"%(degree-i)
            the_text += "$"
        else:
            print("WARNING: Did not recognize func type: ",func)   
        return the_text
    
    def func_to_name(func,names):
        name = ""
        if func['type'] == 'polynomial':
            base_name = 'poly_deg'+str(len(func['coeff'])-1)+'_'+str(func['coeff'][0])
            
        i = 0
        name = base_name
        while name in names:
            i += 1
            name = base_name + "_n%i"%(i)
        names.append(name)
        return name,names
    
    funcs = [
        {'type': 'polynomial','coeff': [1,2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [-1,2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [1,2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [1,0]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [2,0]},# ax^2 + bx + c
        
        {'type': 'polynomial','coeff': [1,0,0]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [1,0,2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [-1,0,2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [1,0,4]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [-1,1,0]}# ax^2 + bx + c
    ]
    
    names = []
    
        
    for func in funcs:
        obj = new_object() 
        
        # print(func)
        name,names = func_to_name(func,names)
        # print(name)
        the_text = func_to_text(func) # Make formula
        names.append(name)
        obj['name'] = name
        obj['func'] = func# marshal.dumps(tstfunc.func_code)
        obj['formula']['text'] = the_text
        obj['formula']['fname'] = '%s_formula.png'%(name)
        obj['graph']['fname'] = '%s_graph.png'%(name)
        obj['table']['fname'] = '%s_table.png'%(name)
        obj_list.append(obj)
        
        
    
    # print(obj_list)
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
    plt.savefig(loc+obj['formula']['fname'], bbox_inches='tight')
    plt.close(fig)
    
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
    plt.savefig(loc+obj['table']['fname'], bbox_inches='tight')
    plt.close(fig)
    
    
    ## Graph
    fig,ax = _inifig()
    
    def func_from_x(func,xarr):
        if func['type'] == 'polynomial':
            
            out = np.zeros(xarr.shape)
            # print(out)
            deg = len(func['coeff'])
            for i,coeff in enumerate(func['coeff']):
                # print(i,coeff)
                out += coeff*np.power(xarr,deg-i-1)
                
            
        else:
            print('WARNING: Did not recognize function type: ',func)
            out = xarr
            
        return out
    
    xarr = np.linspace(obj['graph']['xrange'][0],obj['graph']['xrange'][1],100)
    yarr = func_from_x(obj['func'],xarr)
    # print(obj['graph']['xrange'][0],obj['graph']['xrange'][1])
    # print(xarr,yarr)
    ax.plot(xarr,yarr)
    
    format_graph(ax)
    
    plt.savefig(loc+obj['graph']['fname'], bbox_inches='tight')
    plt.close(fig)
    

def load_json_file(fname):
    
    with open(fname) as infile:
        in_obj_list = json.load(infile)
    return in_obj_list

def make_fname_list(loc,obj_list):
    ## Choose objects
    dictkeys = ['formula','graph','table']
    order = np.random.permutation(len(obj_list))
    # print( order )
    dict_inds = list(np.random.permutation(2))
    while True:
        attempt = np.random.permutation(2)
        if dict_inds[-1] == attempt[0]:
            continue
        dict_inds.extend(attempt)
        
        if len(dict_inds) > 2*len(order):
            dict_inds = dict_inds[:2*len(order)]
            break
    
    # print(dict_inds)
    
    fname_list = []
    for i,ind in enumerate(order):
        # print(i)
        obj = obj_list[ind]
        fname_list.append(  loc+obj[dictkeys[dict_inds[2*i]]]['fname'])
        fname_list.append(loc+obj[dictkeys[dict_inds[2*i+1]]]['fname'])
    fname_list.append(fname_list.pop(0)) # shift all by 1
    
    # print(fname_list)
    
    return fname_list
def make_pages(loc,fname_list):
    
    
    
    ## fname_list to page
    from PIL import Image,ImageDraw

    width, height = int(11.693 * 300),int(8.268 * 300) # A4 at 300dpi
    cellw,cellh = width//5,height//4
    imagew,imageh = int(1.9*300),int(1.9*300)
    # imagew,imageh = int(1.8*300),int(1.8*300)
    padw,padh = (cellw-imagew)//2,(cellh-imageh)//2
    
    groups = [fname_list[i:i+20] for i in range(0, len(fname_list), 20)]
    for ind_group, group in enumerate(groups):
        print(ind_group,group)
        page = Image.new('RGB', (width, height), 'white')
        
        xi,ytoggle,yrow = 0,0,0
        for fname in group:
            # print(xi,ytoggle,yrow)
            xcoord = padw + xi*cellw
            ycoord = padh + (yrow+ytoggle)*cellh
            # print(xcoord,ycoord)
            
            with Image.open(fname) as Im:
                if ytoggle == 0:
                    Im = Im.rotate(180)
                Im = Im.resize((imagew,int(Im.height*imagew/Im.width)))
                page.paste(Im, box=(xcoord, ycoord))
            
            if ytoggle:
                if xi != 4:
                    xi += 1
                else:
                    xi = 0
                    yrow += 2
            ytoggle = 1-ytoggle
            
        draw = ImageDraw.Draw(page)
        
        lw = 20
        # draw.line( (0, page.size[1], page.size[0], 0) ,width=lw, fill=128)
        for i in range(6):
            draw.line( [(i*cellw,0),(i*cellw,height)] ,width=lw, fill=256)
        for i in range(5):
            draw.line( [(0,i*cellh),(width,i*cellh)] ,width=lw, fill=256)
        
        
        page.save(loc+'page{}.pdf'.format(ind_group))


def main():
    loc = "linquad/"
    fname = "cards.json"

    print( "Making .. ",loc, fname )
    
    make_json_file(loc+fname)
    
    in_obj_list = load_json_file(loc+fname)
    
    
    # Make figures per object
    if True:
        for i in range(len(in_obj_list)):
            obj = in_obj_list[i]
            
            make_figures(loc,obj)
    
    # Combine figures to page
    fnames = make_fname_list(loc,in_obj_list)
    make_pages(loc,fnames)
    
    
if __name__ == "__main__":
    main()