import os
import shutil
import time

def get_file(source):
    """This is return the every signle file as well as folder present in the
     folder even if it is inside another folder inside it"""
    a=os.listdir(source)
    list_of_file=[]
    for i in a:
        full_path=os.path.join(source,i)
        if os.path.isdir(full_path):
            list_of_folder.append(full_path)
            list_of_file=list_of_file+get_file(full_path)
        else:
            list_of_file.append(full_path)
    return list_of_file

def get_file_size(file):
    """This will return the file size of every file present"""
    file_size=[]
    for i in file:
        a = os.path.getsize(i) #This will give the file size in bytes
        file_size.append(a)
    return file_size

def backup_file_location(file,folder,source,backup):
    """This will generate the backup location of the source file"""
    backup_file_path=[]
    backup_file_folder=[]
    for i in file:
        string=''
        string=i.replace(source,backup)
        backup_file_path.append(string) 
    for i in folder:
        string=''
        string=i.replace(source,backup)
        backup_file_folder.append(string) 
    return backup_file_path,backup_file_folder

def storage_check_and_copy(main_backup_file,main_backup_folder):
    """It will check if storage is enough to copy or not then print the progress of file transfered
        with percentage speed and time remaining and also copy the file using shutil"""
    total_storage_required=0
    for i in main_backup_file:
        a = os.path.getsize(i[0])
        total_storage_required+=a
    stat = shutil.disk_usage(backup) #this will give the total available and used storage in the device
    if stat[2]>total_storage_required:
        print(f"\n\t\tTOTAL STORAGE REQUIRED = {round(total_storage_required/1024,2)}KB or {round(total_storage_required/1048576,2)}MB or {round(total_storage_required/1073741824,2)}GB")
        print(f"\n\t\tTOTAL STORAGE AVAILABLE = {round(stat[2]/1024,2)}KB or {round(stat[2]/1048576,2)}MB or {round(stat[2]/1073741824,2)}GB\n")
        # shutil.copy2(main_path[count],backup_path[count])
        initial_storage=stat[1] #this will return the used storage in the drive
        current_storage=initial_storage
        initial_time=time.time()#this will return the current time in second
        current_time=initial_time
        try:
            if len(main_backup_file)==0:
                print("\n\t\t    BACKUP DONE       ")
                exit()
            else:
                increase=100/len(main_backup_file)   #percentage increase at every file transfered
                count=0                              #initial file trasfered percentage
                for i in main_backup_folder:
                    os.mkdir(i)
                for i in main_backup_file:
                    try:
                        speed=(current_storage-initial_storage)/((current_time-initial_time)*1048576) # return speed in MB/s
                        time_remaining=((total_storage_required-(current_storage-initial_storage))/1048576)/speed
                    except:
                        speed=0
                        time_remaining=0
                    if time_remaining>60:
                        time_remaining=time_remaining/60
                        if time_remaining>60:
                            time_remaining=str(round((time_remaining)/60,2))+" Hour"
                        else:
                            time_remaining=str(round(time_remaining,2))+" Min"
                    else:
                        time_remaining=str(round(time_remaining,2))+" Sec"
                    print(i[0],"-->",i[1],"      ",round(count,2),"% Done","      ",round(speed,2),"MB/s","      ",time_remaining,"Remaining")
                    shutil.copy2(i[0],i[1])
                    count+=increase
                    # initial_storage=current_storage #don't uncomment if you don't want instantenious speed
                    # initial_time=current_time #don't uncomment if you don't want instantenious speed
                    current_time=time.time()
                    current_storage=shutil.disk_usage(backup)[1]
                print("\n\t\t    BACKUP DONE       ")
        except Exception as e:
            print(e)
    else:
        print(f"\n\t\tTOTAL STORAGE REQUIRED = {round(total_storage_required/1024,2)}KB or {round(total_storage_required/1048576,2)}MB or {round(total_storage_required/1073741824,2)}GB")
        print(f"\n\t\tTOTAL STORAGE AVAILABLE = {round(stat[2]/1024,2)}KB or {round(stat[2]/1048576,2)}MB or {round(stat[2]/1073741824,2)}GB")
        print(f"\n\t\t KINDLY FREE UP SOME SPACE TO CONTINUE BACKUP PROCESS\n")
        retry=input("Type 'yes' if you want to retry:-  ")
        if "yes" in retry or "retry" in retry:
            storage_check_and_copy()
        else:
            exit()

def file_name_editor(trash,backup_path,file_no):
    """This will edit the file name if the same file is present in the destination location"""
    only_file_name=backup_path.split("/")[-1]
    name=only_file_name.split(".")
    name.insert(-1,str(file_no))
    only_file_name=".".join(name)    
    path=trash+"/"+only_file_name
    if os.path.exists(path):
        file_no+=1
        file_name_editor(trash,backup_path,file_no)
    else:
        location=[backup_path,path]
        main_backup_file.append(location)        


def backup_file_protection_module(backup_path,backup):
    """This will save the data present in the file earlier to the another folder named trash so
        if the data is changed in backuped file you have the chance to recover the original file
        while replacing the main file"""
    try:
        try:
            os.mkdir(trash)
        except:
            pass
        only_file_name=backup_path.split("/")[-1]
        path=trash+"/"+only_file_name
        if os.path.exists(path):
            file_no=1
            file_name_editor(trash,backup_path,file_no) 
        else:
            location=[backup_path,path]
            main_backup_file.append(location)        
        # shutil.copy2(backup_path,trash)
    except:
        pass

def backup_module(backup_folder,backup_path,main_path,main_file_size):
    """This will find the list of file in which file content has been changed"""
    count=0
    for i in backup_folder:
        if os.path.isdir(i):
            pass
        else:
            main_backup_folder.append(i)
            # os.mkdir(i)
    for j in backup_path:
        if os.path.exists(j):
            backup_file_size=os.path.getsize(j)
            if backup_file_size==main_file_size[count]:
                pass
            else:
                backup_file_protection_module(backup_path[count],backup)
                location=[main_path[count],backup_path[count]]
                main_backup_file.append(location)
                # shutil.copy2(main_path[count],backup_path[count])
        else:
            location=[main_path[count],backup_path[count]]
            main_backup_file.append(location)
            # shutil.copy2(main_path[count],backup_path[count])
        count+=1

def main(source,backup):
    main_file_path=get_file(source)
    main_file_size=get_file_size(main_file_path)
    backup_file_path,backup_file_folder=backup_file_location(main_file_path,list_of_folder,source,backup)
    backup_module(backup_file_folder,backup_file_path,main_file_path,main_file_size)


if __name__ == '__main__':
    # source="/mnt/Partition_2/mycodes/python codes/backup/system/"
    # backup='/mnt/Partition_2/mycodes/python codes/backup/pendrive/'  
      
    # source='/mnt/Partition_2/mycodes/'
    # backup='/media/abhishek/SD_CARD_32/mycodes/'
    source=input("\nSource location:- ")
    backup=input("\nBackup location:- ")
    main_backup_folder=[]
    main_backup_file=[]
    trash=backup+"trash" #I dont think so you need the "\" sign but we must have to check it in windows
    list_of_folder=[]
    print("Collecting files ....\n")
    main(source,backup)
    print("Files collected ....\n")
    initialization_time=time.time()
    storage_check_and_copy(main_backup_file,main_backup_folder)
    finalization_time=time.time()
    total_time=finalization_time - initialization_time
    if total_time>60:
        total_time=total_time/60
        if total_time>60:
            total_time=total_time/60
            print(f"Time taken to backup :- {round(total_time,2)} Hour")
        else:
            print(f"Time taken to backup :- {round(total_time,2)} Min")
    else:
        print(f"Time taken to backup :- {round(total_time,2)} Sec")