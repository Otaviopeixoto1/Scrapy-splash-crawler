import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from multiprocessing import Process
import time
import os

print("INICIO")
urlBula=sys.argv[1]
nomeMedicamento=sys.argv[2]
nomeMedicamento=nomeMedicamento.replace("/","")

extensao=sys.argv[3]+"-"+sys.argv[4]
extensaolog=sys.argv[3]+"_"+sys.argv[4]

link='https://consultas.anvisa.gov.br/'+ urlBula
attempts=int(sys.argv[5])
letter=sys.argv[6]


options = Options()
options.headless = True

#profile=webdriver.FirefoxProfile()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", "/home/downloads")
#Example:profile.set_preference("browser.download.dir", "C:\Tutorial\down")
options.set_preference("browser.download.useDownloadDir", True)
#profile.set_preference("browser.download.viewableInternally.enabledTypes", "")
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/force-download")
#profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf;text/plain;application/text;text/xml;application/xml")
options.set_preference("pdfjs.disabled", True)



#driver = webdriver.Firefox(options=options,executable_path='/home/geckodriver')
#driver.set_page_load_timeout(3)


count=0
def DownloadFile():
    global count
    global driver
    global options
    driver = webdriver.Firefox(options=options,executable_path='/home/geckodriver')
    driver.set_page_load_timeout(3)
    
    if count>attempts:
        driver.quit()
        time.sleep(1)
        errorlog=open("/home/errorlog.txt","a", encoding='utf-8')
        errorlog.write((nomeMedicamento).encode('utf-8', 'replace').decode()+extensaolog+"\n")
        errorlog.close()
        print("ERRO: "+nomeMedicamento + extensao+" nao foi baixado")
        return
    
    try:
        print("baixando: "+nomeMedicamento+"-t"+str(count))
        count+=1
        driver.get(link)
        
        
        time.sleep(2)
        driver.quit()
        files = os.listdir("/home/downloads")
        
        
        if (len(files) < 1):       
            DownloadFile()
            
        
        else:
            filename=files[0]
        
            old_name = r"/home/downloads/"+ filename
            new_name = r"/home/bulas"+"-"+letter+"/" + nomeMedicamento + extensao + ".pdf"

            os.rename(old_name, new_name)
            time.sleep(1)
            return
    
    except:
        time.sleep(2)
        driver.quit()
        files = os.listdir("/home/downloads")

        if (len(files) < 1):

            DownloadFile()
    

        else:
            time.sleep(1)
            filename=files[0]
            old_name = r"/home/downloads/"+ filename
            new_name = r"/home/bulas"+"-"+letter+ "/" + nomeMedicamento + extensao + ".pdf"

            os.rename(old_name, new_name)
    
            
            return




#filename = '/home/linkbulas.txt'
#with open(filename, 'a') as f:
   #f.write(sys.argv[1])
    #for u in table.findAll('a', attrs={'ng-if':"produto.idBulaPacienteProtegido"}):
        #link_bula=u["href"]
        #f.write(link_bula)
        
p1 = Process(target=DownloadFile, name='donwload1')
p1.start()
p1.join(timeout=attempts*7.5)
p1.terminate()

if p1.exitcode is None:
    files = os.listdir("/home/downloads")
    if (len(files) >= 1):
        time.sleep(1)
        filename=files[0]
        old_name = r"/home/downloads/"+ filename
        new_name = r"/home/bulas"+"-"+letter+"/" + nomeMedicamento + extensao + ".pdf"
        os.rename(old_name, new_name)
    else:
        p2 = Process(target=DownloadFile, name='donwload2')
        p2.start()
        p2.join(timeout=attempts*7.5)
        p2.terminate()    
        if p2.exitcode is None:
            files = os.listdir("/home/downloads")
            if (len(files) >= 1):
                time.sleep(1)
                filename=files[0]
                old_name = r"/home/downloads/"+ filename
                new_name = r"/home/bulas"+"-"+letter+"/" + nomeMedicamento + extensao + ".pdf"
                os.rename(old_name, new_name)
            else:
                errorlog=open("/home/errorlog.txt","a", encoding='utf-8')
                errorlog.write((nomeMedicamento).encode('utf-8', 'replace').decode()+extensaolog+"\n")
                errorlog.close()
                print("ERRO: "+nomeMedicamento + extensao+" nao foi baixado")
#DownloadFile()
#driver.quit()
print("FIM")

    





