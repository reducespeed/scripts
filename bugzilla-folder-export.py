import bugzilla
import os

login_object = bugzilla.Bugzilla(
    url="site/xmlrpc.cgi", 
    user="", 
    password=""
)

if login_object:
    
    # prikupljanje svih produkta
    all_products = login_object.getproducts()
    if all_products:
        
        # prolazak kroz svaki produkt
        for product in all_products:
            
            # formatiranje imena produkta i clasifikacije  koji ce se koristiti u putanji
            classification_name = product["classification"].strip().replace(" ", "_").replace(",", "_").replace(".", "_").replace("\t", "_").replace("/", "-").replace("\"", "-")
            product_name = product["name"].strip().replace(" ", "_").replace(",", "_").replace(".", "_").replace("\t", "_").replace("/", "-").replace("\"", "-")
            
            # prikupljanje komponenti koje pripadaju tekucem produktu  
            components = product["components"]
            if components:
                
                # prolazak kroz svaku komponentu
                for component in components:
                    
                    # formatiranje imena komponente koje ce se koristiti u putanji
                    component_name = component["name"].strip().replace(" ", "_").replace(",", "_").replace(".", "_").replace("\t", "_").replace("/", "-").replace("\"", "-")
                    
                    # prikupljanje bagova koji pripadaju tekucoj komponenti
                    all_bugs = login_object.query(
                        login_object.build_query(
                            product=product["name"], 
                            component=component["name"], 
                            include_fields=["summary"]
                        )
                    )
                    
                    if all_bugs:
                        
                        # prolazak kroz svaki bug
                        for bug in all_bugs:
                            
                            # formatiranje imena buga koje ce se koristiti u putanji
                            bug_name = bug.get_raw_data()["summary"].strip().replace(" ", "_").replace(",", "_").replace(".", "_").replace("\t", "_").replace("/", "-").replace("\"", "-")
                            
                            # formiranje putanje koja sadrzi bug
                            path = f'{classification_name}\\{product_name}\\{component_name}\\{bug_name}'
                            
                            # pravljenje foldera
                            os.makedirs(path, exist_ok=True)
                            
                            # stampanje
                            print(path)
                    else:
                        # formiranje putanje koja sadrzi bug
                        path = f'{classification_name}\\{product_name}\\{component_name}'
                        
                        # pravljenje foldera
                        os.makedirs(path, exist_ok=True)
                            
                        # stampanje
                        print(path)