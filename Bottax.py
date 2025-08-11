# import os
# import streamlit as st
# from langchain_openai import ChatOpenAI 
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.prompts import PromptTemplate
# from langchain.chains import RetrievalQA
# from langchain_community.vectorstores import FAISS
# from datetime import datetime
# from huggingface_hub import InferenceClient
# from langchain.llms.base import LLM
# from typing import Optional, List, Any
# import speech_recognition as sr
# from io import BytesIO
# import wave
# import tempfile

# # Configure page
# st.set_page_config(
#     page_title="BotTax - AI Tax Consultation Assistant", 
#     page_icon="💰", 
#     layout="wide"
# )

# # Vector DB path
# db_path = "vector_store\\faiss_database"

# # Dark blackish themed CSS styling with OpenAI branding colors
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
#     .stApp {
#         background: linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #1a1a1a 50%, #0a0a0a 75%, #000000 100%);
#         font-family: 'Inter', sans-serif;
#         color: #f5f5f5;
#     }
    
#     /* Dark financial brand header with subtle OpenAI accent */
#     .financial-header {
#         background: linear-gradient(135deg, rgba(0, 0, 0, 0.98) 0%, rgba(26, 26, 26, 0.95) 100%);
#         border: 2px solid rgba(64, 64, 64, 0.3);
#         border-radius: 20px;
#         padding: 2.5rem;
#         margin-bottom: 2rem;
#         box-shadow: 
#             0 20px 40px rgba(0, 0, 0, 0.8),
#             inset 0 1px 0 rgba(255, 255, 255, 0.05),
#             0 0 20px rgba(116, 222, 128, 0.03);
#         backdrop-filter: blur(15px);
#         text-align: center;
#         position: relative;
#         overflow: hidden;
#     }
    
#     .financial-header::before {
#         content: '';
#         position: absolute;
#         top: -50%;
#         left: -50%;
#         width: 200%;
#         height: 200%;
#         background: linear-gradient(45deg, transparent, rgba(116, 222, 128, 0.02), transparent);
#         animation: shimmer 8s infinite linear;
#     }
    
#     @keyframes shimmer {
#         0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
#         100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
#     }
    
#     .financial-title {
#         font-size: 3rem;
#         font-weight: 900;
#         background: linear-gradient(135deg, #4a4a4a 0%, #666666 30%, #808080 70%, #595959 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         text-shadow: 0 4px 8px rgba(0,0,0,0.9);
#         margin-bottom: 0.5rem;
#         position: relative;
#         z-index: 2;
#         filter: drop-shadow(0 0 10px rgba(74, 74, 74, 0.8));
#     }
    
#     .financial-subtitle {
#         font-size: 1.3rem;
#         color: #666666;
#         font-weight: 500;
#         margin-bottom: 1rem;
#         position: relative;
#         z-index: 2;
#     }
    
#     .financial-description {
#         color: #888888;
#         font-size: 1rem;
#         margin-top: 1rem;
#         position: relative;
#         z-index: 2;
#     }
    
#     /* Status cards with subtle OpenAI accent */
#     .status-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
#         gap: 1.5rem;
#         margin-bottom: 2rem;
#     }
    
#     .status-card {
#         background: linear-gradient(145deg, rgba(0, 0, 0, 0.9) 0%, rgba(26, 26, 26, 0.8) 100%);
#         border: 1px solid rgba(64, 64, 64, 0.2);
#         border-radius: 16px;
#         padding: 1.8rem;
#         box-shadow: 
#             0 8px 32px rgba(0, 0, 0, 0.6),
#             inset 0 1px 0 rgba(255, 255, 255, 0.02);
#         backdrop-filter: blur(10px);
#         transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
#         position: relative;
#         overflow: hidden;
#     }
    
#     .status-card:hover {
#         transform: translateY(-8px);
#         box-shadow: 
#             0 20px 40px rgba(0, 0, 0, 0.8),
#             0 0 20px rgba(116, 222, 128, 0.05);
#         border-color: rgba(116, 222, 128, 0.2);
#     }
    
#     .status-card.openai-card {
#         border-color: rgba(116, 222, 128, 0.3);
#         box-shadow: 
#             0 8px 32px rgba(0, 0, 0, 0.6),
#             inset 0 1px 0 rgba(255, 255, 255, 0.02),
#             0 0 15px rgba(116, 222, 128, 0.08);
#     }
    
#     .status-card::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: -100%;
#         width: 100%;
#         height: 2px;
#         background: linear-gradient(90deg, transparent, #74DE80, transparent);
#         transition: left 0.5s ease;
#     }
    
#     .status-card:hover::before {
#         left: 100%;
#     }
    
#     .status-icon {
#         font-size: 2.2rem;
#         margin-bottom: 1rem;
#         display: block;
#     }
    
#     .status-title {
#         font-size: 0.9rem;
#         color: #888888;
#         font-weight: 500;
#         margin-bottom: 0.8rem;
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#     }
    
#     .status-value {
#         font-size: 1.6rem;
#         font-weight: 600;
#         color: #f5f5f5;
#         margin-bottom: 0.5rem;
#     }
    
#     .openai-highlight {
#         background: linear-gradient(135deg, #74DE80 0%, #5CB85C 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         filter: drop-shadow(0 0 8px rgba(116, 222, 128, 0.3));
#     }
    
#     .status-indicator {
#         display: inline-flex;
#         align-items: center;
#         gap: 8px;
#     }
    
#     .indicator-dot {
#         width: 12px;
#         height: 12px;
#         border-radius: 50%;
#         background: #74DE80;
#         box-shadow: 0 0 12px rgba(116, 222, 128, 0.6);
#         animation: pulse-glow 2s infinite;
#     }
    
#     @keyframes pulse-glow {
#         0%, 100% { 
#             transform: scale(1);
#             box-shadow: 0 0 12px rgba(116, 222, 128, 0.6);
#         }
#         50% { 
#             transform: scale(1.1);
#             box-shadow: 0 0 20px rgba(116, 222, 128, 0.8);
#         }
#     }
    
#     /* Voice Input Styling */
#     .voice-input-container {
#         background: linear-gradient(145deg, rgba(0, 0, 0, 0.95) 0%, rgba(26, 26, 26, 0.9) 100%);
#         border: 2px solid rgba(64, 64, 64, 0.3);
#         border-radius: 16px;
#         padding: 1.5rem;
#         margin-bottom: 1rem;
#         box-shadow: 
#             0 8px 32px rgba(0, 0, 0, 0.6),
#             inset 0 1px 0 rgba(255, 255, 255, 0.02);
#         backdrop-filter: blur(10px);
#     }
    
#     .voice-button {
#         background: linear-gradient(135deg, #1a1a1a 0%, #333333 100%) !important;
#         color: #f5f5f5 !important;
#         border: 2px solid rgba(116, 222, 128, 0.4) !important;
#         border-radius: 50% !important;
#         width: 80px !important;
#         height: 80px !important;
#         font-size: 2rem !important;
#         transition: all 0.3s ease !important;
#         box-shadow: 
#             0 8px 20px rgba(0, 0, 0, 0.8),
#             0 0 20px rgba(116, 222, 128, 0.1) !important;
#         margin: 0 auto !important;
#     }
    
#     .voice-button:hover {
#         background: linear-gradient(135deg, #333333 0%, #1a1a1a 100%) !important;
#         border-color: rgba(116, 222, 128, 0.6) !important;
#         box-shadow: 
#             0 12px 30px rgba(0, 0, 0, 0.9),
#             0 0 30px rgba(116, 222, 128, 0.3) !important;
#         transform: scale(1.05) !important;
#     }
    
#     .voice-button.recording {
#         background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%) !important;
#         border-color: rgba(255, 68, 68, 0.6) !important;
#         box-shadow: 
#             0 12px 30px rgba(0, 0, 0, 0.9),
#             0 0 30px rgba(255, 68, 68, 0.4) !important;
#         animation: recording-pulse 1.5s ease-in-out infinite !important;
#     }
    
#     @keyframes recording-pulse {
#         0%, 100% { 
#             transform: scale(1.05);
#             box-shadow: 0 12px 30px rgba(0, 0, 0, 0.9), 0 0 30px rgba(255, 68, 68, 0.4);
#         }
#         50% { 
#             transform: scale(1.15);
#             box-shadow: 0 16px 40px rgba(0, 0, 0, 0.9), 0 0 40px rgba(255, 68, 68, 0.6);
#         }
#     }
    
#     /* Chat interface with OpenAI styling */
#     .chat-container {
#         background: linear-gradient(145deg, rgba(0, 0, 0, 0.95) 0%, rgba(26, 26, 26, 0.8) 100%);
#         border: 1px solid rgba(64, 64, 64, 0.15);
#         border-radius: 20px;
#         padding: 2rem;
#         margin-bottom: 2rem;
#         box-shadow: 
#             0 12px 48px rgba(0, 0, 0, 0.7),
#             inset 0 1px 0 rgba(255, 255, 255, 0.02);
#         backdrop-filter: blur(15px);
#         min-height: 500px;
#         max-height: 700px;
#         overflow-y: auto;
#         position: relative;
#     }
    
#     .chat-container::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: 0;
#         right: 0;
#         height: 1px;
#         background: linear-gradient(90deg, transparent, rgba(116, 222, 128, 0.1), transparent);
#     }
    
#     /* Message bubbles */
#     .user-message {
#         background: linear-gradient(135deg, #1a1a1a 0%, #333333 50%, #262626 100%);
#         color: #f5f5f5;
#         padding: 1.2rem 1.8rem;
#         border-radius: 20px 20px 8px 20px;
#         margin: 1rem 0 1rem 15%;
#         box-shadow: 
#             0 6px 20px rgba(0, 0, 0, 0.5),
#             0 2px 4px rgba(0, 0, 0, 0.3);
#         border: 1px solid rgba(64, 64, 64, 0.2);
#         position: relative;
#         word-wrap: break-word;
#         animation: slideInRight 0.3s ease-out;
#     }
    
#     .assistant-message {
#         background: linear-gradient(145deg, rgba(0, 0, 0, 0.98) 0%, rgba(26, 26, 26, 0.9) 100%);
#         color: #f5f5f5;
#         padding: 1.2rem 1.8rem;
#         border-radius: 20px 20px 20px 8px;
#         margin: 1rem 15% 1rem 0;
#         border-left: 4px solid #74DE80;
#         box-shadow: 
#             0 6px 20px rgba(0, 0, 0, 0.6),
#             inset 0 1px 0 rgba(255, 255, 255, 0.02),
#             0 0 15px rgba(116, 222, 128, 0.05);
#         border: 1px solid rgba(116, 222, 128, 0.1);
#         position: relative;
#         word-wrap: break-word;
#         animation: slideInLeft 0.3s ease-out;
#     }
    
#     @keyframes slideInRight {
#         from { transform: translateX(50px); opacity: 0; }
#         to { transform: translateX(0); opacity: 1; }
#     }
    
#     @keyframes slideInLeft {
#         from { transform: translateX(-50px); opacity: 0; }
#         to { transform: translateX(0); opacity: 1; }
#     }
    
#     /* Input section */
#     .input-section {
#         background: linear-gradient(145deg, rgba(0, 0, 0, 0.95) 0%, rgba(26, 26, 26, 0.9) 100%);
#         border: 2px solid rgba(64, 64, 64, 0.3);
#         border-radius: 20px;
#         padding: 1.5rem;
#         margin-top: 2rem;
#         box-shadow: 
#             0 12px 32px rgba(0, 0, 0, 0.7),
#             inset 0 1px 0 rgba(255, 255, 255, 0.02);
#         backdrop-filter: blur(15px);
#         position: relative;
#     }
    
#     .input-section::before {
#         content: '';
#         position: absolute;
#         top: -1px;
#         left: -1px;
#         right: -1px;
#         bottom: -1px;
#         background: linear-gradient(135deg, rgba(116, 222, 128, 0.2), rgba(116, 222, 128, 0.1));
#         border-radius: 20px;
#         z-index: -1;
#         opacity: 0;
#         transition: opacity 0.3s ease;
#     }
    
#     .input-section:hover::before {
#         opacity: 1;
#     }
    
#     /* Textarea styling */
#     .stTextArea textarea {
#         background: rgba(0, 0, 0, 0.8) !important;
#         border: 2px solid rgba(64, 64, 64, 0.3) !important;
#         border-radius: 12px !important;
#         color: #f5f5f5 !important;
#         font-size: 1rem !important;
#         padding: 1rem !important;
#         min-height: 120px !important;
#         resize: vertical !important;
#         backdrop-filter: blur(10px) !important;
#         transition: all 0.3s ease !important;
#         line-height: 1.5 !important;
#     }
    
#     .stTextArea textarea:focus {
#         border-color: rgba(116, 222, 128, 0.4) !important;
#         box-shadow: 0 0 20px rgba(116, 222, 128, 0.1) !important;
#         outline: none !important;
#         min-height: 150px !important;
#     }
    
#     .stTextArea textarea::placeholder {
#         color: #888888 !important;
#         font-style: italic !important;
#     }
    
#     /* Footer */
#     .financial-footer {
#         background: linear-gradient(145deg, rgba(0, 0, 0, 0.98) 0%, rgba(26, 26, 26, 0.9) 100%);
#         border: 1px solid rgba(64, 64, 64, 0.15);
#         border-radius: 16px;
#         padding: 2rem;
#         margin-top: 3rem;
#         text-align: center;
#         backdrop-filter: blur(10px);
#         box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
#     }
    
#     .disclaimer-box {
#         background: rgba(64, 64, 64, 0.1);
#         border: 1px solid rgba(64, 64, 64, 0.3);
#         border-radius: 12px;
#         padding: 1rem;
#         margin-top: 1rem;
#         color: #cccccc;
#     }
    
#     .loading-dots {
#         display: inline-flex;
#         gap: 4px;
#         align-items: center;
#     }
    
#     .loading-dot {
#         width: 8px;
#         height: 8px;
#         border-radius: 50%;
#         background: #74DE80;
#         animation: loading-bounce 1.4s ease-in-out infinite both;
#     }
    
#     .loading-dot:nth-child(1) { animation-delay: -0.32s; }
#     .loading-dot:nth-child(2) { animation-delay: -0.16s; }
    
#     @keyframes loading-bounce {
#         0%, 80%, 100% { 
#             transform: scale(0);
#             opacity: 0.5;
#         }
#         40% { 
#             transform: scale(1);
#             opacity: 1;
#         }
#     }
    
#     /* Scrollbar */
#     ::-webkit-scrollbar {
#         width: 10px;
#     }
    
#     ::-webkit-scrollbar-track {
#         background: rgba(0, 0, 0, 0.8);
#         border-radius: 5px;
#     }
    
#     ::-webkit-scrollbar-thumb {
#         background: linear-gradient(135deg, #333333, #74DE80);
#         border-radius: 5px;
#         border: 1px solid rgba(255, 255, 255, 0.05);
#     }
    
#     ::-webkit-scrollbar-thumb:hover {
#         background: linear-gradient(135deg, #404040, #74DE80);
#     }
    
#     /* Hide Streamlit elements */
#     .stDeployButton { display: none; }
#     #MainMenu { visibility: hidden; }
#     footer { visibility: hidden; }
#     header { visibility: hidden; }
    
#     /* Button styling with OpenAI accent */
#     .stButton > button {
#         background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%) !important;
#         color: #f5f5f5 !important;
#         border: 2px solid rgba(255, 255, 255, 0.2) !important;
#         border-radius: 12px !important;
#         padding: 0.8rem 2rem !important;
#         font-weight: 600 !important;
#         font-size: 1rem !important;
#         transition: all 0.3s ease !important;
#         box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6) !important;
#     }
    
#     .stButton > button:hover {
#         background: linear-gradient(135deg, #1a1a1a 0%, #333333 100%) !important;
#         border-color: rgba(255, 255, 255, 0.2) !important;
#         box-shadow: 
#             0 6px 20px rgba(0, 0, 0, 0.8),
#             0 0 15px rgba(116, 222, 128, 0.2) !important;
#         transform: translateY(-2px) !important;
#     }
    
#     /* Responsive design */
#     @media (max-width: 768px) {
#         .financial-title { font-size: 2rem; }
#         .user-message, .assistant-message { 
#             margin-left: 5%; 
#             margin-right: 5%; 
#         }
#         .status-grid { grid-template-columns: 1fr; }
#     }
# </style>
# """, unsafe_allow_html=True)

# # Cache the vector store loading
# @st.cache_resource
# def load_vector_store():
#     try:
#         embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#         db = FAISS.load_local(db_path, embeddings=embeddings, allow_dangerous_deserialization=True)
#         return db
#     except Exception as e:
#         # st.write(f"Loading from: {db_path}")
#         # st.error(f"Failed to load tax database: {str(e)}")
#         # print(f"Failed to load tax database: {str(e)}")
#         return None

# # Voice recognition function
# def transcribe_audio(uploaded_file):
#     """Transcribe audio bytes to text using speech_recognition library"""
#     try:
#         # Initialize recognizer
#         recognizer = sr.Recognizer()
#         audio_bytes = uploaded_file.read()

#         # Create a temporary file to save the audio
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
#             temp_audio.write(audio_bytes)
#             temp_audio_path = temp_audio.name
        
#         # Load and transcribe the audio file
#         with sr.AudioFile(temp_audio_path) as source:
#             # Record the audio file
#             audio_data = recognizer.record(source)
            
#             # Use Google's speech recognition (free tier)
#             try:
#                 text = recognizer.recognize_google(audio_data)
#                 return text
#             except sr.RequestError:
#                 # Fallback to offline recognition if Google is unavailable
#                 try:
#                     text = recognizer.recognize_sphinx(audio_data)
#                     return text
#                 except sr.RequestError:
#                     return "Speech recognition service unavailable. Please try typing your question."
#             except sr.UnknownValueError:
#                 return "Could not understand the audio. Please try speaking more clearly or use text input."
    
#     except Exception as e:
#         return f"Error processing audio: {str(e)}"
    
#     finally:
#         # Clean up temporary file
#         try:
#             os.unlink(temp_audio_path)
#         except:
#             pass

# # Updated prompt template optimized for GPT-4 conversational style
# PROMPT_TEMPLATE = """
# You are BotTax, an expert AI tax assistant powered by OpenAI's GPT-4. Use the context below to provide accurate, professional tax advice using real regulations, deductions, and current tax law.

# Context:
# {context}

# Question:
# {question}

# Please provide a comprehensive, helpful response that includes:
# - Direct answer to the question
# - Relevant tax implications
# - Practical recommendations
# - Any important disclaimers or limitations

# Response:
# """

# def get_prompt(template):
#     return PromptTemplate(
#         template=template,
#         input_variables=["context", "question"]
#     )

# # OpenAI API Key
# OPENAI_API_KEY = os.getenv("HF_TOKEN") 

# # GPT-4 model initialization
# @st.cache_resource
# def get_openai_model():
#     try:
#         llm = ChatOpenAI(
#             model_name="gpt-4",
#             temperature=0.3,
#             max_tokens=1024,
#             openai_api_key=OPENAI_API_KEY
#         )
#         return llm
#     except Exception as e:
#         st.error(f"Failed to initialize OpenAI GPT-4 model: {str(e)}")
#         return None

# def display_chat_message(role, content):
#     """Display a chat message with enhanced dark styling"""
#     if role == "user":
#         # Check if message came from voice input
#         voice_indicator = "🎤" if content.startswith("[Voice Input]") else "👤"
#         display_content = content.replace("[Voice Input] ", "") if content.startswith("[Voice Input]") else content
        
#         st.markdown(f"""
#         <div class="user-message">
#             <strong>{voice_indicator} Taxpayer:</strong><br>
#             {display_content}
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         # Format assistant response to separate main answer from sources
#         parts = content.split("\n\nSource Docs:\n")
#         main_answer = parts[0]
#         sources = parts[1] if len(parts) > 1 else ""
        
#         st.markdown(f"""
#         <div class="assistant-message">
#             <strong>💰 BotTax AI (GPT-4):</strong><br>
#             {main_answer}
#         </div>
#         """, unsafe_allow_html=True)
        
#         if sources:
#             with st.expander("📋 View Tax Documentation Sources", expanded=False):
#                 st.text(sources)

# def process_query(query, is_voice=False):
#     """Process the user query and generate response"""
#     # Show loading animation
#     st.markdown(f"""
#     <div style="text-align: center; padding: 2rem; background: rgba(116, 222, 128, 0.05); border: 1px solid rgba(116, 222, 128, 0.1); border-radius: 12px; margin: 1rem 0;">
#         <div class="loading-dots">
#             <div class="loading-dot"></div>
#             <div class="loading-dot"></div>
#             <div class="loading-dot"></div>
#         </div>
#         <br>
#         <span style="color: #74DE80; font-weight: 500;">🧠 OpenAI GPT-4 is analyzing tax regulations and crafting your personalized expert response...</span>
#         {f"<br><small style='color: #888888;'>🎤 Processing voice input</small>" if is_voice else ""}
#     </div>
#     """, unsafe_allow_html=True)
    
#     try:
#         # Load vector store
#         db = load_vector_store()
#         if db is None:
#             error_msg = "❌ Tax database unavailable. Please ensure the tax knowledge base is properly configured."
#             st.error(error_msg)
#             st.session_state.messages.append({'role': 'assistant', 'content': error_msg})
#             st.rerun()
            
        
#         # Setup retrieval
#         retriever = db.as_retriever(search_kwargs={"k": 6})  # More sources for comprehensive advice
#         llm = get_openai_model()
        
#         if llm is None:
#             error_msg = "❌ OpenAI GPT-4 engine initialization failed. Please verify your API key and connection."
#             st.error(error_msg)
#             st.session_state.messages.append({'role': 'assistant', 'content': error_msg})
#             st.rerun()
            
        
#         prompt = get_prompt(PROMPT_TEMPLATE)
        
#         # Setup RetrievalQA chain
#         retrieval_qa = RetrievalQA.from_chain_type(
#             llm=llm,
#             chain_type="stuff",
#             retriever=retriever,
#             return_source_documents=True,
#             chain_type_kwargs={"prompt": prompt}
#         )
        
#         # Get response
#         response = retrieval_qa.invoke({"query": query})
        
#         result = response["result"]
#         source_documents = response["source_documents"]
        
#         # Clean up the response
#         result = result.strip()
#         if result.startswith("Response:"):
#             result = result[9:].strip()
        
#         # Add voice processing acknowledgment if applicable
#         if is_voice:
#             result = f"🎤 *Processed from voice input* \n\n{result}"
        
#         # Format full response
#         original_res = result + "\n\nSource Docs:\n" + str(source_documents)
        
#         # Add assistant message to session state
#         st.session_state.messages.append({'role': 'assistant', 'content': original_res})
        
#         # Rerun to display the new messages
#         st.rerun()
        
#     except Exception as e:
#         error_msg = f"❌ Tax consultation error: {str(e)}"
#         st.error(error_msg)
#         st.session_state.messages.append({'role': 'assistant', 'content': error_msg})
#         st.rerun()
    
#     # Dark footer with OpenAI branding
#     st.markdown("---")
    
    

# def main():
#     # Enhanced dark header with BotTax branding
#     st.markdown("""
#     <div class="financial-header">
#         <div class="financial-title">💰 BotTax</div>
#         <div class="financial-subtitle">AI-Powered Tax Consultation Assistant</div>
#         <div class="financial-description">
#             🧾 Smart tax planning & compliance • Powered by OpenAI GPT-4
#             <br>
#             💡 Get expert tax guidance • 🎤 Voice-enabled for hands-free consultation
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()
    
#     # Enhanced status grid with OpenAI branding and voice feature
#     st.markdown('<div class="status-grid">', unsafe_allow_html=True)
    
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.markdown("""
#         <div class="status-card">
#             <div class="status-icon">📡</div>
#             <div class="status-title">System Status</div>
#             <div class="status-value">
#                 <div class="status-indicator">
#                     <div class="indicator-dot"></div>
#                     Active & Ready
#                 </div>
#             </div>
#             <small style="color: #888888;">Tax consultation available 24/7</small>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#         <div class="status-card">
#             <div class="status-icon">🤖</div>
#             <div class="status-title">AI Engine</div>
#             <div class="status-value">OpenAI GPT-4</div>
#             <small >Advanced reasoning & tax expertise</small>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("""
#         <div class="status-card">
#             <div class="status-icon">🎤</div>
#             <div class="status-title">Voice Input</div>
#             <div class="status-value">Enabled</div>
#             <small >Speak your tax questions naturally</small>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         st.markdown("""
#         <div class="status-card">
#             <div class="status-icon">⏳</div>
#             <div class="status-title">Tax Year</div>
#             <div class="status-value">2025</div>
#             <small style="color: #888888;">Current regulations updated</small>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # Initialize session state
#     if 'messages' not in st.session_state:
#         st.session_state.messages = []
    
#     # Display welcome message if no messages
#     if not st.session_state.messages:
#         st.markdown("""
#         <div class="assistant-message">
#             <strong>💰 BotTax AI (GPT-4):</strong><br>
#             Welcome to BotTax! I'm your advanced tax consultation assistant powered by OpenAI's GPT-4. I combine 
#             sophisticated AI reasoning with comprehensive tax knowledge to provide you with accurate, personalized 
#             tax guidance and strategic advice.
#             <br><br>
#             <span style="color: #74DE80;">🎤 NEW: Voice Input Available!</span> You can now speak your tax questions 
#             directly - just click the microphone button and ask naturally.
#             <br><br>
#             <em>💡 Popular tax questions I excel at:</em><br>
#             • "How do I calculate capital gains tax on stock sales?"<br>
#             • "What are the current tax brackets and optimal strategies?"<br>
#             • "Can I claim home office deductions as a remote worker?"<br>
#         </div>
#         """, unsafe_allow_html=True)
    
#     # Show previous messages
#     for message in st.session_state.messages:
#         display_chat_message(message['role'], message['content'])
    
#     # Enhanced input section with voice capability
#     st.markdown("### 💬 Ask Your Tax Question")
    
#     # Combined Input Section (Text + Voice) - UPDATED SECTION
#     st.markdown("""
#     <style>
#     .chat-input-wrapper {
#         display: flex;
#         align-items: center;
#         border: 1px solid #444;
#         border-radius: 12px;
#         padding: 0.5rem;
#         background-color: #1e1e1e;
#         margin-bottom: 1rem;
#     }
#     .chat-input-wrapper textarea {
#         flex: 1;
#         border: none !important;
#         background: transparent;
#         color: #f5f5f5 !important;
#         font-size: 1rem;
#         resize: none;
#         padding: 0.5rem;
#     }
#     .chat-input-wrapper textarea:focus {
#         outline: none !important;
#         box-shadow: none !important;
#     }
#     .voice-button {
#         margin-left: 10px;
#         background-color: #333;
#         border: 2px solid #555;
#         border-radius: 50%;
#         padding: 0.6rem;
#         cursor: pointer;
#         transition: background 0.2s ease;
#     }
#     .voice-button:hover {
#         background-color: #444;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # Layout: Chat input + Mic icon
#     st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)
#     user_query = st.text_area(
#         label="",
#         placeholder="Type your tax question here or click the mic 🎤...",
#         key="tax_query_input",
#         label_visibility="collapsed",
#         height=100
#     )
#     # Audio input within chat
#     audio_bytes = st.audio_input("", key="voice_input_inline")
#     st.markdown('</div>', unsafe_allow_html=True)

#     # If audio recorded
#     if audio_bytes:
#         with st.spinner("🎤 Processing your voice input..."):
#             transcribed_text = transcribe_audio(audio_bytes)
            
#             if transcribed_text and not transcribed_text.startswith("Error") and not transcribed_text.startswith("Could not") and not transcribed_text.startswith("Speech recognition"):
#                 st.success(f"🎤 Transcribed: {transcribed_text}")
#                 voice_query = f"[Voice Input] {transcribed_text}"
#                 st.session_state.messages.append({'role': 'user', 'content': voice_query})
#                 process_query(transcribed_text, is_voice=True)
#             else:
#                 st.error(f"❌ {transcribed_text}")

#     # Submit Button
#     submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
#     with submit_col2:
#         submit_button = st.button(
#             "🤖 Get Expert Tax Advice (GPT-4)",
#             use_container_width=True,
#             type="primary"
#         )

#     # If text submitted
#     if submit_button and user_query.strip():
#         st.session_state.messages.append({'role': 'user', 'content': user_query})
#         process_query(user_query)


import os
import streamlit as st
from langchain_openai import ChatOpenAI 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from datetime import datetime
from huggingface_hub import InferenceClient
from langchain.llms.base import LLM
from typing import Optional, List, Any
import speech_recognition as sr
from io import BytesIO
import wave
import tempfile
import hashlib

# Configure page
st.set_page_config(
    page_title="BotTax - AI Tax Consultation Assistant", 
    page_icon="💰", 
    layout="wide"
)

# Vector DB path
db_path = "vector_store\\faiss_database"

# Dark blackish themed CSS styling with OpenAI branding colors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #1a1a1a 50%, #0a0a0a 75%, #000000 100%);
        font-family: 'Inter', sans-serif;
        color: #f5f5f5;
    }
    
    /* Dark financial brand header with subtle OpenAI accent */
    .financial-header {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.98) 0%, rgba(26, 26, 26, 0.95) 100%);
        border: 2px solid rgba(64, 64, 64, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.8),
            inset 0 1px 0 rgba(255, 255, 255, 0.05),
            0 0 20px rgba(116, 222, 128, 0.03);
        backdrop-filter: blur(15px);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .financial-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(116, 222, 128, 0.02), transparent);
        animation: shimmer 8s infinite linear;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .financial-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #4a4a4a 0%, #666666 30%, #808080 70%, #595959 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 8px rgba(0,0,0,0.9);
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
        filter: drop-shadow(0 0 10px rgba(74, 74, 74, 0.8));
    }
    
    .financial-subtitle {
        font-size: 1.3rem;
        color: #666666;
        font-weight: 500;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
    }
    
    .financial-description {
        color: #888888;
        font-size: 1rem;
        margin-top: 1rem;
        position: relative;
        z-index: 2;
    }
    
    /* Status cards with subtle OpenAI accent */
    .status-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .status-card {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.9) 0%, rgba(26, 26, 26, 0.8) 100%);
        border: 1px solid rgba(64, 64, 64, 0.2);
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .status-card:hover {
        transform: translateY(-8px);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.8),
            0 0 20px rgba(116, 222, 128, 0.05);
        border-color: rgba(116, 222, 128, 0.2);
    }
    
    .status-card.openai-card {
        border-color: rgba(116, 222, 128, 0.3);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.02),
            0 0 15px rgba(116, 222, 128, 0.08);
    }
    
    .status-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #74DE80, transparent);
        transition: left 0.5s ease;
    }
    
    .status-card:hover::before {
        left: 100%;
    }
    
    .status-icon {
        font-size: 2.2rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .status-title {
        font-size: 0.9rem;
        color: #888888;
        font-weight: 500;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-value {
        font-size: 1.6rem;
        font-weight: 600;
        color: #f5f5f5;
        margin-bottom: 0.5rem;
    }
    
    .openai-highlight {
        background: linear-gradient(135deg, #74DE80 0%, #5CB85C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 8px rgba(116, 222, 128, 0.3));
    }
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    .indicator-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #74DE80;
        box-shadow: 0 0 12px rgba(116, 222, 128, 0.6);
        animation: pulse-glow 2s infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 0 12px rgba(116, 222, 128, 0.6);
        }
        50% { 
            transform: scale(1.1);
            box-shadow: 0 0 20px rgba(116, 222, 128, 0.8);
        }
    }
    
    /* Voice Input Styling */
    .voice-input-container {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.95) 0%, rgba(26, 26, 26, 0.9) 100%);
        border: 2px solid rgba(64, 64, 64, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
    }
    
    .voice-button {
        background: linear-gradient(135deg, #1a1a1a 0%, #333333 100%) !important;
        color: #f5f5f5 !important;
        border: 2px solid rgba(116, 222, 128, 0.4) !important;
        border-radius: 50% !important;
        width: 80px !important;
        height: 80px !important;
        font-size: 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            0 8px 20px rgba(0, 0, 0, 0.8),
            0 0 20px rgba(116, 222, 128, 0.1) !important;
        margin: 0 auto !important;
    }
    
    .voice-button:hover {
        background: linear-gradient(135deg, #333333 0%, #1a1a1a 100%) !important;
        border-color: rgba(116, 222, 128, 0.6) !important;
        box-shadow: 
            0 12px 30px rgba(0, 0, 0, 0.9),
            0 0 30px rgba(116, 222, 128, 0.3) !important;
        transform: scale(1.05) !important;
    }
    
    .voice-button.recording {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%) !important;
        border-color: rgba(255, 68, 68, 0.6) !important;
        box-shadow: 
            0 12px 30px rgba(0, 0, 0, 0.9),
            0 0 30px rgba(255, 68, 68, 0.4) !important;
        animation: recording-pulse 1.5s ease-in-out infinite !important;
    }
    
    @keyframes recording-pulse {
        0%, 100% { 
            transform: scale(1.05);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.9), 0 0 30px rgba(255, 68, 68, 0.4);
        }
        50% { 
            transform: scale(1.15);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.9), 0 0 40px rgba(255, 68, 68, 0.6);
        }
    }
    
    /* Chat interface with OpenAI styling */
    .chat-container {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.95) 0%, rgba(26, 26, 26, 0.8) 100%);
        border: 1px solid rgba(64, 64, 64, 0.15);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 
            0 12px 48px rgba(0, 0, 0, 0.7),
            inset 0 1px 0 rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        min-height: 500px;
        max-height: 700px;
        overflow-y: auto;
        position: relative;
    }
    
    .chat-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(116, 222, 128, 0.1), transparent);
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #1a1a1a 0%, #333333 50%, #262626 100%);
        color: #f5f5f5;
        padding: 1.2rem 1.8rem;
        border-radius: 20px 20px 8px 20px;
        margin: 1rem 0 1rem 15%;
        box-shadow: 
            0 6px 20px rgba(0, 0, 0, 0.5),
            0 2px 4px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(64, 64, 64, 0.2);
        position: relative;
        word-wrap: break-word;
        animation: slideInRight 0.3s ease-out;
    }
    
    .assistant-message {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.98) 0%, rgba(26, 26, 26, 0.9) 100%);
        color: #f5f5f5;
        padding: 1.2rem 1.8rem;
        border-radius: 20px 20px 20px 8px;
        margin: 1rem 15% 1rem 0;
        border-left: 4px solid #74DE80;
        box-shadow: 
            0 6px 20px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.02),
            0 0 15px rgba(116, 222, 128, 0.05);
        border: 1px solid rgba(116, 222, 128, 0.1);
        position: relative;
        word-wrap: break-word;
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Input section */
    .input-section {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.95) 0%, rgba(26, 26, 26, 0.9) 100%);
        border: 2px solid rgba(64, 64, 64, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 2rem;
        box-shadow: 
            0 12px 32px rgba(0, 0, 0, 0.7),
            inset 0 1px 0 rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        position: relative;
    }
    
    .input-section::before {
        content: '';
        position: absolute;
        top: -1px;
        left: -1px;
        right: -1px;
        bottom: -1px;
        background: linear-gradient(135deg, rgba(116, 222, 128, 0.2), rgba(116, 222, 128, 0.1));
        border-radius: 20px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .input-section:hover::before {
        opacity: 1;
    }
    
    /* Textarea styling */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid rgba(64, 64, 64, 0.3) !important;
        border-radius: 12px !important;
        color: #f5f5f5 !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        min-height: 120px !important;
        resize: vertical !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        line-height: 1.5 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(116, 222, 128, 0.4) !important;
        box-shadow: 0 0 20px rgba(116, 222, 128, 0.1) !important;
        outline: none !important;
        min-height: 150px !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #888888 !important;
        font-style: italic !important;
    }
    
    /* Footer */
    .financial-footer {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.98) 0%, rgba(26, 26, 26, 0.9) 100%);
        border: 1px solid rgba(64, 64, 64, 0.15);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 3rem;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
    }
    
    .disclaimer-box {
        background: rgba(64, 64, 64, 0.1);
        border: 1px solid rgba(64, 64, 64, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        color: #cccccc;
    }
    
    .loading-dots {
        display: inline-flex;
        gap: 4px;
        align-items: center;
    }
    
    .loading-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #74DE80;
        animation: loading-bounce 1.4s ease-in-out infinite both;
    }
    
    .loading-dot:nth-child(1) { animation-delay: -0.32s; }
    .loading-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes loading-bounce {
        0%, 80%, 100% { 
            transform: scale(0);
            opacity: 0.5;
        }
        40% { 
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.8);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #333333, #74DE80);
        border-radius: 5px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #404040, #74DE80);
    }
    
    /* Hide Streamlit elements */
    .stDeployButton { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Button styling with OpenAI accent */
    .stButton > button {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%) !important;
        color: #f5f5f5 !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1a1a1a 0%, #333333 100%) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        box-shadow: 
            0 6px 20px rgba(0, 0, 0, 0.8),
            0 0 15px rgba(116, 222, 128, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .financial-title { font-size: 2rem; }
        .user-message, .assistant-message { 
            margin-left: 5%; 
            margin-right: 5%; 
        }
        .status-grid { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# Cache the vector store loading
@st.cache_resource
def load_vector_store():
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.load_local(db_path, embeddings=embeddings, allow_dangerous_deserialization=True)
        return db
    except Exception as e:
        # st.write(f"Loading from: {db_path}")
        # st.error(f"Failed to load tax database: {str(e)}")
        # print(f"Failed to load tax database: {str(e)}")
        return None

# Voice recognition function
def transcribe_audio(uploaded_file):
    """Transcribe audio bytes to text using speech_recognition library"""
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()
        audio_bytes = uploaded_file.read()

        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        
        # Load and transcribe the audio file
        with sr.AudioFile(temp_audio_path) as source:
            # Record the audio file
            audio_data = recognizer.record(source)
            
            # Use Google's speech recognition (free tier)
            try:
                text = recognizer.recognize_google(audio_data)
                return text
            except sr.RequestError:
                # Fallback to offline recognition if Google is unavailable
                try:
                    text = recognizer.recognize_sphinx(audio_data)
                    return text
                except sr.RequestError:
                    return "Speech recognition service unavailable. Please try typing your question."
            except sr.UnknownValueError:
                return "Could not understand the audio. Please try speaking more clearly or use text input."
    
    except Exception as e:
        return f"Error processing audio: {str(e)}"
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_audio_path)
        except:
            pass

# Updated prompt template optimized for GPT-4 conversational style
PROMPT_TEMPLATE = """
You are BotTax, an expert AI tax assistant powered by OpenAI's GPT-4. Use the context below to provide accurate, professional tax advice using real regulations, deductions, and current tax law.

Context:
{context}

Question:
{question}

Please provide a comprehensive, helpful response that includes:
- Direct answer to the question
- Relevant tax implications
- Practical recommendations
- Any important disclaimers or limitations

Response:
"""

def get_prompt(template):
    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

# OpenAI API Key
OPENAI_API_KEY = os.getenv("HF_TOKEN") 

# GPT-4 model initialization
@st.cache_resource
def get_openai_model():
    try:
        llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.3,
            max_tokens=1024,
            openai_api_key=OPENAI_API_KEY
        )
        return llm
    except Exception as e:
        st.error(f"Failed to initialize OpenAI GPT-4 model: {str(e)}")
        return None

def display_chat_message(role, content):
    """Display a chat message with enhanced dark styling"""
    if role == "user":
        # Check if message came from voice input
        voice_indicator = "🎤" if content.startswith("[Voice Input]") else "👤"
        display_content = content.replace("[Voice Input] ", "") if content.startswith("[Voice Input]") else content
        
        st.markdown(f"""
        <div class="user-message">
            <strong>{voice_indicator} Taxpayer:</strong><br>
            {display_content}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Format assistant response to separate main answer from sources
        parts = content.split("\n\nSource Docs:\n")
        main_answer = parts[0]
        sources = parts[1] if len(parts) > 1 else ""
        
        st.markdown(f"""
        <div class="assistant-message">
            <strong>💰 BotTax AI (GPT-4):</strong><br>
            {main_answer}
        </div>
        """, unsafe_allow_html=True)
        
        if sources:
            with st.expander("📋 View Tax Documentation Sources", expanded=False):
                st.text(sources)
def process_query(query, is_voice=False):
    """Process the user query and generate response"""
    # Show loading animation
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: rgba(116, 222, 128, 0.05); border: 1px solid rgba(116, 222, 128, 0.1); border-radius: 12px; margin: 1rem 0;">
        <div class="loading-dots">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
        <br>
        <span style="color: #74DE80; font-weight: 500;">🧠 OpenAI GPT-4 is analyzing tax regulations and crafting your personalized expert response...</span>
        {f"<br><small style='color: #888888;'>🎤 Processing voice input</small>" if is_voice else ""}
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Load vector store
        db = load_vector_store()
        if db is None:
            error_msg = "❌ Tax database unavailable. Please ensure the tax knowledge base is properly configured."
            st.error(error_msg)
            st.session_state.messages.append({'role': 'assistant', 'content': error_msg})
            st.rerun()
            
        
        # Setup retrieval
        retriever = db.as_retriever(search_kwargs={"k": 6})  # More sources for comprehensive advice
        llm = get_openai_model()
        
        if llm is None:
            error_msg = "❌ OpenAI GPT-4 engine initialization failed. Please verify your API key and connection."
            st.error(error_msg)
            st.session_state.messages.append({'role': 'assistant', 'content': error_msg})
            st.rerun()
            
        
        prompt = get_prompt(PROMPT_TEMPLATE)
        
        # Setup RetrievalQA chain
        retrieval_qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        
        # Get response
        response = retrieval_qa.invoke({"query": query})
        
        result = response["result"]
        source_documents = response["source_documents"]
        
        # Clean up the response
        result = result.strip()
        if result.startswith("Response:"):
            result = result[9:].strip()
        
        # Add voice processing acknowledgment if applicable
        if is_voice:
            result = f"🎤 *Processed from voice input* \n\n{result}"
        
        # Format full response
        original_res = result + "\n\nSource Docs:\n" + str(source_documents)
        
        # Add assistant message to session state
        st.session_state.messages.append({'role': 'assistant', 'content': original_res})
        
        # Rerun to display the new messages
        st.rerun()
        
    except Exception as e:
        error_msg = f"❌ Tax consultation error: {str(e)}"
        st.error(error_msg)
        st.session_state.messages.append({'role': 'assistant', 'content': error_msg})
        st.rerun()
    
    # Dark footer with OpenAI branding
    st.markdown("---")
    
    

def main():
    # Enhanced dark header with BotTax branding
    st.markdown("""
    <div class="financial-header">
        <div class="financial-title">💰 BotTax</div>
        <div class="financial-subtitle">AI-Powered Tax Consultation Assistant</div>
        <div class="financial-description">
            🧾 Smart tax planning & compliance • Powered by OpenAI GPT-4
            <br>
            💡 Get expert tax guidance • 🎤 Voice-enabled for hands-free consultation
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
    # Enhanced status grid with OpenAI branding and voice feature
    st.markdown('<div class="status-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">📡</div>
            <div class="status-title">System Status</div>
            <div class="status-value">
                <div class="status-indicator">
                    <div class="indicator-dot"></div>
                    Active & Ready
                </div>
            </div>
            <small style="color: #888888;">Tax consultation available 24/7</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">🤖</div>
            <div class="status-title">AI Engine</div>
            <div class="status-value">OpenAI GPT-4</div>
            <small >Advanced reasoning & tax expertise</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">🎤</div>
            <div class="status-title">Voice Input</div>
            <div class="status-value">Enabled</div>
            <small >Speak your tax questions naturally</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">⏳</div>
            <div class="status-title">Tax Year</div>
            <div class="status-value">2025</div>
            <small style="color: #888888;">Current regulations updated</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display welcome message if no messages
    if not st.session_state.messages:
        st.markdown("""
        <div class="assistant-message">
            <strong>💰 BotTax AI (GPT-4):</strong><br>
            Welcome to BotTax! I'm your advanced tax consultation assistant powered by OpenAI's GPT-4. I combine 
            sophisticated AI reasoning with comprehensive tax knowledge to provide you with accurate, personalized 
            tax guidance and strategic advice.
            <br><br>
            <span style="color: #74DE80;">🎤 NEW: Voice Input Available!</span> You can now speak your tax questions 
            directly - just click the microphone button and ask naturally.
            <br><br>
            <em>💡 Popular tax questions I excel at:</em><br>
            • "How do I calculate capital gains tax on stock sales?"<br>
            • "What are the current tax brackets and optimal strategies?"<br>
            • "Can I claim home office deductions as a remote worker?"<br>
        </div>
        """, unsafe_allow_html=True)
    
    # Show previous messages
    for message in st.session_state.messages:
        display_chat_message(message['role'], message['content'])
    
    # Enhanced input section with voice capability
    st.markdown("### 💬 Ask Your Tax Question")
    
    # Voice Input Section
    st.markdown("""
    <div class="voice-input-container">
        <div style="text-align: center; margin-bottom: 1rem;">
            <h4 style="margin-bottom: 0.5rem;">🎤 Voice Input</h4>
            <p style="color: #888888; font-size: 0.9rem; margin-bottom: 1.5rem;">
                Click the microphone to record your tax question. Speak clearly for best results.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice input controls
    

voice_col1, voice_col2, voice_col3 = st.columns([1, 2, 1])

with voice_col2:
    # Initialize session state variables for voice processing
    if "voice_processed" not in st.session_state:
        st.session_state.voice_processed = False
    if "last_audio_hash" not in st.session_state:
        st.session_state.last_audio_hash = None

    audio_bytes = st.audio_input("Record your tax question", key="voice_input")

    if audio_bytes:
        # Read the bytes from the file-like object and create a hash
        audio_data = audio_bytes.read()
        audio_bytes.seek(0)  # Reset the file pointer for later use
        current_audio_hash = hashlib.md5(audio_data).hexdigest()
        
        # Only process if this is a new audio recording
        if current_audio_hash != st.session_state.last_audio_hash:
            st.session_state.last_audio_hash = current_audio_hash
            
            with st.spinner("🎤 Processing your voice input..."):
                transcribed_text = transcribe_audio(audio_bytes)

                if transcribed_text and not transcribed_text.startswith(("Error", "Could not", "Speech recognition")):
                    st.success(f"🎤 Transcribed: {transcribed_text}")
                    
                    # Add to chat history and process
                    st.session_state.messages.append({'role': 'user', 'content': transcribed_text})
                    process_query(transcribed_text, is_voice=True)
                else:
                    st.error(f"❌ {transcribed_text}")
    else:
        # Reset when no audio present
        st.session_state.last_audio_hash = None
    
    st.markdown("---")
    
    # Text Input Section
    # Use text_area with improved dynamic height
    user_query = st.text_area(
        label="Tax query input",
        placeholder="Type your tax question here... (e.g., 'What are the standard deduction amounts for 2025?', 'How do I optimize my tax strategy for retirement planning?')",
        key="tax_query",
        help="💡 Pro tip: GPT-4 excels at complex scenarios - provide details about your specific situation for the most accurate advice",
        label_visibility="hidden"
    )
    
    # Add submit button with OpenAI styling
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    
    with submit_col2:
        submit_button = st.button(
            "🤖 Get Expert Tax Advice (GPT-4)",
            use_container_width=True,
            type="primary"
        )
    
    # Process query when submitted
    if submit_button and user_query.strip():
        # Add user message to session state
        st.session_state.messages.append({'role': 'user', 'content': user_query})
        process_query(user_query)