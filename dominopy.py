
import numpy as np
import matplotlib.pyplot as plt
import json
import random

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


def get_functions():
    # funcs = [
    #     {'type': 'polynomial','coeff': [2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [0.5]},# ax^2 + bx + c
        
    #     {'type': 'polynomial','coeff': [1,2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [-1,2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [1,2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [1,-2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [-1,-2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [1,-2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [1,0]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [2,0]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [-1,0]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [3,0]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [0.5,0]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [-3,0]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [-0.5,0]},# ax^2 + bx + c
        
    #     {'type': 'polynomial','coeff': [1,0,0]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [1,0,2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [1,0,-2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [-1,0,2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [-1,0,-2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [1,0,4]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [1,-2,0]}# ax^2 + bx + c
    # ]
    
    # funcs = [ # simple
    #     {'type': 'polynomial','coeff': [1,2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [-1,2]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [1,0]},# ax^2 + bx + c
    #     {'type': 'polynomial','coeff': [3,0]},# ax^2 + bx + c
        
    #     {'type': 'polynomial','coeff': [1,0,2]},# ax^2 + bx + c
        
    # ]
    
    funcs = [ # harder
        {'type': 'polynomial','coeff': [-1,-2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [0.5,0]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [1,2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [-1,2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [1,0]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [3,0]},# ax^2 + bx + c
        
        {'type': 'polynomial','coeff': [1,0,-2]},# ax^2 + bx + c
        {'type': 'polynomial','coeff': [1,0,2]},# ax^2 + bx + c
        
    ]
    return funcs

def merge_pdfs(filenames,outfilename,delete=False):
    ''' () -> float

    '''
    from PyPDF2 import PdfFileMerger, PdfFileReader

    merger = PdfFileMerger()
    for filename in filenames:
        with open(filename,'rb') as fd:
            merger.append(PdfFileReader(fd))

    while True:
        try:
            merger.write(outfilename)
            break
        except IOError as msg:
            print("Could not write file:",msg)
            input( "Fix it and press Enter to try again" )

    if delete:
        from os import remove
        for filename in filenames: remove(filename)

    return

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
        thedict['table'] = {'range':[-3,-2,-1,0,1,2,3]}
        thedict['func'] = {'type': 'polynomial','coeff': [0,0,0]}# ax^2 + bx + c
        
        return thedict
    
    def format_if_fraction(term):
        from fractions import Fraction
        # print(Fraction(term).as_integer_ratio())
        int_ratio = Fraction(term).as_integer_ratio()
        if int_ratio[1] == 1:
            return str(term)
        else:
            if int_ratio[0] < 0:
                return r"-\frac{%i}{%i}"%(-1*int_ratio[0],int_ratio[1])
            else:
                return r"\frac{%i}{%i}"%(int_ratio[0],int_ratio[1])
    
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
                        the_text += format_if_fraction(term)
                elif term < 0: # Negative
                    if term != -1:
                        the_text += format_if_fraction(term)
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
    
    funcs = get_functions()
    
    names = []
    
        
    for func in funcs:
        obj = new_object() 
        
        # print(func)
        name,names = func_to_name(func,names)
        # print(name)
        the_text = func_to_text(func) # Make formula
        names.append(name)
        obj['name'] = name
        obj['type'] = "formule_graph_table"
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
    
    name = obj.get('name', "noname")
    
    def _inifig():
        fig = plt.figure(figsize=(3,3),frameon=True) # (8.26772,11.6929)
        ax =  fig.add_axes((0, 0, 1, 1))#fig.add_subplot(111)
        
        fig.subplots_adjust(left=0,right=1.,bottom=0,top=1.,wspace=0.,hspace=0.)
        return fig,ax

    ## Formula
    fig,ax = _inifig()
    ax.text(0.5, 0.5, obj['formula'].get('text',""), fontsize=24, horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
    
    format_formulatable(ax)
    plt.savefig(loc+obj['formula']['fname'], bbox_inches='tight')
    plt.close(fig)
    
    ## Table
    fig,ax = _inifig()
    
    tablecontent = [[float(x) for x in obj['table']['range']],[]]
    
    tablecontent[1] = func_from_x(obj['func'],np.array(tablecontent[0]))
    
    the_table = ax.table( cellText = tablecontent , rowLabels=['$x$','$y$'], edges='open', loc='center',cellLoc='center')
    
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    
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
    
    
    
    xarr = np.linspace(obj['graph']['xrange'][0],obj['graph']['xrange'][1],100)
    yarr = func_from_x(obj['func'],xarr)
    # print(obj['graph']['xrange'][0],obj['graph']['xrange'][1])
    # print(xarr,yarr)
    ax.plot(xarr,yarr, c=(235/256.,105/256.,10/256.))
    
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
    
    print(dict_inds)
    if dict_inds[0] == 1:
        dict_inds[0] = 2
    else:
        dict_inds[1] = 2
    if dict_inds[5] == 1:
        dict_inds[5] = 2
    else:
        dict_inds[6] = 2
    
    fname_list = []
    for i,ind in enumerate(order):
        # print(i)
        obj = obj_list[ind]
        fname_list.append(  loc+obj[dictkeys[dict_inds[2*i]]]['fname'])
        fname_list.append(loc+obj[dictkeys[dict_inds[2*i+1]]]['fname'])
    fname_list.append(fname_list.pop(0)) # shift all by 1
    
    # make groups of 2
    fname_list = [ (fname_list[2*i],fname_list[2*i+1]) for i in range(len(fname_list)//2) ]
    
    # print(fname_list)
    
    return fname_list

def find_first_coprime(b,start=2):
    from math import gcd        

    def check_co_prime(num, M):
        return gcd(num, M) == 1 

    def get_smallest_co_prime(M):
        for i in range(start, M): # for every number *i* starting from 2 up to M
            if check_co_prime(i, M): # check if *i* is coprime with M
                return i # if it is, return i as the result

    return get_smallest_co_prime(b)

def make_code(settings):
    
    codetype = settings.get('type','iamodb')
    n = settings.get('len',1)
    
    loc = settings.get('loc',"numberpics/")
        
    if codetype == 'iamodb':
        
        b = n
        a = settings.get('a',find_first_coprime(b,start=3*b//4))
        
        code_res = {'a':a,'b':b}
        
        code_res['code_list'] = [ loc+"%i.jpg"%(i*a % b) for i in range(n) ]
        code_res['code_n'] = [(i*a % b) for i in range(n)]
        code_res['zero'] = loc+"ol_%i.jpg"%(a)
        # code_res['code_list'][0] = code_res['zero']
        
        # print(a,b)
        # print(code_res['code_list'])
        
    else:
        print("WARNING: Could not find codetype: ",settings)
        code_res = {'code_list':[]}
    
    return code_res
    
def make_pages(loc,fname_list,out_fname=None,
               code_settings={},
               repeat=1,random_order = False):
    if out_fname is None: out_fname = "pages"
    
    # Make code
    code_res = make_code(code_settings)
    code_list = code_res.get('code_list',[])
    print("CODE: a=%i, b=%i, n=%i"%(code_res['a'],code_res['b'],len(code_list)))
    
    # print(code_res)
    
    ## fname_list to page
    from PIL import Image,ImageDraw,ImageFont

    width, height = int(11.693 * 300),int(8.268 * 300) # A4 at 300dpi
    cellw,cellh = width//5,height//4
    imagew,imageh = int(1.9*300),int(1.9*300)
    # imagew,imageh = int(1.8*300),int(1.8*300)
    padw,padh = (cellw-imagew)//2,(cellh-imageh)//2
    codeImw,codeImh = int(0.2*300),int(0.2*300)
    
    if random_order:
        random.shuffle(fname_list)
        random.shuffle(code_list)
    
    if repeat > 1:
        old_code_list = code_list[:]
        old_fname_list = fname_list[:]

        for i in range(repeat-1):
            code_list.extend(old_code_list)
            fname_list.extend(old_fname_list)
        
    
    
    groups = [fname_list[i:i+10] for i in range(0, len(fname_list), 10)]
    groups_code = [code_list[i:i+10] for i in range(0, len(code_list), 10)]
    
    page_list = []
    
    # For each page
    for ind_group, group in enumerate(groups):
        group_code = groups_code[ind_group]
        print(ind_group,group,group_code)
        page = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(page)
            
        xi,yrow = 0,0
        order = range(len(group))
        for ind_card in order:
            card = group[ind_card]
            code = group_code[ind_card]
            
            for toggle in range(2):
                fname = card[toggle]
                # print(xi,ytoggle,yrow)
                xcoord = padw + xi*cellw
                ycoord = padh + (yrow+toggle)*cellh
                # print(xcoord,ycoord)
                with Image.open(fname) as Im:
                    if toggle == 0:
                        Im = Im.rotate(180)
                    Im = Im.resize((imagew,int(Im.height*imagew/Im.width)))
                    page.paste(Im, box=(xcoord, ycoord))
                
                code_x,code_y = xcoord-padw+codeImw//2,ycoord-padh//2
                with Image.open(code) as codeIm:
                    if toggle == 0:
                        codeIm = codeIm.rotate(180)
                        code_x = -1*code_x + (2*xi+1)*cellw
                        code_y = -1*code_y + (2*yrow+1)*cellh
                        code_x += -codeImw
                        code_y += -codeImh
                    codeIm = codeIm.resize((codeImw,int(codeIm.height*codeImw/codeIm.width)))
                    page.paste(codeIm, box=(code_x,code_y))
                # draw.text((xcoord-padw//2,ycoord),code,font=font, fill=(0, 0, 0, 255))

            if xi != 4:
                xi += 1
            else:
                xi = 0
                yrow += 2
            
        
        lw = 20
        # draw.line( (0, page.size[1], page.size[0], 0) ,width=lw, fill=128)
        for i in range(6):
            draw.line( [(i*cellw,0),(i*cellw,height)] ,width=lw, fill=256)
        for i in range(5):
            draw.line( [(0,i*cellh),(width,i*cellh)] ,width=lw, fill=256)
        
        save_fname = loc+out_fname+'_{}.pdf'.format(ind_group)
        page.save(save_fname)
        page_list.append(save_fname)
    
    merge_pdfs(page_list,loc+out_fname+".pdf")


def generate_numberpics():
    
    
    for i in range(100):
        
        for j in range(2):
            fig = plt.figure(figsize=(2,2),frameon=True) # (8.26772,11.6929)
            ax =  fig.add_axes((0, 0, 1, 1))#fig.add_subplot(111)
            
            fig.subplots_adjust(left=0,right=1.,bottom=0,top=1.,wspace=0.,hspace=0.)
            
            ax.spines['left'].set_color('none')
            ax.spines['left'].set_position('center')
            ax.spines['right'].set_color('none')
            ax.spines['right'].set_position('center')
            ax.spines['bottom'].set_color('none')
            ax.spines['bottom'].set_position('center')
            ax.spines['top'].set_color('none')
            ax.spines['top'].set_position('center')
            ax.set_xticks([], [])
            ax.set_yticks([], [])
            
            if j:
                the_text = "$%i$"%i
                fname = '%i.jpg'%i
            else:
                the_text = "$\overline{%i}$"%i
                fname = 'ol_%i.jpg'%i
            ax.text(0.5,0.5,the_text, size=88, horizontalalignment='center', verticalalignment='center',transform =ax.transAxes)
            fig.savefig('numberpics/'+fname)#,bbox_inches='tight' )
            plt.close(fig)
        

    
    

def main():
    
    # generate_numberpics()
    
    name = "harder_4lin1qua_withtable"
    
    loc = "linquad/"
    fname = "%s.json"%(name)

    print( "Making .. ",loc, name )
    
    print("> Make json")
    make_json_file(loc+fname)
    
    in_obj_list = load_json_file(loc+fname)
    
    
    # Make figures per object
    print("> Make figures")
    if True:
        for i in range(len(in_obj_list)):
            obj = in_obj_list[i]
            
            make_figures(loc+'figures/',obj)
    
    # Combine figures to page
    print("> Make Pages")
    out_fname = name
    fnames = make_fname_list(loc+"figures/",in_obj_list)
    
    
    code_settings = {'codetype':'iamodb','len':len(fnames),'a':5
                     }
    
    make_pages(loc,fnames,out_fname=out_fname,
               code_settings=code_settings,random_order=True)#,repeat=2)
    
    
if __name__ == "__main__":
    main()