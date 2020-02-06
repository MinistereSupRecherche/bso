import fastText
from notebook_utils import *

model = fastText.load_model('/media/jerem/DATA/Eric/PascalFrancis/dataset/model_pf.bin')

def get_category(title, is_strict = True, nb_top = 10, verbose=False):
    title_norm = normalize_text(title).lower()
    prediction = model.predict(title_norm,nb_top)
    
    if(verbose):
        print(prediction)
            
    for i, k in enumerate(prediction[0]):
        

        if is_strict and prediction[1][i] < 0.1:
            break
            
        #Medical
        for elt in ["__label__pascal::002B", "__label__macrodomain::per", "__label__macrodomain::med", \
                   "__label__macrodomain::gbm", "__label__macrodomain::ped", "__label__macrodomain::neu", \
                   "__label__macrodomain::mtr", "__label__macrodomain::gen", "__label__macrodomain::lab", \
                   "__label__macrodomain::pne"]:
            if elt in k:
                return "Medical research"
############################################################    
        
            
        #Biology
        for elt in ["__label__pascal::002A", "__label__macrodomain::eto", "__label__macrodomain::blc", \
                   "__label__macrodomain::blg", "__label__macrodomain::btc", "__label__macrodomain::mic"]:
            if elt in k:
                return "Biology (fond.)"
            

##########################################################################    

        for elt in ["__label__pascal::001D09", "__label__macrodomain::gch", "__label__macrodomain::pha", \
                   "__label__pascal::001D10", "__label__pascal::001D07", "__label__macrodomain::ply",  "__label__pascal::001D08"]:
            if elt in k:
                return "Chemistry"# "Chemical engineering"
            
                #chemistry
        for elt in ["__label__pascal::001C", "__label__macrodomain::chg:", "__label__macrodomain::chi",\
                   "__label__macrodomain::cho"]:
            if elt in k:
                return "Chemistry"# "Chemical sciences"
#######################################################

        #civil eng.
        for elt in ["__label__macrodomain::gci","__label__pascal::001D14"]:
            if elt in k:
                return "Engineering"#"Civil Engineering"
            
                    #electrical, electronic
        for elt in ["__label__pascal::001D05", "__label__pascal::001D03", \
                    "__label__macrodomain::eln::fr_Electronique", "__label__macrodomain::elt", "__label__macrodomain::met"]:
            if elt in k:
                return "Engineering"#"Electrical eng., electronic eng."
       
        #mechanical eng.
        for elt in ["__label__macrodomain::gmc","__label__pascal::001D12", "__label__pascal::001D11", \
                    "__label__pascal::001D15"]:
            if elt in k:
                return "Engineering"#"Mechanical Engineering"
            

########################################################################"

        #Physical sciences, Astronomy
        for elt in ["__label__pascal::001E03", "__label__pascal::001B",\
                    "__label__macrodomain::pam", "__label__macrodomain::pth", "__label__macrodomain::phq", \
                   "__label__macrodomain::ppl", "__label__macrodomain::pec", \
                   "__label__macrodomain::mec", "__label__macrodomain::opt"]:
            if elt in k:
                return "Physical sciences, Astronomy"
            
            
#########################################################  

        #Mathematics
        for elt in ["__label__pascal::001A02", "__label__macrodomain::mat"]:
            if elt in k:
                return "Mathematics"
########################################################     

        for elt in ["_label__macrodomain::inf::fr_Informatique", "__label__pascal::001A01", "__label__pascal::001D02", \
                    "__label__pascal::001D02B07", "__label__pascal::001D02A", "__label__francis::790"]:
            if elt in k:
                return "Computer and \n information sciences"
            
                #telecommunication
        for elt in ["__label__pascal::001D04", "__label__macrodomain::tel"]:
            if elt in k:
                return "Computer and \n information sciences"#"Telecommunications and information theory"
            
        for elt in ["__label__macrodomain::aut", \
                   "__label__pascal::001D01A", "__label__pascal::001D01"]:
            if elt in k:
                return "Computer and \n information sciences"#"Control theory and operations research"
            
###############################################################         
            
        #Agriculture
        for elt in ["__label__pascal::002A32", "__label__pascal::002A14", \
                    "__label__pascal::002A33", \
                    "__label__macrodomain::for::fr_Foresterie,_sylviculture", \
                   "__label__macrodomain::agr"]:
            if elt in k:
                return "Earth, Ecology, \nEnergy and applied biology" #"Agriculture, forestry, fisheries"
            
                #environment
        for elt in ["__label__macrodomain::env", "__label__pascal::001D16", "__label__pascal::001E",\
                    "__label__pascal::001D06C", "__label__macrodomain::mto", "__label__macrodomain::oce", \
                   "__label__macrodomain::eko", "__label__macrodomain::glo"]:
            if elt in k:
                return "Earth, Ecology, \nEnergy and applied biology" #"Earth and environmental sciences"
            
        for elt in [ "__label__macrodomain::ene", "__label__pascal::001D06"]:
            if elt in k:
                return "Earth, Ecology, \nEnergy and applied biology" # "Energy"

            
########################################################################       

        
        #laws
        for elt in ["__label__francis::528-"]:
            if elt in k:
                return "Social sciences" #"Law"
                #sociology
        for elt in ["__label__francis::521", "__label__macrodomain::soc::fr_Sociologie::en_Sociology"]:
            if elt in k:
                return "Social sciences" #"Sociology"
            
        for elt in ["__label__macrodomain::tra"]:
            if elt in k:
                return "Social sciences" #"Economics and Transports"
            
          
        for elt in ["__label__francis::617","__label__pascal::001D06A", "__label__pascal::001D01A14", \
                   "__label__macrodomain::ges"]:
            if elt in k:
                return "Social sciences"# "Economics and Transports"
            
        
        for elt in ["__label__macrodomain::geo", "__label__francis::531"]:
            if elt in k:
                return "Social sciences"#"Geography"
            
        for elt in ["__label__francis::528-321", "__label__macrodomain::scp"]:
            if elt in k:
                return "Social sciences"# "Political sciences"
            
        for elt in ["__label__macrodomain::psy::", "__label__francis::770-"]:
            if elt in k:
                return "Social sciences"# "Psychology, psychopathology, psychiatry"
            
                    
        for elt in ["__label__francis::520", "__label__macrodomain::edu", "__label__francis::521-34", "__label__pascal::002A26K"]:
            if elt in k:
                return "Social sciences"#"Educational sciences"
            
        for elt in ["__label__macrodomain::com", "__label__macrodomain::doc"]:
            if elt in k:
                return "Social sciences"#"Information and communications"
            
####################################################################

        for elt in ["__label__francis::519-6", "__label__francis::540"]:
            if elt in k:
                return "Humanities" #"Art"

        for elt in ["__label__francis::526", "__label__francis::525"]:
            if elt in k:
                return "Humanities" # "Archeology and History"
            
        for elt in ["__label__francis::522"]:
            if elt in k:
                return "Humanities" #"History of science and technology"
            
        for elt in ["__label__francis::524", "_label__francis::523", "__label__macrodomain::lng"]:
            if elt in k:
                return "Humanities" # "Languages and literature"
            
        #philosophy
        for elt in ["__label__francis::519", "__label__francis::527"]:
            if elt in k:
                return "Humanities" #"Philosophy, Ethics, Religion"
            
                
        for elt in ["__label__francis::529", "__label__macrodomain::eth"]:
            if elt in k:
                return "Humanities" #"Other humanities"
            

###########################################################""


    return "unknown"
