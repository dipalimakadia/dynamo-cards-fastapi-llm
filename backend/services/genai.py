from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAI
from vertexai.generative_models import GenerativeModel
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from tqdm import tqdm
import json
import re 
import logging

#configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiProcessor:
    def __init__(self, model_name, project):
        self.model = VertexAI(model_name=model_name, project=project)
        
    def generate_document_summary(self, docmuents: list, **args):
        
        chain_type = "map_reduce" if len(docmuents) > 10 else "stuff"
        
        chain = load_summarize_chain(
            chain_type=chain_type,
            llm = self.model,
            **args
        )
            
        return chain.run(docmuents)
    
    def count_total_token(self, docs: list):
        temp_model = GenerativeModel("gemini-1.5-flash")
        total = 0
        logger.info("Counting total billable character..")
        

        for doc in tqdm(docs): 
            total += temp_model.count_tokens(doc.page_content).total_billable_characters
        return total
    
    def get_model(self):
        return self.model
    
    

class YoutubeProcessor:
    
    def __init__(self,genai_processor: GeminiProcessor):
        # self.genai_processor = genai_processor
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 0
        )
        self.GeminiProcessor = genai_processor
    
    def retrieve_youtube_documents(self, video_url: str, verbose= False):
        loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=True)
        docs = loader.load()
        result = self.text_splitter.split_documents(docs)
        
        author = result[0].metadata['author']
        length = result[0].metadata['length']
        title = result[0].metadata['title']
        total_size = len(result)
        total_billable_characters = self.GeminiProcessor.count_total_token(result)
        
        if verbose:
            logger.info(f"{author}\n{length}\n{title}\n{total_size}\n{total_billable_characters}")
        
        return result
    

    def find_key_concepts(self, documents:list, sample_size: int=0, verbose=False):
        #iterate through all documents of group size N and find key concepts
        
        if sample_size > len(documents):
            raise ValueError("Group size is larger than the number of documents")
        
        #Optimize sample size given no input
        if sample_size == 0:
            sample_size = len(documents) // 5
            if verbose: 
                logging.info(f"No sample size specified. Setting number of documents per sample as 5. Sample Size: {sample_size}")
        
        #Find num of documents in each group
        num_docs_per_group = len(documents) //sample_size + (len(documents) % sample_size > 0)
        
        #Check thresholds for response quality
        if num_docs_per_group >= 10:
            raise ValueError("Each group has more than 10 documents and quality will be degraded significantly. Increase the sample_size parameter to reduce the number of documents per group.")
        elif num_docs_per_group > 5:
            logging.warn("Each group has more than 5 documents and output quality is likely to be degraded. Consider increasing the sample size. ")
        
        
        #Split the doc in chunks of size num_docs_per_group
        groups = [documents[i: i+num_docs_per_group] for i in range(0, len(documents), num_docs_per_group)]
        
        batch_concepts = []
        batch_cost = 0
        
        logger.info("finding ket concepts...")
        for group in tqdm(groups):
            #Combine content of documents per group
            group_content = ""
            
            for doc in group:
                group_content += doc.page_content
            
            #Prompt for finding concepts
            prompt = PromptTemplate(
                template = """
                Find and define key concepts or terms found in the text: 
                {text}
                
                Respond in the following format as a string seprating each concept with a comma:
                {{"concept": "definition", "concept": "definition", ... }}
                """,
                
                input_variables=["text"]
            )
            
            #create chain
            chain = prompt | self.GeminiProcessor.model
            # chain = prompt | self.genai_processor.get_model()
            
            def clean_json_string(json_str):
                """Clean JSON String capturing only the value between curly braces
                Args:
                    json_str (str): uncleaned string
                Returns:
                    str: cleaned string
                """
                # Define a regex pattern to match everything before and after the curly braces
                pattern = r'^.*?({.*}).*$'
                # Use re.findall to extract the JSON part from the string
                matches = re.findall(pattern, json_str, re.DOTALL)
                if matches:
                    # If there's a match, return the first one (should be the JSON)
                    return matches[0]
                else:
                    # If no match is found, return None
                    return None
            
            #Run chain
            output_concept = chain.invoke({"text": group_content})
            clean_chain = clean_json_string(output_concept)
            batch_concepts.append(clean_chain)
            
            #Post Processing Observation
            if verbose: 
                total_input_char = len(group_content)
                total_input_cost = (total_input_char/1000) * 0.000125
                
                logging.info(f"Running chain on {len(group)} documents")
                logging.info(f"Total input characters: {total_input_char}")
                logging.info(f"Total cost: {total_input_cost}")
                
                total_output_char = len(clean_chain)
                total_output_cost = (total_output_char/1000) * 0.000375
                
                # logging.info(f"Running chain on {len(group)} documents")
                logging.info(f"Total outut characters: {total_output_char}")
                logging.info(f"Total cost: {total_output_cost}")
                
                batch_cost += total_input_cost + total_output_cost
                logging.info(f"Total group cost: {total_input_cost + total_output_cost}\n")
                
        #Convert each JSON string in batch_concepts to a Pyton 
        processed_concepts = [json.loads(concept) for concept in batch_concepts]
            
        logging.info(f"Total Analysis Cost: ${batch_cost}");   
        return processed_concepts
            