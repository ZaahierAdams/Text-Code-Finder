from os import walk as os_walk
from os import path as os_path
from time import time as time

while True:

    # User inputs
    def inputs():
        source      = input('\n(1) Parent/source Directory: ')
        target      = input('\n(2) Text/Code to search for: ') 

        ex1         = input('\n(3) File extensions (eg. json, txt, etc...) separate extensions by comma: ')     # input
        ex2         = list(map(lambda ele: str.replace(ele.strip(), ".", ""), ex1.split(",")))                  # convert to list, strip whitespaces, remove dots
        ex3         = list(filter(None, ex2))                                                                   # remove empty strings
        extensions  = [ele.lower() for ele in ex3]                                                              # strings to lower

        file1       = input('\n(4) Search only for files with name (if left blank will search for all files): ')
        file2       = list(map(lambda ele: str.replace(ele, ".", ""), file1.split(",")))
        file3       = list(filter(None, file2))
        filenames   = [ele.lower() for ele in file3]
        
        return source, target, extensions, filenames


    # Console text for Progress
    def test_folder(type, item, tab):
        print(f"{tab}L Scanning {type}: {item}")


    # Error message when failed to read file
    def read_failure(name):
        print(f"\tL !!! FAILED reading {name} !!!")


    # Console decorator text
    def margin():
        return '-'*90


    # Console text for Results
    def results(source, target, extensions, filenames, searched_folders, searched_files, occur_total, read_fail, dict):
        
        extentions_text = extensions if len(extensions) > 0 else "< None >"
        filenames_text  = filenames if len(filenames) > 0 else "< All >"

        print("\n\n"+margin())
        print('\nUser Input:')
        print(f'* Target text/code:\t\t{target}')
        print(f'* Directory scanned:\t\t{source}')
        print(f'* File extensions searched:\t{extentions_text}')
        print(f'* File names searched:\t\t{filenames_text}')

        print("\nResults:")
        print(f"* Folders searched:\t\t{searched_folders}")
        print(f"* Files searched:\t\t{searched_files}")
        print(f"* Failed to read:\t\t{read_fail}")
        print(f"* Total Occurances:\t\t{occur_total}")

        print("\nOccurances:")
        for key in dict:
            print(f"\n- {key}.{dict[key]['extention'] }: ")
            print(f"\t - Occurances:\t\t{len(dict[key]['lines'])}")
            print(f"\t - Fullpath:\t\t{dict[key]['fullpath']}")
            print(f"\t - Lines:\t\t{dict[key]['lines']}")
        print(margin())


    # Option to restart application
    def hang():
        while True:
            close = input("\n...Completed ...Restart? (y/n): ")
            close = close.lower().strip()
            if close == 'y':
                return True
            elif close == 'n':
                return False
            else:
                pass

    
    # main
    def code_finder():    

        while True:
            source, target, extensions, filenames = inputs()
            if source != "" and target != "" and bool(extensions): # Not checking for valid directory 
                break
            else:
                print(margin()+"\nInvalid input provided!\nPlease try again:\n"+margin())

        searched_folders= 0
        searched_files  = 0
        read_fail       = 0
        occur_total     = 0

        # Dictionary of Occurances
        dict_occur      = {}

        print(margin())
        print("\n...Scan Started...")

        # start timer
        t0 = time() 

        for root, dirs, files in os_walk((os_path.normpath(source)), topdown=False):

            # Search folder
            test_folder("folder",root.split('\\')[-1],"\n")
            searched_folders+=1

            # Scan files in folder
            for file in files:

                dir = root + '\\' + file
                file_name   = file.split('.')[0]
                file_ext    = file.split('.')[-1]
                
                # Check for accepted extensions
                if (file_ext.lower() in extensions) and ( (len(filenames) == 0) or (len(filenames) and (file_name in filenames)) ):
                    test_folder("file", file,"\t")
                    
                    # Read file
                    try:
                        with open(dir) as file_opened:
                            searched_files+=1
                            # iterate lines
                            for num, line in enumerate(file_opened, 1):

                                # found target in line
                                if target in line:
                                    occur_total+=1
                                    
                                    # Populate dictionary
                                    if file_name in dict_occur.keys():
                                        dict_occur[file_name]['lines'].append(num)
                                    else:
                                        dict_occur[file_name]               = {}
                                        dict_occur[file_name]['fullpath']   = dir
                                        dict_occur[file_name]['extention']  = file_ext
                                        dict_occur[file_name]['lines']      = [num]
                                else:
                                    pass
                    except Exception as error:
                        #print(error)
                        read_fail+=1
                        read_failure(file)
                else:
                    pass
        
        # end timer
        t1 = time()
        td = round((t1 - t0), 3)

        print(f"\n\n...Scan Completed in {td} seconds...")
        results(source, target, extensions, filenames, searched_folders, searched_files, occur_total, read_fail, dict_occur)
        return hang()
        

    # check for restart
    result = code_finder()
    if result:
        pass
    else:
        break
