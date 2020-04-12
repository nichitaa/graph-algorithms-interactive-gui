from tkinter import *
from tkinter import ttk
from tkCanvasGraph import *
from collections import defaultdict
from heapq import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import filedialog

global final, new, new1
final , new, new1 = [], [], []

class Graph:
    global final
    final = []

    def __init__(self,vertices):
        self.V= vertices #No. of vertices
        self.graph = []
        self.graph_list_scc = defaultdict(list)
        self.new = []
        self.Time = 0

    def addEdgeScc(self,u,v):
        self.graph_list_scc[u].append(v)

    def clear_all_lists(self):
        global graph
        self.graph.clear()

    def SCCUtil(self,u, low, disc, stackMember, st):
        global final, new, new1
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        stackMember[u] = True
        st.append(u)
        for v in self.graph_list_scc[u]:
            if disc[v] == -1 :
                self.SCCUtil(v, low, disc, stackMember, st)
                low[u] = min(low[u], low[v])
            elif stackMember[v] == True:
                low[u] = min(low[u], disc[v])
        w = -1 #To store stack extracted vertices
        if low[u] == disc[u]:
            while w != u:
                w = st.pop()
                print (w, end='')
                new.append(w)

                stackMember[w] = False
            new1 = new.copy()
            new.clear()
            final.append(new1)

    def SCC(self):
        disc = [-1] * (self.V)
        low = [-1] * (self.V)
        stackMember = [False] * (self.V)
        st =[]
        for i in range(self.V):
            if disc[i] == -1:
                self.SCCUtil(i, low, disc, stackMember, st)

    def addEdge(self,u,v,w):
        self.graph.append([u,v,w])
    #  find set of an element i
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])
    # union of two sets of x and y
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else :
            parent[yroot] = xroot
            rank[xroot] += 1
    def KruskalMST(self):
        global result
        result = []
        i = 0
        e = 0
        self.graph =  sorted(self.graph,key=lambda item: item[2])
        parent = [] ; rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V -1 :
            u,v,w =  self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent ,v)
            if x != y:
                e = e + 1
                result.append([u,v,w])
                self.union(parent, rank, x, y)
        return result


edges, verticles ,edges_dj= [], [], []
edges_djikstra, res_path ,res1= [], [], []
after ,final1, str_final= [], [], []

def SCC_Algorithm(event):
    global final, g , verticles, edges, final1, str_final
    final.clear()
    final1.clear()
    str_final.clear()

    n = len(verticles)
    print("--------vertices nr")
    print(n)
    g = Graph(n)

    for i in range(len(edges)):
        ver1 = edges[i][0].label
        v1 = int(ver1)
        ver2 = edges[i][1].label
        v2 = int(ver2)
        str_weight = edges[i][2].label
        int_weight = int(str_weight)
        g.addEdgeScc(v1,v2)
    g.SCC()
    print("before======")
    print(final)

    for i in range(len(final)):
        str_final = [str(item) for item in final[i]]
        final1.append(str_final)
    print(final1)
    for i in range(len(final1)):
        print('final1 ------')
        print(final1[i])
        for j in range(len(edges)):
            q = 0
            if edges[j][0].label in final1[i]:
                if edges[j][1].label in final1[i]:
                    q = 1
                    print('----here----')
                if q == 0:
                    frame.canvas.delete_element(edges[j][2])
                    after.append(edges[j][2])



def splitscc(l,n):
    new = []
    for i in range(0, len(l)):
        j=i-1
        if j==-1:
            pass
        if len(l)==1:
            new.append(l)
            return new
        else:
            new.append([l[j],l[i]])
    return new


def dijkstra(edges, f, t):
    g1 = defaultdict(list)
    for l,r,c in edges:
        g1[l].append((c,r))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path += (v1, )
            if v1 == t: return (cost, path)

            for c, v2 in g1.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf")


def search(x):
    x1 = x
    for i in range(len(verticles)):
        if verticles[i].label == x1:
            return i
    return 1000


def search_weight(u,v,w):
    global edges
    x = 0
    for i in range(len(edges)):
        if edges[i][0].label == u and edges[i][1].label == v:
            x = 1
            print('nu poate acelasi drum sa aiba 2 lungimi diferite')
            return x
    return x

def add_edge(event):
    global verticles, edges, edges_dj, edges_djikstra

    u = vertexA.get()
    v1 = int(u)
    v = vertexB.get()
    v2 = int(v)
    w = weight.get()
    wght = int(w)
    if not u.isdigit():
        return
    if not v.isdigit():
        return
    if not w.isdigit():
        return
    #g.addEdge(v1,v2,wght)
    vertexA.delete(0, END)
    vertexB.delete(0, END)
    weight.delete(0,  END)
    if u == v :
        return
        print('equal edges')

    idx_u = search(u)
    #print(idx_u)
    idx_v = search(v)
    #print(idx_v)
    wgh_exists = search_weight(u,v,w)

    if idx_u == 1000 and idx_v == 1000:
        u = Vertex(frame.canvas, label=u)
        frame.canvas.add_vertex(u)

        v = Vertex(frame.canvas, label=v)
        frame.canvas.add_vertex(v)

        verticles.append(u)
        verticles.append(v)

        edge = Edge(frame.canvas, u, v, label=w)
        frame.canvas.add_edge(edge)
        edges.append([u, v, edge])
        edges_dj.append([u,v,wght])
        edges_djikstra.append([u.label, v.label, wght])

    if idx_u != 1000 and idx_v == 1000:
        v = Vertex(frame.canvas, label=v)
        frame.canvas.add_vertex(v)
        edge = Edge(frame.canvas,verticles[idx_u], v, label=w)
        frame.canvas.add_edge(edge)
        verticles.append(v)
        edges.append([verticles[idx_u], v, edge])
        edges_dj.append([verticles[idx_u],v,wght])
        edges_djikstra.append([verticles[idx_u].label, v.label, wght])

    if idx_u == 1000 and idx_v != 1000:
        u = Vertex(frame.canvas, label=u)
        frame.canvas.add_vertex(u)
        edge = Edge(frame.canvas,u, verticles[idx_v], label=w)
        frame.canvas.add_edge(edge)
        verticles.append(u)
        edges.append([u,verticles[idx_v], edge])
        edges_dj.append([u,verticles[idx_v],wght])
        edges_djikstra.append([u.label, verticles[idx_v].label, wght])

    if  idx_u != 1000 and idx_v != 1000 and wgh_exists == 0:
        exit = 0
        for i in range(len(edges)):
            if edges[i][0].label == u and edges[i][1].label == v and edges[i][2].label == w:
                exit = 1
        if exit == 0:
            edge = Edge(frame.canvas,verticles[idx_u], verticles[idx_v], label=w)
            frame.canvas.add_edge(edge)
            edges.append([verticles[idx_u], verticles[idx_v], edge])
            edges_dj.append([verticles[idx_u],verticles[idx_v],wght])
            edges_djikstra.append([verticles[idx_u].label, verticles[idx_v].label, wght])

    for i in range(len(edges)):
        print(edges[i][0].label)
        print(edges[i][1].label)
        print(edges[i][2].label)


def singleVertex(event):
    global verticles, edges
    u = entry_vertex.get()
    if not u.isdigit():
        return
    entry_vertex.delete(0, END)
    esi = 0
    for i in range(len(verticles)):
        if verticles[i].label == u:
            esi = 1
    if esi == 0:
        u = Vertex(frame.canvas, label=u)
        frame.canvas.add_vertex(u)
        verticles.append(u)


    for i in range(len(verticles)):
        print(verticles[i].label)


def refresh_graph(event):
    global verticles, edges,edges_dj, edges_djikstra, res_path, res1, new
    for j in range(len(edges)):
        frame.canvas.delete_element(edges[j][2])
    for i in range(len(verticles)):
        frame.canvas.delete_element(verticles[i])
    verticles.clear()
    edges.clear()
    edges_dj.clear()
    edges_djikstra.clear()
    #g.clear_all_lists()



def Kruskal1(event):
    global result, edges, g, verticles, after
    n = len(verticles)
    g = Graph(n)
    for i in range(len(edges)):
        ver1 = edges[i][0].label
        v1 = int(ver1)
        ver2 = edges[i][1].label
        v2 = int(ver2)
        str_weight = edges[i][2].label
        int_weight = int(str_weight)
        g.addEdge(v1,v2,int_weight)

    g.KruskalMST()
    print(result)
    print("---------")
    for i in range(len(edges)):
        exists = 0
        for j in range(len(result)):
            vertexul1 = int(edges[i][0].label)
            vertexul2 = int(edges[i][1].label)
            greutatea = int(edges[i][2].label)
            if vertexul1 == result[j][0] and vertexul2 == result[j][1] and greutatea == result[j][2] :
                print(vertexul1)
                print(vertexul2)
                print(greutatea)
                print(i)
                print(j)
                print(exists)
                exists = 1
        if exists == 0 :
            frame.canvas.delete_element(edges[i][2])
            after.append(edges[i][2])
    path_weight = 0
    for i in range(len(result)):
        path_weight = path_weight + result[i][2]
    print('path weight')
    print(path_weight)
    kruskal_weight["text"] = "Total weight for this path is :  {}".format(path_weight)


def Djikstra_frame(event):
    global edges_dj, edges_djikstra, edges, res_path, res1, new, after
    after.clear()
    start_pos = start_entry.get()
    end_pos = end_entry.get()

    res1 = dijkstra(edges_djikstra, start_pos, end_pos)
    print(res1)
    print(res1[0])
    res_path = res1[1]
    print(res_path)
    edge_size = 2
    new = list(split2(res_path,edge_size))
    print(new)
    index_to_delete = []
    for i in range(len(edges)):
        exists = 0
        for j in range(len(new)):
            vertexul1 = edges[i][0].label
            vertexul2 = edges[i][1].label
            greutatea1 = int(edges[i][2].label)

            if vertexul1 == new[j][0] and vertexul2 == new[j][1] :
                exists = 1
        if exists == 0:
            frame.canvas.delete_element(edges[i][2])
            index_to_delete.append(i)
            after.append(edges[i][2])

    djikstra_weight["text"] = "Total weight for this path is :  {}".format(res1[0])
    '''print(index_to_delete)
    for i in range(len(edges)):
        print(edges[i])
    for i in range(len(edges)):
        for j in range(len(index_to_delete)):
            if i == index_to_delete[j]:
                del edges[j]'''

def rebuild2(event):
    global edges, verticles, edges_dj, edges_djikstra, after
    for i in range(len(after)):
        frame.canvas.add_edge(after[i])
    after.clear()
    djikstra_weight["text"] = "Total weight for this path is :__"
    kruskal_weight["text"] = "Total weight for this path is :__"

def split2(l, n):
    new = []
    for i in range(0, len(l)):
        j=i-1
        if j == -1:
            pass
        else:
            new.append([l[j],l[i]])
    return new


def exit():
    root.destroy()
    root1.destroy()


def Import():
    global verticles, edges, edges_dj, edges_djikstra
    of = askopenfilename()
    file = open(of, "r")

    listed = []

    count = 0

    with open(of, 'r') as f:
        for items in f:
            count += 1
    print("Total number of lines is:", count)

    for i in range(0, count):
        line = file.readline()
        for u in line.split(' '):
            listed.append(u)
        vertex1 = listed[0]
        vertex2 = listed[1]
        weight_1 =listed[2].rstrip()
        weight_int = int(weight_1)

        print(vertex1)
        print(vertex2)
        print(weight_1)

        idx_v1 = search(vertex1)
        #print(idx_u)
        idx_v2 = search(vertex2)
        #print(idx_v)

        if idx_v1 == 1000 and idx_v2 == 1000:
            vertex1 = Vertex(frame.canvas, label=vertex1)
            frame.canvas.add_vertex(vertex1)

            vertex2 = Vertex(frame.canvas, label=vertex2)
            frame.canvas.add_vertex(vertex2)

            verticles.append(vertex1)
            verticles.append(vertex2)

            edge = Edge(frame.canvas, vertex1, vertex2, label=weight_1)
            frame.canvas.add_edge(edge)
            edges.append([vertex1, vertex2, edge])
            edges_dj.append([vertex1,vertex2,weight_int])
            edges_djikstra.append([vertex1.label, vertex2.label, weight_int])

        if idx_v1 != 1000 and idx_v2 == 1000:
            vertex2 = Vertex(frame.canvas, label=vertex2)
            frame.canvas.add_vertex(vertex2)
            edge = Edge(frame.canvas,verticles[idx_v1], vertex2, label=weight_1)
            frame.canvas.add_edge(edge)
            verticles.append(vertex2)
            edges.append([verticles[idx_v1], vertex2, edge])
            edges_dj.append([verticles[idx_v1], vertex2, weight_int])
            edges_djikstra.append([verticles[idx_v1].label, vertex2.label, weight_int])

        if idx_v1 == 1000 and idx_v2 != 1000:
            vertex1 = Vertex(frame.canvas, label=vertex1)
            frame.canvas.add_vertex(vertex1)
            edge = Edge(frame.canvas,vertex1, verticles[idx_v2], label=weight_1)
            frame.canvas.add_edge(edge)
            verticles.append(vertex1)
            edges.append([vertex1,verticles[idx_v2], edge])
            edges_dj.append([vertex1,verticles[idx_v2],weight_int])
            edges_djikstra.append([vertex1.label, verticles[idx_v2].label, weight_int])

        if  idx_v1 != 1000 and idx_v2 != 1000:
            exit = 0
            for i in range(len(edges)):
                if edges[i][0].label == vertex1 and edges[i][1].label == vertex2 and edges[i][2].label == weight_1:
                    exit = 1
            if exit == 0:
                edge = Edge(frame.canvas,verticles[idx_v1], verticles[idx_v2], label=weight_1)
                frame.canvas.add_edge(edge)
                edges.append([verticles[idx_v1], verticles[idx_v2], edge])
                edges_dj.append([verticles[idx_v1],verticles[idx_v2],weight_int])
                edges_djikstra.append([verticles[idx_v1].label, verticles[idx_v2].label, weight_int])
        listed.clear()


def Export():

    file = filedialog.asksaveasfile(mode="w")
    if file != None:
        for i in range(len(edges)):
            vertexul1 = edges[i][0].label
            vertexul2 = edges[i][1].label
            greutatea = edges[i][2].label
            file.write(vertexul1+' ')
            file.write(vertexul2+' ')
            file.write(greutatea+'\n')


    file.close()


def delete_an_edge(event):
    global edges_dj, edges_djikstra, edges, res_path, res1, new, verticles
    v1_to_delete = vertexA_delete.get()
    v2_to_delete = vertexB_delete.get()
    w_to_delete = weight_delete.get()

    vertexA_delete.delete(0, END)
    vertexB_delete.delete(0, END)
    weight_delete.delete(0,  END)

    print("verticles")
    for i in range(len(verticles)):
        print(verticles[i].label)
    print("edges")
    for i in range(len(edges)):
        print(edges[i][0].label)
        print(edges[i][1].label)
        print(edges[i][2].label)
    vert1 = 1000
    vert2 = 1000
    for i in range(len(edges)):
        if edges[i][0].label == v1_to_delete and edges[i][1].label == v2_to_delete and edges[i][2].label == w_to_delete:
            frame.canvas.delete_element(edges[i][2])
            vert1 = edges[i][0].label
            vert2 = edges[i][1].label
            del edges[i]
            del edges_djikstra[i]
            del edges_dj[i]
            print('verticles delet')
            print(vert1)
            print(vert2)
            break
    if vert1 != 1000 and vert2 != 1000:
        e1=0
        e2=0

        for i in range(len(edges)):
            e1 = 0
            if vert1 == edges[i][0].label or vert1 == edges[i][1].label:
                e1 = 1
                break

        for i in range(len(edges)):
            e2 = 0
            if vert2 == edges[i][0].label or vert2 == edges[i][1].label:
                e2 = 1
                break
        if e1 == 0:
            for i in range(len(verticles)):
                if verticles[i].label == vert1:
                    frame.canvas.delete_element(verticles[i])
                    del verticles[i]
        if e2 == 0:
            for i in range(len(verticles)):
                if verticles[i].label == vert2:
                    frame.canvas.delete_element(verticles[i])
                    del verticles[i]


    print("new------verticles")
    for i in range(len(verticles)):
        print(verticles[i].label)
    print("new--------edges")
    for i in range(len(edges)):
        print(edges[i][0].label)
        print(edges[i][1].label)
        print(edges[i][2].label)


def about():
    answer = askokcancel(\
"Info",\
"This is a simple program on graph representation algorithms.\
In order to add an edge to the graph window,\
the vertices must be integers no other symbols are accepted for \
labeling the vertices(for weights too).\n\
Created by Nichita Pasecinic, first year software engineer\n\
Date : 25/03/2020")


def help():
    help = askokcancel("How to use Kruskal/Dijkstra","In order to create a valid graph for Kruskal algorighm \
on NON ORIENTED graph is necessary to add all edges in a correct way. First, \
enter the vertex '0' into the box '<< Vertex 1', and start built connections \
from vertex '0' to the rest of vertices, after all connections are build for \
the first vertex(0) start building edges for next vertex '1',  the order is \
important, connections must be consecutive. \n\
Example : \n\
'0 - vertex1'  \n\
'1 - veretx2'  \n\
'5 - weight'    \n\
                \n\
'0 - vertex1' \n\
'3 - veretx2'\n\
'7 - weight'\n\
\n\
'0 - vertex1'\n\
'2 - veretx2'\n\
'5 - weight'\n\
\n\
'0 - vertex1'\n\
'1 - veretx2'\n\
'5 - weight'\n\
Those are all connections for vertex 0\n\
'1 - vertex1'\n\
'2 - veretx2'\n\
'9 - weight'\n\
\n\
'1 - vertex1'\n\
'3 - veretx2'\n\
'5 - weight'\n\
Those are all connections for vertex 1\n\
\n\
'2 - vertex1'\n\
'3 - veretx2'\n\
'8 - weight'\n\
Those are all connections for vertex 2\n\
For Dijkstra algorithm the order of inputing the edges does not matter. \
Input the start vertex and the end vertex from already created graph \
and press the button 'dijkstra algorithm' , on the graph will remain \
the shortesth path for chosen vertices and the vertices that were not included \
in the path.\
")

top_block = "#b0bec5"
highlight_backg = top_block

txt_color = "#000000"
alg_color = txt_color

ufo = "#cfd8dc"
bg_alg = ufo

on_click ="#e2f1f8"

entry_color = "#eceff1"

buttons_color = "#eeeeee"

root = Tk()
root1 = Tk()
root1.geometry("700x760+20+20")
root1.title("YOUR GRAPH")
root.title("GRAPHS ALGORITHMS (SDA-project)")
root.geometry("760x760+721+20")
root.configure(bg=ufo)


root.iconbitmap(r'cat.ico')
root1.iconbitmap(r'cat.ico')


main_menu = Menu(root)
root.configure(menu=main_menu)

first_item = Menu(main_menu, tearoff=0,background=ufo, foreground='#000000',activebackground='#eeeeee', activeforeground='#000000')
main_menu.add_cascade(label="Menu", menu=first_item)


first_item.add_command(label="Import graph", command=Import)
first_item.add_command(label="Export graph", command=Export)
first_item.add_command(label="Help", command=help)
first_item.add_command(label="About", command=about)
first_item.add_command(label="Exit", command=exit)


frame = CanvasFrame(root1)
frame.pack(fill="both", expand=TRUE)

# FRAME 1   ........................  ADD A NEW EDGE .................

frame1 = Frame(root, bg=ufo,  highlightbackground=highlight_backg, highlightthickness=2)
frame1.grid(row=0, column=0, sticky=NSEW)

l0=Label(frame1, text=" ADD A NEW EDGE TO GRAPH  ", font="Times 16 bold", bg=top_block ,relief=RAISED, fg=txt_color)
l1=Label(frame1, text="<<  vertex 1",  font="Times 16", bg=ufo, fg=txt_color)
l2=Label(frame1, text="<<  vertex 2",  font="Times 16", bg=ufo, fg=txt_color)
l3=Label(frame1, text="<<  edge weight",font="Times 16", bg=ufo, fg=txt_color)
add_button = Button(frame1, text="add edge", width=12, font="Times 10", bg=buttons_color, fg=txt_color, activebackground=on_click)
delete_graph = Button(frame1, text="delete graph", width=10, height=1, font="Times 10", bg=buttons_color, fg=txt_color, activebackground=on_click)

vertexA = Entry(frame1, font=14, width=10, bg=entry_color, fg=txt_color)
vertexB = Entry(frame1, font=14, width=10, bg=entry_color, fg=txt_color)
weight =  Entry(frame1, font=14, width=10, bg=entry_color, fg=txt_color)

l0.grid(row=0, columnspan=2, sticky=NSEW)
l1.grid(row=1, column=1, sticky=W)
l2.grid(row=2, column=1, sticky=W)
l3.grid(row=3, column=1, sticky=W)

vertexA.grid(row=1, column=0,  sticky=E)
vertexB.grid(row=2, column=0,  sticky=E)
weight.grid(row=3 , column=0, sticky=E)
add_button.grid(row=4, column=0, sticky=E)
delete_graph.grid(row=4,column=1)
# FRAME 2 .....................................  ADD A SINGLE VERTEX ............................

frame2= Frame(root, bg=ufo,  highlightbackground=highlight_backg, highlightthickness=2)
frame2.grid(row=1, column=1, sticky=NSEW)

single_vertex=Label(frame2, text="ADD A SINGLE VERTEX TO GRAPH", font="Times 16 bold", bg=top_block, relief=RAISED, fg=txt_color, width=35)
label_vertex=Label(frame2,text="<<  vertex          ",  font="Times 16", bg=ufo, fg=txt_color,)
entry_vertex = Entry(frame2, font=14,  bg=entry_color, fg=txt_color, width=10)
add_vertex_button = Button(frame2, text="add vertex",font="Times 10" ,width=12, bg=buttons_color, fg=txt_color, activebackground=on_click)

single_vertex.grid(row=0, columnspan=2)
label_vertex.grid(row=1, column=1, sticky=W)
entry_vertex.grid(row=1, column=0, sticky=E)
add_vertex_button.grid(row=2,column=0, sticky=E)

# FRAME 3 ........................................ DIJKSTRA .....................................

frame3= Frame(root, bg=ufo,  highlightbackground=highlight_backg, highlightthickness=2)
frame3.grid(row=1, column=0, sticky=NSEW)

dj_label = Label(frame3, text="  FOR DIJKSTRA ALGORITHM  ", font="times 16 bold", bg=top_block, relief=RAISED, fg=txt_color)
start_label = Label(frame3,text="<< start vertex",  font="times 16", bg=ufo, fg=txt_color)
end_label = Label(frame3,text="<< end  vertex",  font="times 16", bg=ufo, fg=txt_color)
start_entry = Entry(frame3, font=14, width=10, bg=entry_color, fg=txt_color)
end_entry = Entry(frame3, font=14, width=10, bg=entry_color, fg=txt_color)

dj_label.grid(row=0, columnspan=2, sticky=W)
start_label.grid(row=1, column=1, sticky=W)
end_label.grid(row=2, column=1, sticky=W)
start_entry.grid(row=1, column=0, sticky=E)
end_entry.grid(row=2, column=0, sticky=E)

# FRAME 4 ...................................... ALGORITHMS DESCTRIPTION ..........................................

frame4 = Frame(root,  highlightbackground=highlight_backg, highlightthickness=2, bg=top_block)
frame4.grid(row=2, column=0 ,columnspan=2, sticky=NSEW)

algorithm = Label(frame4, text="                                  ALGORITHMS DESCRIPTION    ", font="times 16 bold", bg=top_block, fg=alg_color)
algorithm.grid(row=0, column=0, columnspan=3,sticky=NSEW)

# FRAME 5 ...................................... KRUSKAL BUTTON..............................................

frame5 = Frame(root, bg=bg_alg,  highlightbackground=top_block, highlightthickness=2)
frame5.grid(row=3, column=0, sticky=NSEW)

kruskal_button = Button(frame5, text="Kruskal algorithm  ", font='times 12', fg=alg_color, bg=buttons_color, activebackground=on_click)
kruskal_button.grid(row=0, column=0, padx=3, pady=3)
back_button_kruskal = Button(frame5, text=" ⤺ back to the graph ", font='times 12', fg=alg_color, bg=buttons_color, activebackground=on_click)
back_button_kruskal.grid(row=0, column=1, padx=3, pady=3)

kruskal_weight = Label(frame5, text="Total weight for this path is :__", bg=ufo, fg=txt_color, font='times 16')
kruskal_weight.grid(row=1,column=0, columnspan=3, sticky=NSEW)


# FRAME 6 ..................................... KRUSKAL ALGORITHM INFO .................................

frame6 = Frame(root, bg=bg_alg,  highlightbackground=top_block, highlightthickness=2)
frame6.grid(row=3, column=1, columnspan=2, sticky=NSEW)

kruskal_label = Label(frame6, text= \
"- is a minimum-spanning-tree algorithm which finds an edge of the  least  \n\
possible weight that connects any two trees in the forest. It is a greedy              \n\
algorithm in graph theory as it finds a minimum spanning tree for a connected \n\
weighted graph adding increasing cost arcs at each step. This means it finds \n\
a subset of the edges that forms a tree that includes every vertex, where the \n\
total weight of all the edges in the tree is minimized." , bg=bg_alg, font="times 10",relief=GROOVE,fg=alg_color)
kruskal_label.grid(row=0,column=0,rowspan=3, sticky=NSEW)

# FRAME 7 .................................... DIJKSTRA BUTTON ..........................................

frame7 = Frame(root, bg=bg_alg,  highlightbackground=top_block, highlightthickness=2)
frame7.grid(row=4, column=0, sticky=NSEW)

djikstra_button = Button(frame7, text="Djikstra algorithm  ", font="times 12", fg=alg_color, bg=buttons_color, activebackground=on_click)
djikstra_button.grid(row=0, column=0, padx=3, pady=3)
back_button_djikstra = Button(frame7, text=" ⤺ back to the graph ", font='times 12', fg=alg_color, bg=buttons_color, activebackground=on_click)
back_button_djikstra.grid(row=0, column=1, padx=3, pady=3)

djikstra_weight = Label(frame7, text="Total weight for this path is :__", bg=ufo, fg=txt_color, font='times 16')
djikstra_weight.grid(row=1, column=0, columnspan=4)

# FRAME 8 ......................................... DIJKSTRA ALGORITHM INFO .............................

frame8 = Frame(root, bg=bg_alg,  highlightbackground=top_block, highlightthickness=2)
frame8.grid(row=4, column=1, columnspan=2, sticky=NSEW)

djikstra_label = Label(frame8, text= \
"- is an algorithm for finding the shortest paths between nodes in a graph,           \n \
which may represent, for example, road networks. In this exemple, the \n\
algorithm will show the shortest path between 'Start vertex' and 'End vertex' \n\
in a directed graph. Input first the 'Start vertex' and 'End vertex' before \n\
pressing the button 'dijkstra algorithm' ." , bg=bg_alg, font="times 10", relief=GROOVE, fg=alg_color)
djikstra_label.grid(row=0,column=0,rowspan=3, sticky=NSEW)

# FRAME 9 ....................................... DELETE AN EDGE ..........................................

frame9 = Frame(root, bg=ufo,  highlightbackground=highlight_backg, highlightthickness=2)
frame9.grid(row=0, column=1, sticky=NSEW)

delete_edge_label = Label(frame9, text=" REMOVE AN EDGE FROM THE GRAPH     ", font="Times 16 bold", bg=top_block, relief=RAISED , fg=txt_color)
vertex1_delete=Label(frame9, text="<<  vertex 1",  font="Times 16", bg=ufo, fg=txt_color)
vertex2_delete=Label(frame9, text="<<  vertex 2",  font="Times 16", bg=ufo, fg=txt_color)
weight_delete_label=Label(frame9, text="<<  edge weight",font="Times 16", bg=ufo, fg=txt_color)
delete_dege_button = Button(frame9, text="delete", width=12, font="Times 10",bg=buttons_color, fg=txt_color, activebackground=on_click)


vertexA_delete = Entry(frame9, font=14, width=10, bg=entry_color, fg=txt_color)
vertexB_delete = Entry(frame9, font=14, width=10, bg=entry_color, fg=txt_color)
weight_delete =  Entry(frame9, font=14, width=10, bg=entry_color, fg=txt_color)


delete_edge_label.grid(row=0, columnspan=2, sticky=NW)
vertex1_delete.grid(row=1, column=1, sticky=W)
vertex2_delete.grid(row=2, column=1, sticky=W)
weight_delete_label.grid(row=3, column=1, sticky=W)


vertexA_delete.grid(row=1, column=0, sticky=E)
vertexB_delete.grid(row=2, column=0, sticky=E)
weight_delete.grid(row=3 , column=0, sticky=E)
delete_dege_button.grid(row=4, column=0, sticky=E)

# FRAME 10 ....................................... SCC ALGORITH BUTTON .....................................

frame10 = Frame(root, bg=bg_alg,  highlightbackground=top_block, highlightthickness=2)
frame10.grid(row=5, column=0, sticky=NSEW)

scc_button = Button(frame10, text="  SCC algorithm    ", font="times 12", fg=alg_color, bg=buttons_color, activebackground=on_click)
scc_button.grid(row=0, column=0, padx=3, pady=3)
back_button_scc = Button(frame10, text=" ⤺ back to the graph ", font='times 12', fg=alg_color, bg=buttons_color, activebackground=on_click)
back_button_scc.grid(row=0, column=1, padx=3, pady=3)

scc_alg = Label(frame10, text="Strongly connected components", bg=ufo, fg=txt_color, font='times 16')
scc_alg.grid(row=1, column=0, columnspan=4)

# FRAME 11 .......................................SCC ALGORITHM INFO .......................................

frame11 = Frame(root, bg=bg_alg,  highlightbackground=top_block, highlightthickness=2)
frame11.grid(row=5, column=1, columnspan=2, sticky=NSEW)

scc_label = Label(frame11, text= \
"A directed graph is called strongly connected if there is a path in each      \n\
direction between each pair of vertices of the graph. That is, a path exists     \n\
from the first vertex in the pair to the second, and another path exists from         \n\
the second vertex to the first. In a directed graph G that may not itself be       \n\
strongly connected, a pair of vertices u and v are said to be strongly         \n\
connected to each other if there is a path in each direction between them." , bg=bg_alg, font="times 10", relief=GROOVE, fg=alg_color)
scc_label.grid(row=0,column=0,rowspan=3, sticky=NSEW)

# FRAME 12 ...................................... CREATOR .................................................


frame12 = Frame(root, bg=bg_alg,  highlightbackground=top_block, highlightthickness=0)
frame12.grid(row=6, column=1, columnspan=2, sticky=NSEW)

photo = PhotoImage(file="150.png", width=150, height=150)
ph_label = Label(frame12, image=photo, bg=bg_alg)

me = Label(frame12, text=" ", bg=ufo, fg=txt_color, font='times 12' )
nichita = Label(frame12, text="Author : Nichita Pasecinic", bg=ufo, fg=txt_color, font='times 12' )
#me.grid(row=0, column=0, sticky=NW)
nichita.pack(side=BOTTOM, anchor=E)
ph_label.pack(side=RIGHT)
me.pack(side=TOP, anchor=E)



back_button_scc.bind("<Button-1>",rebuild2 )
scc_button.bind("<Button-1>", SCC_Algorithm)
delete_dege_button.bind("<Button-1>", delete_an_edge)
add_button.bind("<Button-1>", add_edge)
kruskal_button.bind("<Button-1>", Kruskal1)
djikstra_button.bind("<Button-1>", Djikstra_frame)
add_vertex_button.bind("<Button-1>", singleVertex)
delete_graph.bind("<Button-1>", refresh_graph)
back_button_kruskal.bind("<Button-1>", rebuild2)
back_button_djikstra.bind("<Button-1>", rebuild2)


root.mainloop()
