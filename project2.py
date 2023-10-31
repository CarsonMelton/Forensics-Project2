import os
import sys
import math

# Need to add comments and edit the zip logic

file_header = {
    'MPG': '000001b3', 
    'PDF': '25504446', 
    'BMP': '424d', 
    'GIF1': '474946383761',
    'GIF2': '474946383961', 
    'JPG': 'ffd8ff', 
    'DOCX': '504b030414000600', 
    'AVI': '52494646',
    'PNG': '89504e470d0a1a0a',
    'ZIP': '504b0304' 
    }


file_footer = {
    'MPG1': '000001b7',
    'MPG2': '000001b9', 
    'PDF1': '0d2525454f460d000000', 
    'PDF2': '0d0a2525454f460d0a000000',
    'PDF3': '0a2525454f460a000000', 
    'PDF4': '0a2525454f46000000', 
    'GIF': '003b000000', 
    'JPG': 'ffd9000000',
    'DOCX': '504b0506', 
    'PNG': '49454e44ae426082',
    'ZIP': '504b'
    }

def FileRecovery(disk_hex):
    
    total_found = 0

    for Header in file_header:
        search = 0 
        loc = disk_hex.find(file_header[Header])
        while loc != -1:

            # MPG
            if Header == 'MPG':
		
                if (loc % 512) == 0:
                    
                    total_found = total_found + 1

                    footer = disk_hex.find(file_footer['MPG1'], loc)
                    if footer == -1: 
                        footer = disk_hex.find(file_footer['MPG2'], loc) 
                    footer = footer + 7 
                    #Creating the file
                    File_name = 'File' + str(total_found) + '.mpg' 
                    
                    start_offset = int(loc / 2) 
                    end_offset = int(math.ceil(footer / 2))
                    file_size = end_offset - start_offset
                    
                    #Printing the file name, start and end offsets
                    print(File_name, end = ', ')
                    print('Start Offset: ' + str(hex(start_offset)), end = ", ") 
                    print('End Offset: ' + str(hex(end_offset)))
                    
                    #File extraction function
                    File_Extract(start_offset,file_size, File_name)
                    search = footer

                else:
                    search = loc + 8

            elif Header == 'PDF':
                if (loc % 512) == 0:
                    print()
                    total_found = total_found + 1

                    footer = disk_hex.find(file_footer['PDF1'], loc)
                    end_offset = 13 

                    if footer == -1: 
                        
                        footer = disk_hex.find(file_footer['PDF2'], loc) 
                        end_offset = 17 
                        
                    if footer == -1:
                        footer = disk_hex.find(file_footer['PDF3'], loc) 
                        end_offset = 13 
                    
                    if footer == -1:
                        footer = disk_hex.find(file_footer['PDF4'], loc) 
                        end_offset = 11 
                    
                    end_offset = end_offset + footer
                    File_name = 'File' + str(total_found) + '.pdf'
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(end_offset / 2))
                    file_size = end_offset - start_offset
                    print(File_name, end = ', ')
                    print('Start Offset: ' + str(hex(start_offset)), end = ", ")
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,file_size, File_name)

                    search = footer

                else:
                    search = loc + 8

            elif Header == 'BMP':
                if (loc % 512) == 0 and disk_hex[(loc + 12):(loc + 20)] == '00000000':
                        total_found = total_found + 1
                        File_name = 'File' + str(total_found) + '.bmp'

                        file_size = str(disk_hex[loc + 10: loc + 12])
                        file_size = file_size + str(disk_hex[loc + 8: loc + 10])
                        file_size = file_size + str(disk_hex[loc + 6: loc + 8])
                        file_size = file_size + str(disk_hex[loc + 4: loc + 6])

                        file_size = int(file_size, 16) 
                        start_offset = int(loc / 2)
                        end_offset = start_offset + file_size
                        print(File_name, end = ', ')
                        print('Start Offset: ' + str(hex(start_offset)), end = ", ")
                        print('End Offset: ' + str(hex(end_offset)))

                        File_Extract(start_offset,file_size, File_name)
                        
                        search = loc + file_size
                else:
                    search = loc + 4

            elif Header == 'GIF1':
                if (loc % 512) == 0:
                    
                    total_found = total_found + 1

                    footer = disk_hex.find(file_footer['GIF'], loc)
                    footer = footer + 3 
                    File_name = 'File' + str(total_found) + '.gif'
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    file_size = end_offset - start_offset
                    print(File_name, end = ', ')
                    print('Start Offset: ' + str(hex(start_offset)), end = ", ")
                    print('End Offset: ' + str(hex(end_offset)))
                    File_Extract(start_offset,file_size, File_name)

                else:
                    search = loc + 12

            elif Header == 'GIF2':
                if (loc % 512) == 0:
                    print()
                    total_found = total_found + 1
                    footer = disk_hex.find(file_footer['GIF'], loc)
                    footer = footer + 3 
                    File_name = 'File' + str(total_found) + '.gif'
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    file_size = end_offset - start_offset
                    print(File_name, end = ', ')
                    print('Start Offset: ' + str(hex(start_offset)), end = ", ")
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,file_size, File_name)

                    search = footer

                else:
                    search = loc + 12

            elif Header == 'JPG':
                if (loc % 512) == 0:
                    print()
                    total_found = total_found + 1

		   
                    footer = disk_hex.find(file_footer['JPG'], loc)
                    footer = footer + 3 
                    
                    File_name = 'File' + str(total_found) + '.jpg'
                    
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    file_size = end_offset - start_offset
                    print(File_name, end = ', ')
                    print('Start Offset: ' + str(hex(start_offset)), end = ", ")
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,file_size, File_name)

                    search = footer
                else:
                    search = loc + 6

            elif Header == 'DOCX':
                
                if (loc % 512) == 0:
                    total_found = total_found + 1        
                    footer = disk_hex.find(file_footer['DOCX'], loc)
                    footer = footer + 43 
		            
                    File_name = 'File' + str(total_found) + '.docx'
                   
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    file_size = end_offset - start_offset
                    print(File_name, end = ', ')
                    print('Start Offset: ' + str(hex(start_offset)), end = ", ")
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,file_size, File_name)
                    
                    search = footer

                else:
                    search = loc + 16

            elif Header == 'AVI':
                if (loc % 512) == 0:
                    if (disk_hex[(loc + 16):(loc + 32)] == '415649204c495354'):
                        total_found = total_found + 1

                        File_name = 'File' + str(total_found) + '.avi'

                        file_size = str(disk_hex[loc + 14: loc + 16])
                        file_size = file_size + str(disk_hex[loc + 12: loc + 14])
                        file_size = file_size + str(disk_hex[loc + 10: loc + 12])
                        file_size = file_size + str(disk_hex[loc + 8: loc + 10])
                        file_size = int(file_size, 16) + 8 
                        start_offset = int(loc / 2)
                        end_offset = start_offset + file_size
                        print(File_name, end = ', ')
                        print('Start Offset: ' + str(hex(start_offset)), end = ", ")
                        print('End Offset: ' + str(hex(end_offset)))

                        File_Extract(start_offset,file_size, File_name)

                        search = loc + file_size
                else:
                    search = loc + 32

            elif Header == 'PNG':
                if (loc % 512) == 0:
                    total_found = total_found + 1
                    footer = disk_hex.find(file_footer['PNG'], loc)
                    footer = footer + 15  
                    File_name = 'File' + str(total_found) + '.png'
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    file_size = end_offset - start_offset
                    print(File_name, end = ', ')
                    print('Start Offset: ' + str(hex(start_offset)), end = ", ")
                    print('End Offset: ' + str(hex(end_offset)))
                    
                    File_Extract(start_offset,file_size, File_name)

                    search = footer
                else:
                    search = loc + 16
            
            elif Header == "ZIP":
                if loc%512 == 0:
                    total_found = total_found + 1

                    # Find the footer for the ZIP file
                    footer = disk_hex.find(file_footer['ZIP'], loc+len(file_header['ZIP']))
                    if footer == -1:
                        search = loc + len(file_header['ZIP'])
                        continue
                    end_offset = footer + len(file_footer['ZIP'])
                    File_name = 'File' + str(total_found) + '.zip'

                    start_offset = int(loc/2) + len(file_header['ZIP'])
                    end_offset = int(math.ceil(end_offset/2))
                    file_size = end_offset - start_offset
                    print(File_name, end = ', ')
                    print('Start Offset: ' + str(hex(start_offset)), end = ", ")
                    print('End Offset: ' + str(hex(end_offset)))
                    
                    File_Extract(start_offset,file_size, File_name)
                    search = footer*2
                else:
                    search = loc + len(file_header['ZIP'])

                    
            loc = disk_hex.find(file_header[Header], search)

def File_Extract(start_offset,count, file_name):
    extraction_command = 'dd if=' + str(sys.argv[1]) + ' of=' + str(file_name) + ' bs=1 skip=' + str(start_offset) + ' count='+ str(count)
    os.system(extraction_command)

    generateHash(file_name)

def generateHash(inputFile):
    hash = 'sha256sum ' + inputFile
    os.system(hash)


if __name__ == "__main__":
    input_disk_path = sys.argv[1]
    with open(sys.argv[1], 'rb') as disk_image:
        disk_data = disk_image.read().hex()
    disk_image.close()
    FileRecovery(disk_data)
