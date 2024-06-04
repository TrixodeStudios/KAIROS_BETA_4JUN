# import argparse
# import asyncio
# import json
# from database import Session, Conversations
# from gemini import analyze_conversation
# from config import GEMINI_MODELS, ANALYSIS_FEATURES


# async def process_conversation(conversation_id, model, features):
#     session = Session()
#     try:
#         conversation = session.query(Conversations).get(conversation_id)
#         if not conversation:
#             print(f"Conversation with ID {conversation_id} not found.")
#             return

#         # Prepare data for Gemini
#         prepared_data = [
#             {"role": "system", "content": "You are an expert conversation analyst. I'll provide you with a conversation and your task is to analyze it. I want you to extract sentiments, entities, intents, and topics."},
#             {"role": "user", "content": conversation.text},
#         ]

#         results = await analyze_conversation(prepared_data, model=model, features=features)

#         # Process and store results
#         if results:
#             for feature in features:
#                 session.add(AnalysisResults(
#                     conversation_id=conversation.id,
#                     feature=feature,
#                     result=json.dumps(results.get(feature, "")),
#                 ))

#         session.commit()

#     except Exception as e:
#         print(f"Error processing conversation {conversation_id}: {e}")
#         session.rollback()
#     finally:
#         session.close()


# async def main():
#     parser = argparse.ArgumentParser(description="Analyze conversations using Gemini Pro.")
#     parser.add_argument("--model", choices=GEMINI_MODELS.keys(), default="chat-bison", help="The Gemini model to use")
#     parser.add_argument("--features", nargs="+", choices=ANALYSIS_FEATURES, default=ANALYSIS_FEATURES, help="The features to extract (sentiment, entities, intents, topics, summary, translation)")
#     args = parser.parse_args()

#     session = Session()
#     conversations = session.query(Conversations).all()
#     session.close()

#     tasks = [process_conversation(conversation.id, GEMINI_MODELS[args.model], args.features) for conversation in conversations]
#     await asyncio.gather(*tasks)


# if __name__ == "__main__":
#     asyncio.run(main())
import argparse
import asyncio
import json
from database import Session, Conversations, AnalysisResults
from gemini import analyze_conversation
from config import GEMINI_MODELS, ANALYSIS_FEATURES


async def process_conversation(conversation_id, model, features):
    """Processes a single conversation asynchronously."""
    
    session = Session()
    try:
        conversation = session.query(Conversations).get(conversation_id)
        if not conversation:
            print(f"Conversation with ID {conversation_id} not found.")
            return

        # Prepare data for Gemini
        prepared_data = [
            {"role": "system", "content": "You are an expert conversation analyst. I'll provide you with a conversation and your task is to analyze it. I want you to extract sentiments, entities, intents, and topics."},
            {"role": "user", "content": conversation.text},
        ]

        results = await analyze_conversation(prepared_data, model=model, features=features)

        # Process and store results
        if results:
            for feature in features:
                session.add(AnalysisResults(
                    conversation_id=conversation.id,
                    feature=feature,
                    result=json.dumps(results.get(feature, "")),
                ))

        session.commit()

    except Exception as e:
        print(f"Error processing conversation {conversation_id}: {e}")
        session.rollback()
    finally:
        session.close()


async def main():
    """The main entry point for the script."""
    
    parser = argparse.ArgumentParser(description="Analyze conversations using Gemini Pro.")
    parser.add_argument("--model", choices=GEMINI_MODELS.keys(), default="chat-bison", help="The Gemini model to use")
    parser.add_argument("--features", nargs="+", choices=ANALYSIS_FEATURES, default=ANALYSIS_FEATURES, help="The features to extract (sentiment, entities, intents, topics, summary, translation)")
    args = parser.parse_args()

    session = Session()
    conversations = session.query(Conversations).all()
    session.close()

    tasks = [process_conversation(conversation.id, GEMINI_MODELS[args.model], args.features) for conversation in conversations]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())







