function main(splash)
assert(splash:go(splash.args.url))
splash:wait(splash.args.wait)
os = require "os"

local letter=splash.args.letter

local med_baixados=splash.args.med_baixados


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
