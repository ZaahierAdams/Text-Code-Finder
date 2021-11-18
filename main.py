from os import walk as os_walk
from os import path as os_path

def inputs():
    source      = input('\n(1) Parent/source Directory: ')
    target      = input('\n(2) Code to search for: ') 
    
    ex1         = input('\n(3) File extensions (eg. json, txt, etc...) separate extensions by comma: ') 
    ex2         = list(map(lambda ele: str.replace(ele, ".", ""), ex1.split(",")))
    extensions  = [ele.lower() for ele in ex2]
    
    return source, target, extensions


def test_folder(type, item, tab):
    print(f"{tab}L Scanning {type}: {item}")


def read_failure(name):
    print(f"\tL !!! FAILED reading {name} !!!")


def margin():
    return '-'*60


def results(searched_folders, searched_files, occur_total, read_fail, dict):
    print("\n\n"+margin())
    print("\nResults:")
    print(f"* Folders searched:\t{searched_folders}")
    print(f"* Files searched:\t{searched_files}")
    print(f"* Failed to read:\t{read_fail}")
    print(f"* Total Occurances:\t{occur_total}")
    for key in dict:
        print(f"\n- {key}: ")
        print(f"\t - Occurances:\t{len(dict[key]['lines'])}")
        print(f"\t - Fullpath:\t{dict[key]['fullpath']}")
        print(f"\t - Lines:\t{dict[key]['lines']}")
    print(margin())


def hang():
    close = input("\n...Completed...Hit any button to close.")


def main():    
    source, target, extensions = inputs()

    searched_folders= 0
    searched_files  = 0
    read_fail       = 0
    occur_total     = 0

    # Dictionary of Occurances
    dict_occur      = {}

    print(margin())
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
            if file_ext.lower() in extensions:
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

    results(searched_folders, searched_files, occur_total, read_fail, dict_occur)

main()
hang()