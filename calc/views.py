from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Structures
from .models import Pipes
from .models import Project
from .models import Generic_Structures
import csv
import io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from .forms import CreateNewProjectNameForm
import pandas as pd
import numpy as np
from django_pandas.io import read_frame
import re
from decimal import Decimal
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from .serializers import PipesSerializer
import math
import logging
import xlsxwriter

from rest_framework import generics

# Create your views here.

global active_project

@login_required(login_url = 'login_page')
def index1(request):

    if 'active_project' not in request.session:
        request.session['active_project'] = None

    active_project_0 = request.session['active_project']
    active_project = str(active_project_0)
    structures = Structures.objects.all().filter( project_id = active_project)
    projects = Project.objects.all()
    pipes = Pipes.objects.all().filter( project_id = active_project).order_by('system','order','pipe_id')
    return render(request, 'index1.html',{"structures" : structures, "pipes" : pipes, "projects" : projects}  )

@login_required(login_url = 'login_page')
def developer(request):
    return render(request, 'index_developer.html' )

@login_required(login_url = 'login_page')
def create_new_project_name(request):
    if request.method == 'POST':
        new = request.POST.get('new_project_name')
        proj = Project(project_id = new)
        proj.save()
        return redirect('index1')
    return render(request, 'index1.html')

@login_required(login_url = 'login_page')
def select_project(request):
    if request.method == 'POST':
        active = request.POST.get('select-project')
        active_project = active
        request.session['active_project'] = active_project
        return redirect('index1')
    return render(request, 'index1.html', {'active_project' : active_project} )

@login_required(login_url = 'login_page')
def upload_template_file(request):
    if request.method == 'GET':
        return render(request, "index_developer.html")
    try:
        print('upload_template_file checkpoint 1')
        xl_file = request.FILES["excel_file"]
        print(xl_file)
        df = pd.read_excel(xl_file, sheet_name=0)

        for row in df.index:
            _, created = Generic_Structures.objects.get_or_create(
                structure_type = df.iloc[row][0],
                drop_across_bottom = df.iloc[row][1],
                maximum_depth = df.iloc[row][2],
                minimum_depth_18_inch = df.iloc[row][3],
                minimum_depth_24_inch = df.iloc[row][4],
                minimum_depth_30_inch = df.iloc[row][5],
                minimum_depth_36_inch = df.iloc[row][6],
                minimum_depth_42_inch = df.iloc[row][7],
                minimum_depth_48_inch = df.iloc[row][8],
                minimum_depth_54_inch = df.iloc[row][9],
                minimum_depth_60_inch = df.iloc[row][10],
                minimum_depth_72_inch = df.iloc[row][11],
                minimum_depth_78_inch = df.iloc[row][12]
                )

    finally:
        return render(request, "index_developer.html")

@login_required(login_url = 'login_page')
def upload_structures_file(request):
    if request.method == 'GET':
        return redirect('index1')
    try:
        csv_file = request.FILES["csv_file"]
        df = pd.read_csv(csv_file, sep=',', skipinitialspace=True,header=0)
        active = request.session['active_project']
        df[['Node - ID']] = df[['Node - ID']].apply(pd.to_numeric, errors='coerce').fillna(df)
        df['Node - ID'] = df['Node - ID'].astype(str)
        df['Node - ID'] = df['Node - ID'].str.replace('.0', '', regex = False)
        for row in df.index:
            _, created = Structures.objects.get_or_create(
                structure_id = df.iloc[row][0],
                type_and_size = df.iloc[row][1],
                surface_elevation = df.iloc[row][2],
                project_id = str(active)
                )
    finally:
        return redirect('index1')

@login_required(login_url = 'login_page')
def upload_pipes_file(request):
    if request.method == 'GET':
        return redirect('index1')
    try:
        csv_file = request.FILES["csv_file_p"]
        df = pd.read_csv(csv_file, sep = ',', skipinitialspace=True)
        df = df.dropna(how='all', axis='columns')
        df[['Link - Upstream Node']] = df[['Link - Upstream Node']].apply(pd.to_numeric, errors='coerce').fillna(df)
        df['Link - Upstream Node'] = df['Link - Upstream Node'].astype(str)
        df['Link - Upstream Node'] = df['Link - Upstream Node'].str.replace('.0', '', regex = False)
        active = request.session['active_project']
        for row in df.index:
            _, created = Pipes.objects.get_or_create(
                pipe_id = df.iloc[row][0],
                upstream_node = df.iloc[row][1],
                downstream_node = df.iloc[row][2],
                pipe_size = df.iloc[row][3],
                pipe_length = df.iloc[row][4],
                discharge = df.iloc[row][5],
                upstream_invert = df.iloc[row][6],
                downstream_invert = df.iloc[row][7],
                project_id = str(active)
            )
    finally:
        print("upload_pipes_file method 5 ")
        return redirect('index1')

global sys_lib
global chkd
global sys_lib

@login_required(login_url = 'login_page')
def order_pipes_create_systems(request):
    
    active_project_0 = request.session['active_project']
    active_project = str(active_project_0)
    all_pipe_entries = Pipes.objects.all().filter( project_id = active_project)
    df = read_frame(all_pipe_entries)
    df[:]['order'] = 0
    
    sys_no = 0
    chkd = []
    sys_lib = {}

    for i in df.index:
        fp = df.iloc[i:i+1]
        pipe_empty = pd.isnull(fp['upstream_node'].iloc[0])
        logging.warning(pipe_empty)
        if pipe_empty:
            logging.warning(pipe_empty)
            Pipes.objects.filter(pipe_id = str(fp.iloc[0]['pipe_id'])).update(order = 0, system = 0)
            chkd.extend(fp['pipe_id'])
        if fp['upstream_node'].iloc[0] == 'nan':
            pipe_empty = True
        if not pipe_empty:

            if not_in_list(fp,chkd):
                sys_no = sys_no + 1
                sys_lib[sys_no] = {}
                fdsp = find_furthest_downstream_pipe(df,fp)
                order = 1
                sys_lib[sys_no][order] = fdsp
                print("order")
                print(sys_no)
                print(order)
                Pipes.objects.filter(pipe_id = str(fdsp.iloc[0]['pipe_id'])).update(order = order, system = sys_no)
                chkd.extend(fdsp['pipe_id'])
                for row_i in df.index:
                    print(df.iloc[row_i]['pipe_id'])
                    print(fdsp.iloc[0]['pipe_id'])
                    if df.iloc[row_i]['pipe_id'] == str(fdsp['pipe_id']):
                        df.iloc[row_i]['order'] = order
                usp = next_upstream_pipe(df,fdsp)
                if not usp.empty:
                    range_0 = len(usp)
                    for rw in range(range_0):
                        cur_usp = usp.iloc[rw:rw+1]
                        if not cur_usp.empty:

                            order = order + 1
                            sys_lib[sys_no][order] = cur_usp
                            Pipes.objects.filter(pipe_id = str(cur_usp.iloc[0]['pipe_id'])).update(order = order, system = sys_no)
                            
                            while unchecked_entries(sys_lib[sys_no], chkd):
                                
                                pip = retrieve_unchecked_entry(sys_lib[sys_no], chkd)
                                chkd.extend(pip['pipe_id'])
                                usp_n = next_upstream_pipe(df,pip)
                                if not usp_n.empty:
                                        range_n = len(usp_n)
                                        for z in range(range_n):
                                            pip_z = usp_n.iloc[z:z+1]
                                            order = order + 1
                                            sys_lib[sys_no][order] = pip_z
                                            Pipes.objects.filter(pipe_id = str(pip_z.iloc[0]['pipe_id'])).update(order = order, system = sys_no)
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)

    all_pipe_entries = Pipes.objects.all().filter( project_id = active_project)
    df = read_frame(all_pipe_entries)
    df.sort_values(['system', 'order'], ascending=[True, True], inplace=True)
    #df.to_csv(r"C:\Users\Stude\OneDrive\Documents\Python Scripts\Geopak Import\Test_Output\Network_Order.csv")
    return redirect('index1')

def retrieve_unchecked_entry(sys, chkl):
    Range = len(sys)
    for row in sys:
        if sys[row]['pipe_id'].values[0] not in chkl:
            return sys[row]        

def unchecked_entries(sys, chkl):
    Range = len(sys)
    for row in sys:
        if sys[row]['pipe_id'].values[0] not in chkl:
            return True        
    return False

def not_in_list(single,chkl):
    dec = True 
    for entry in chkl:
        if single['pipe_id'].values[0] == entry:
            dec = False
    return dec

def find_furthest_downstream_pipe(df,pipe):
    if pd.isnull(pipe['upstream_node'].iloc[0]):
        return pipe
    ndsp = df.loc[ df['upstream_node'] == pipe.iloc[0]['downstream_node'] ]
    if not ndsp.empty:
        while not ndsp.empty:
            fdsp = ndsp
            ndsp = df.loc[ df['upstream_node'] == ndsp['downstream_node'].values[0] ]
        return fdsp
    else:
        return pipe

def next_upstream_pipe(df,pipe):
    nusp = df.loc[ df['downstream_node'] == pipe['upstream_node'].values[0] ]
    return nusp

def pipes_upstream(sys,pipe):
    usp = sys.loc[sys['downstream_node'] == pipe['upstream_node'] ]
    return usp

def pipe_size_to_integer(pipe_size):
    if 'Inch' in pipe_size:
        pipe_size_replace = pipe_size.replace(" Inch Dia. Circular","")
        pipe_size_integer = int(pipe_size_replace)
    if 'ft' in pipe_size:
        #pipe_size_replace = pipe_size.str.replace("*ft x *ft Box","*")
        #pipe_size_replace = [int(i) for i in pipe_size.split() if i.isdigit()]
        pipe_size_replace = re.findall(r"(\d+)ft Box", pipe_size)
        pipe_size_integer = int(pipe_size_replace[0]) * 12
    return pipe_size_integer

@login_required(login_url = 'login_page')
def analyse_systems(request):
    data = {'pipe_size':['12 Inch Dia. Circular','15 Inch Dia. Circular','18 Inch Dia. Circular','24 Inch Dia. Circular','30 Inch Dia. Circular',
        '36 Inch Dia. Circular','42 Inch Dia. Circular','48 Inch Dia. Circular','54 Inch Dia. Circular',
        '60 Inch Dia. Circular','66 Inch Dia. Circular','72 Inch Dia. Circular','78 Inch Dia. Circular','6ft x 6ft Box','8ft x 6ft Box'],
        'pipe_size_t':['minimum_depth_12_inch','minimum_depth_15_inch','minimum_depth_18_inch','minimum_depth_24_inch','minimum_depth_30_inch','minimum_depth_36_inch',
        'minimum_depth_42_inch','minimum_depth_48_inch','minimum_depth_54_inch','minimum_depth_60_inch','minimum_depth_66_inch',
        'minimum_depth_72_inch','minimum_depth_78_inch','minimum_depth_72_inch','minimum_depth_72_inch']}
    pipe_switcher = pd.DataFrame(data)
    pipe_switcher['pipe_size'] = pipe_switcher['pipe_size'].astype(str)
    active_project_0 = request.session['active_project']
    active_project = str(active_project_0)
    all_pipe_entries = Pipes.objects.all().filter(project_id = active_project)
    all_structure_entries = Structures.objects.all().filter(project_id = active_project)
    all_template_entries = Generic_Structures.objects.all()
    df = read_frame(all_pipe_entries)
    dfs = read_frame(all_structure_entries)
    dft = read_frame(all_template_entries)
    max_system = max(df['system']) + 1
    for sys in range(1,max_system):
        
        df_sys = df[(df['system'] == sys )]
        df_sys = df_sys.sort_values(by='order', ascending=False)
        sys_size = max(df_sys['order'])
        for rev_ord in range(0, sys_size):
            upstream_structure_id = df_sys.iloc[rev_ord]['upstream_node']
            upstream_structure = dfs.loc[dfs['structure_id'] == upstream_structure_id]
            upstream_structure_type = upstream_structure['type_and_size'].values[0]
            upstream_structure_template = dft.loc[dft['structure_type'] == upstream_structure_type]
            pipe_size = df_sys.iloc[rev_ord]['pipe_size']
            pipe_size_int = pipe_size_to_integer(pipe_size)
            pipe_size_refor = str(pipe_size).replace(' ','\s+')
            pipe_size_t = pipe_switcher[pipe_switcher['pipe_size'].str.contains(pipe_size_refor)]
            pipe_size_field = pipe_size_t["pipe_size_t"]
            upstream_structure_depth = upstream_structure_template[pipe_size_field]
            minimum_depth_upstream_structure = upstream_structure_depth[pipe_size_field].values[0]
            if math.isnan(float(minimum_depth_upstream_structure)):
                messages.warning(request, 'Minimum depth upstream structure is Null. Check pipe structure can fit pipe size' )
                break
            pipe = df_sys.iloc[rev_ord]
            pipe_id = str(pipe['pipe_id'])
            upstream_pipes = pipes_upstream(df_sys, pipe)
            inbound_inverts = []
            upstream_structure_Surface_elevation = upstream_structure['surface_elevation'].values[0]
            upstream_invert = upstream_structure_Surface_elevation - minimum_depth_upstream_structure
            upstream_invert = upstream_invert[0]
            gradient = pipe['design_gradient']
            upstream_structure_drop_structure = pipe['upstream_structure_drop_structure']
            if not upstream_pipes.empty:
                range_usp = len(upstream_pipes)
                for row in range(range_usp):
                    upstream_pipe = upstream_pipes.iloc[row]
                    upstream_pipe_downstream_invert = upstream_pipe['design_downstream_invert']
                    upstream_pipe_size = upstream_pipe['pipe_size']
                    upstream_pipe_size_int = pipe_size_to_integer(upstream_pipe_size)
                    if pipe_size == upstream_pipe_size:
                        drop = upstream_structure_template['drop_across_bottom'].values[0]
                    else:
                        drop = Decimal(pipe_size_int - upstream_pipe_size_int)/12
                    inbound_invert = upstream_pipe_downstream_invert - drop
                    inbound_inverts.append(inbound_invert)
                lowest_inbound_invert = min(Decimal(s) for s in inbound_inverts)  #float
                upstream_invert = min(upstream_invert,lowest_inbound_invert)
            Pipes.objects.filter(pipe_id = pipe_id).update( design_upstream_invert = upstream_invert)
            df_sys.loc[df_sys['pipe_id'] == pipe_id, 'design_upstream_invert'] = upstream_invert
            pipe_length = pipe['pipe_length']
            downstream_invert_from_gradient = upstream_invert - (gradient * pipe_length)
            downstream_structure_id = df_sys.iloc[rev_ord]['downstream_node']
            downstream_structure = dfs.loc[dfs['structure_id'] == downstream_structure_id]
            downstream_structure_type = downstream_structure['type_and_size'].values[0]
            downstream_structure_template = dft.loc[dft['structure_type'] == downstream_structure_type]
            downstream_structure_depth = downstream_structure_template[pipe_size_field]
            minimum_depth_downstream_structure = downstream_structure_depth[pipe_size_field].values[0]
            minimum_depth_downstream_structure = minimum_depth_downstream_structure.flat[0]
            downstream_structure_surface_elevation = downstream_structure['surface_elevation'].values[0]
            downstream_invert_from_minimum_depth = downstream_structure_surface_elevation - minimum_depth_downstream_structure
            downstream_invert = min(downstream_invert_from_gradient,downstream_invert_from_minimum_depth)
            if upstream_structure_drop_structure:
                minimum_gradient = Decimal(0.005)
                downstream_invert_from_gradient = upstream_invert - (minimum_gradient * pipe_length)
                downstream_invert = min(downstream_invert_from_gradient,downstream_invert_from_minimum_depth)
                upstream_invert = downstream_invert + (gradient * pipe_length)

            Pipes.objects.filter(pipe_id = pipe_id).update( design_downstream_invert = downstream_invert )
            df_sys.loc[df_sys['pipe_id'] == pipe_id, 'design_downstream_invert'] = downstream_invert

    return redirect('index1')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('index1')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('index1')

        return render(request, 'login.html' )

def logout_user(request):
    logout(request)
    return redirect('login_page')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('index1')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login_page')
        output = {'form' : form }
        return render(request, 'register.html', output)

def export_design(request):
    active_project_0 = request.session['active_project']
    active_project = str(active_project_0)
    all_pipe_entries = Pipes.objects.all().filter( project_id = active_project)
    df = read_frame(all_pipe_entries)
    #response = HttpResponse(content_type='text/csv')
    #response['Content-Disposition'] = 'attachment; filename=export.csv'
    #df.to_csv(path_or_buf=response, encoding='utf-8', index=False, sep='\t')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=PipeDesign.xlsx'
    writer = pd.ExcelWriter('pandasEx.xlsx',  
                   engine ='xlsxwriter') 
    # Write a dataframe to the worksheet. 
    df.to_excel(writer, sheet_name ='Sheet1') 
    # Close the Pandas Excel writer 
    # object and output the Excel file. 
    writer.save() 
    response.write(writer)
    return response
    
class PipesList(generics.ListCreateAPIView):
    queryset = Pipes.objects.all()
    serializer_class = PipesSerializer

class PipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pipes.objects.all()
    serializer_class = PipesSerializer

def empty_project(request):
    active_project_0 = request.session['active_project']
    active_project = str(active_project_0)
    Pipes.objects.filter(project_id = active_project).delete()
    return redirect('index1')