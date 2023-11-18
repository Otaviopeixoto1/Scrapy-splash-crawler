function main(splash)
assert(splash:go(splash.args.url))
splash:wait(splash.args.wait)
os = require "os"

--os.execute("echo bttminer | adduser splash sudo")

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
    
        local nome_medicamento=splash:select("#containerTable > table > tbody > tr:nth-child("..tostring(i)..") > td:nth-child(2) > a"):text()
    	local expediente=splash:select("#containerTable > table > tbody > tr:nth-child("..tostring(i)..") > td:nth-child(4)"):text()
        

        if expediente ==  reqexpediente then

            --Download das bulas do paciente:
            if tipo == "paciente" then
                local el_bula_paciente=splash:select("#containerTable > table > tbody > tr:nth-child(2) > td:nth-child(6) > a")
                local url_paciente=el_bula_paciente["attributes"]["href"]
    
                os.execute("echo bttminer | sudo -S python3 /home/bula_script.py '".. url_paciente .. "' '" .. nome_medicamento .. "' '_paciente' ".. expediente .." '".. tostring(splash.args.attempts) .. "' '".. letter .. "'" )
            end


        
        
            --Download das bulas do profissional:
            if tipo == "profissional" then
                local el_bula_profissional=splash:select("#containerTable > table > tbody > tr:nth-child(2) > td:nth-child(7) > a")
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
