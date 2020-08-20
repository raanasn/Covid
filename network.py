import csv
import networkx as nx
import xlsxwriter
import multiprocessing


def multiprocessing_func(path,name,begin,end,workbook):
    for file_number in range(begin,end):
        print(file_number)
        worksheet = workbook.add_worksheet(str(file_number))
        print("creating graph ..")
        G = nx.Graph()
        with open(path + '/' + name + '/' + 'edge_' + name + "_" + str(file_number)+ '.csv', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                G.add_edge(row[0],row[2],weight=row[1])
        print(file_number," graph finished, calculating properties")
        '''GD=G.copy()
        GD = GD.to_directed()
        while 1==1:
            try:
                list_cycle=nx.find_cycle(GD)
            except:
                break
            GD.remove_edge(list_cycle[0][0], list_cycle[0][1])
        for c in nx.strongly_connected_components(GD):
                sub=GD.subgraph(c)
                print("periphery: ", nx.periphery(sub))
                print("center: ", nx.center(sub))
                print("longest path: ", nx.dag_longest_path_length(sub))'''
        col_num=0
        for c in sorted(nx.connected_components(G), key = len, reverse=True):
            sub=G.subgraph(c)
            p=nx.periphery(sub)
            c=nx.center(sub)
            row_num=0
            for item in p:
                worksheet.write(row_num,col_num,item)
                row_num+=1
            row_num = 0
            for item in c:
                worksheet.write(row_num, col_num+1, item)
                row_num += 1
            col_num = col_num+3
        print(file_number," ************************************")
    workbook.close()

    '''paths = nx.all_simple_paths(G, source='رونالدو', target='ایران')
    print(list(paths))'''


if __name__ == '__main__':
    name = "twitter"
    path = "F:\CovidChallenge\out"
    workbook = xlsxwriter.Workbook(name + '.xlsx')
    processes = []
    for i in range(1, 92,10):
        p = multiprocessing.Process(target=multiprocessing_func, args=(path,name,i,i+10,workbook))
        processes.append(p)
        p.start()
    p = multiprocessing.Process(target=multiprocessing_func, args=(path, name, 93, 95))
    processes.append(p)
    p.start()
    for process in processes:
        process.join()
