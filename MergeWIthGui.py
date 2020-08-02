import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from tkinter import*
import os, PyPDF2


root = Tk()

root.title("PDF merge")

#함수

    #파일 추가 
def add_file():

    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요", 
    filetypes = (("PDF 파일", "*.pdf"),("모든 파일", "*.*")), initialdir = "C:/")
    
    #출력
    for file in files: 
        list_file.insert(END, file)


    # 파일 삭제
def del_file():

    for index in reversed(list_file.curselection()):
        list_file.delete(index)

    # 저장 경로
def browse_dest_path():
    folder_selected  = filedialog.askdirectory()
    if folder_selected == '':
        return
    txt_dest_path.delete(0,END)
    txt_dest_path.insert(0, folder_selected)



def start():
 
    if list_file.size() == 0:
        msgbox.showinfo("파일 경로 없음","파일 경로를 지정해주세요.")
        return

    if len(txt_dest_path.get()) == 0:
        msgbox.showinfo(title="저장 경로 없음", message="저장 경로를 지정해주세요.")
        return
    
    if len(txt_dest_path.get()) == 0:
        msgbox.showinfo(title="저장명 없음", message="병합 파일명을 지정해주세요.")
        return
    merge_image()
    return

# pdf 통합 작업
def merge_image():

    # all_name = list_file.get(0)
    # len_all = len(all_name)
    # pdf_name = all_name.split('/')[-1]
    # len_pdf = len(pdf_name)

    # print(all_name[:len_all-len_pdf-1])



    pdf_list = list_file.get(0,END)
    
    
    pdf_merger = PyPDF2.PdfFileMerger(strict=False)
    progress = 0
    one_path = 0
    for one in pdf_list:
        
        all_name = one
        len_all = len(all_name)
        pdf_name = all_name.split('/')[-1]
        len_pdf = len(pdf_name)


        last_path = one_path
        one_path = all_name[:len_all-len_pdf-1]

        pdf_merger.append(one)
        
        if last_path != one_path:
            os.chdir(one_path)

        progress += 0.9/len(pdf_list)*100
        p_var.set(progress)
        progress_bar.update()

   
    os.chdir(txt_dest_path.get())    
    pdf_merger.write(new_name.get() +".pdf") 
    progress = 100
    p_var.set(progress)
    progress_bar.update()

    msgbox.showinfo("완료","병합이 완료되었습니다.")
    pdf_merger.close()
    return
        





#저장 경로
path_frame = LabelFrame(root, text="저장경로")
path_frame.pack(fill="x",padx =5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill = "x", expand=True, padx =5, pady=5, ipady=4)

btn_dest_path = Button(path_frame, text="찾아보기", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)




#list frame
list_frame = Frame(root)
list_frame.pack(fill="both",padx =5, pady=5)

lbl_list = Label(list_frame, text="병합할 파일",relief="sunken", width=68)
lbl_list.pack(side="top")

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode = "extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# 파일 프레임 (파일 추가, 선택 삭제)
file_frame = Frame(root)
file_frame.pack(padx =5, pady=5, fill='x')

# name_frame = LabelFrame(root, text="저장 파일명")
# name_frame.pack(side="right",padx =5, pady=5, ipady=5)
lbl_name = Label(file_frame, text="병합된 파일명: ", width=8, anchor="e")
lbl_name.pack(side="left", fill="x", expand=True)

new_name = Entry(file_frame)
new_name.pack(side="left", expand=True, padx =2, pady=2, ipady=4)


btn_add_file = Button(file_frame, padx=5, pady=5, width=10,text="파일 추가", command = add_file)
btn_add_file.pack(side="left",padx =5, pady=5)

btn_del_file = Button(file_frame, padx=5, pady=5, width=10,text="선택 삭제", command= del_file)
btn_del_file.pack(side="right",padx =5, pady=5)




# 진행 상황
frame_progress = LabelFrame(root, text="진행상황")
frame_progress.pack(fill="x",padx =5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x",padx =5, pady=5)

#실행 프레임

frame_run = Frame(root,padx =5, pady=5)
frame_run.pack(fill="x", ipady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)



root.resizable(False, False)
root.mainloop()
 