# import google.generativeai as genai
# import json
# from config import GEMINI_API_KEY, client_options, GEMINI_MODELS
# from database import Session, TokenUsage, AnalysisResults 


# def get_token_count(text):
#     # This is a simplified estimation.  Actual token usage might vary.
#     return len(text)

# def get_estimated_cost(model, total_tokens):
#     # Replace with your actual pricing details from Gemini documentation
#     pricing = {
#         "models/gemini-1.5-flash": 0.002,  # Example pricing per 1K tokens
  
#         # Add more models as needed
#     }
#     price_per_1k_tokens = pricing.get(model, 0)
#     return (total_tokens / 1000) * price_per_1k_tokens

# def analyze_conversation(conversation_data, model="models/gemini-1.5-flash", features=None):
#     try:
#         features = features or ["sentiment", "entities", "intents", "topics", "summary"]
#         system_prompt = "You are an expert conversation analyst. Analyze the following conversation. Extract the following information:\n"
#         for feature in features:
#             system_prompt += f"- {feature}\n"
        
#         messages = [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": conversation_data[1]['content']},
#         ]

#         response = genai.generate_text(model=model, prompt={"messages": messages})

#         if response.result:
#             # Count tokens, estimate cost, and store in database
#             total_tokens = get_token_count(conversation_data, model)
#             estimated_cost = get_estimated_cost(model, total_tokens)
#             store_token_usage(conversation_data, model, total_tokens, estimated_cost)

#             # Store analysis results
#             store_analysis_results(conversation_data, model, response.result, features) 

#             return response.result 
#         else:
#             raise Exception(f"Gemini API error: {response.error}")
#     except Exception as e:
#         print(f"Error analyzing conversation: {e}")
#         # Here you can implement more robust error handling, such as:
#         # - Logging the error with more details
#         # - Notifying administrators
#         # - Retrying the request after a delay
#         return None
    
# def store_token_usage(conversation_data, model, total_tokens, estimated_cost):
#     session = Session()
#     new_entry = TokenUsage(
#         conversation_id=conversation_data[1]['content'], # Assuming this is how you get the conversation ID
#         model=model,
#         total_tokens=total_tokens,
#         estimated_cost=estimated_cost
#     )
#     session.add(new_entry)
#     session.commit()
#     session.close()

# def store_analysis_results(conversation_data, model, result, features):
#     session = Session()
#     for feature in features:
#         new_entry = AnalysisResults(
#             conversation_id=conversation_data[1]['content'],
#             feature=feature,
#             result=json.dumps(result.get(feature, "")),  # Store the result or an empty string if not found
#         )
#         session.add(new_entry)
#     session.commit()
#     session.close() 
import google.generativeai as genai
import json
from config import GEMINI_API_KEY, client_options, GEMINI_MODELS
from database import Session, TokenUsage, AnalysisResults 


def get_token_count(text):
    # This is a simplified estimation.  Actual token usage might vary.
    return len(text)


def get_estimated_cost(model, total_tokens):
    # Replace with your actual pricing details from Gemini documentation
    pricing = {
        "models/gemini-1.5-flash": 0.002,  # Example pricing per 1K tokens
        # Add more models as needed
    }
    price_per_1k_tokens = pricing.get(model, 0)
    return (total_tokens / 1000) * price_per_1k_tokens

def analyze_conversation(conversation_data, model="models/gemini-1.5-flash", features=None):
    try:
        features = features or ["sentiment", "entities", "intents", "topics", "summary"]
        system_prompt = "You are an expert conversation analyst. Analyze the following conversation. Extract the following information:\n"
        for feature in features:
            system_prompt += f"- {feature}\n"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": conversation_data[1]['content']},
        ]

        response = genai.generate_text(model=model, prompt={"messages": messages})

        if response.result:
            # Count tokens, estimate cost, and store in database
            total_tokens = get_token_count(conversation_data, model)
            estimated_cost = get_estimated_cost(model, total_tokens)
            store_token_usage(conversation_data, model, total_tokens, estimated_cost)

            # Store analysis results
            store_analysis_results(conversation_data, model, response.result, features) 

            return response.result 
        else:
            raise Exception(f"Gemini API error: {response.error}")
    except Exception as e:
        print(f"Error analyzing conversation: {e}")
        # Here you can implement more robust error handling, such as:
        # - Logging the error with more details
        # - Notifying administrators
        # - Retrying the request after a delay
        return None
    
def store_token_usage(conversation_data, model, total_tokens, estimated_cost):
    session = Session()
    new_entry = TokenUsage(
        conversation_id=conversation_data[1]['content'], # Assuming this is how you get the conversation ID
        model=model,
        total_tokens=total_tokens,
        estimated_cost=estimated_cost
    )
    session.add(new_entry)
    session.commit()
    session.close()

def store_analysis_results(conversation_data, model, result, features):
    session = Session()
    for feature in features:
        new_entry = AnalysisResults(
            conversation_id=conversation_data[1]['content'],
            feature=feature,
            result=json.dumps(result.get(feature, "")),  # Store the result or an empty string if not found
        )
        session.add(new_entry)
    session.commit()
    session.close() 
