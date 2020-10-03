# -*- coding: utf-8 -*-
"""
@About - Watson NLP Entity data extraction
@author: Sanjay Tanneeru
"""
#You would need to sign up with IBM NLP service for api key, they have a trial version
def NLP_Authentication(): 
    from ibm_watson import NaturalLanguageUnderstandingV1 
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    
    authenticator = IAMAuthenticator('<Authentication key>')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
                                    version='<version date>',
                                    authenticator=authenticator)        
    natural_language_understanding.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')

    return natural_language_understanding

def EntityDataframe(entity_URL,entity_company,entity_relevance,entity_date):
    import pandas as pd
    
    DF_News_USA_Entity = pd.DataFrame(columns=['URL','Company_Name','Relevance','Current_Date'])

    DF_News_USA_Entity['URL']           = entity_URL
    DF_News_USA_Entity['Company_Name']  = entity_company
    DF_News_USA_Entity['Relevance']     = entity_relevance
    DF_News_USA_Entity['Current_Date']  = entity_date
    
    return DF_News_USA_Entity

def main():
    #import packages
    from datetime import date
    from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions
    
    #Example URL
    URL = ['https://www.cnbc.com/2019/03/22/reuters-america-update-4-german-bund-yield-crashes-below-zero-for-first-time-since-2016-as-bleak-data-rattles-markets.html']
    
    #NLP Processing begin
    #Get NPL authentication key object
    natural_language_understanding = NLP_Authentication()
    
    url             = []
    company         = []
    relevance       = []
    current_date    = []
    count           = 0

    for u in URL:
        count += 1
        
        print("Processing "+ str(count))
        try:
            response = natural_language_understanding.analyze(url=u,features=Features(entities=EntitiesOptions(sentiment=True,limit=50))).get_result()
            entities=response['entities']   
            company_list=[]
            
            for i in entities:
                if i['type']=='Company':
                    company_list.append(i)
                    
            if len(entities) > 0 :
                relevance_score=max([i['relevance'] for i in company_list])
                for i in company_list:
                    if i['relevance']==relevance_score:
                        company_name=i['text']
            else:
                relevance_score='NA'
                company_name='NA'
                
            url.append(u)
            relevance.append(relevance_score)
            company.append(company_name)
            current_date.append(date.today().strftime('%m/%d/%Y'))
        
        except:
            continue
    
    Processed_USA_Entity_DF = EntityDataframe(url,company,relevance,current_date)
    
    if len(Processed_USA_Entity_DF) > 0:
        Processed_USA_Entity_DF.to_csv('<Enter CSV file name>')
    else:
        return
if __name__ == '__main__':
    main()