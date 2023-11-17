#commands for basic config of switch and client pc
#enable
#conf t
#int g0/0
#ip add 192.168.1.1 255.255.255.0
#no shut
#line vty 0 4 
#tr in al
#login local
#username cisco secret cisco
#ip domain-name domain.com
#hostname R1
#enable secret class
#cry key gen rsa
#2048
#ip ssh version 2
#exit
#copy run start

#sudo ifconfig ens160 192.168.1.3

 
import pexpect #Import Pexpect for terminal automation
import re      #Import RegularExpressinos for the use of match() in task 2
#global Session #made session global for now so threes no erros when puching it through functions, change later

#NOTE: these varibles are hardcoded for now, move to a file and extract the data into a list to use from there 
#NOTE: In some Expect() error checks there are nested ifs for redundancy in ther case there is more than one posability on the terminal line, 
# CLEAN this up, find way to make expect content varible  and use IF OR Expect() outputs a True False statment so may need to just add a second line with a new var when making the expect check 
#NOTE: alot of code and space is wasited on the error check, Make it a function.
#Define variables 
#varibles given from EVE-NG Basic Configuration change if needs be for submission
ip_address = '192.168.1.1'
username = 'cisco'
password = 'cisco'
EnablePassword = 'class'
#create funtion to chose ssh or telnet, user will pick and new function will launch 
def chosefunc():    
    while True:
        print('\n____USER INPUT____')
        print('1. Telnet to Device')
        print('2. SSH to Device')
        #op = input('Option: ')
        op = '1' # hardcode option for testing
        if op == '1':
            Telnetfunc()
            break#to leave the loop once the session has been created

        elif op == '2':
            SSHfunc()
            break #to leave the loop once the session has been created
        else:
            print('incorrect input try again')
        


#_______________________________________________________________________________________________TASK1_______________________________________________________________________________________________#    
#_________________________________Telnet______________________________________#
def Telnetfunc(): #Function used for telnetting to the network device 
    global Session
    print('telnet')

    Session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8', timeout=10) #Create the telnetting session via the spawn method, using utf encoding and set the time out timer to 10s
    TelnetResult = Session.expect(['Username:', pexpect.TIMEOUT])                 #Expect to see 'Username:' in the terminal after successfull telnet login, save reult as var TelnetResult for error checking 
    
    
    if TelnetResult == 0: #Error check for the above expect statment, if expect finds 'Username:' after succsessfull login attempt pass on, ELSE telnet attmept was unsucsessful; inform the user and quit
        print('--- Telnet attempt Succsessful')
        pass
    else:
        print('--- Telnet attempt uncuccsessful')
        exit()

     
    Session.sendline(username)                                    #Send var username to terminal to log-in with the spesified username
    TelnetResult = Session.expect(['Password:', pexpect.TIMEOUT]) #Expect to see 'Password:' in the terminal after successfull username input, save reult as var TelnetResult for error checking 

   
    if TelnetResult == 0:  #Error check for the above expect statment, if expect finds 'Password:' after succsessfull input pass on, ELSE username was unsucsessful; inform the user and quit
        print('--- Username attempt Succsessful')
        pass
    else:
        print('--- Username attempt uncuccsessful', username)
        exit()

    
    Session.sendline(password)                          #Send var password to terminal to log-in with the spesified password 
    TelnetResult=Session.expect(['#', pexpect.TIMEOUT]) #Expect to see '#' after succsessful login with username and password 

    
    if TelnetResult == 0: #error check for the above expect statment, if expect finds '#:' after succsessfull  log-in pass on, ELSE password was incorect; inform the user and quit
        print('--- password Log-in attempt Succsessful')
        pass
    #This else is for future proofing. In some cases while testing when inputting a username and password to enter via telnet, you would gain accsess at user EXEC(>) not privliged EXEC(#)
    #Created a nested IF for when this situation occurs to send user to privliged EXEC mode so the rest of the script can run as usual. 
    #There may be a cleaner way to do this. store expect as a string varible and check the result? but this works for now.
    else:
        TelnetResult=Session.expect(['>', pexpect.TIMEOUT])#Expect to see '>' after succsessful login with username and password
        if TelnetResult == 0:
            Session.sendline('enable') #send 'enable' to the terminal to enter privliged EXEC mode 
            Session.sendline(EnablePassword) #sned the enable password to the terminal to enter privliged EXEC mode
            pass
        else:
            print('--- password Login attempt uncuccsessful', password)
            exit()

    # Display a success message if it works
    print('------------------------------------------------------')
    print('')
    print('--- Success! connecting to: ', ip_address)
    print('--- Username: ', username)
    print('--- Password: ', password)
    print('')
    print('------------------------------------------------------')

    # Terminate telnet to device and close session
    #Session.sendline('quit')
    #Session.close()
    #exit() # quit program to close the loop
    
#_________________________________SSH______________________________________#
def SSHfunc():
    global Session
    print('SSH')
    # #Create the SSH session via the spawn method, using utf encoding and set the time out timer to 10s
    Session = pexpect.spawn('ssh ' + username + '@' + ip_address, encoding='utf-8', timeout=10)
    SshResult = Session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF]) #Expect Password after succsessful SSH connection

    #Error check above expect statment if SSH session was sucsesful pass on
    #ELSE acts as a second error check for when establishing ssh connecton for the first time allowing the conection and generating a key for the machine to help with redundancy
    #if the key needed generating re-do the error check in the nested list
    if SshResult == 0:
        print('Key Accsepted')
        pass
    else:
        Session.sendline('yes') #Coudnt figure out how to get expect to work the text that appers for the first ssh login but this has been test and works
        SshResult = Session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
        if SshResult == 0:
            print('Key generated')
            pass
        else:
            print('--- FAILURE! creating session for: ', ip_address,'KEY not generated')
            exit()

    Session.sendline(password) #after succsessful SSH sesion creation send the password to the terminal to loging
    SshResult1 = Session.expect(['#', pexpect.TIMEOUT, pexpect.EOF]) #expect '#' after successfull login and entering Privliged EXEC
    SshResult2 = Session.expect(['>', pexpect.TIMEOUT, pexpect.EOF]) #expect '>' after successfull login and entering User EXEC

    if SshResult1 == 0: #if terminal expects '#' pass on
        print('in privliged mode')
        pass
    elif SshResult2 == 0: #if terminal expects '>' end the enable comand and enable password and redo the error check
        print('eneted at user mode')
        Session.sendline('enable')
        Session.sendline(EnablePassword)
        
        SshResult = Session.expect(['#', pexpect.TIMEOUT, pexpect.EOF]) #redo of the error check if user was in '>' now in '#'
        if SshResult == 0: #if terminal expects '#' pass on
            print('in privliged mode')
            pass
        else:
            print('Error entering #')
            exit()
    else:
        print('password failed')
        exit()

    # Display a success message if works
    print('------------------------------------------------------')
    print('')
    print('--- Success! connecting to: ', ip_address)
    print('--- Username: ', username)
    print('--- Password: ', password)
    print('')
    print('-------untitled folder---------------------------------------------')
    
    #Session.sendline('quit')
    #Session.close()
   # exit() # quit program to close the loo

def HostName():
    Session.sendline('conf t') #send conf t(congiure terminal) to the terminal to enter global configuation
    NameResult=Session.expect(['\(config\)#', pexpect.TIMEOUT])#Expect to see '(config)#' after sending the conf t comand to the terminal use .\\ arounf conf
    #Config error check
    if NameResult == 0:
        print('--- Entering Config mode')
        
        pass
    else:
        print('--- Entering config uncuccsessful')
        exit()

    print('\nPlease enter the name of the Device')
    #Hostname = input('Name:') #user inputs a new hostname, save as a varible for sendline later
    Hostname = 'R1' #Hardcode for testing
    Session.sendline(f'hostname {Hostname}') #send the hostname command with the hostname varible to set the new name, note the sting has to be set this way as sendline() only take 1 positinal argument
    print(Hostname+'(config)#')
    NameResult=Session.expect([Hostname+'\(config\)#', pexpect.TIMEOUT])#Expect to see the new 'hostname(config)#' after its been set

    #host name error check 
    if NameResult == 0:
        print('--- Name change Succsesful')
        Session.sendline('exit') # exit global configuration after hostname change (for future proofing incase adding more functions)
        pass
    else:
        print('--- Hostname error could not set',Hostname)
        Session.sendline('exit')
        exit()


#func print running config into a file
#NOTE: logfile shows the comands to enter&exit show run, test ways to remove this
def ShowRun():
    Output = open('ShowRunOut.txt','w')                  #Create and open a new file in which the running config will be saved 
    Session.sendline('terminal length 0')                #Set the terminal length to capture all of the running config in one print
    Session.sendline('show run')                         #Send the 'show run' command to print the running config in the terminal 
    Session.logfile = Output                             #Use logfile to copy and print what comes through the terminal to the output var file
    Session.expect([pexpect.TIMEOUT,pexpect.EOF])        #
    print('Running config copied to file succsessfully') #Print to let the user know file has been printed
    with open("ShowRunOut.txt", "r") as RunOut:          #Set the created file as var Runout
        for line in RunOut:                              #Loops for each line in the file
            print(line)                                  #Print each line



#_______________________________________________________________________________________________TASK2_______________________________________________________________________________________________#    

#func that copies the running config using logfile and cleans up the file for manual comparrison. This file and the StartUpBackup wil be compared
#while this will use essentially the same file created in 'showrun()' for running config. 
#This is set up for the event that I have enought time to add more user input. In future version the user should be able to pick if it wants to use showrun() or hostName() funcs for example 
#NOTE: Idealy i'd use tfpt for this but i cant get it working, further testing requried 
def ConfigPrints():
    Session.sendline('terminal length 0') #'Terminal length 0' only needs to be sent sent once for both run commands to printed entirely 

    #ShowRun Config Part, finds and prints the config into a txt file using logfile
    ShowRunOut = open('ShowRunComp.txt','w') #create and open a new file in which the running config will be saved for the comparrison 
    Session.sendline('show run') #Send the 'show run' command to print the running config in the terminal 
    Session.logfile = ShowRunOut #Use logfile to copy and print what comes through the terminal to the ShowRunOut var file
    Session.expect([pexpect.TIMEOUT,pexpect.EOF]) #
    print('Running config copied to file succsessfully') 

#Clean up the file and remove the tag alongs from logfile print and put into a new file for the comparison 
    with open("ShowRunComp.txt", "r") as read, open( 'outputRun.txt', 'w') as out: # set the read file and output file varibles 
    
        for line in read: # loop for each line in the dead file 
            if re.match('R1#', line): #if it finds a match for 'R1#' ignore
                continue
            if re.match('terminal length 0', line): #if it finds a match for 'terminal length 0' ignore
                continue 
            out.write(line) # all non ignored lines are writen into the new comparison file
    
    #StartUp Config Part
    #NOTE: this is not needed as the ofline version has already been created. USE THIS IN CASE my understanding of having a pre-exiting config file downlaoded with the main script was incorrect
    #this part of the script creats the ShowStartBackup in all but name
    #ShowStartOut = open('ShowStartComp.txt','w') #create and open a new file in which the StartUp config will be saved for the comparrison 
    #Session.sendline('show start') # send the 'show start' command to print the startup-config config in the terminal #THIS IS THE OFLINE VERSION NEEDED THE TASK 2#
    #Session.logfile = ShowStartOut #use logfile to copy and print wwhat comes through the terminal to the output var file
    #Session.expect([pexpect.TIMEOUT,pexpect.EOF]) #
    #print('Running config copied to file succsessfully2') #print to let the user know file has been printed
    #with open("ShowStartComp.txt", "r") as f,open( 'outputStart.txt', 'w') as o:

    #    for line in f:

    #        if re.match('!', line):
    #            continue
    #        if re.match('R1#', line):
    #            continue
    #        if re.match('show start', line):
    #            continue
    #        o.write(line)    

#Function that picks out the chosen lines for comapring running and stat up config and creates a file to be used by CompPrint()

def CompFile():
    with open("ShowRun.txt", "r") as read, open( 'CompFile.txt', 'w') as prints:
        
        for line in read:

            if re.match('version', line):
                    prints.write(line.rstrip('\n')+', ')
            if re.match('hostname', line):
                    prints.write(line.rstrip('\n')+', ')
            if re.match('ip domain name', line):
                    prints.write(line.rstrip('\n')+',' )
            if re.match(' ip address', line):
                    
                    prints.write(line.rstrip('\n')+', ')
            if re.match('ip ssh version', line):
                    prints.write(line)
            continue
        read.close()

    with open("ShowStart.txt", "r") as read, open( 'CompFile.txt', 'a') as prints:
        
        for line in read:

            if re.match('version', line):
                    prints.write(line.rstrip('\n')+', ')
            if re.match('hostname', line):
                    prints.write(line.rstrip('\n')+', ')
            if re.match('ip domain name', line):
                    prints.write(line.rstrip('\n')+',' )
            if re.match(' ip address', line):
                    
                    prints.write(line.rstrip('\n')+', ')
            if re.match('ip ssh version', line):
                    prints.write(line)
            continue
        read.close()
        prints.close()

def CompPrint():
    print('')
    print('  Comparison between the running config and startup config')
    print('------------------------------------------------------------')

    file = open('CompFile.txt', 'r') # open comparison file
    for line in file:
        
        CompareDicList = line.strip().split(',') #exctract content from file 
    
        CompareDic = {} # create a dictonary to store each result separately to be called individually 
        CompareDic['version'] = CompareDicList[0]
        CompareDic['Hostname'] = CompareDicList[1]
        CompareDic['Domain-name'] = CompareDicList[2]
        CompareDic['IP ADD'] = CompareDicList[3]
        CompareDic['SSH version'] = CompareDicList[4]

        #print the Dic content, hard coded for now. turn to for loop
        print(CompareDic['version'],CompareDic['Hostname'],CompareDic['Domain-name'],CompareDic['IP ADD'],CompareDic['SSH version'])

    file.close()
    print('')

def main():
    chosefunc()
    HostName()
    ShowRun()
    ConfigPrints()
    CompFile()
    CompPrint()


    
    
main()
