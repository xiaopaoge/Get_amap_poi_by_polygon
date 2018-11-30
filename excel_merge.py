import xlrd
import xlsxwriter
import os
 
#打开一个excel文件
def open_xls(file):
    fh=xlrd.open_workbook(file)
    return fh
 
#获取excel中所有的sheet表
def getsheet(fh):
    return fh.sheets()
 
#获取sheet表的行数
def getnrows(fh,sheet):
    table=fh.sheets()[sheet]
    return table.nrows
 
#读取文件内容并返回行内容
def getFilect(file,shnum):
    fh=open_xls(file)
    table=fh.sheets()[shnum]
    num=table.nrows
    for row in range(num):
        rdata=table.row_values(row)
        datavalue.append(rdata)
    return datavalue
 
#获取sheet表的个数
def getshnum(fh):
    x=0
    sh=getsheet(fh)
    for sheet in sh:
        x+=1
    return x
 

def all_file(path_par):
    path_list=[]
    for parent,dirnames,filenames in os.walk(path_par): #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:
            c=os.path.join(parent, filename)
            path_list.append(c)
    return path_list

if __name__=='__main__':
    #定义要合并的excel文件列表
    filepath=r''
    allxls=all_file(filepath)
    #存储所有读取的结果
    datavalue=[]
    for fl in allxls:
        fh=open_xls(fl)
        x=getshnum(fh)
        for shnum in range(x):
            print("正在读取文件："+str(fl)+"的第"+str(shnum)+"个sheet表的内容...")
            rvalue=getFilect(fl,shnum)
    #定义最终合并后生成的新文件
    endfile=r''
    wb1=xlsxwriter.Workbook(endfile)
    #创建一个sheet工作对象
    ws=wb1.add_worksheet()
    for a in range(len(rvalue)):
        for b in range(len(rvalue[a])):
            c=rvalue[a][b]
            ws.write(a,b,c)
    wb1.close()
    print("文件合并完成")
