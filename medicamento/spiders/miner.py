
import scrapy
from scrapy_splash import SplashRequest
#import pandas as pd
from bs4 import BeautifulSoup
import os
from csv import DictReader
#import time
class MySpider(scrapy.Spider):
    name="miner"
    script1 = """
    function main(splash)
    	assert(splash:go(splash.args.url))
    	splash:wait(splash.args.wait)
    	os = require "os"
    	
    	local letter=splash.args.letter
    	
    	-- dicionário contendo os expedientes já baixados !!!
    	local med_baixados=splash.args.med_baixados
    	--print(med_baixados["1394254219"])
    	
    	function isInMedBaixados(key)
    	    return med_baixados[key]~=nil
    	end
    	
    	
    	function scroll(num_scrolls,scroll_delay)
        

            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {return document.body.scrollHeight;}"
            )
            

            for _ = 1, num_scrolls do
                local height = get_body_height()
                for i = 1, num_scrolls do
                    scroll_to(0, height * i/num_scrolls)
                    splash:wait(scroll_delay/10)
                end
            end        
        end
        
        scroll (math.random(4, 10),2)
        --local button_list = splash:select_all("button.btn.btn-default.ng-scope")
        --local el_expand=button_list[#button_list]
        --assert(el_expand:mouse_click{})
        
        splash:wait(math.random(4, 10)) 
        
        
        splash:set_viewport_full() 
        splash:wait(math.random(1, 3)) 
        
        
        local last_num
        local pagenum_list = splash:select_all("a.ng-scope[ng-switch-when=last]")

        if next(pagenum_list) == nil then
            last_num=1
        
        else
            
            local str_last_num= pagenum_list[#pagenum_list]:text()
            last_num=tonumber(str_last_num)
        end
        
        
        
        local data = ""
        
        for i = 1, last_num do
  	    local html=splash:html()
            print("page: " .. tostring(i) )

	    local medicamentos = splash:select_all("#containerTable > table > tbody > tr")
	    
  	    for i = 2, #medicamentos do
  	    
  	    	local nome_medicamento=splash:select("#containerTable > table > tbody > tr:nth-child("..tostring(i)..") > td:nth-child(1) > a"):text()
  	    	local expediente=splash:select("#containerTable > table > tbody > tr:nth-child("..tostring(i)..") > td:nth-child(3)"):text()
  	    	
  	    	local el_bula_paciente=splash:select("#containerTable > table > tbody > tr:nth-child("..tostring(i)..") > td:nth-child(5) > a")
  	        local url_paciente=el_bula_paciente["attributes"]["href"]
  	        
  	    	local el_bula_profissional=splash:select("#containerTable > table > tbody > tr:nth-child("..tostring(i)..") > td:nth-child(6) > a")
  	    	local url_profissional=el_bula_profissional["attributes"]["href"]
  	    	
  	    	
  	    	
  	    	if isInMedBaixados(expediente .. "paciente") then goto continue1 end
  	    	
  	  --Download das bulas do paciente:
  	        
  	        os.execute("echo bttminer | sudo -S python3 /home/bula_script.py '".. url_paciente .. "' '" .. nome_medicamento .. "' '_paciente' ".. expediente .." '".. tostring(splash.args.attempts) .. "' '".. letter .. "'" )
  	        
  	        
  	        ::continue1::
  	        
  	        if isInMedBaixados(expediente .. "profissional") then goto continue2 end
  	        
          --Download das bulas do profissional:
                
  	    	os.execute("echo bttminer | sudo -S python3 /home/bula_script.py '".. url_profissional .. "' '" .. nome_medicamento .. "' '_profissional' ".. expediente .." '".. tostring(splash.args.attempts) .. "' '".. letter .. "'")
  	    	
  	    	::continue2::
  	    	
  	    end
  	    
  	    splash:wait(5) 
            data = data .. html  
            splash:set_viewport_full() 
            splash:wait(math.random(2, 5)) 
            
            
            -- Terminar aqui caso não seja possível selecional esse elemento: 
            if not splash:select("a.ng-scope[ng-switch-when=next]") then
                if last_num == 1 then
                    return data
                else
                    
                    splash:wait(math.random(2, 5))
                    
                    if not splash:select("a.ng-scope[ng-switch-when=next]") then
                        print("ERRO: Ocorreu um problema no site")
                        return data
                    end
                    
                end           
            end
            
            
            local el = splash:select("a.ng-scope[ng-switch-when=next]")
            assert(el:mouse_click{})
            splash:wait(math.random(2, 5))
            
        end
	
        return data
    end
    """
    script2 = """
    function main(splash)
    	assert(splash:go(splash.args.url))
    	splash:wait(splash.args.wait)
    	os = require "os"
        
        local letter=splash.args.letter
        
    	function scroll(num_scrolls,scroll_delay)
        

            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {return document.body.scrollHeight;}"
            )
            

            for _ = 1, num_scrolls do
                local height = get_body_height()
                for i = 1, num_scrolls do
                    scroll_to(0, height * i/num_scrolls)
                    splash:wait(scroll_delay/10)
                end
            end        
        end
        
        
        
        splash:wait(math.random(8, 15)) 

        splash:set_viewport_full() 
        splash:wait(math.random(2, 6)) 
        
  	local last_num
  	splash:wait(math.random(4, 8)) 
        local pagenum_list = splash:select_all("a.ng-scope[ng-switch-when=last]")

        if next(pagenum_list) == nil then
            last_num=1
        
        else
            
            local str_last_num= pagenum_list[#pagenum_list]:text()
            last_num=tonumber(str_last_num)
        end
        
        local reqexpediente=splash.args.expediente
  	local tipo= splash.args.tipobula
        
  	for i = 1, last_num do
  	    
  	    
  	    local medicamentos = splash:select_all("#containerTable > table > tbody > tr")
  	    print("Repescando o Medicamento !")
  	    print("Numero de medicamentos na pag = " .. tostring(#medicamentos) )
  	    
  	    
  	    for i = 2, #medicamentos do
  	    
  	        local nome_medicamento=splash:select("#containerTable > table > tbody > tr:nth-child("..tostring(i)..") > td:nth-child(1) > a"):text()
  	    	local expediente=splash:select("#containerTable > table > tbody > tr:nth-child("..tostring(i)..") > td:nth-child(3)"):text()
  	        
        
                if expediente ==  reqexpediente then
        
  	            --Download das bulas do paciente:
  	            if tipo == "paciente" then
  	                local el_bula_paciente=splash:select("#containerTable > table > tbody > tr:nth-child(2) > td:nth-child(5) > a")
  	                local url_paciente=el_bula_paciente["attributes"]["href"]
  	    
  	                os.execute("echo bttminer | sudo -S python3 /home/bula_script.py '".. url_paciente .. "' '" .. nome_medicamento .. "' '_paciente' ".. expediente .." '".. tostring(splash.args.attempts) .. "' '".. letter .. "'" )
  	            end
  	
  	
  	        
  	        
                    --Download das bulas do profissional:
                    if tipo == "profissional" then
  	                local el_bula_profissional=splash:select("#containerTable > table > tbody > tr:nth-child(2) > td:nth-child(6) > a")
  	                local url_profissional=el_bula_profissional["attributes"]["href"]
  	    
  	                os.execute("echo bttminer | sudo -S python3 /home/bula_script.py '".. url_profissional .. "' '" .. nome_medicamento .. "' '_profissional' ".. expediente .." '".. tostring(splash.args.attempts) .. "' '".. letter .. "'")
  	            end
  	    
  	        end
  	    end
  	end
  	
  	    	
        splash:wait(math.random(2, 8)) 
        local html=splash:html()
        return html
        
    end
    """
    #https://consultas.anvisa.gov.br/#/medicamentos/25351185745200412/
    base_url = "https://consultas.anvisa.gov.br/#/bulario/q/?nomeProduto="
    letters=[]
    currentletter=""
    currentindex=0
    downloaderrors=[]
    currentdindex=0
    meta={'COOKIES_DEBUG': True}
    
    def start_requests(self):
        
        #escolhendo as letras que serão baixadas:
        
        letterfile = open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/crawlerstatus.csv","r")
        lines=letterfile.readlines()
        letterfile.close()
        for l in lines:
            a=l.strip("\n").split(",")
            if a[1]=="0":
                self.letters.append(a[0])
        print(self.letters)
        
        #Executando o splash:
        
        self.currentletter=self.letters[0]
        url=self.base_url + self.currentletter
            
        #Limpando o arquivo errorlog.txt:
        f = open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/dockerfolder/errorlog.txt","w", encoding='utf-8')
        f.close()
        #Criando um dicionario com os medicamentos já baixados:
        files = os.listdir("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/dockerfolder/bulas"+"-"+ self.currentletter)
        print("Numero de arquivos já baixados=" + str(len(files)))
        expedientes={} #Lista com os expedientes dos medicamentos baixados
        for fi in files:
            s=fi.split("-")
            extensão=(s[-2].split("_"))[-1]
            expedientes[ (s[-1].replace(".pdf",""))+extensão ]=True 
            #time.sleep(10)
        yield SplashRequest(url=url, callback=self.parse1, endpoint='execute', args={'wait': 3, 'lua_source': self.script1,'timeout':36000, 'med_baixados':expedientes, 'attempts': 10, 'letter': self.currentletter})
	        
    
     
    def parse1(self, response):  
        #Abrindo errorlog para repescagem dos arquivos
        errorlog=open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/dockerfolder/errorlog.txt","r", encoding='utf-8')
        erlines=errorlog.readlines()
        errorlog.close()
        
        #Limpando novamente arquivo errorlog.txt:
        f = open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/dockerfolder/errorlog.txt","w", encoding='utf-8')
        f.close()
        
        
        
        lstring=""
        if len(erlines)>0:
            for l in erlines:
                if l != "":
                    self.downloaderrors.append(l.strip("\n").split("_"))
                
                
                
        #Os erros que sobraram vão ser reportados no csv a partir do Status
        #status == 0 => as duas bulas foram baixadas 
        #status == 1 => uma das duas bulas foi baixada 
        #status == 2 => nenhuma bula foi baixada
        erros={'paciente':[], 'profissional': []}
        erexpedientes=[]
        
        
        
        
        
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


         
        campos=['Medicamento','Empresa','CNPJ',"Processo",'Expediente','Data de Publicação', 'Status']
        head=",".join(campos)+"\n"
        csvfile= open('medicamentos.csv', mode='r', encoding='utf-8') 
        lines=csvfile.readlines()
        csvfile.close()
        
                
        csvfile=open('medicamentos.csv', mode='w', encoding='utf-8') 
        csvfile.write(head)
        
        
        print("Download Errors:")
        print(self.downloaderrors)
        
        
        
        #Erros detectados:
        if len(self.downloaderrors)>0:

            for l in erlines:
                a=l.strip("\n").split("_")
                erexpedientes.append(a[2])
                if a[1] == 'paciente':
                    erros['paciente'].append(a[0])
                else:
                    erros['profissional'].append(a[0])
        
            for i in range(len(med_names)):
                status=0
                
                if ((med_names[i] in erros['paciente']) and (med_names[i] in erros['profissional']) and (expedientes[i] in erexpedientes)):
                    status=2
                elif ((med_names[i] in erros['paciente']) or (med_names[i] in erros['profissional']) and (expedientes[i] in erexpedientes)):
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
            
            #Repescagem
            
            print("Iniciando repescagem das bulas: "+lstring)
            print(erros)
            print(self.downloaderrors)    
            tipo=self.downloaderrors[self.currentdindex][1]
            link="https://consultas.anvisa.gov.br/#/bulario/q/?nomeProduto="
            yield SplashRequest(url=link+self.downloaderrors[self.currentdindex][0], callback=self.parse2, endpoint='execute', args={'wait': 3, 'lua_source': self.script2,'timeout':36000,'tipobula': tipo,'expediente': self.downloaderrors[self.currentdindex][2] ,'attempts': 20, 'letter':  self.currentletter})
            
            
            
            
            
            
            
        #Não há erros detectados
        else:
            print("Nenhum erro detectado")   

        
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
        
        
            #atualizando o status da letra baixada
        
            letterfile = open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/crawlerstatus.csv","r")
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
                    
            letterfile = open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/crawlerstatus.csv","w")
            for l in newlines:
                letterfile.write(l)
            letterfile.close()
        
            #continuar para a proxima letra
            if self.currentindex < (len(self.letters)-1):
                print("Iniciando o Proximo REQUEST")
                self.currentindex+=1
                
                print(self.currentindex)
                
                self.currentletter=self.letters[self.currentindex]
                
                print("Iniciando a letra: "+self.currentletter)
                #Limpando o arquivo errorlog.txt:
                f = open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/dockerfolder/errorlog.txt","w", encoding='utf-8')
                f.close()
                #Criando um dicionario com os medicamentos já baixados:
                files = os.listdir("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/dockerfolder/bulas"+"-"+ self.currentletter)
                print("Numero de arquivos já baixados=" + str(len(files)))
                expedientes={} #Lista com os expedientes dos medicamentos baixados
                for fi in files:
                    s=fi.split("-")
                    extensão=(s[-2].split("_"))[-1]
                    expedientes[ (s[-1].replace(".pdf",""))+extensão ]=True 
            
                url=self.base_url + self.currentletter
                
                yield SplashRequest(url=url, callback=self.parse1, endpoint='execute', args={'wait': 3, 'lua_source': self.script1,'timeout':36000, 'med_baixados':expedientes, 'attempts': 10, 'letter': self.currentletter})
        
 
 
 
 
 
 
 
 
 
 
 
 
 
 
    def parse2(self, response):
        self.currentdindex+=1
        if self.currentdindex<len(self.downloaderrors):
            print("Chamando Parse2 (Contunuando repescagem)")
            
        
            tipo=self.downloaderrors[self.currentdindex][1]
            link="https://consultas.anvisa.gov.br/#/bulario/q/?nomeProduto="
            yield SplashRequest(url=link+self.downloaderrors[self.currentdindex][0], callback=self.parse2, endpoint='execute', args={'wait': 3, 'lua_source': self.script2,'timeout':36000,'tipobula': tipo,'expediente':self.downloaderrors[self.currentdindex][2],'attempts': 20, 'letter':  self.currentletter})
        
        else:
            self.downloaderrors.clear()
            self.currentdindex=0
            print("Chamando Parse2 (Fim da repescagem)") 
                
            #Verificando se sobraram erros no errorlog
            errorlog=open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/dockerfolder/errorlog.txt","r", encoding='utf-8')
            lines=errorlog.readlines()
            errorlog.close()
        
            #Limpando errorlog mais uma vez     
            f = open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/dockerfolder/errorlog.txt","w", encoding='utf-8')
            f.close()
        
            #Os erros que sobraram vão ser reportados no csv a partir do Status
            #status == 0 => as duas bulas foram baixadas 
            #status == 1 => uma das duas bulas foram baixadas 
            #status == 2 => nenhuma bula foi baixada
            erros={'paciente':[], 'profissional': []}
            erexpedientes=[]
            
            for l in lines:
                a=l.strip("\n").split("_")
                erexpedientes.append(a[2])
                if a[1]=='paciente':
                    erros['paciente'].append(a[0])
                else:
                    erros['profissional'].append(a[0])
            #######################################################
            print("ERROS RESTANTES: ")
            print(erros)
            #######################################################
         
            campos=['Medicamento','Empresa','CNPJ',"Processo",'Expediente','Data de Publicação', 'Status']
            head=",".join(campos)+"\n"
            #csvfile= open('medicamentos.csv', mode='r', encoding='utf-8') 
            #lines=csvfile.readlines()
            #csvfile.close()
            newlinescsv=[]
            with open('medicamentos.csv', mode='r', encoding='utf-8') as my_file:
                #passing file object to DictReader()
                csv_dict_reader = DictReader(my_file)

                
                #c=0
                for i in csv_dict_reader:
                    print(i)
                    #l=lines[c]
                #linelist=l.encode('utf-8', 'replace').decode().strip("\n").split(",",6)
                #print(linelist)
                    name=i["Medicamento"]
                    empresa=i["Empresa"]
                    cnpj=i["CNPJ"]
                    proc=i["Processo"]
                    exped=i["Expediente"]
                    datapub=i["Data de Publicação"]
                
                #name=linelist[0]
                #exped=linelist[4]
                #linelist.remove(name)
                #rlist=linelist[:(len(linelist)-1)]
                
                
                
                    status=0
                    if ((name in erros['paciente']) and (name in erros['profissional']) and (exped in erexpedientes) ):
                        status=2
                    elif ((name in erros['paciente']) or (name in erros['profissional']) and (exped in erexpedientes) ):
                        status=1
                
                #resto=(",".join(rlist))+","+str(status)+"\n"
                #newline=name+resto
                    newline=name+","+empresa+","+str(cnpj)+","+ str(proc)+","+str(exped)+","+str(datapub)+","+str(status)+"\n"
                    newlinescsv.append(newline)
                    #if newline == l:
                    #    continue
                    #else:
                    #    lines.remove(l)
                    #    lines.append(newline)
                    
                    #c+=1
                    
                    
                
            csvfile=open('medicamentos.csv', mode='w', encoding='utf-8') 
            csvfile.write(head)    
            for l in newlinescsv:
                if l == head:
                    continue
                else:
                    csvfile.write(l)
            csvfile.close()
        
        
            #atualizando o status da letra baixada
        
            letterfile = open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/crawlerstatus.csv","r")
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
                    
                
            letterfile = open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/crawlerstatus.csv","w")
            for l in newlines:
                letterfile.write(l)
            letterfile.close()
        
        
        
            if self.currentindex < (len(self.letters)-1):
                print("Iniciando o proximo REQUEST")
                self.currentindex+=1
                
                self.currentletter=self.letters[self.currentindex]
                
                print("Iniciando a letra: "+self.currentletter)
                #Limpando o arquivo errorlog.txt:
                f = open("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/dockerfolder/errorlog.txt","w", encoding='utf-8')
                f.close()
                #Criando um dicionario com os medicamentos já baixados:
                files = os.listdir("/home/otavio/Desktop/modelos/teste_scrapy/Scrapy_Crawler/dockerfolder/bulas"+"-"+ self.currentletter)
                print("Numero de arquivos já baixados=" + str(len(files)))
                expedientes={} #Lista com os expedientes dos medicamentos baixados
                for fi in files:
                    s=fi.split("-")
                    extensão=(s[-2].split("_"))[-1]
                    expedientes[ (s[-1].replace(".pdf",""))+extensão ]=True 
            
                url=self.base_url + self.currentletter
                
                yield SplashRequest(url=url, callback=self.parse1, endpoint='execute', args={'wait': 3, 'lua_source': self.script1,'timeout':36000, 'med_baixados':expedientes, 'attempts': 10, 'letter': self.currentletter})
        
