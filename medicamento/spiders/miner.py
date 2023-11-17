
import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
import os
from csv import DictReader

class MySpider(scrapy.Spider):
    name="miner"
    script1 = ""
    script2 = ""
    base_url = "https://consultas.anvisa.gov.br/#/bulario/q/?nomeProduto="
    errorLogPath = "../../dockerfolder/errorlog.txt"
    crawlerStatusPath = "../../crawlerstatus.csv"
    
    leafletsPath = "../../dockerfolder/bulas"
    
    letters=[]
    currentletter=""
    currentindex=0
    downloaderrors=[]
    currentdindex=0
    meta={'COOKIES_DEBUG': True}
    
    def start_requests(self):
    
    	with open("../splash_scripts/splash_request.lua") as f:
    		script1 = f.read()
    		
    	with open("../splash_scripts/splash_retry.lua") as f:
    		script2 = f.read()
    
        
        #looping over the letters of the alphabet:
        letterfile = open(crawlerStatusPath,"r")
        lines=letterfile.readlines()
        letterfile.close()
        for l in lines:
            a=l.strip("\n").split(",")
            if a[1]=="0":
                self.letters.append(a[0])
        print(self.letters)
        
        
        self.currentletter=self.letters[0]
        url=self.base_url + self.currentletter
            
        # Cleaning errorLog:
        f = open(errorLogPath,"w", encoding='utf-8')
        f.close()
        
        # Creating dict with the already downloaded leaflets (to avoid them when restarting):
        files = os.listdir(leafletsPath+"-"+ self.currentletter)
        print("Number of already downloaded files = " + str(len(files)))
        expedientes = {} 
        
        for fi in files:
            s=fi.split("-")
            extension=(s[-2].split("_"))[-1]
            expedientes[(s[-1].replace(".pdf",""))+extension]=True 
        
        # Sending requests to splash:
        yield SplashRequest(url=url, callback=self.parse1, endpoint='execute', args={'wait': 3, 'lua_source': self.script1,'timeout':36000, 'med_baixados':expedientes, 'attempts': 10, 'letter': self.currentletter})
	        
    
    
    # First attempt at downloading all files:
    def parse1(self, response):  
        #Open errorLog to retry downloading missed files
        errorlog=open(errorLogPath,"r", encoding='utf-8')
        erlines=errorlog.readlines()
        errorlog.close()
        
        #Clean errorLog again
        f = open(errorLogPath,"w", encoding='utf-8')
        f.close()

        lstring=""
        if len(erlines)>0:
            for l in erlines:
                if l != "":
                    self.downloaderrors.append(l.strip("\n").split("_"))
                
        errors={'paciente':[], 'profissional': []}
        erexpedientes=[]
        
        # Get the html to fill a table with extra data for the leaflets
        f_content=response.body
        soup = BeautifulSoup(f_content, 'html5lib')

        tables = soup.findAll('table')


        cols=tables[0].findAll('th', attrs={'translate':"",'class':"ng-scope"})
        columns=[]
        for col in cols:
            columns.append(col.text)

        med_names=[]
        n_proc=[]
        empresas=[]
        cnpj=[]
        expedientes=[]
        data_pub=[]
        
        for table in tables:
        
            data_names=table.findAll('a', attrs={'class':"ng-binding"})
            for dat in data_names:
                #atualmente os remédios tem um " " adicional na frente do nome. Essa solução usando o [1:] é Temporária
                med_names.append((dat.text)[1:])
                
            for u in table.findAll('a', attrs={'class':"ng-binding"}):
                link_proc=u["href"]
                n_proc.append(link_proc.replace("#/medicamentos/","").replace("/",""))
                
            data_info=table.findAll('td', attrs={'class':"text-center col-sm-1 ng-binding"})
            
            for i in range(0, len(data_info),3):
                empresa_cnpj=data_info[i].text.split(" - ")
                empresas.append(empresa_cnpj[0])
                cnpj.append(empresa_cnpj[1])
                expedientes.append(data_info[i+1].text)
                data_pub.append(data_info[i+2].text)


         
        campos = ['Medicamento','Empresa','CNPJ',"Processo",'Expediente','Data de Publicação', 'Status']
        head = ",".join(campos)+"\n"
        csvfile = open('medicamentos.csv', mode='r', encoding='utf-8') 
        lines = csvfile.readlines()
        csvfile.close()
                
        csvfile = open('medicamentos.csv', mode='w', encoding='utf-8') 
        csvfile.write(head)
        
        
        print("Download Errors:")
        print(self.downloaderrors)

        #Detected Errors:
        if len(self.downloaderrors)>0:
            for l in erlines:
                a=l.strip("\n").split("_")
                erexpedientes.append(a[2])
                if a[1] == 'paciente':
                    errors['paciente'].append(a[0])
                else:
                    errors['profissional'].append(a[0])
        
            for i in range(len(med_names)):
                status=0
                
                if ((med_names[i] in errors['paciente']) and (med_names[i] in errors['profissional']) and (expedientes[i] in erexpedientes)):
                    status=2
                elif ((med_names[i] in errors['paciente']) or (med_names[i] in errors['profissional']) and (expedientes[i] in erexpedientes)):
                    status=1
                
            
                s2=(str(med_names[i])+","+str(empresas[i])+","+str(cnpj[i])+","+str(n_proc[i])+","+str(expedientes[i]) +","+str(data_pub[i])+","+ str(2) + "\n").encode('utf-8', 'replace').decode()
                s1=(str(med_names[i])+","+str(empresas[i])+","+str(cnpj[i])+","+str(n_proc[i])+","+str(expedientes[i]) +","+str(data_pub[i])+","+ str(1) + "\n").encode('utf-8', 'replace').decode()
            
            
                newline=(str(med_names[i])+","+str(empresas[i])+","+str(cnpj[i])+","+str(n_proc[i])+","+str(expedientes[i]) +","+str(data_pub[i])+","+ str(status) + "\n").encode('utf-8', 'replace').decode()
                
                if newline in lines:
                    continue
                elif s2 in lines:
                    lines.remove(s2)
                    lines.append(newline)
                elif s1 in lines:
                    lines.remove(s1)
                    lines.append(newline)
                else:
                    lines.append(newline)
            
            
            for l in lines:
                if l == head:
                    continue
                else:
                    csvfile.write(l)
            csvfile.close()
            
            
            print("Retrying to download leaflets: "+lstring)
            print(errors)
            print(self.downloaderrors)    
            tipo=self.downloaderrors[self.currentdindex][1]
            yield SplashRequest(url=base_url+self.downloaderrors[self.currentdindex][0], callback=self.parse2, endpoint='execute', args={'wait': 3, 'lua_source': self.script2,'timeout':36000,'tipobula': tipo,'expediente': self.downloaderrors[self.currentdindex][2] ,'attempts': 20, 'letter':  self.currentletter})
            
        #No errors detected
        else:
            print("No errors detected")   

        
            for i in range(len(med_names)):
                status=0
                        
                s2=(str(med_names[i])+","+str(empresas[i])+","+str(cnpj[i])+","+str(n_proc[i])+","+str(expedientes[i]) +","+str(data_pub[i])+","+ str(2) + "\n").encode('utf-8', 'replace').decode()
                s1=(str(med_names[i])+","+str(empresas[i])+","+str(cnpj[i])+","+str(n_proc[i])+","+str(expedientes[i]) +","+str(data_pub[i])+","+ str(1) + "\n").encode('utf-8', 'replace').decode()
            
            
                newline=(str(med_names[i])+","+str(empresas[i])+","+str(cnpj[i])+","+str(n_proc[i])+","+str(expedientes[i]) +","+str(data_pub[i])+","+ str(status) + "\n").encode('utf-8', 'replace').decode()
            
            
                if newline in lines:
                    continue
                elif s2 in lines:
                    lines.remove(s2)
                    lines.append(newline)
                elif s1 in lines:
                    lines.remove(s1)
                    lines.append(newline)
                else:
                    lines.append(newline)
            
            
            for l in lines:
                if l == head:
                    continue
                else:
                    csvfile.write(l)
            csvfile.close()
        
        
            #Updating the satus of the leaflets:
        
            letterfile = open(crawlerStatusPath,"r")
            lines=letterfile.readlines()
            letterfile.close()
            
            newlines=[]
            for l in lines:
                a=l.strip("\n").split(",")
                if a[0]==self.currentletter:
                    update=self.currentletter+","+"1\n"
                    newlines.append(update)
                else:
                    newlines.append(l)
                    
            letterfile = open(crawlerStatusPath,"w")
            for l in newlines:
                letterfile.write(l)
            letterfile.close()
        
            # Continue to the next starting letter:
            if self.currentindex < (len(self.letters)-1):
                print("Starting next REQUEST")
                self.currentindex+=1
                
                print(self.currentindex)
                
                self.currentletter=self.letters[self.currentindex]
                
                print("Starting letter: "+self.currentletter)
                
                #Clean errorLog
                f = open(errorLogPath,"w", encoding='utf-8')
                f.close()
                
                #Creat dict with already downloaded leaflets
                files = os.listdir(leafletsPath+"-"+ self.currentletter)
                print("Number of already downloaded leaflets =" + str(len(files)))
                expedientes={} 
                for fi in files:
                    s=fi.split("-")
                    extension=(s[-2].split("_"))[-1]
                    expedientes[ (s[-1].replace(".pdf",""))+extension ]=True 
            
                url=self.base_url + self.currentletter
                
                yield SplashRequest(url=url, callback=self.parse1, endpoint='execute', args={'wait': 3, 'lua_source': self.script1,'timeout':36000, 'med_baixados':expedientes, 'attempts': 10, 'letter': self.currentletter})
        
 
 
 
 
 
 
 
 
 
 
 
 
 
    # Here we specifically try to download the files with errors
    def parse2(self, response):
        self.currentdindex+=1
        if self.currentdindex<len(self.downloaderrors):
            print("Calling Parse2 (Continuing retry)")
            tipo=self.downloaderrors[self.currentdindex][1]

            yield SplashRequest(url = base_url+self.downloaderrors[self.currentdindex][0], callback=self.parse2, endpoint='execute', args={'wait': 3, 'lua_source': self.script2,'timeout':36000,'tipobula': tipo,'expediente':self.downloaderrors[self.currentdindex][2],'attempts': 20, 'letter':  self.currentletter})
        
        else:
            self.downloaderrors.clear()
            self.currentdindex=0
            print("Calling Parse2 (End of retry)") 
                
            #Verifying if there are any errors left on errorlog
            errorlog=open(errorLogPath,"r", encoding='utf-8')
            lines=errorlog.readlines()
            errorlog.close()   
            f = open(errorLogPath,"w", encoding='utf-8')
            f.close()
        
            errors={'paciente':[], 'profissional': []}
            erexpedientes=[]
            
            for l in lines:
                a=l.strip("\n").split("_")
                erexpedientes.append(a[2])
                if a[1]=='paciente':
                    errors['paciente'].append(a[0])
                else:
                    errors['profissional'].append(a[0])


            print("REMAINING ERRORS: ")
            print(errors)

         
            campos=['Medicamento','Empresa','CNPJ',"Processo",'Expediente','Data de Publicação', 'Status']
            head=",".join(campos)+"\n"
            newlinescsv=[]
            
            with open('medicamentos.csv', mode='r', encoding='utf-8') as my_file:
                #passing file object to DictReader()
                csv_dict_reader = DictReader(my_file)

                for i in csv_dict_reader:
                    print(i)
                    name=i["Medicamento"]
                    empresa=i["Empresa"]
                    cnpj=i["CNPJ"]
                    proc=i["Processo"]
                    exped=i["Expediente"]
                    datapub=i["Data de Publicação"]
        
                    status=0
                    if ((name in errors['paciente']) and (name in errors['profissional']) and (exped in erexpedientes) ):
                        status=2
                    elif ((name in errors['paciente']) or (name in errors['profissional']) and (exped in erexpedientes) ):
                        status=1
                
                    newline=name+","+empresa+","+str(cnpj)+","+ str(proc)+","+str(exped)+","+str(datapub)+","+str(status)+"\n"
                    newlinescsv.append(newline)
                    
                    
                
            csvfile=open('medicamentos.csv', mode='w', encoding='utf-8') 
            csvfile.write(head)    
            for l in newlinescsv:
                if l == head:
                    continue
                else:
                    csvfile.write(l)
            csvfile.close()
        
        
            letterfile = open(crawlerStatusPath,"r")
            lines=letterfile.readlines()
            letterfile.close()
            
            newlines=[]
            for l in lines:
                a=l.strip("\n").split(",")
                if a[0]==self.currentletter:
                    update=self.currentletter+","+"1\n"
                    newlines.append(update)
                else:
                    newlines.append(l)
                    
                
            letterfile = open(crawlerStatusPath,"w")
            for l in newlines:
                letterfile.write(l)
            letterfile.close()
        
        
        
            if self.currentindex < (len(self.letters)-1):
                print("Starting the next REQUEST")
                self.currentindex+=1
                
                self.currentletter=self.letters[self.currentindex]
                
                print("Starting to download leaflets with letter: "+self.currentletter)
                f = open(errorLogPath,"w", encoding='utf-8')
                f.close()

                files = os.listdir(leafletsPath+"-"+ self.currentletter)
                print("Number of downloaded files = " + str(len(files)))
                expedientes={} 
                for fi in files:
                    s=fi.split("-")
                    extensão=(s[-2].split("_"))[-1]
                    expedientes[ (s[-1].replace(".pdf",""))+extensão ]=True 
            
                url=self.base_url + self.currentletter
                
                yield SplashRequest(url=url, callback=self.parse1, endpoint='execute', args={'wait': 3, 'lua_source': self.script1,'timeout':36000, 'med_baixados':expedientes, 'attempts': 10, 'letter': self.currentletter})
        
